#!/bin/bash

# Robot Startup Script

# Set up virtual environment
python3 -m venv robot_env
source robot_env/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the robot main script
python src/main.py

# Optional: Keep terminal open for debugging
read -p "Press enter to exit"
