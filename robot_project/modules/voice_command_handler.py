import os
import importlib
import logging
import inspect
import re

class VoiceCommandHandler:
    def __init__(self, commands_dir):
        """
        Initialize voice command handler
        
        :param commands_dir: Directory containing voice command scripts
        """
        self.logger = logging.getLogger(__name__)
        self.commands_dir = commands_dir
        self.commands = {}
        self.reload_commands()
    
    def reload_commands(self):
        """
        Dynamically load all command scripts from the commands directory
        """
        self.commands.clear()
        
        # Ensure commands directory exists
        if not os.path.exists(self.commands_dir):
            os.makedirs(self.commands_dir)
        
        # Load all Python files in the commands directory
        for filename in os.listdir(self.commands_dir):
            if filename.endswith('.py') and not filename.startswith('__'):
                try:
                    # Convert filename to module name
                    module_name = f"voice_commands.{filename[:-3]}"
                    
                    # Import the module
                    module = importlib.import_module(module_name)
                    
                    # Find and register command functions
                    for name, func in inspect.getmembers(module, inspect.isfunction):
                        if hasattr(func, 'voice_command'):
                            self.commands[func.voice_command.lower()] = func
                    
                    self.logger.info(f"Loaded commands from {filename}")
                except Exception as e:
                    self.logger.error(f"Error loading command script {filename}: {e}")
    
    def process_command(self, text):
        """
        Process a voice command
        
        :param text: Recognized voice command text
        :return: Result of command execution
        """
        # Normalize the text
        text = text.lower().strip()
        
        # Try exact match first
        if text in self.commands:
            try:
                return self.commands[text]()
            except Exception as e:
                self.logger.error(f"Error executing command {text}: {e}")
                return f"Error executing command: {e}"
        
        # Try partial matching
        for command, func in self.commands.items():
            if command in text:
                try:
                    return func()
                except Exception as e:
                    self.logger.error(f"Error executing command {command}: {e}")
                    return f"Error executing command: {e}"
        
        return "Command not recognized"

def voice_command(command):
    """
    Decorator to mark functions as voice commands
    
    :param command: Trigger phrase for the command
    :return: Decorated function
    """
    def decorator(func):
        func.voice_command = command
        return func
    return decorator
