#!/usr/bin/python3

import io
import logging
import socketserver
import subprocess
from http import server
from threading import Condition
from libcamera import Transform

from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput

PORT = 80

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

def get_temperature():
    result = subprocess.run(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE, text=True)
    temp_output = result.stdout.strip()
    temperature = temp_output.replace('temp=', '')
    return temperature

def get_uptime():
    result = subprocess.run(['uptime', '-p'], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

html_template = read_file('/home/pi/index.html')
content_file = '/home/pi/content.txt'

class StreamingOutput(io.BufferedIOBase):
    def __init__(self):
        self.frame = None
        self.condition = Condition()

    def write(self, buf):
        with self.condition:
            self.frame = buf
            self.condition.notify_all()


class StreamingHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
            file_content = read_file(content_file)
            uptime = get_uptime()
            temperature = get_temperature()
            html_content = html_template.replace('{{ file_content }}', file_content)
            html_content = html_content.replace('{{ uptime }}', uptime)
            html_content = html_content.replace('{{ temperature }}', temperature)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        elif self.path == '/index.html':
            file_content = read_file(content_file)
            uptime = get_uptime()
            temperature = get_temperature()
            html_content = html_template.replace('{{ file_content }}', file_content)
            html_content = html_content.replace('{{ uptime }}', uptime)
            html_content = html_content.replace('{{ temperature }}', temperature)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_content.encode('utf-8'))
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Age', 0)
            self.send_header('Cache-Control', 'no-cache, private')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=FRAME')
            self.end_headers()
            try:
                while True:
                    with output.condition:
                        output.condition.wait()
                        frame = output.frame
                    self.wfile.write(b'--FRAME\r\n')
                    self.send_header('Content-Type', 'image/jpeg')
                    self.send_header('Content-Length', len(frame))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
            except Exception as e:
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
        else:
            self.send_error(404)
            self.end_headers()


class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True


picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (1024, 768)}, transform=Transform(hflip = True, vflip = True)))
output = StreamingOutput()
picam2.start_recording(MJPEGEncoder(), FileOutput(output))

try:
    address = ('', PORT)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
finally:
    picam2.stop_recording()
