import serial
import threading
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__, template_folder='.')
socketio = SocketIO(app, cors_allowed_origins="*")

# Change 'COM3' to your Arduino port (Windows: COM3/COM4, Linux/Mac: /dev/ttyUSB0)
SERIAL_PORT = 'COM3'
BAUD_RATE = 9600

def read_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        while True:
            line = ser.readline().decode('utf-8').strip()
            if line.isdigit():
                value = int(line)
                voltage = round((value / 1023.0) * 5.0, 3)  # Convert to voltage
                socketio.emit('pcm_data', {'raw': value, 'voltage': voltage})
    except Exception as e:
        print(f"Serial error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    thread = threading.Thread(target=read_serial, daemon=True)
    thread.start()
    socketio.run(app, debug=True, port=5000)