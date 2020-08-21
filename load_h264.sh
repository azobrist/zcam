#!/bin/bash

#check if file server was created
svr=./fileserver
if [ ! d $svr ]; then
    echo "run create_file_server.sh first"
fi

ffmpeg -f h264 -i zcam.h264 -c:v copy zcam.mp4
ts=$(date '+%Y%m%d%H%M%S')
mv zcam.mp4 $svr/$ts.mp4
