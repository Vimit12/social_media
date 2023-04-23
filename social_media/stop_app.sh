#!/bin/bash

# Find the PID of the process that is using port 8000
PID=$(lsof -ti tcp:8000)

if [[ -z "$PID" ]]; then
  echo "No process is currently using port 8000"
else
  # Stop the process using the PID
  echo "Stopping process $PID"
  kill $PID
  sudo kill -9 $(sudo lsof -t -i:8000)
  echo "Process stopped"
fi
