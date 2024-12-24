import logging
import sys
import os

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.movement import RobotMovement
from src.object_detection import ObjectDetector
from src.voice_command import VoiceCommandProcessor
from src.navigation import NavigationSystem

# Configure logging
logging.basicConfig(
    filename='../logs/robot.log', 
    level=logging.INFO, 
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('RobotMain')

class HomeRobot:
    def __init__(self):
        try:
            self.movement = RobotMovement()
            self.object_detector = ObjectDetector()
            self.voice_processor = VoiceCommandProcessor()
            self.navigation = NavigationSystem()
            
            logger.info("Robot systems initialized successfully")
        except Exception as e:
            logger.error(f"Initialization error: {e}")
            raise

    def run(self):
        try:
            while True:
                # Listen for voice commands
                command = self.voice_processor.listen()
                
                if command:
                    self.process_command(command)
                
                # Continuous object detection
                detected_objects = self.object_detector.detect_objects()
                if detected_objects:
                    self.handle_object_detection(detected_objects)
        
        except KeyboardInterrupt:
            logger.info("Robot shutdown initiated")
        except Exception as e:
            logger.error(f"Runtime error: {e}")

    def process_command(self, command):
        logger.info(f"Processing command: {command}")
        
        if "move forward" in command:
            self.movement.forward()
        elif "move backward" in command:
            self.movement.backward()
        elif "turn left" in command:
            self.movement.turn_left()
        elif "turn right" in command:
            self.movement.turn_right()
        elif "stop" in command:
            self.movement.stop()

    def handle_object_detection(self, objects):
        logger.info(f"Objects detected: {objects}")
        # Implement object avoidance or interaction logic
        self.navigation.avoid_obstacles(objects)

def main():
    robot = HomeRobot()
    robot.run()

if __name__ == "__main__":
    main()
