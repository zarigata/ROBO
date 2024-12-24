import pyaudio
import wave
import speech_recognition as sr
import threading
import time
import queue
from datetime import datetime
import os

class AudioModule:
    def __init__(self, sample_rate=16000, chunk_size=1024):
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self.audio = pyaudio.PyAudio()
        self.recording = False
        self.audio_queue = queue.Queue()
        self.recognizer = sr.Recognizer()
        self.commands = {}
        self.recording_thread = None
        
        # Create recordings directory if it doesn't exist
        self.recordings_dir = "recordings"
        if not os.path.exists(self.recordings_dir):
            os.makedirs(self.recordings_dir)

    def register_command(self, command, callback):
        """Register a voice command with its callback function"""
        self.commands[command.lower()] = callback

    def remove_command(self, command):
        """Remove a registered voice command"""
        if command.lower() in self.commands:
            del self.commands[command.lower()]

    def _record_audio(self):
        """Internal method to record audio"""
        stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )

        while self.recording:
            data = stream.read(self.chunk_size)
            self.audio_queue.put(data)

        stream.stop_stream()
        stream.close()

    def start_recording(self):
        """Start recording audio"""
        self.recording = True
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.recording_thread.start()

    def stop_recording(self):
        """Stop recording audio and save to file"""
        if self.recording:
            self.recording = False
            self.recording_thread.join()
            
            # Save recorded audio
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(self.recordings_dir, f"recording_{timestamp}.wav")
            
            frames = []
            while not self.audio_queue.empty():
                frames.append(self.audio_queue.get())

            with wave.open(filename, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(self.sample_rate)
                wf.writeframes(b''.join(frames))
            
            return filename
        return None

    def listen_for_command(self, timeout=5):
        """Listen for a voice command with timeout"""
        with sr.Microphone() as source:
            print("Listening for command...")
            try:
                audio = self.recognizer.listen(source, timeout=timeout)
                text = self.recognizer.recognize_google(audio).lower()
                print(f"Heard: {text}")
                
                # Check if the text matches any registered commands
                for command, callback in self.commands.items():
                    if command in text:
                        callback(text)
                        return text
                
                return text
            except sr.WaitTimeoutError:
                print("No speech detected within timeout")
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
        return None

    def __del__(self):
        """Cleanup audio resources"""
        if self.recording:
            self.stop_recording()
        self.audio.terminate()

# Example usage of custom commands
def example_command_handler(text):
    print(f"Executing command for: {text}")

if __name__ == "__main__":
    # Test the module
    audio = AudioModule()
    
    # Register a test command
    audio.register_command("hello robot", example_command_handler)
    
    # Test recording
    print("Recording for 5 seconds...")
    audio.start_recording()
    time.sleep(5)
    filename = audio.stop_recording()
    print(f"Saved recording to: {filename}")
    
    # Test voice command
    result = audio.listen_for_command()
    if result:
        print(f"Command recognized: {result}")
