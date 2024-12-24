from ultralytics import YOLO
import cv2
import yaml
import os

class Detector:
    def __init__(self):
        # Load YOLOv8n - the smallest and fastest model
        self.model = YOLO('yolov8n.pt')
        self.locations = {}
        self.load_locations()

    def load_locations(self):
        """Load saved locations from YAML file"""
        if os.path.exists('locations.yaml'):
            with open('locations.yaml', 'r') as f:
                self.locations = yaml.safe_load(f) or {}

    def save_locations(self):
        """Save locations to YAML file"""
        with open('locations.yaml', 'w') as f:
            yaml.dump(self.locations, f)

    def detect_objects(self, frame):
        """Detect objects in the frame"""
        results = self.model(frame, conf=0.5)
        return results[0]

    def register_location(self, name, frame):
        """Register a new location with its detected objects"""
        results = self.detect_objects(frame)
        detected_objects = []
        
        for r in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = r
            detected_objects.append({
                'class': results.names[int(class_id)],
                'confidence': score,
                'bbox': [x1, y1, x2, y2]
            })
        
        self.locations[name] = detected_objects
        self.save_locations()
        return detected_objects
