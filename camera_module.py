from picamera2 import Picamera2
import time
import cv2
import numpy as np

class CameraModule:
    def __init__(self):
        self.camera = Picamera2()
        # Configure camera for 640x480 resolution
        config = self.camera.create_preview_configuration(main={"size": (640, 480)})
        self.camera.configure(config)
        self.camera.start()
        # Allow camera to warm up
        time.sleep(2)

    def capture_frame(self):
        """Capture a single frame from the camera"""
        frame = self.camera.capture_array()
        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def __del__(self):
        """Cleanup camera resources"""
        if hasattr(self, 'camera'):
            self.camera.stop()
            self.camera.close()
