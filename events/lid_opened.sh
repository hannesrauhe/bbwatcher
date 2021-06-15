#!/bin/bash

blink1-tool --rgb 0000FF -l1
rfkill unblock bluetooth
nohup bluealsa-aplay 00:00:00:00:00:00 > /dev/nullq 2> /dev/null < /dev/null &
systemctl start shairport-sync