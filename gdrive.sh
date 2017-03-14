#!/bin/bash
#This scrpit backs up my project to google drive.
#new to github, will use this untill I'm confident with the basics
filename=`date +"git_%d-%m_Time_%I-%M%p".tar.gz`
echo $filename
echo " archiving now"
tar -zcvf "$filename" *
echo " Uploading now"

gdrive upload --parent 0B8i5vCWNLhOGTF9OYlFESm5XNnc "$filename"
echo " removing local archive"
rm $filename
echo "DONE"
