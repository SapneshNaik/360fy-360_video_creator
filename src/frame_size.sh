#!/bin/bash
inputVid=$1
resolution=`ffmpeg -i "$inputVid" 2>&1 | grep -oP 'Stream .*, \K[0-9]+x[0-9]+'`
echo $resolution