from influxdb import line_protocol
from influxdb_client import InfluxDBClient # 2.x
from influxdb_client.client.write_api import SYNCHRONOUS, WritePrecision
from pathlib import Path,PurePath
import influxdb # 1.x
import json
import time
import socket
import sys

config_dir = PurePath(Path.joinpath(Path.home(), ".fritzflux"))
config_path = Path.joinpath(config_dir, "config.json")

# uses parts of fritzflux (simply copied over what I need)
DefaultFFConfig = {
  "fb_address": "fritz.box",
  "fb_user": "",
  "fb_pass": "",
  "influxdb_connections": [{
    "address": "localhost",
    "port": 8086,
    "user": "root",
    "pass": "root",
    "database": ""
    },
    {
    "url": "",
    "token": "",
    "org": "",
    "bucket": ""
  }],
  "hostname": socket.gethostname()
}

def is_influx2_db(c):
  return "url" in c and len(c["url"]) > 0

class CoffeeFlux:
  def __init__(self, ff_config):
    self.ic = []
    for iconfig in ff_config["influxdb_connections"]:
      if is_influx2_db(iconfig):
        self.ic.append(InfluxDBClient(url=iconfig["url"], token=iconfig["token"]))
      else:
        self.ic.append(influxdb.InfluxDBClient(host=iconfig["address"], port=iconfig["port"],
                                               username=iconfig["user"], password=iconfig["pass"], database=iconfig["database"]))
    self.config = ff_config

  def push(self, consul_name):
    json_body = {
      "tags": {
        "sender": "coffeebot",
        "hostname": self.config["hostname"]
      },
      "points": []
    }

    t = int(time.time())

    f_status = {
      "consul": (consul_name, "name"),
    }

    for name, (v, f) in f_status.items():
      m = {"measurement": name, "fields": {f: v}, "time": t}
      json_body["points"].append(m)

    lines = line_protocol.make_lines(json_body)
    print(lines)

    for iconfig, ic in zip(self.config["influxdb_connections"], self.ic):
      try:
        if is_influx2_db(iconfig):
          write_api = ic.write_api(write_options=SYNCHRONOUS)
          write_api.write(iconfig["bucket"], iconfig["org"],
                          lines, write_precision=WritePrecision.S)
          print("Written to Influx 2.x bucket", iconfig["bucket"], "on host", iconfig["url"])
        else:
          ic.write_points(lines, protocol="line_protocol", time_precision="s")
          print("Written to Influx 1.x database",
                iconfig["database"], "on host", iconfig["address"])
      except Exception as e:
        print("Failed to write to connection:", iconfig, "Error:", e)

def read_config():
  config = {}
  with open(str(config_path), 'r') as config_file:
    config = json.load(config_file)

  keys_not_in_config = DefaultFFConfig.keys()-config.keys()
  if len(keys_not_in_config)>0:
    print("Please set following keys in config: ", keys_not_in_config)
    sys.exit(0)
  return config

if __name__ == '__main__':
  if(len(sys.argv)==1):
    print("usage %s <consul_name>"%sys.argv[0])
    sys.exit(1)
  ffc = read_config()
  ff=CoffeeFlux(ffc)
  ff.push(sys.argv[1])

