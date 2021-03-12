#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

DAY=$(date +%j)
CONSUL_FILE=/tmp/consul.${DAY}

if [ ! -f "$CONSUL_FILE" ] ; then
  curl --data-urlencode query@${DIR}/query.sparql  https://query.wikidata.org/sparql?format=json -o $CONSUL_FILE
fi

NAME=$(jq ".results.bindings[${DAY}].itemLabel.value" $CONSUL_FILE)
LINK=$(jq ".results.bindings[${DAY}].item.value" $CONSUL_FILE)
DESC=$(jq ".results.bindings[${DAY}].itemDescription.value" $CONSUL_FILE)

echo -n "The consul of the day is: "
if [ -n "$USE_HTML" ] ; then
  echo -n "<a href=" $LINK ">"
  echo -n ${NAME//\"/}
  echo "</a>"
elif [ -n "$USE_MD" ] ; then
  echo "[${NAME//\"/}](${LINK//\"/})"
else
  echo "${NAME//\"/} (${LINK//\"/}) - ${DESC//\"/}"
fi

