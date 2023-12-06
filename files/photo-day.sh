rm photo-day.jpg
sudo systemctl stop camera.service
python3 /var/www/html/picamera-jpeg.py
sudo systemctl start camera.service
