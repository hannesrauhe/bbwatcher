#!/bin/bash

MSG="It's coffee time!"
if [ -n "$1" ] ; then
  MSG=${1//\"/\\\"}
fi
curl -X POST --data-urlencode "payload={\"channel\": \"$CHANNEL\", \"username\": \"coffeebot\", \"text\": \"$MSG\", \"icon_emoji\": \":coffee:\"}" $SLACK_HOOK_ADDRESS
