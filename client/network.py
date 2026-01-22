# client/network.py
import socket
import threading
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from common.constants import PORT, HEADER_SIZE, FORMAT

class NetworkClient:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self, ip_address):
        try:
            self.client.connect((ip_address, PORT))
            self.connected = True
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def send_raw(self, data):
        """Sends raw bytes to the server"""
        if self.connected:
            try:
                self.client.send(data)
            except:
                self.connected = False

    def receive_loop(self, callback_func):
        """Runs in a thread, constantly listening for messages"""
        while self.connected:
            try:
                message = self.client.recv(HEADER_SIZE)
                if message:
                    callback_func(message)
                else:
                    self.connected = False
                    break
            except:
                self.connected = False
                break