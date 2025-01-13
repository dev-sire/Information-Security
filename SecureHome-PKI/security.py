from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_x509_certificate, Encoding

class SecurityManager:
    def __init__(self, ca_certificate_path):
        with open(ca_certificate_path, 'rb') as f:
            self.ca_certificate = load_pem_x509_certificate(f.read())
        self.access_control_rules = { 
            "TemperatureSensor": ["read"],
            "CleaningSensor": ["read", "control"],
            "LightSensor": ["read", "control"] 
        } 

    def authenticate_device(self, device_certificate):
        try:
            device_cert = load_pem_x509_certificate(device_certificate)
            device_cert.public_key().verify(
                # Assuming signature is provided separately
                device_cert.signature, 
                # Assuming device certificate data is used for verification
                device_cert.public_bytes(encoding=serialization.Encoding.PEM), 
                padding=serialization.Prehashed(hashes.SHA256()),
                algorithm=hashes.SHA256()
            )
            return True
        except Exception as e:
            print(f"Authentication failed: {e}")
            return False

    def authorize_access(self, device_name, resource):
        if device_name in self.access_control_rules:
            if resource in self.access_control_rules[device_name]:
                return True
        return False