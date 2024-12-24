from camera_module import CameraModule
from detector import Detector
from audio_module import AudioModule
import argparse
import time
import os

class RobotAssistant:
    def __init__(self):
        self.camera = CameraModule()
        self.detector = Detector()
        self.audio = AudioModule()
        self._setup_voice_commands()

    def _setup_voice_commands(self):
        """Setup default voice commands"""
        self.audio.register_command("register location", self._handle_register_location)
        self.audio.register_command("list locations", self._handle_list_locations)
        self.audio.register_command("start detection", self._handle_start_detection)

    def _handle_register_location(self, command_text):
        """Handle the register location command"""
        print("Please say the location name...")
        location_name = self.audio.listen_for_command()
        if location_name:
            print(f"Registering location: {location_name}")
            frame = self.camera.capture_frame()
            objects = self.detector.register_location(location_name, frame)
            print(f"Detected objects at {location_name}:")
            for obj in objects:
                print(f"- {obj['class']} (confidence: {obj['confidence']:.2f})")

    def _handle_list_locations(self, command_text):
        """Handle the list locations command"""
        print("Registered locations:")
        for location, objects in self.detector.locations.items():
            print(f"\n{location}:")
            for obj in objects:
                print(f"- {obj['class']} (confidence: {obj['confidence']:.2f})")

    def _handle_start_detection(self, command_text):
        """Handle the start detection command"""
        print("Starting continuous detection. Say 'stop detection' to end.")
        try:
            while True:
                frame = self.camera.capture_frame()
                results = self.detector.detect_objects(frame)
                print("\nDetected objects:")
                for r in results.boxes.data.tolist():
                    x1, y1, x2, y2, score, class_id = r
                    print(f"- {results.names[int(class_id)]} (confidence: {score:.2f})")
                
                # Check for stop command
                command = self.audio.listen_for_command(timeout=1)
                if command and "stop detection" in command:
                    print("Stopping detection...")
                    break
        except KeyboardInterrupt:
            print("\nStopping detection...")

def main():
    parser = argparse.ArgumentParser(description='House Assistant Robot')
    parser.add_argument('--register', type=str, help='Register a new location')
    parser.add_argument('--list', action='store_true', help='List all registered locations')
    parser.add_argument('--voice', action='store_true', help='Start voice command mode')
    args = parser.parse_args()

    robot = RobotAssistant()

    if args.voice:
        print("Starting voice command mode...")
        print("Available commands:")
        print("- 'register location'")
        print("- 'list locations'")
        print("- 'start detection'")
        try:
            while True:
                robot.audio.listen_for_command()
        except KeyboardInterrupt:
            print("\nExiting voice command mode...")
    elif args.register:
        frame = robot.camera.capture_frame()
        objects = robot.detector.register_location(args.register, frame)
        print(f"Detected objects at {args.register}:")
        for obj in objects:
            print(f"- {obj['class']} (confidence: {obj['confidence']:.2f})")
    elif args.list:
        robot._handle_list_locations(None)
    else:
        robot._handle_start_detection(None)

if __name__ == "__main__":
    main()
