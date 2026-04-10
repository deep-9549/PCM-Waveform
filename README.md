# PCM Waveform Monitor

A Flask and Socket.IO project that streams Arduino ADC values to a web UI and visualizes the PCM waveform in real time.

## Features

- Reads Arduino serial data from Python
- Sends live samples to the browser with Socket.IO
- Displays voltage, raw ADC, min/max, and a scrolling waveform
- Includes a theory page explaining PCM concepts

## Requirements

- Python 3.13
- Git
- A virtual environment is recommended
- An Arduino connected on the configured COM port

The Python dependencies are listed in [requirements.txt](requirements.txt).

## Installation

1. Clone the repository.
2. Open a terminal in the project folder.
3. Create and activate a virtual environment.

```powershell
python -m venv .venv
& ".venv\Scripts\Activate.ps1"
```

4. Install the dependencies.

```powershell
& ".venv\Scripts\python.exe" -m pip install -r requirements.txt
```

5. Connect your Arduino and confirm the COM port in `server.py`.

## Run

```powershell
& ".venv\\Scripts\\python.exe" server.py
```

## Notes

- Update `SERIAL_PORT` in `server.py` if your Arduino is not on `COM3`.
- The app uses `Flask`, `Flask-SocketIO`, and `pyserial` from `requirements.txt`.

## Troubleshooting

- If the browser does not load the page, make sure the Flask server is running and open http://127.0.0.1:5000/.
- If you see `ModuleNotFoundError`, reinstall dependencies with `& ".venv\Scripts\python.exe" -m pip install -r requirements.txt`.
- If the serial port fails, confirm the Arduino is connected and update `SERIAL_PORT` in `server.py` to the correct COM port.
- If Socket.IO does not connect, refresh the page after the server starts and check that port 5000 is not blocked.