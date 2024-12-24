# Raspberry Pi Robot Project

## Project Structure
```
robot_project/
│
├── main.py             # Main robot control script
├── requirements.txt    # Project dependencies
│
├── modules/            # Core functional modules
│   ├── voice_module.py
│   └── esp_communication.py
│
├── esp_firmware/       # ESP8266/ESP32 Firmware
│   ├── motor_controller/
│   │   └── motor_controller.ino
│   └── sensor_hub/
│       └── sensor_hub.ino
│
├── sensors/            # Sensor and detection modules
│   └── object_detection.py
│
├── utils/              # Utility functions
│   └── error_handler.py
│
├── config/             # Configuration files
│   └── voice_commands.json
│
└── logs/               # Log storage
```

## Setup Instructions

### Prerequisites
- Raspberry Pi 4
- Raspbian OS
- Python 3.7+

### Installation
1. Clone the repository
2. Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Download Lightweight YOLO Model
```bash
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt -O config/yolov8n.pt
```

### Running the Robot
```bash
python main.py
```

## ESP Firmware Setup

### Prerequisites
- Arduino IDE
- ESP8266 Board Package
- Libraries:
  - ESP8266WiFi
  - ESPNow
  - VL53L0X (for distance sensor)

### Firmware Flashing
1. Open Arduino IDE
2. Select appropriate ESP8266 board
3. Flash `motor_controller.ino` to motor control ESP
4. Flash `sensor_hub.ino` to sensor hub ESP

### Hardware Connections
- Motor Controller ESP:
  - Motor A: D1, D2, D5
  - Motor B: D3, D4, D6

- Sensor Hub ESP:
  - VL53L0X: I2C (SDA/SCL)
  - Additional sensors can be added

### Communication Protocol
- Uses ESP-NOW for low-latency communication
- Supports motor commands and sensor data retrieval

## Voice Commands
- "go forward"
- "go backward"
- "stop"
- "detect objects"

## Troubleshooting
- Ensure all GPIO connections are correct
- Check microphone and camera permissions
- Review logs in `logs/` directory

## Safety Notes
- Always supervise robot during operation
- Keep clear of moving parts
- Disconnect power when not in use
