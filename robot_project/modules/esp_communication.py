import serial
import json
import logging
import threading
import queue
import time

from utils.error_handler import GlobalErrorHandler

class ESPCommunicationManager:
    def __init__(self, port='/dev/ttyUSB0', baud_rate=115200):
        self.logger = logging.getLogger(__name__)
        self.error_handler = GlobalErrorHandler()
        
        self.port = port
        self.baud_rate = baud_rate
        self.serial_connection = None
        
        # Thread-safe communication queues
        self.send_queue = queue.Queue()
        self.receive_queue = queue.Queue()
        
        # Communication threads
        self.send_thread = None
        self.receive_thread = None
        
        self.is_running = False
    
    def connect(self):
        """
        Establish serial connection with ESP modules
        """
        try:
            self.serial_connection = serial.Serial(
                port=self.port, 
                baudrate=self.baud_rate, 
                timeout=1
            )
            self.is_running = True
            
            # Start communication threads
            self.send_thread = threading.Thread(target=self._send_messages)
            self.receive_thread = threading.Thread(target=self._receive_messages)
            
            self.send_thread.start()
            self.receive_thread.start()
            
            self.logger.info(f"Connected to ESP modules on {self.port}")
        except Exception as e:
            self.error_handler.handle_error(e, "ESP Module Connection")
    
    def _send_messages(self):
        """
        Thread for sending messages to ESP modules
        """
        while self.is_running:
            try:
                if not self.send_queue.empty():
                    message = self.send_queue.get()
                    encoded_message = json.dumps(message).encode('utf-8') + b'\n'
                    self.serial_connection.write(encoded_message)
                    self.logger.debug(f"Sent message: {message}")
                time.sleep(0.1)
            except Exception as e:
                self.error_handler.handle_error(e, "Message Sending")
    
    def _receive_messages(self):
        """
        Thread for receiving messages from ESP modules
        """
        while self.is_running:
            try:
                if self.serial_connection.in_waiting:
                    message = self.serial_connection.readline().decode('utf-8').strip()
                    if message:
                        parsed_message = json.loads(message)
                        self.receive_queue.put(parsed_message)
                        self.logger.debug(f"Received message: {parsed_message}")
                time.sleep(0.1)
            except Exception as e:
                self.error_handler.handle_error(e, "Message Receiving")
    
    def send_motor_command(self, command, speed=50):
        """
        Send motor control command to ESP motor controller
        """
        message = {
            'type': 'motor_command',
            'command': command,
            'speed': speed
        }
        self.send_queue.put(message)
    
    def send_sensor_request(self, sensor_type):
        """
        Request sensor data from ESP sensor hub
        """
        message = {
            'type': 'sensor_request',
            'sensor': sensor_type
        }
        self.send_queue.put(message)
    
    def get_sensor_data(self, timeout=2):
        """
        Retrieve sensor data with timeout
        """
        try:
            return self.receive_queue.get(timeout=timeout)
        except queue.Empty:
            self.logger.warning("No sensor data received")
            return None
    
    def close(self):
        """
        Close serial connection and stop threads
        """
        self.is_running = False
        if self.send_thread:
            self.send_thread.join()
        if self.receive_thread:
            self.receive_thread.join()
        
        if self.serial_connection:
            self.serial_connection.close()
        
        self.logger.info("ESP Communication Manager closed")
