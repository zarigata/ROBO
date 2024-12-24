from ultralytics import YOLO
import cv2
import logging
import numpy as np

from utils.error_handler import GlobalErrorHandler

class ObjectDetector:
    def __init__(self, model_path='/home/pi/ROBO/robot_project/config/yolov8n.pt'):
        self.logger = logging.getLogger(__name__)
        self.error_handler = GlobalErrorHandler()
        
        try:
            # Load a lightweight YOLO model (nano version)
            self.model = YOLO(model_path)
            self.logger.info("Object detection model loaded successfully")
        except Exception as e:
            self.error_handler.handle_error(e, "Object Detection Model Loading")
            self.model = None
    
    def detect(self, confidence_threshold=0.5):
        """
        Detect objects in the current environment
        
        Args:
            confidence_threshold (float): Minimum confidence to report an object
        
        Returns:
            list: Detected objects with their details
        """
        try:
            # Capture frame from camera
            camera = cv2.VideoCapture(0)
            if not camera.isOpened():
                self.logger.error("Could not open camera")
                return []
            
            ret, frame = camera.read()
            camera.release()
            
            if not ret:
                self.logger.warning("Failed to capture frame")
                return []
            
            # Run inference
            results = self.model(frame, conf=confidence_threshold)
            
            # Process and return detected objects
            detected_objects = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    cls = int(box.cls[0])
                    conf = float(box.conf[0])
                    label = self.model.names[cls]
                    
                    detected_objects.append({
                        'label': label,
                        'confidence': conf
                    })
            
            return detected_objects
        
        except Exception as e:
            self.error_handler.handle_error(e, "Object Detection")
            return []
    
    def scan_environment(self):
        """
        Comprehensive environment scanning method
        """
        try:
            objects = self.detect()
            if objects:
                self.logger.info("Environment Scan Results:")
                for obj in objects:
                    self.logger.info(f"- {obj['label']} (Confidence: {obj['confidence']:.2f})")
            else:
                self.logger.info("No objects detected in the environment")
        except Exception as e:
            self.error_handler.handle_error(e, "Environment Scanning")
