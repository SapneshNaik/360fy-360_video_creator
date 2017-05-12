#!/bin/bash
#This file takes audio and video from temp_data folder and joins them and then stores the resultant video into
#the user specififed final location
`ffmpeg -loglevel panic -i ../temp_data/video.mp4 -i ../temp_data/audio.mp3 -c copy -map 0:0 -map 1:0 -flags +global_header ../temp_data/video_a.mp4 -y`
`ffmpeg -loglevel panic -i ../temp_data/video_unscaled.mp4 -i ../temp_data/audio.mp3 -c copy -map 0:0 -map 1:0 -flags +global_header ../temp_data/video_audio.mp4  -y`
