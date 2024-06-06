#!/bin/bash
echo 'Mažu fotku'
rm /home/pi/WEB/photo-day.jpg
echo 'Vypínám službu'
sudo systemctl stop camera.service
echo 'Fotím'
sudo -u pi libcamera-jpeg -o /home/pi/WEB/photo-day.jpg --rotation 180
echo 'Zapínám službu'
sudo systemctl start camera.service
