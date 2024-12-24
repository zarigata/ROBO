import logging
import traceback
import sys

class GlobalErrorHandler:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def handle_error(self, error, context="Unknown"):
        """
        Centralized error handling method with logging and optional recovery
        
        Args:
            error (Exception): The exception that occurred
            context (str): Context where the error occurred
        """
        # Log the full error traceback
        error_message = f"Error in {context}: {str(error)}"
        self.logger.error(error_message)
        self.logger.error(traceback.format_exc())
        
        # Optional: Send error notification (e.g., to a monitoring service)
        # self.send_error_notification(error_message)
    
    def send_error_notification(self, message):
        """
        Placeholder for sending error notifications via email, SMS, etc.
        """
        # Implement notification logic here
        pass
    
    def safe_exit(self, exit_code=1):
        """
        Safely exit the application with proper logging
        """
        self.logger.critical("Critical error. Initiating safe shutdown.")
        sys.exit(exit_code)
