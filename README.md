# picamera_2-overlay
Text overlay for live streaming from RaspberryPi camera on Bookworm.

# Update 2024-08
For Raspberry Pi Zero2 and Camera module V3 (Wide) is resolution quiet bigger -> higher CPU consumption -> higher temperature. Because of this is new web.py file where camera.service is disabled by default and start only on HTML page load. After interval camera.service is stopped. This means CPU and temperature saving.   
For V1 cameras is web_old.py suitable enough.

### picamera2-overlay
Simple text (or whatever) overlay for picamera web stream (tested on Raspberry OS Bookworm (64bit) with libcamera on RaspberryPi).
   
Now no need to use Nginx or Apache, everything is driven by Python :)   
With these Python scripts you can see custom data via overlay (I set uptime, CPU temp). You can also see content of some file - for example weather forecast saved in TXT file.   
You can also take a photo, HDR photo and 15sec video. I want to add night photo in next update.

![screenshot](https://github.com/vitasrutek/picamera_2-overlay/blob/v2/files/screen.png)

### Instalation

```sh
# update system and install software
sudo apt update
sudo apt install python3
sudo apt install -y python3-picamera2 --no-install-recommends

# clone repo
git clone https://github.com/vitasrutek/picamera_2-overlay.git

Edit all downloaded files to change absolute paths to GitHub cloned folder

# create service for PiCamera (picamera.py is from official repository picamera2 - mjpeg_server - only edited for rotation and resolution)
sudo cat > /etc/systemd/system/camera.service <<'EOF'
[Unit]
Description=Service for PiCamera
After=network.targer

[Service]
ExecStart=sudo python3 /home/pi/picamera.py
User=pi

[Install]
WantedBy=multi-user.target
EOF


# create service for web overlay
sudo cat > /etc/systemd/system/web.service <<'EOF'
[Unit]
Description=Service for Web/Picamera
After=network.target

[Service]
ExecStart=sudo python3 /home/pi/WEB/web.py
WorkingDirectory=/home/pi/WEB
User=pi

[Install]
WantedBy=multi-user.target
EOF

# set correct permissions
sudo chmod -R 755 /path/to/downloaded/github/folder

# make files executable
cd /path/to/downloaded/github/folder/files
chmod +x *.sh

# enable and start services
sudo systemctl daemon-reload
sudo systemctl enable web.service ## camera.service -> do this for well cooled devices (not for Zero2 and V3 camera)
sudo systemctl start web.service ## camera.service -> do this for well cooled devices (not for Zero2 and V3 camera)
```


Note that to edit all nessecary files for IP address and folder location change.

Edit files and commands at will. Overlay text is defined in web.py.
