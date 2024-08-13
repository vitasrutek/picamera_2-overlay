#!/bin/bash
echo 'Mažu fotku'
rm /home/pi/WEB/photo-night.jpg
#echo 'Vypínám službu'
#sudo systemctl stop camera.service
echo 'Fotím'
sudo -u pi rpicam-still -o /home/pi/WEB/photo-night.jpg --shutter 5000000 --gain 5 --awbgains 2,2 --immediate
#sudo -u pi python3 night.py
#echo 'Zapínám službu'
#sudo systemctl start camera.service
