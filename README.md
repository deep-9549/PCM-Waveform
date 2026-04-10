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

## Issues Faced and Fixes

- We hit repeated `PermissionError(13, 'Access is denied')` errors on `COM12` when multiple server instances tried to open the same serial port. This was fixed by making the app run in a single stable process and adding a startup lock so a second copy exits cleanly instead of fighting for the port.
- The Arduino output was not always a plain number, so the web UI originally received no samples. We fixed that by parsing labeled serial lines such as `Analog: 621  PCM: 155` and by ignoring occasional noisy bytes during serial reads.
- A generated `.server.lock` file is now ignored by Git so it stays local and does not get pushed again.