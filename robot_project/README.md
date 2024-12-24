# Home Robot Project

## Overview
A Raspberry Pi 4 based home robot with capabilities:
- Object Detection
- Voice Command Recognition
- Autonomous Movement

## Hardware Requirements
- Raspberry Pi 4
- Camera Module
- Motor Kit
- Speakers
- Microphone

## Setup Instructions
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure hardware connections in `config/hardware_config.py`

3. Run main robot script:
```bash
python src/main.py
```

## Modules
- `src/movement.py`: Robot locomotion control
- `src/object_detection.py`: Computer vision for object recognition
- `src/voice_command.py`: Speech recognition and processing
- `src/navigation.py`: Path planning and obstacle avoidance

## Configuration
Adjust robot behavior in `config/` directory configuration files.

## Troubleshooting
Check `logs/` directory for runtime logs and error tracking.
