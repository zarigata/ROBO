# Hardware Configuration

# Motor Configuration
MOTOR_CONFIG = {
    'left_motor_pin': 1,   # Adjust based on your actual motor connections
    'right_motor_pin': 2,
    'default_speed': 0.5
}

# Camera Configuration
CAMERA_CONFIG = {
    'device_index': 0,     # Default camera
    'resolution': (640, 480),
    'framerate': 30
}

# Voice Configuration
VOICE_CONFIG = {
    'language': 'en-US',
    'recognition_sensitivity': 0.7,
    'wake_word': 'robot'
}

# Sensor Configuration
SENSOR_CONFIG = {
    'ultrasonic_trigger_pin': 17,
    'ultrasonic_echo_pin': 27,
    'infrared_sensor_pin': 22
}
