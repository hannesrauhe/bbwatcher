from bluepy.btle import Scanner, DefaultDelegate

def onDeviceChanged(addr, data):
  print("Device %s, value %s" % (addr,data))

# The devices we're searching for
devices = [
  "fd:77:74:17:54:ee"
];
# Whatever the last data was
lastAdvertising = {}

# Gets the actual scanning data
class ScanDelegate(DefaultDelegate):
  def __init__(self):
    DefaultDelegate.__init__(self)
  def handleDiscovery(self, dev, isNewDev, isNewData):
    # if not dev.addr in devices: return
    for (adtype, desc, value) in dev.getScanData():
      if adtype==255 and value[:4]=="9005": # Manufacturer Data
        data = value[4:]
        if not dev.addr in lastAdvertising or lastAdvertising[dev.addr] != data:
          onDeviceChanged(dev.addr, data)
        lastAdvertising[dev.addr] = data
      else:
        print("Device ",dev.addr,isNewDev,isNewData)
        lastAdvertising[dev.addr] = value

# Start scanning
scanner = Scanner().withDelegate(ScanDelegate())
scanner.clear()
scanner.start()
# Keep scanning in  10 second chunks
while True: scanner.process(10)
# in case were wanted to finish, we should call 'stop'
scanner.stop()
