#!/bin/bash
echo 'Mažu fotku'
rm /home/pi/WEB/photo-hdr.jpg
echo 'Vypínám službu'
sudo systemctl stop camera.service
echo 'Fotím'
sudo -u pi rpicam-still --ev -2 --denoise cdn_off --post-process-file hdr.json -o /home/pi/WEB/photo-hdr.jpg --rotation 180
echo 'Zapínám službu'
sudo systemctl start camera.service
