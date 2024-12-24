import cv2
import logging
import numpy as np
import time
from config.config import RobotConfig

class VisionModule:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.camera = None
        self.running = False
        self._initialize_camera()
    
    def _initialize_camera(self):
        """Initialize the webcam."""
        try:
            # Try multiple video device indices
            for device in range(3):  # Try devices 0, 1, 2
                self.camera = cv2.VideoCapture(device)
                if self.camera.isOpened():
                    # Only log if we want to show debug information
                    # self.logger.debug(f"Successfully opened camera on device {device}")
                    break
            
            if not self.camera or not self.camera.isOpened():
                raise IOError("Cannot open any webcam")
            
            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        except Exception as e:
            self.logger.error(f"Camera initialization failed: {e}")
            raise
    
    def detect_objects(self, frame):
        """
        Basic object detection using Haar Cascades
        Replace with more advanced detection as needed
        """
        try:
            # Load a pre-trained classifier (face detection as an example)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # Convert to grayscale for detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            
            return [{'type': 'face', 'count': len(faces)}]
        except Exception as e:
            self.logger.error(f"Object detection error: {e}")
            return []
    
    def run(self):
        """Main vision processing loop."""
        self.running = True
        
        while self.running:
            try:
                # Capture frame
                ret, frame = self.camera.read()
                if not ret:
                    self.logger.error("Failed to capture frame")
                    time.sleep(1)
                    continue
                
                # Detect objects
                objects = self.detect_objects(frame)
                
                # Only log objects if there are any
                if objects and objects[0]['count'] > 0:
                    self.logger.info(f"Detected objects: {objects}")
                
                time.sleep(0.1)  # Prevent high CPU usage
            
            except Exception as e:
                self.logger.error(f"Error in vision processing: {e}")
                time.sleep(1)
    
    def stop(self):
        """Stop the vision module."""
        self.running = False
        if self.camera:
            self.camera.release()
