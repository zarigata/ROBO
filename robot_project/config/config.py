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
    
    # Ensure logs directory exists
    os.makedirs(LOGS_DIR, exist_ok=True)
    
    # Fallback log file path
    FALLBACK_LOG_PATH = '/tmp/robot_assistant.log'
    
    # Determine log file path with permission checks
    LOG_FILE_PATH = FALLBACK_LOG_PATH
    try:
        # Try to use project logs directory first
        project_log_path = os.path.join(LOGS_DIR, 'robot_assistant.log')
        
        # Check if we can write to the project log directory
        if os.access(LOGS_DIR, os.W_OK):
            # Try to create and write to the log file
            with open(project_log_path, 'a') as f:
                os.chmod(project_log_path, 0o666)
            LOG_FILE_PATH = project_log_path
    except Exception as e:
        print(f"Warning: Could not use project log path. Falling back to {FALLBACK_LOG_PATH}")
        print(f"Log path error details: {e}")
    
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
