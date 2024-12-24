import logging
import sys
import traceback

from modules.voice_module import VoiceCommandHandler
from modules.esp_communication import ESPCommunicationManager
from sensors.object_detection import ObjectDetector
from utils.error_handler import GlobalErrorHandler

class RobotController:
    def __init__(self):
        # Configure global logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='/home/pi/ROBO/robot_project/logs/robot_main.log'
        )
        self.logger = logging.getLogger(__name__)
        
        # Initialize modules with error handling
        self.error_handler = GlobalErrorHandler()
        self.voice_handler = None
        self.esp_comm = None
        self.object_detector = None
        
        self.initialize_modules()
    
    def initialize_modules(self):
        try:
            self.voice_handler = VoiceCommandHandler()
            self.esp_comm = ESPCommunicationManager()
            self.esp_comm.connect()
            self.object_detector = ObjectDetector()
        except Exception as e:
            self.error_handler.handle_error(e, "Module Initialization")
    
    def run(self):
        try:
            while True:
                # Main robot control loop
                voice_command = self.voice_handler.listen()
                if voice_command:
                    self.process_command(voice_command)
                
                # Periodic object detection
                detected_objects = self.object_detector.detect()
                if detected_objects:
                    self.handle_object_detection(detected_objects)
                
                # Periodic sensor data retrieval
                self.check_environment_sensors()
        
        except KeyboardInterrupt:
            self.logger.info("Robot shutdown initiated.")
        except Exception as e:
            self.error_handler.handle_error(e, "Main Robot Loop")
    
    def process_command(self, command):
        try:
            # Route commands to ESP motor controller
            if "move forward" in command:
                self.esp_comm.send_motor_command("forward", speed=70)
            elif "move backward" in command:
                self.esp_comm.send_motor_command("backward", speed=70)
            elif "stop" in command:
                self.esp_comm.send_motor_command("stop")
        except Exception as e:
            self.error_handler.handle_error(e, f"Command Processing: {command}")
    
    def handle_object_detection(self, objects):
        try:
            # Logic for handling detected objects
            for obj in objects:
                self.logger.info(f"Detected object: {obj}")
                # Add specific handling logic here
        except Exception as e:
            self.error_handler.handle_error(e, "Object Detection Handling")

    def check_environment_sensors(self):
        try:
            # Request sensor data periodically
            self.esp_comm.send_sensor_request("environment")
            sensor_data = self.esp_comm.get_sensor_data()
            
            if sensor_data:
                self.logger.info(f"Environment Sensors: {sensor_data}")
                # Add logic to react to sensor data if needed
        except Exception as e:
            self.error_handler.handle_error(e, "Sensor Data Retrieval")

def main():
    robot = RobotController()
    robot.run()

if __name__ == "__main__":
    main()
