# Virtual Finger Writing

Virtual Finger Writing is a real-time computer vision project that lets users write in the air using hand gestures captured through a webcam. The application tracks finger movement and displays the writing on a virtual canvas.

## Features

- Real-time webcam-based hand tracking
- Air writing using index finger movement
- Gesture-based mode switching
- Multiple brush color options
- Eraser tool
- Clear canvas option
- One-click Windows runner

## Tech Stack

- Python
- OpenCV
- MediaPipe
- NumPy

## How It Works

The webcam captures live video input, and MediaPipe detects hand landmarks in each frame. The program tracks the index finger position and uses simple gestures to switch between drawing and selection modes.

## Gesture Controls

- Raise only the index finger to draw.
- Raise the index and middle finger together to enter selection mode.
- Move your finger to the top menu to select color, use eraser, or clear the canvas.
- Press `Q` to quit the application.

## Project Structure

```text
virtual-finger-writing/
|-- virtual_finger_writing.py
|-- requirements.txt
|-- run_air_writing.bat
|-- README.md
|-- .gitignore
```

## Requirements

- Python 3.11 or Python 3.12
- A working webcam

## Quick Start on Windows

For Windows users, run the project directly by double-clicking:

```text
run_air_writing.bat
```

The batch file automatically uses the project virtual environment and installs missing dependencies the first time it runs.

## Manual Installation

Open a terminal in the project folder and run:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run Manually

```powershell
.\.venv\Scripts\python.exe virtual_finger_writing.py
```

## Dependencies

```text
opencv-python==4.10.0.84
mediapipe==0.10.14
numpy==1.26.4
```

## Compatibility Note

This project uses the MediaPipe hand-tracking solutions API. For best compatibility, use Python 3.11 or 3.12. Newer Python versions may install a MediaPipe build that does not include the required legacy hand-tracking module.

## Future Improvements

- Save drawings as images
- Add adjustable brush thickness
- Improve stroke smoothing
- Add handwriting-to-text conversion

## Author

Khushi
