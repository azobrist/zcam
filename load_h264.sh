#!/bin/bash

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

#check if file server was created
svr=./fileserver
if [ ! d $svr ]; then
    echo "run create_file_server.sh first"
fi

ffmpeg -f h264 -i zcam.h264 -c:v copy zcam.mp4
ts=$(date '+%Y%m%d%H%M%S')
mv zcam.mp4 $svr/$ts.mp4
