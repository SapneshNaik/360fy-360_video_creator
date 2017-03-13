#!/bin/bash
#echo "ffmpeg -r $framerate -i vid_files/frames/FY%06d.png -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' -s $resolution -c:v libx264 vid_files/video.mp4 -y"


# $1 is frame rate and $2 is resolution/frame size

#hq one below
#`ffmpeg -r $framerate -i vid_files/frames/FY%06d.png -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' -s $resolution -c:v libx264 -profile:v high444 -refs 16 -crf 0 -preset ultrafast vid_files/video.mp4 -y`

`ffmpeg -r $1 -i ../temp_data/frames/FY%06d.png -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' -s $2 -c:v libx264 -profile:v high444 -refs 16  -preset ultrafast ../temp_data/video.mp4 -y`
#`ffmpeg -framerate $1 -i vid_files/frames/FY%06d.png -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' -codec copy -s $resolution vid_files/video.mp4 -y`
#`ffmpeg -f image2 -r $1 -i vid_files/frames/FY%06d.png -vcodec libx264 -profile:v high444 -refs 16 -crf 0 -preset ultrafast vid_files/frames/FY%06d.png/video.mp4 -y`
#`ffmpeg -r $framerate  -i vid_files/frames/FY%06d.png -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' -s $resolution -c:v mjpeg -q:v 3 -an vid_files/output.mov`
#-crf 0
