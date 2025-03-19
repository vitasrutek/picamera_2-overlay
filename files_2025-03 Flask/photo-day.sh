#!/bin/bash
echo 'Mažu fotku'
rm /home/vita/WEB/photo-day.jpg
echo 'Vypínám službu'
sudo systemctl stop camera.service
echo 'Fotím'
sudo -u vita rpicam-still --tuning-file /usr/share/libcamera/ipa/rpi/vc4/imx708_wide.json -t 10 --autofocus-on-capture 1  --autofocus-mode auto -q 100 -o /home/vita/WEB/photo-day.jpg #--rotation 180
echo 'Zapínám službu'
sudo systemctl start camera.service
