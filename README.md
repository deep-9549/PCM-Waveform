# PCM Waveform Monitor

A Flask and Socket.IO project that streams Arduino ADC values to a web UI and visualizes the PCM waveform in real time.

## Features

- Reads Arduino serial data from Python
- Sends live samples to the browser with Socket.IO
- Displays voltage, raw ADC, min/max, and a scrolling waveform
- Includes a theory page explaining PCM concepts

## Requirements

- Python 3.13
- Flask
- Flask-SocketIO
- pyserial
- An Arduino connected on the configured COM port

## Run

```powershell
& ".venv\\Scripts\\python.exe" server.py
```

## Notes

- Update `SERIAL_PORT` in `server.py` if your Arduino is not on `COM3`.