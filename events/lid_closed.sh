#!/bin/bash

killall bluealsa-aplay
blink1-tool --off -l1
rfkill block bluetooth