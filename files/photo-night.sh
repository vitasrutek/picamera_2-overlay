rm photo-night.jpg
sudo systemctl stop camera.service
python3 picamera-jpeg-night.py
sudo systemctl start camera.service
