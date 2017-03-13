#!/bin/bash
inputVid=$1


frames=`ffmpeg -i "$1" 2>&1 | sed -n "s/.*, \(.*\) fp.*/\1/p"`
echo $frames