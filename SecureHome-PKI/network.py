import socket
import ssl
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

class WirelessNetwork:
    def __init__(self, server_address, server_certificate):
        self.server_address = server_address
        self.server_certificate = server_certificate
        self.context = ssl.create_default_context(cafile=server_certificate)
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_REQUIRED
        self.sockets = {}

    def connect_device(self, device):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        with self.context.wrap_socket(client_socket, server_hostname=self.server_address[0]) as sock:
            sock.connect(self.server_address)
            sock.sendall(device.certificate.public_bytes(encoding=serialization.Encoding.PEM))
            self.sockets[device.name] = sock

    def send_command_to_device(self, device_name, command):
        if device_name in self.sockets:
            try:
                encrypted_message = self.encrypt_message(command, device_name)
                self.sockets[device_name].sendall(encrypted_message)
            except Exception as e:
                print(f"Error sending command to {device_name}: {e}")
        else:
            print(f"Device '{device_name}' not connected.")

    def encrypt_message(self, message, device_name):
        cert = self.sockets[device_name].getpeercert()
        public_key = serialization.load_pem_public_key(cert['subjectKeyIdentifier'][0].encode())

        encrypted_message = public_key.encrypt(
            message.encode(),
            padding.PKCS1v15()
        )
        return encrypted_message