#!/usr/bin/python3

import sys,time,subprocess,json
from enum import Enum
from pathlib import Path,PurePath


# usb panic button settings -> move to config at some point
idVendor = 0x1d34
idProduct = 0x000d
scriptDir = "/etc/bbwatcher/events"
config_dir = PurePath("/etc/bbwatcher")
config_path = Path.joinpath(config_dir, "config.json")

DefaultBBWConfig = {
    "button_type": "usb",
}

def create_config(config_dict={}, extend=False):
    if not Path(config_path).exists() or extend:
        if not Path(config_dir).is_dir():
            Path(config_dir).mkdir()
        config_file = open(str(config_path), 'w')
        json.dump({**DefaultBBWConfig,**config_dict}, config_file, indent=2)
        print("Created config file at %s. Please set values and restart."%config_path)
        sys.exit(0)

def read_config():
    create_config()
    config = {}
    with open(str(config_path), 'r') as config_file:
        config = json.load(config_file)

    keys_not_in_config = DefaultBBWConfig.keys()-config.keys()
    if len(keys_not_in_config)>0:
        print("Please set following keys in config: ", keys_not_in_config)
        create_config(config, True)
    return config


class ButtonState(Enum):
  UNDEF=0
  LID_DOWN=21
  PRESSED=22
  LID_UP=23

def findButton():
  import usb
  for bus in usb.busses():
    for dev in bus.devices:
      if dev.idVendor == idVendor and dev.idProduct == idProduct:
        return dev
  return None

def stateChange(last,new):
  try:
    if new==ButtonState.PRESSED:
      print("Button pressed")
      subprocess.call(scriptDir+"/button_pressed.sh")
    elif last==ButtonState.LID_DOWN and new==ButtonState.LID_UP:
      print("Lid opened")
      subprocess.call(scriptDir+"/lid_opened.sh")
    elif last==ButtonState.LID_UP and new==ButtonState.LID_DOWN:
      print("Lid closed")
      subprocess.call(scriptDir+"/lid_closed.sh")
  except Exception as e:
    print("Executing script failed: ",e)

def usbButton():
  import usb
  dev = findButton()
  if dev == None:
    print("Cannot find panic button device")
    sys.exit(1)

  handle = dev.open()
  interface = dev.configurations[0].interfaces[0][0]
  endpoint = interface.endpoints[0]

  try:
    handle.detachKernelDriver(interface)
  except Exception:
    pass

  handle.claimInterface(interface)

  last_event = 0x0
  while True:
    result = handle.controlMsg(requestType=0x21,
                              request= 0x09,
                              value= 0x0200,
                              buffer="\x00\x00\x00\x00\x00\x00\x00\x02")

    try:
      result = handle.interruptRead(endpoint.address, endpoint.maxPacketSize)
      if result[0]!=last_event:
        stateChange(ButtonState(last_event), ButtonState(result[0]))
        last_event = result[0]
      time.sleep(endpoint.interval / float(1000))
    except Exception as e:
      print(e, result) # result is int sometimes?

  handle.releaseInterface()

def serialButton():
  import serial
  ser = serial.Serial('/dev/ttyUSB0',115200)

  last_time = time.time()
  while True:
    line = ser.readline()
    if(last_time+1>time.time()):
      # triggered only once per second
      continue
    # if line:
    #   print(line.decode(encoding="utf-8"))

    if line.startswith(b"PRESS"):
      last_time=time.time()
      stateChange(ButtonState.UNDEF,ButtonState.PRESSED)

if __name__ == "__main__":
  bbc = read_config()
  if bbc["button_type"]=="serial":
    serialButton()
  else:
    usbButton()
