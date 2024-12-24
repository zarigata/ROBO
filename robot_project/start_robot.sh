#!/bin/bash

# Robot Assistant Startup Script

# Project root directory
PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Activate virtual environment
source "${PROJECT_ROOT}/venv/bin/activate"

# Set environment
export PYTHONPATH="${PROJECT_ROOT}:$PYTHONPATH"

# Ensure logs directory exists and is writable
mkdir -p "${PROJECT_ROOT}/logs"
chmod 777 "${PROJECT_ROOT}/logs"

# Ensure required system packages are installed
sudo apt-get update
sudo apt-get install -y \
    python3-pyaudio \
    portaudio19-dev \
    alsa-utils \
    jackd2 \
    pulseaudio \
    flac

# Install or upgrade Python dependencies
pip install --upgrade \
    SpeechRecognition \
    pyaudio \
    numpy \
    opencv-python \
    RPi.GPIO \
    python-json-logger

# Run the robot assistant
python "${PROJECT_ROOT}/src/main.py"
