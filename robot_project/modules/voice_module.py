import logging
import time
import os

try:
    import speech_recognition as sr
except ImportError:
    sr = None
    print("Warning: speech_recognition module not available")

from config.config import RobotConfig
from modules.voice_command_handler import VoiceCommandHandler

class VoiceModule:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.recognizer = None
        self.microphone = None
        self.running = False
        
        # Setup voice command handler
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.commands_dir = os.path.join(project_root, 'voice_commands')
        self.command_handler = VoiceCommandHandler(self.commands_dir)
        
        # Initialize only if speech recognition is available
        if sr:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
            except Exception as e:
                self.logger.error(f"Voice module initialization failed: {e}")
                sr = None
    
    def process_voice_command(self, audio):
        """
        Process and interpret voice commands.
        """
        if not sr:
            self.logger.warning("Speech recognition not available")
            return None
        
        try:
            # Use Google Speech Recognition
            text = self.recognizer.recognize_google(
                audio, 
                language=RobotConfig.MODULES['voice']['language']
            )
            self.logger.info(f"Recognized command: {text}")
            
            # Process the command
            result = self.command_handler.process_command(text)
            self.logger.info(f"Command result: {result}")
            
            return text
        except sr.UnknownValueError:
            self.logger.warning("Could not understand audio")
        except sr.RequestError as e:
            self.logger.error(f"Could not request results; {e}")
        return None
    
    def run(self):
        """Main voice recognition loop."""
        if not sr:
            self.logger.warning("Cannot start voice module - speech recognition not available")
            return
        
        self.running = True
        self.logger.info("Voice module started")
        
        with self.microphone as source:
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source)
        
        while self.running:
            try:
                with self.microphone as source:
                    self.logger.debug("Listening for command")
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=3)
                
                # Process the recognized audio
                self.process_voice_command(audio)
                
                time.sleep(0.1)  # Prevent high CPU usage
            
            except Exception as e:
                self.logger.error(f"Error in voice processing: {e}")
                time.sleep(1)
    
    def stop(self):
        """Stop the voice module."""
        self.running = False
        self.logger.info("Voice module stopped")
    
    def reload_commands(self):
        """
        Reload voice command scripts
        """
        self.command_handler.reload_commands()
