#!/bin/bash
ffmpeg -f h264 -i picam.h264 -c:v copy movie.mp4
ts=$(date '+%Y%m%d%H%M%S')
mv movie.mp4 /var/www/html/$ts.mp4