# picamera_2-overlay
overlay for live streaming from RaspberryPi camera on Bookworm.

# picamera-overlay
Simple text (or whatever) overlay for picamera web stream (tested on Raspberry OS Bookworm (64bit) with libcamera on RaspberryPi)

Now no need to use Nginx or Apache, everything is driven by Python :)

![screenshot](https://github.com/vitasrutek/picamera-overlay/blob/v2/screen.PNG)

```
sudo apt update
```
```
sudo apt install python3
```
```
sudo apt install -y python3-picamera2 --no-install-recommends
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
ExecStart=python3 /home/pi/picam.py

[Install]
WantedBy=multi-user.target
```
and activate service:
```
sudo systemctl enable camera.service
sudo systemctl start camera.service
```

# Bottom in dev...


After these steps everything should be almost ready.
Check service status for nginx and php8.2 and camera to be sure everything works fine.

Next you must allow www-data user to run SUDO commands (stop and start camera.service for take static picture in full resolution)
```
sudo visudo
```
and add this
```
www-data   ALL=NOPASSWD: /var/www/html/photo-day.sh, /var/www/html/photo-night.sh
```


After this you can now copy  all files to /var/www/html (photo*, index.php, temperature*, uptime.sh) and for .sh files make chmod +x.

Note that to edit all nessecary files for IP address change.

Temperature shell files are for read values from CPU and from 1wire sensor. I could not resolve how to put commands directly to index.php so this is such a workaround.

Edit files and commands at will. Overlay text is defined in index.php.
