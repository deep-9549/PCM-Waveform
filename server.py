import serial
import threading
import os
import re
import time
import sys
import msvcrt
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__, template_folder='.')
socketio = SocketIO(app, cors_allowed_origins="*")

# Change 'COM3' to your Arduino port (Windows: COM3/COM4, Linux/Mac: /dev/ttyUSB0)
SERIAL_PORT = 'COM12'
BAUD_RATE = 9600
LOCK_FILE = os.path.join(os.path.dirname(__file__), '.server.lock')

def acquire_single_instance_lock():
    """Return lock handle if acquired, otherwise None when another instance exists."""
    try:
        lock_handle = open(LOCK_FILE, 'w')
        msvcrt.locking(lock_handle.fileno(), msvcrt.LK_NBLCK, 1)
        lock_handle.write(str(os.getpid()))
        lock_handle.flush()
        return lock_handle
    except OSError:
        return None

def parse_adc_value(line: str):
    """Extract ADC value (0-1023) from multiple possible serial formats."""
    if not line:
        return None

    # Fast path for plain integer lines like "512".
    if line.isdigit():
        value = int(line)
        return value if 0 <= value <= 1023 else None

    # Support labeled payloads like "Analog: 621  PCM: 155".
    analog_match = re.search(r'analog\s*:\s*(\d+)', line, re.IGNORECASE)
    if analog_match:
        value = int(analog_match.group(1))
        return value if 0 <= value <= 1023 else None

    # Fallback: use the first numeric token if present.
    number_match = re.search(r'(\d+)', line)
    if number_match:
        value = int(number_match.group(1))
        return value if 0 <= value <= 1023 else None

    return None

def read_serial():
    while True:
        try:
            with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
                # Give MCU time to settle after opening/reset.
                time.sleep(2)
                while True:
                    line = ser.readline().decode('utf-8', errors='ignore').strip()
                    value = parse_adc_value(line)
                    if value is not None:
                        voltage = round((value / 1023.0) * 5.0, 3)  # Convert to voltage
                        socketio.emit('pcm_data', {'raw': value, 'voltage': voltage})
        except serial.SerialException as e:
            print(f"Serial error: {e}")
        except Exception as e:
            print(f"Unexpected serial read error: {e}")

        # Retry connection if port disappears or read loop exits unexpectedly.
        time.sleep(1)

@app.route('/')
def index():
    return render_template('index.html', serial_port=SERIAL_PORT, baud_rate=BAUD_RATE)

if __name__ == '__main__':
    instance_lock = acquire_single_instance_lock()
    if instance_lock is None:
        print('Another server instance is already running. Close the other process and try again.')
        sys.exit(1)

    debug_mode = False
    # Flask debug reloader launches the script twice; only start serial once.
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not debug_mode:
        thread = threading.Thread(target=read_serial, daemon=True)
        thread.start()
    socketio.run(app, debug=debug_mode, port=5000)