import logging
import time
from adafruit_motorkit import MotorKit

class RobotMovement:
    def __init__(self):
        self.kit = MotorKit()
        self.logger = logging.getLogger('RobotMovement')
        self.logger.info("Movement system initialized")

    def forward(self, speed=0.5, duration=None):
        self.logger.info("Moving forward")
        self.kit.motor1.throttle = speed
        self.kit.motor2.throttle = speed
        if duration:
            time.sleep(duration)
            self.stop()

    def backward(self, speed=0.5, duration=None):
        self.logger.info("Moving backward")
        self.kit.motor1.throttle = -speed
        self.kit.motor2.throttle = -speed
        if duration:
            time.sleep(duration)
            self.stop()

    def turn_left(self, speed=0.5, duration=0.5):
        self.logger.info("Turning left")
        self.kit.motor1.throttle = -speed
        self.kit.motor2.throttle = speed
        time.sleep(duration)
        self.stop()

    def turn_right(self, speed=0.5, duration=0.5):
        self.logger.info("Turning right")
        self.kit.motor1.throttle = speed
        self.kit.motor2.throttle = -speed
        time.sleep(duration)
        self.stop()

    def stop(self):
        self.logger.info("Stopping motors")
        self.kit.motor1.throttle = 0
        self.kit.motor2.throttle = 0
