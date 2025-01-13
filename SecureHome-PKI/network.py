import socket
import ssl
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes

class WirelessNetwork:
    def __init__(self, server_address, server_certificate):
        self.server_address = server_address
        self.server_certificate = server_certificate
        self.context = ssl.create_default_context(cafile="server.crt", capath=server_certificate)
        self.context.check_hostname = False  # For development purposes, remove for production
        self.context.verify_mode = ssl.CERT_REQUIRED  # Enforce certificate verification
        self.sockets = {}

    def connect_device(self, device):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with self.context.wrap_socket(client_socket, server_hostname=self.server_address) as sock:
            sock.connect(self.server_address)
            # Send device certificate for authentication
            sock.sendall(device.certificate.public_bytes(encoding=serialization.Encoding.PEM))
            # Receive and verify server certificate
            server_cert_bytes = sock.recv(1024)
            server_cert = serialization.load_pem_x509_certificate(server_cert_bytes)
            # ... (Verify server certificate) 
            self.sockets[device.name] = sock

    def send_command_to_device(self, device_name, command):
        if device_name in self.sockets:
            try:
                # Encrypt message using RSA
                encrypted_message = self.encrypt_message(command, device_name)
                # Send encrypted message
                self.sockets[device_name].sendall(encrypted_message)
            except Exception as e:
                print(f"Error sending command to {device_name}: {e}")
        else:
            print(f"Device '{device_name}' not connected.")

    def encrypt_message(self, message, device_name):
        # Get the device's public key
        device_public_key = self.sockets[device_name].getpeercert() 
        # Encrypt the message using the device's public key
        public_key = serialization.load_pem_public_key(device_public_key.encode())
        encrypted_message = public_key.encrypt(
            message.encode(),
            padding=serialization.PKCS1v15()
        )
        return encrypted_message