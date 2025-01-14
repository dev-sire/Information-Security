from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
import random
import socket

class BaseDevice:
    def __init__(self, name, host, port):
        self.name = name
        self.status = False
        self.data = None
        self.private_key = None
        self.public_key = None
        self.certificate = None
        self.host = host
        self.port = port
        self.socket = None

    def generate_keys(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def sign_data(self, data):
        hashed_data = hashes.Hash(hashes.SHA256())
        hashed_data.update(data.encode())
        digest = hashed_data.finalize()

        signature = self.private_key.sign(
            digest,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return signature

    def verify_signature(self, data, signature):
        try:
            self.public_key.verify(
                signature,
                data.encode(),
                padding=serialization.Prehashed(hashes.SHA256()),
                algorithm=hashes.SHA256()
            )
            return True
        except InvalidSignature:
            return False

    def send_message(self, recipient, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((recipient.host, recipient.port))
                s.sendall(message.encode())
        except Exception as e:
            print(f"Error sending message to {recipient.name}: {e}")

    def send_message_to_server(self, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.server_host, self.server_port))
                s.sendall(message.encode())
        except Exception as e:
            print(f"Error sending message to server: {e}")

    def receive_message(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((self.host, self.port))
                s.listen()
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        self.process_received_message(data)
        except Exception as e:
            print(f"Error receiving message: {e}")

    def process_received_message(self, data):
        try:
            message, signature = data.decode().split("|")
            self.receive_and_process_message(message, signature)
        except Exception as e:
            print(f"Error processing received message: {e}")

    def receive_and_process_message(self, message, signature):
        if self.verify_signature(message, signature):
            decrypted_message = self.decrypt_message(message)
            command = self.extract_command(decrypted_message)
            self.execute_command(command)
        else:
            print(f"Invalid signature for message to {self.name}")

    def decrypt_message(self, encrypted_message):
        decrypted_message = self.private_key.decrypt(
            encrypted_message,
            padding=serialization.PKCS1v15()
        )
        return decrypted_message.decode()

    def extract_command(self, decrypted_message):
        command = decrypted_message.split(":")[1].strip()
        return command

    def execute_command(self, command):
        if command == "start":
            self.status = True
            print(f"Starting {self.name}")
        elif command == "stop":
            self.status = False
            print(f"Stopping {self.name}")
        else:
            print(f"Unknown command: {command}")

class HomeSensor(BaseDevice):
    def __init__(self, name, type, unit, host, port):
        super().__init__(name, host, port)
        self.type = type
        self.unit = unit
        self.generate_keys()

    def read_data(self):
        self.data = random.uniform(20, 30)
        return f"Current {self.type}: {self.data} {self.unit}"

class CleaningSensor(BaseDevice):
    def __init__(self, name, host, port):
        super().__init__(name, host, port)
        self.generate_keys()

    def detect_dirt(self):
        dirt_level = random.randint(0, 100)
        self.data = f"Dirt Level: {dirt_level}%"
        return self.data

class LightSensor(BaseDevice):
    def __init__(self, name, host, port):
        super().__init__(name, host, port)
        self.generate_keys()

    def measure_light(self):
        light_level = random.randint(0, 100)
        self.data = f"Light Level: {light_level}%"
        return self.data
