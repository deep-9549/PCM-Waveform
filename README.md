# PCM Waveform Monitor

A Flask and Socket.IO project that streams Arduino ADC values to a web UI and visualizes the PCM waveform in real time.

It now includes:

- A desktop monitor with a live waveform, live ADC stats, and a theremin-style oscillator
- A second oscillator canvas that shows the generated tone shape and frequency in real time
- An aliasing and Nyquist demo with pause control and interactive sliders
- A mobile layout for phone screens with its own route at `/mobile`
- A live frequency readout so the pitch mapping is easy to explain during demos

## Features

- Reads Arduino serial data from Python
- Sends live samples to the browser with Socket.IO
- Displays voltage, raw ADC, min/max, and a scrolling waveform
- Plays a theremin-style tone where ADC value controls oscillator pitch
- Shows a second live oscillator waveform display with waveform selection
- Includes an aliasing and Nyquist demo with animated sampling visualization
- Includes a theory page explaining PCM concepts
- Provides a mobile-friendly view for phones and tablets

## Requirements

- Python 3.13
- Git
- A virtual environment is recommended
- An Arduino connected on the configured COM port
- A browser that supports the Web Audio API for the theremin demo

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

## Project Routes

- `/` opens the desktop PCM monitor
- `/mobile` opens the mobile-optimized view

The Flask app is bound to `0.0.0.0` on port `5000`, so devices on the same Wi-Fi network can open the site from your computer's LAN IP.

## Run

```powershell
& ".venv\\Scripts\\python.exe" server.py
```

Then open one of these in your browser:

- `http://127.0.0.1:5000/` for the desktop view
- `http://127.0.0.1:5000/mobile` for the mobile view
- `http://YOUR_LAN_IP:5000/mobile` on your phone while on the same Wi-Fi

## Demo Controls

- The desktop page has a Pause button that freezes the waveform and audio together.
- The Play Audio button starts a theremin-style oscillator whose pitch is controlled by the ADC value.
- The waveform selector lets you switch between sine, square, sawtooth, and triangle tones.
- The live frequency readout shows the current pitch in hertz.
- The aliasing page lets you compare signal frequency and sample rate and pause the animation while explaining Nyquist.

## Notes

- Update `SERIAL_PORT` in `server.py` if your Arduino is not on `COM3`.
- The app uses `Flask`, `Flask-SocketIO`, and `pyserial` from `requirements.txt`.
- The audio demo uses the browser's Web Audio API, so it usually needs a user click before sound starts.

## Troubleshooting

- If the browser does not load the page, make sure the Flask server is running and open http://127.0.0.1:5000/.
- If you see `ModuleNotFoundError`, reinstall dependencies with `& ".venv\Scripts\python.exe" -m pip install -r requirements.txt`.
- If the serial port fails, confirm the Arduino is connected and update `SERIAL_PORT` in `server.py` to the correct COM port.
- If Socket.IO does not connect, refresh the page after the server starts and check that port 5000 is not blocked.
- If the phone shows a bad request, make sure you are using `http://` and not `https://`.
- If audio does not start, click the Play Audio button once to satisfy the browser's audio permission requirement.

## Issues Faced and Fixes

- We hit repeated `PermissionError(13, 'Access is denied')` errors on `COM12` when multiple server instances tried to open the same serial port. This was fixed by making the app run in a single stable process and adding a startup lock so a second copy exits cleanly instead of fighting for the port.
- The Arduino output was not always a plain number, so the web UI originally received no samples. We fixed that by parsing labeled serial lines such as `Analog: 621  PCM: 155` and by ignoring occasional noisy bytes during serial reads.
- The server now exposes both desktop and mobile routes, and listens on `0.0.0.0` so devices on the same network can connect.
