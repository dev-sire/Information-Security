from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.exceptions import InvalidSignature
import random

class BaseDevice:
    def __init__(self, name):
        self.name = name
        self.status = False
        self.data = None
        self.private_key = None
        self.public_key = None
        self.certificate = None 

    def generate_keys(self):
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.public_key = self.private_key.public_key()

    def sign_data(self, data):
        signature = self.private_key.sign(
            data.encode(),
            padding=serialization.Prehashed(hashes.SHA256()),
            algorithm=hashes.SHA256()
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
    def __init__(self, name, type, unit):
        super().__init__(name)
        self.type = type
        self.unit = unit
        self.generate_keys()

    def read_data(self):
        self.data = random.uniform(20, 30)
        return f"Current {self.type}: {self.data} {self.unit}"

class CleaningSensor(BaseDevice):
    def __init__(self, name):
        super().__init__(name)
        self.generate_keys()

    def detect_dirt(self):
        dirt_level = random.randint(0, 100)
        self.data = f"Dirt Level: {dirt_level}%"
        return self.data

class LightSensor(BaseDevice):
    def __init__(self, name):
        super().__init__(name)
        self.generate_keys()

    def measure_light(self):
        light_level = random.randint(0, 100)
        self.data = f"Light Level: {light_level}%"
        return self.data

if __name__ == "__main__":
    home_sensor = HomeSensor("TemperatureSensor", "Temperature", "Celsius")
    cleaning_sensor = CleaningSensor("CleaningSensor")
    light_sensor = LightSensor("LightSensor")

    # Simulate data collection
    home_sensor_data = home_sensor.read_data()
    cleaning_sensor_data = cleaning_sensor.detect_dirt()
    light_sensor_data = light_sensor.measure_light()

    # Print data
    print(home_sensor_data)
    print(cleaning_sensor_data)
    print(light_sensor_data)