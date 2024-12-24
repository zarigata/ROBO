import logging
import time
import RPi.GPIO as GPIO

class MotorModule:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.running = False
        
        # Motor GPIO pin configuration
        self.LEFT_MOTOR_PINS = {
            'forward': 17,   # GPIO pin for left motor forward
            'backward': 27   # GPIO pin for left motor backward
        }
        
        self.RIGHT_MOTOR_PINS = {
            'forward': 22,   # GPIO pin for right motor forward
            'backward': 23   # GPIO pin for right motor backward
        }
        
        # Initialize GPIO
        self._setup_gpio()
    
    def _setup_gpio(self):
        """Set up GPIO pins for motor control."""
        try:
            GPIO.setmode(GPIO.BCM)
            
            # Set up motor control pins as outputs
            for pin in list(self.LEFT_MOTOR_PINS.values()) + list(self.RIGHT_MOTOR_PINS.values()):
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.LOW)
            
            self.logger.info("Motor GPIO pins initialized successfully")
        except Exception as e:
            self.logger.error(f"GPIO setup failed: {e}")
    
    def move_forward(self, duration=None):
        """Move the robot forward."""
        try:
            GPIO.output(self.LEFT_MOTOR_PINS['forward'], GPIO.HIGH)
            GPIO.output(self.RIGHT_MOTOR_PINS['forward'], GPIO.HIGH)
            
            if duration:
                time.sleep(duration)
                self.stop_motors()
        except Exception as e:
            self.logger.error(f"Forward movement failed: {e}")
    
    def move_backward(self, duration=None):
        """Move the robot backward."""
        try:
            GPIO.output(self.LEFT_MOTOR_PINS['backward'], GPIO.HIGH)
            GPIO.output(self.RIGHT_MOTOR_PINS['backward'], GPIO.HIGH)
            
            if duration:
                time.sleep(duration)
                self.stop_motors()
        except Exception as e:
            self.logger.error(f"Backward movement failed: {e}")
    
    def turn_left(self, duration=None):
        """Turn the robot left."""
        try:
            GPIO.output(self.LEFT_MOTOR_PINS['backward'], GPIO.HIGH)
            GPIO.output(self.RIGHT_MOTOR_PINS['forward'], GPIO.HIGH)
            
            if duration:
                time.sleep(duration)
                self.stop_motors()
        except Exception as e:
            self.logger.error(f"Left turn failed: {e}")
    
    def turn_right(self, duration=None):
        """Turn the robot right."""
        try:
            GPIO.output(self.LEFT_MOTOR_PINS['forward'], GPIO.HIGH)
            GPIO.output(self.RIGHT_MOTOR_PINS['backward'], GPIO.HIGH)
            
            if duration:
                time.sleep(duration)
                self.stop_motors()
        except Exception as e:
            self.logger.error(f"Right turn failed: {e}")
    
    def stop_motors(self):
        """Stop all motor movement."""
        try:
            # Set all motor pins to LOW
            for pin in list(self.LEFT_MOTOR_PINS.values()) + list(self.RIGHT_MOTOR_PINS.values()):
                GPIO.output(pin, GPIO.LOW)
        except Exception as e:
            self.logger.error(f"Motor stop failed: {e}")
    
    def run(self):
        """Start motor module."""
        self.running = True
        self.logger.info("Motor module started")
        
        while self.running:
            # Example: Periodic checks or autonomous movement logic
            time.sleep(1)
    
    def stop(self):
        """Stop the motor module and clean up GPIO."""
        try:
            # Stop motors first
            self.stop_motors()
            
            # Clean up GPIO
            GPIO.cleanup()
            
            self.running = False
            self.logger.info("Motor module stopped")
        except Exception as e:
            self.logger.error(f"Motor module stop failed: {e}")
