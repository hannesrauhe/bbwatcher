#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [ -f $DIR/env ] ; then
  source "$DIR/env"
fi

if [ -n "${RADIO-}" ] ; then
  killall mplayer
  blink1-tool --rgb FF9900 -l1
  mplayer -playlist http://streaming.radio.co/s774887f7b/listen.m3u -really-quiet > /dev/null 2> /dev/null < /dev/null &
fi

MSG="It's coffee time. $($DIR/consuloftheday/query.sh)"
echo $MSG
if [ $(date +%H) -ge "8" ] && [ $(date +%H) -lt "10" ] ; then
  $DIR/coffeebot/notify_slack.sh "$MSG"
fi
