#!/bin/bash
echo 'Mažu video'
rm /home/pi/WEB/video.mp4
#rm /home/pi/WEB/video.avi
#echo 'Vypínám službu'
#sudo systemctl stop camera.service
echo 'Nahrávám video'
sudo -u pi python3 /home/pi/WEB/videoP.py
#echo 'Prevadim na AVI'
#sudo -u pi ffmpeg -i video.h264 video.avi
#echo 'Zapínám službu'
#sudo systemctl start camera.service
