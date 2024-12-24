import logging
from modules.voice_command_handler import voice_command

logger = logging.getLogger(__name__)

@voice_command("hello")
def say_hello():
    """Respond with a greeting"""
    logger.info("Greeting command triggered")
    return "Hello! How can I help you today?"

@voice_command("what time is it")
def tell_time():
    """Tell the current time"""
    from datetime import datetime
    current_time = datetime.now().strftime("%I:%M %p")
    logger.info(f"Time requested: {current_time}")
    return f"The current time is {current_time}"

@voice_command("stop")
def stop_robot():
    """Stop all robot operations"""
    logger.warning("Stop command triggered")
    # Add logic to stop robot operations
    return "Stopping all operations"
