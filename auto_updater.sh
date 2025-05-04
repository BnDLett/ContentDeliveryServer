#!/bin/sh

SCRIPT_PATH=$(dirname "$(realpath "$0")")
cd "$SCRIPT_PATH" || (echo "Failed to start program." && exit)

while true
do
  echo "Checking for updates..."
  git pull
  # Sleeps for 43200 seconds; aka 12 hours.
  sleep 43200
done
