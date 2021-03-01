#!/bin/bash

killall mplayer
killall bluealsa-aplay
blink1-tool --off -l1
rfkill block bluetooth
