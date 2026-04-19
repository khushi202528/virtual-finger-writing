@echo off
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    py -3.11 -m venv .venv
)
".venv\Scripts\python.exe" -m pip show mediapipe >nul 2>nul
if errorlevel 1 (
    ".venv\Scripts\python.exe" -m pip install --upgrade pip
    ".venv\Scripts\python.exe" -m pip install -r requirements.txt
)
".venv\Scripts\python.exe" virtual_finger_writing.py
pause
