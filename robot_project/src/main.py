import logging
import logging.config
import logging.handlers
import threading
import time
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import RobotConfig
from modules.vision_module import VisionModule
from modules.voice_module import VoiceModule
from modules.motor_module import MotorModule
from utils.error_handler import RobotErrorHandler

def setup_logging():
    """
    Safely set up logging with multiple fallback mechanisms
    """
    try:
        # Ensure logs directory exists
        os.makedirs(RobotConfig.LOGS_DIR, exist_ok=True)
        
        # Try to set directory and file permissions
        try:
            os.chmod(RobotConfig.LOGS_DIR, 0o777)
        except Exception as e:
            print(f"Warning: Could not set logs directory permissions: {e}")
        
        # Configure logging
        logging.config.dictConfig(RobotConfig.LOGGING_CONFIG)
        
        # Additional fallback logging setup
        root_logger = logging.getLogger()
        
        # Ensure console handler
        if not any(isinstance(handler, logging.StreamHandler) for handler in root_logger.handlers):
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s'))
            root_logger.addHandler(console_handler)
        
        return True
    except Exception as e:
        # Absolute fallback logging
        print(f"Critical error setting up logging: {e}")
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('/tmp/robot_assistant_fallback.log', mode='a')
            ]
        )
        return False

class RobotAssistant:
    def __init__(self):
        # Set up logging first
        logging_setup_success = setup_logging()
        
        # If logging setup failed, we'll use a basic logger
        self.logger = logging.getLogger(__name__)
        
        # Error handler
        self.error_handler = RobotErrorHandler()
        
        # Initialize modules
        self.modules = {}
        self._initialize_modules()
        
    def _initialize_modules(self):
        """Initialize all robot modules with error handling."""
        module_classes = {
            'vision': VisionModule,
            'voice': VoiceModule,
            'motor_control': MotorModule
        }
        
        for module_name, module_class in module_classes.items():
            try:
                if RobotConfig.MODULES.get(module_name, {}).get('enabled', False):
                    self.modules[module_name] = module_class()
                    self.logger.info(f"Initialized {module_name} module successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize {module_name} module: {e}")
                self.error_handler.handle_module_error(module_name, e)
    
    def start(self):
        """Start the robot assistant with module threads."""
        self.logger.info("Starting Robot Assistant")
        
        # Create threads for each module
        module_threads = []
        for module_name, module in self.modules.items():
            thread = threading.Thread(
                target=module.run, 
                name=f"{module_name}_thread",
                daemon=True
            )
            thread.start()
            module_threads.append(thread)
        
        # Main monitoring loop
        try:
            while True:
                # Check module health
                for thread in module_threads:
                    if not thread.is_alive():
                        self.logger.warning(f"Module {thread.name} has stopped unexpectedly")
                        self.error_handler.handle_thread_failure(thread.name)
                
                time.sleep(5)  # Check every 5 seconds
        
        except KeyboardInterrupt:
            self.logger.info("Robot Assistant shutting down")
        except Exception as e:
            self.logger.critical(f"Unexpected error in main loop: {e}")
            self.error_handler.handle_critical_error(e)
        finally:
            # Graceful shutdown
            for module_name, module in self.modules.items():
                module.stop()

def main():
    robot = RobotAssistant()
    robot.start()

if __name__ == "__main__":
    main()
