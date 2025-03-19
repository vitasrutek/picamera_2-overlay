#!/bin/bash
echo 'Mažu fotku'
rm /home/vita/WEB/photo-night.jpg
echo 'Vypínám službu'
sudo systemctl stop camera.service
echo 'Fotím'
sudo -u vita rpicam-still -o /home/vita/WEB/photo-night.jpg --shutter 5000000 --gain 5 --awbgains 2,2 --immediate
echo 'Zapínám službu'
sudo systemctl start camera.service
