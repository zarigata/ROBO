import logging
from modules.voice_command_handler import voice_command
from modules.motor_module import MotorModule

logger = logging.getLogger(__name__)
motor_controller = MotorModule()

@voice_command("move forward")
def move_forward():
    """Move the robot forward"""
    logger.info("Moving robot forward")
    motor_controller.move_forward()
    return "Moving forward"

@voice_command("move backward")
def move_backward():
    """Move the robot backward"""
    logger.info("Moving robot backward")
    motor_controller.move_backward()
    return "Moving backward"

@voice_command("turn left")
def turn_left():
    """Turn the robot left"""
    logger.info("Turning robot left")
    motor_controller.turn_left()
    return "Turning left"

@voice_command("turn right")
def turn_right():
    """Turn the robot right"""
    logger.info("Turning robot right")
    motor_controller.turn_right()
    return "Turning right"

@voice_command("stop moving")
def stop_motors():
    """Stop robot movement"""
    logger.info("Stopping robot motors")
    motor_controller.stop()
    return "Stopped moving"
