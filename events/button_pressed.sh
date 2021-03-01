#!/bin/bash

killall mplayer
blink1-tool --rgb FF9900 -l1
mplayer -playlist http://streaming.radio.co/s774887f7b/listen.m3u -really-quiet > /dev/null 2> /dev/null < /dev/null &
