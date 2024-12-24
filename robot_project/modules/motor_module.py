import RPi.GPIO as GPIO
import logging
import time

from utils.error_handler import GlobalErrorHandler

class MotorController:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_handler = GlobalErrorHandler()
        
        # GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        
        # Motor A connections
        self.ENA = 25  # Enable pin
        self.IN1 = 23  # Input 1
        self.IN2 = 24  # Input 2
        
        # Motor B connections
        self.ENB = 17  # Enable pin
        self.IN3 = 27  # Input 3
        self.IN4 = 22  # Input 4
        
        # Setup GPIO pins
        self.setup_gpio()
    
    def setup_gpio(self):
        """
        Setup GPIO pins for motor control
        """
        try:
            # Set up motor control pins as output
            GPIO.setup(self.ENA, GPIO.OUT)
            GPIO.setup(self.IN1, GPIO.OUT)
            GPIO.setup(self.IN2, GPIO.OUT)
            
            GPIO.setup(self.ENB, GPIO.OUT)
            GPIO.setup(self.IN3, GPIO.OUT)
            GPIO.setup(self.IN4, GPIO.OUT)
            
            # Create PWM instances for speed control
            self.pwm_a = GPIO.PWM(self.ENA, 100)
            self.pwm_b = GPIO.PWM(self.ENB, 100)
            
            # Start PWM with 0% duty cycle
            self.pwm_a.start(0)
            self.pwm_b.start(0)
            
            self.logger.info("Motor GPIO setup completed successfully")
        
        except Exception as e:
            self.error_handler.handle_error(e, "Motor GPIO Setup")
    
    def move_forward(self, speed=50, duration=1):
        """
        Move robot forward
        
        Args:
            speed (int): Motor speed (0-100)
            duration (float): Movement duration in seconds
        """
        try:
            # Set motor directions for forward movement
            GPIO.output(self.IN1, GPIO.HIGH)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.IN3, GPIO.HIGH)
            GPIO.output(self.IN4, GPIO.LOW)
            
            # Set motor speeds
            self.pwm_a.ChangeDutyCycle(speed)
            self.pwm_b.ChangeDutyCycle(speed)
            
            # Move for specified duration
            time.sleep(duration)
            self.stop()
        
        except Exception as e:
            self.error_handler.handle_error(e, "Forward Movement")
    
    def move_backward(self, speed=50, duration=1):
        """
        Move robot backward
        
        Args:
            speed (int): Motor speed (0-100)
            duration (float): Movement duration in seconds
        """
        try:
            # Set motor directions for backward movement
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.HIGH)
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.HIGH)
            
            # Set motor speeds
            self.pwm_a.ChangeDutyCycle(speed)
            self.pwm_b.ChangeDutyCycle(speed)
            
            # Move for specified duration
            time.sleep(duration)
            self.stop()
        
        except Exception as e:
            self.error_handler.handle_error(e, "Backward Movement")
    
    def stop(self):
        """
        Stop all motor movement
        """
        try:
            # Set all motor control pins to low
            GPIO.output(self.IN1, GPIO.LOW)
            GPIO.output(self.IN2, GPIO.LOW)
            GPIO.output(self.IN3, GPIO.LOW)
            GPIO.output(self.IN4, GPIO.LOW)
            
            # Stop PWM
            self.pwm_a.ChangeDutyCycle(0)
            self.pwm_b.ChangeDutyCycle(0)
            
            self.logger.info("Motors stopped")
        
        except Exception as e:
            self.error_handler.handle_error(e, "Motor Stop")
    
    def execute_command(self, command):
        """
        Execute motor commands based on voice input
        
        Args:
            command (str): Voice command to execute
        """
        try:
            if "forward" in command:
                self.move_forward()
            elif "backward" in command:
                self.move_backward()
            elif "stop" in command:
                self.stop()
            else:
                self.logger.warning(f"Unrecognized motor command: {command}")
        
        except Exception as e:
            self.error_handler.handle_error(e, f"Motor Command: {command}")
    
    def __del__(self):
        """
        Cleanup GPIO on object destruction
        """
        try:
            self.stop()
            GPIO.cleanup()
            self.logger.info("GPIO cleaned up successfully")
        except Exception as e:
            self.error_handler.handle_error(e, "GPIO Cleanup")
