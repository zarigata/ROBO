import speech_recognition as sr
import logging
import pyttsx3

class VoiceCommandProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.text_to_speech = pyttsx3.init()
        self.logger = logging.getLogger('VoiceCommand')
        
        # Configure text-to-speech
        self.text_to_speech.setProperty('rate', 150)
        self.text_to_speech.setProperty('volume', 0.8)

    def listen(self, timeout=5):
        try:
            with self.microphone as source:
                self.logger.info("Listening for command...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=timeout)

            try:
                command = self.recognizer.recognize_google(audio).lower()
                self.logger.info(f"Recognized command: {command}")
                return command
            except sr.UnknownValueError:
                self.logger.warning("Could not understand audio")
                self.speak("Sorry, I didn't catch that.")
                return None
            except sr.RequestError:
                self.logger.error("Speech recognition service error")
                self.speak("I'm having trouble understanding you.")
                return None

        except Exception as e:
            self.logger.error(f"Voice command error: {e}")
            return None

    def speak(self, text):
        try:
            self.logger.info(f"Speaking: {text}")
            self.text_to_speech.say(text)
            self.text_to_speech.runAndWait()
        except Exception as e:
            self.logger.error(f"Text-to-speech error: {e}")
