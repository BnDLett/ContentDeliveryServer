#!/bin/sh

SCRIPT_PATH=$(dirname "$(realpath "$0")")
cd "$SCRIPT_PATH" || (echo "Failed to start program." && exit)

echo "Starting auto-updater job."
"$SCRIPT_PATH"/auto_updater.sh &

echo "Starting gunicorn."
cd "$SCRIPT_PATH"/ContentDeliveryServer || (echo "Failed to start." && kill "$(jobs -p)" && exit)

CORE_COUNT=$(nproc --all)

if [ -e server.crt ] && [ -e server.key ]
then
  gunicorn -w "$CORE_COUNT" 'main:app' -b 0.0.0.0:8080 --certfile=server.crt --keyfile=server.key --reload
else
  gunicorn -w "$CORE_COUNT" 'main:app' -b 0.0.0.0:8080 --reload
fi

kill "$(jobs -p)"

