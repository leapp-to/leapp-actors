#!/bin/sh
if [ "$2" == "True" ]; then
  sudo docker start $1 2>&1 > /dev/null
fi;
