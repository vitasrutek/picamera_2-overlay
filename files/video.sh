#!/bin/bash
echo 'Mažu video'
rm /home/pi/WEB/video.h264
echo 'Vypínám službu'
sudo systemctl stop camera.service
echo 'Nahrávám video'
sudo -u pi rpicam-vid -t 15s -o /home/pi/WEB/video.h264 --rotation 180 --width 1280 --height 968
echo 'Zapínám službu'
sudo systemctl start camera.service
