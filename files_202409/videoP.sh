#!/bin/bash
echo 'Mažu video'
rm /home/pi/WEB/video.mp4
echo 'Vypínám službu'
sudo systemctl stop camera.service
echo 'Nahrávám video'
sudo -u pi python3 /home/pi/WEB/videoP.py
echo 'Zapínám službu'
sudo systemctl start camera.service
