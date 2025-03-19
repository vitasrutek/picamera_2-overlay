#!/usr/bin/python3

import io
import logging
import socketserver
from http import server
from threading import Condition
from libcamera import Transform

from picamera2 import Picamera2
from picamera2.encoders import MJPEGEncoder
from picamera2.outputs import FileOutput

PORT = 8000

PAGE = """\
<html>
<head>
</head>
<body>
<img src="stream.mjpg" width="1366" height="768" />
</body>
</html>
"""

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
            print("Přesměrování na /index.html")
            self.send_response(301)
            self.send_header('Location', '/index.html')
            self.end_headers()
        elif self.path == '/index.html':
            print("Načítání stránky index.html")
            content = PAGE.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html')
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == '/stream.mjpg':
            print("Přístup k /stream.mjpg")
            if not self.server.is_recording:
                print("Spouštím nahrávání...")
                picam2.start_recording(MJPEGEncoder(), FileOutput(output))
                self.server.is_recording = True
            else:
                print("Nahrávání již běží.")

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
                print(f"Klient {self.client_address} odpojen: {e}")
                logging.warning(
                    'Removed streaming client %s: %s',
                    self.client_address, str(e))
            finally:
                # Když klient opustí stránku, zastavíme nahrávání
                if self.server.is_recording:
                    print("Klient se odpojil, zastavuji nahrávání...")
                    picam2.stop_recording()
                    self.server.is_recording = False
        else:
            print(f"Chyba 404: Soubor {self.path} nenalezen.")
            self.send_error(404)
            self.end_headers()

class StreamingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

    def __init__(self, server_address, RequestHandlerClass):
        super().__init__(server_address, RequestHandlerClass)
        self.is_recording = False  # Přidání proměnné pro sledování stavu nahrávání

print("Konfigurace kamery...")
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration(main={"size": (1920, 1080)}, transform=Transform(hflip=False, vflip=False)))
output = StreamingOutput()

try:
    print(f"Spouštím server na portu {PORT}...")
    address = ('', PORT)
    server = StreamingServer(address, StreamingHandler)
    server.serve_forever()
except KeyboardInterrupt:
    print("Server ukončen uživatelem.")
finally:
    if server.is_recording:
        print("Zastavuji nahrávání...")
        picam2.stop_recording()
