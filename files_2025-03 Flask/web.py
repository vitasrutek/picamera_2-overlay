from flask import Flask, render_template, send_file, jsonify, redirect, request
import subprocess
import os

app = Flask(__name__)

# Nastavení pracovního adresáře
os.chdir('/home/vita/WEB')

# Funkce pro čtení souboru
def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

# Získání teploty CPU
def get_temperature():
    result = subprocess.run(['vcgencmd', 'measure_temp'], stdout=subprocess.PIPE, text=True)
    temp_output = result.stdout.strip()
    temperature = temp_output.replace('temp=', '')
    return temperature

# Získání venkovní teploty (DS18B20)
def get_venku():
    try:
        with open('/sys/bus/w1/devices/28-011919dc4f67/w1_slave', 'r') as file:
            tempread = file.read()
            temperature_str = tempread.split('t=')[-1]
            temperature = float(temperature_str) / 1000.0
            return f"{temperature:.2f}"
    except Exception as e:
        return f"Error reading temperature: {e}"

# Získání uptime
def get_uptime():
    result = subprocess.run(['uptime', '-p'], stdout=subprocess.PIPE, text=True)
    return result.stdout.strip()

@app.route('/')
def index():
    file_content = read_file('/home/vita/WEB/content.txt')
    uptime = get_uptime()
    return render_template('index.html', file_content=file_content, uptime=uptime)

@app.route('/out_temp')
def out_temp():
    outtemp = get_venku()
    return jsonify({"outtemperature": outtemp})

@app.route('/cpu_temp')
def cpu_temp():
    temp = get_temperature()
    return jsonify({"temperature": temp})

@app.route('/photo-<name>.jpg')
def serve_photo(name):
    filename = f'/home/vita/WEB/photo-{name}.jpg'
    return send_file(filename, mimetype='image/jpeg')

@app.route('/video.mp4')
def serve_video():
    return send_file('/home/vita/WEB/video.mp4', mimetype='video/mp4')

# POST verze pro tlačítka
@app.route('/script_photo-<name>', methods=['POST'])
def run_script_post(name):
    try:
        result = subprocess.run(['/usr/bin/sudo', f'/home/vita/WEB/photo-{name}.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return f'Error running script: {result.stderr}', 500
        return redirect(f'/photo-{name}.jpg')
    except Exception as e:
        return f'Internal server error: {e}', 500

# GET verze pro zadání do adresního řádku
@app.route('/script_photo-<name>', methods=['GET'])
def run_script_get(name):
    try:
        result = subprocess.run(['/usr/bin/sudo', f'/home/vita/WEB/photo-{name}.sh'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            return f'Error running script: {result.stderr}', 500
        return send_file(f'/home/vita/WEB/photo-{name}.jpg', mimetype='image/jpeg')
    except Exception as e:
        return f'Internal server error: {e}', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
