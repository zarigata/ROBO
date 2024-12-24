#!/bin/bash

# Robot Assistant Startup Script

# Set environment
export PROJECT_ROOT="/home/pi/ROBO/robot_project"
export PYTHONPATH="${PROJECT_ROOT}"

# Ensure logs directory exists and is writable
mkdir -p "${PROJECT_ROOT}/logs"
chmod 777 "${PROJECT_ROOT}/logs"

# Install system dependencies
sudo apt-get update
sudo apt-get install -y \
    python3-pyaudio \
    portaudio19-dev

# Activate virtual environment
source "${PROJECT_ROOT}/venv/bin/activate"

# Upgrade pip
pip install --upgrade pip

# Install project dependencies
pip install --no-warn-script-location \
    numpy \
    opencv-python \
    SpeechRecognition \
    pyserial \
    RPi.GPIO \
    python-json-logger

# Start the robot assistant
python "${PROJECT_ROOT}/src/main.py"
