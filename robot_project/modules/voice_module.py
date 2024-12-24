import speech_recognition as sr
import logging
import json
import os

from utils.error_handler import GlobalErrorHandler

class VoiceCommandHandler:
    def __init__(self, commands_file='/home/pi/ROBO/robot_project/config/voice_commands.json'):
        self.logger = logging.getLogger(__name__)
        self.error_handler = GlobalErrorHandler()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.commands_file = commands_file
        self.commands = self.load_commands()
    
    def load_commands(self):
        """
        Load voice commands from a JSON configuration file
        """
        try:
            with open(self.commands_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.warning(f"Commands file {self.commands_file} not found. Using empty command set.")
            return {}
        except json.JSONDecodeError:
            self.error_handler.handle_error(
                Exception("Invalid JSON in commands file"), 
                "Voice Command Loading"
            )
            return {}
    
    def reload_commands(self):
        """
        Dynamically reload voice commands from configuration file
        """
        self.commands = self.load_commands()
        self.logger.info("Voice commands reloaded successfully")
    
    def listen(self, timeout=5):
        """
        Listen for voice commands with error handling
        
        Args:
            timeout (int): Maximum seconds to listen for a command
        
        Returns:
            str: Recognized command or None
        """
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                self.logger.info("Listening for command...")
                
                audio = self.recognizer.listen(source, timeout=timeout)
                command = self.recognizer.recognize_google(audio).lower()
                
                self.logger.info(f"Recognized command: {command}")
                return self.process_command(command)
        
        except sr.UnknownValueError:
            self.logger.warning("Could not understand audio")
        except sr.RequestError as e:
            self.error_handler.handle_error(e, "Speech Recognition Request")
        except Exception as e:
            self.error_handler.handle_error(e, "Voice Command Listening")
        
        return None
    
    def process_command(self, command):
        """
        Process and validate recognized voice command
        
        Args:
            command (str): Raw voice command
        
        Returns:
            str: Processed command or None
        """
        try:
            # Basic command matching and validation
            for key, variations in self.commands.items():
                if any(variant in command for variant in variations):
                    return key
            
            self.logger.warning(f"No matching command found for: {command}")
            return None
        
        except Exception as e:
            self.error_handler.handle_error(e, f"Command Processing: {command}")
            return None
