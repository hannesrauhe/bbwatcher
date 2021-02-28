# bbwatcher
A daemon that watches the big red button (tested with an old dream cheeky button) and executes events

## Prerequisites

The Watcher needs python3 and python-usb.

## Install

By default the watcher runs as root. To enable the systemd service, do the following

```
# put the executable and the systemd-config in place:
sudo ln -s ~/bbwatcher/bigbuttonwatcher/bigbuttonwatcher.py /usr/bin/bigbuttonwatcher
sudo ln -s ~/bbwatcher/systemd/bigbuttonwatcher.service /etc/systemd/system

# create the config dir
sudo mkdir /etc/bbwatcher/events

# start the watcher
sudo systemctl start bigbuttonwatcher.service

# check the logs
journalctl -u bigbuttonwatcher.service

# enable the watcher at startup
sudo systemctl enable bigbuttonwatcher.service
```

The watcher executes scripts it finds in `/etc/bbwatcher/events` (again, as root), there should be one script per event. Check the examples here: https://github.com/hannesrauhe/bbwatcher/tree/main/events
