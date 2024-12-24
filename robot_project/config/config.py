import os

class RobotConfig:
    # Hardware Configuration
    WEBCAM_DEVICE = '/dev/video0'  # Logitech webcam
    RASPBERRY_PI = True

    # Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOGS_DIR = os.path.join(BASE_DIR, 'logs')
    
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
            'default': {
                'level': 'INFO',
                'formatter': 'standard',
                'class': 'logging.FileHandler',
                'filename': os.path.join(LOGS_DIR, 'robot_assistant.log')
            },
            'console': {
                'level': 'DEBUG',
                'formatter': 'standard',
                'class': 'logging.StreamHandler'
            }
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['default', 'console'],
                'level': 'INFO',
                'propagate': True
            }
        }
    }
