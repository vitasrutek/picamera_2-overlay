# picamera_2-overlay
overlay for live streaming from RaspberryPi camera on Bullseye

# picamera-overlay
Simple text (or whatever) overlay for picamera web stream (tested on Raspberry OS Bullseye (64bit) with libcamera)

Due to my limited skills in Python and PHP, any better programmer can do it better. But this is probably better solution than annotationtext directly from picamera.
Overlay is realized with picamera web stream and side running PHP for showing wanted values (for my purpose uptime, temp sensor and CPU temp). Next choise is link for capturing JPG photo in day or night.
In the end, there will be 2 services - one for camera streaming and one for HTML overlay.

![screenshot](https://github.com/vitasrutek/picamera-overlay/blob/main/screenshot.PNG)

First of all you need picamera installed - https://picamera.readthedocs.io/en/release-1.13/install.html
Then you have to install Lighttpd (but Nginx is probably better) and PHP.
```
sudo apt update
```
```
sudo apt install python3
```
```
sudo apt install lighttpd
sudo lighttpd-enable-mod userdir
sudo service lighttpd reload
```
```
sudo apt install php7.4 php7.4-cgi php7.4-cli php7.4-fpm
sudo lighttpd-enable-mod fastcgi fastcgi-php
sudo service lighttpd reload
```
After these steps everything should be ready.

Next you must allow www-data user to run SUDO commands (stop and start camera.service for take static picture in full resolution)
```
sudo visudo
```
and add this
```
www-data   ALL=NOPASSWD: /var/www/html/photo-day.sh, /var/www/html/photo-night.sh
```

Create picamera service (name camera.service)
```
sudo nano /etc/systemd/system/camera.service
```

and add this (or copy prepared file):
```
[Unit]
Description=Service for PiCamera

[Service]
ExecStart=python3 /home/pi/camera.py

[Install]
WantedBy=multi-user.target
```
and activate service:
```
sudo systemctl enable camera.service
sudo systemctl start camera.service
```

and service for HTML:
```
[Unit]
Description=Spousteni HTML

[Service]
ExecStart=python3 /home/pi/html.py

[Install]
WantedBy=multi-user.target
```
After this you can now copy  all files to /var/www/html (photo*, index.php, temperature*, uptime.sh).

Note that to edit all nessecary files for IP address change.

Temperature shell files are for read values from CPU and from 1wire sensor. I could not resolve how to put commands directly to index.php so this is such a workaround.

Edit files and commands at will. Overlay text is defined in index.php.
