#!/bin/bash
filename=`date +"Date_%d-%m_Time_%I-%M%p".tar.gz`
echo $filename
tar -zcvf "$filename" *
gdrive upload --parent 0B8i5vCWNLhOGTF9OYlFESm5XNnc "$filename"
rm $filename
echo "DONE"
