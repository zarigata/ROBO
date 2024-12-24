import os
import logging
import sys

class RobotConfig:
    # Hardware Configuration
    WEBCAM_DEVICE = '/dev/video0'  # Logitech webcam
    RASPBERRY_PI = True

    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')
    
    # Ensure logs directory exists with full permissions
    os.makedirs(LOGS_DIR, exist_ok=True)
    try:
        os.chmod(LOGS_DIR, 0o777)
    except Exception as e:
        print(f"Warning: Could not set logs directory permissions: {e}")
    
    # Log file path
    LOG_FILE_PATH = os.path.join(LOGS_DIR, 'robot_assistant.log')
    
    # Ensure log file exists and is writable
    try:
        with open(LOG_FILE_PATH, 'a') as f:
            os.chmod(LOG_FILE_PATH, 0o666)
    except Exception as e:
        print(f"Warning: Could not set log file permissions: {e}")
    
    # Module Configurations
    MODULES = {
        'vision': {
            'enabled': True,
            'confidence_threshold': 0.6
        },
        'voice': {
            'enabled': True,
            'language': 'en-US'
        },
        'motor_control': {
            'enabled': True,
            'max_speed': 100
        }
    }

    # Logging Configuration
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.StreamHandler',
                'stream': sys.stdout
            },
            'file': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOG_FILE_PATH,
                'maxBytes': 10*1024*1024,  # 10 MB
                'backupCount': 3,
                'mode': 'a',
            }
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console', 'file'],
                'level': 'INFO',
                'propagate': True
            }
        }
    }
