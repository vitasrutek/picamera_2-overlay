#!/usr/bin/python3

import io
import logging
import socketserver
import subprocess
import os
from http import server
from threading import Condition, Timer
import time
import sys
import json

PORT = 80

os.chdir('/home/pi/WEB')

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def get_temperature():
    result = subprocess.run(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE, text=True)
    temp_output = result.stdout.strip()
    temperature = temp_output.replace('temp=', '')
    return temperature

def get_venku():
    result = subprocess.run(['/usr/bin/bash', '/home/pi/WEB/teplota.sh'], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

def get_uptime():
    result = subprocess.run(['uptime', '-p'], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

html_template = read_file('/home/pi/WEB/index.html')
content_file = '/home/pi/WEB/content.txt'

class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/cpu_temp':
            temp = os.popen("vcgencmd measure_temp").readline().replace("temp=", "").replace("'C\n", "")
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"temperature": temp}).encode())
        elif self.path == '/':
            try:
                file_content = read_file(content_file)
                uptime = get_uptime()
                venku = get_venku()
                html_content = html_template.replace('{{ file_content }}', file_content)
                html_content = html_content.replace('{{ uptime }}', uptime)
                html_content = html_content.replace('{{ venku }}', venku)
                #self.start_service()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            except Exception as e:
                self.send_error(500, f"Internal server error: {e}")
        elif self.path == '/index.html':
            try:
                file_content = read_file(content_file)
                uptime = get_uptime()
                venku = get_venku()
                html_content = html_template.replace('{{ file_content }}', file_content)
                html_content = html_content.replace('{{ uptime }}', uptime)
                html_content = html_content.replace('{{ venku }}', venku)
                #self.start_service()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html_content.encode('utf-8'))
            except Exception as e:
                self.send_error(500, f"Internal server error: {e}")
        elif self.path == '/photo-day.jpg':
            try:
                with open('/home/pi/WEB/photo-day.jpg', 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'image/jpeg')
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, "File not found")
        elif self.path == '/photo-hdr.jpg':
            try:
                with open('/home/pi/WEB/photo-hdr.jpg', 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'image/jpeg')
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, "File not found")
        elif self.path == '/photo-night.jpg':
            try:
                with open('/home/pi/WEB/photo-night.jpg', 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'image/jpeg')
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, "File not found")
        elif self.path == '/video.mp4':
            try:
                with open('/home/pi/WEB/video.mp4', 'rb') as file:
                    self.send_response(200)
                    self.send_header('Content-type', 'video/mp4')
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, "File not found")

    def do_POST(self):
        if self.path == '/script_photo-day':
            try:
                result = subprocess.run(['/usr/bin/sudo', '/home/pi/WEB/photo-day.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode != 0:
                    raise Exception(f"Error running script: {result.stderr}")
                self.send_response(303)
                self.send_header('Location', '/photo-day.jpg')
                self.end_headers()
            except Exception as e:
                self.send_error(500, f"Internal server error: {e}")
        if self.path == '/script_photo-hdr':
            try:
                result = subprocess.run(['/usr/bin/sudo', '/home/pi/WEB/photo-hdr.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode != 0:
                    raise Exception(f"Error running script: {result.stderr}")
                self.send_response(303)
                self.send_header('Location', '/photo-hdr.jpg')
                self.end_headers()
            except Exception as e:
                self.send_error(500, f"Internal server error: {e}")

        elif self.path == '/script_photo-night':
            try:
                result = subprocess.run(['/usr/bin/sudo', '/home/pi/WEB/photo-night.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode != 0:
                    raise Exception(f"Error running script: {result.stderr}")
                self.send_response(303)
                self.send_header('Location', '/photo-night.jpg')
                self.end_headers()
            except Exception as e:
                self.send_error(500, f"Internal server error: {e}")

        elif self.path == '/script_video':
            try:
                result = subprocess.run(['/usr/bin/sudo', '/home/pi/WEB/videoP.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if result.returncode != 0:
                    raise Exception(f"Error running script: {result.stderr}")
                self.send_response(303)
                self.send_header('Location', '/video.mp4')
                self.end_headers()
            except Exception as e:
                self.send_error(500, f"Internal server error: {e}")

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

try:
    address = ('', PORT)
    server = StreamingServer(address, StreamingHandler)

    print("Server běží na portu ", PORT)
    server.serve_forever()
except KeyboardInterrupt:
    print("\nZachyceno ukončení (Ctrl+C), vypínám...")
finally:
    stop_service()
