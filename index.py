import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import subprocess
import webbrowser

# Nastavte URL pro získání obrazu
CAMERA_URL = "http://192.168.1.159:8000/stream.mjpg"

# Třída pro obsluhu HTTP požadavků
class StreamingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            # Získáme aktuální čas
            current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            # Získáme dobu provozu (uptime)
            uptime = subprocess.check_output(['uptime']).decode('utf-8')

            # HTML kód pro zobrazení času, doby provozu a tlačítka pro fotografování
            html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Camera Stream</title>
    <style>
        .container {{
            position: relative;
            width: 640px;
            height: 480px;
        }}
        #text-overlay {{
            position: absolute;
            top: 10px;
            left: 10px;
            background-color: rgba(255, 255, 255, 0.7);
            padding: 10px;
        }}
        #photo-button {{
            position: absolute;
            bottom: 10px;
            left: 10px;
            padding: 10px;
            background-color: #3498db;
            color: white;
            text-decoration: none;
            border: none;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <h1>Camera Stream with Time and Uptime</h1>
    <div class="container">
        <div id="text-overlay">
            <p>Current Time: {current_time}</p>
            <p>Uptime: {uptime}</p>
        </div>
        <img src="{CAMERA_URL}" width="640" height="480">
        <a id="photo-button" href="http://192.168.1.159/photo-day.php" target="_blank">Take Picture</a>
    </div>
</body>
</html>
"""

            self.wfile.write(html_content.encode())
        else:
            self.send_error(404)

# Funkce pro spuštění HTTP serveru
def start_http_server():
    server_address = ('', 8080)
    httpd = HTTPServer(server_address, StreamingHandler)
    print("Server běží na portu 8080")
    httpd.serve_forever()

# Hlavní funkce
def main():
    # Spustíme HTTP server v samostatném vlákně
    http_thread = threading.Thread(target=start_http_server)
    http_thread.start()

if __name__ == '__main__':
    main()
