#!/bin/bash

while true; 
do
  if  ! python3 main.py > /dev/null; then 
    break
  fi
  echo "Ran $(date)"
  sleep 2s
done

