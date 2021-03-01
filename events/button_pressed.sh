#!/bin/bash

killall mplayer
mplayer -playlist http://streaming.radio.co/s774887f7b/listen.m3u -really-quiet > /dev/null 2> /dev/null < /dev/null &
