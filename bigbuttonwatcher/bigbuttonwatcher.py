#!/usr/bin/python3

import usb,sys,time,subprocess
from enum import Enum

idVendor = 0x1d34
idProduct = 0x000d
scriptDir = "/etc/bbwatcher/events"

class ButtonState(Enum):
  UNDEF=0
  LID_DOWN=21
  PRESSED=22
  LID_UP=23

def findButton():
  for bus in usb.busses():
    for dev in bus.devices:
      if dev.idVendor == idVendor and dev.idProduct == idProduct:
        return dev
  return None

def state_change(last,new):
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

def main():
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
        state_change(ButtonState(last_event), ButtonState(result[0]))
        last_event = result[0]
      time.sleep(endpoint.interval / float(1000))
    except Exception as e:
      print(e, result) # result is int sometimes?

  handle.releaseInterface()

if __name__ == "__main__":
    main()
