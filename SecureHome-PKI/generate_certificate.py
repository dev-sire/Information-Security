from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.x509.extensions import SubjectAlternativeName, DNSName
from cryptography.hazmat.primitives import serialization
import datetime

def generate_self_signed_cert(common_name, dns_name=None):
    """Generates a self-signed certificate with optional DNS name."""

    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # Create subject name
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, "PK"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "Sindh"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, "Karachi"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Sirecorp"),
        x509.NameAttribute(NameOID.ORGANIZATIONAL_UNIT_NAME, "90"),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name)
    ])

    # Create issuer name (same as subject for self-signed cert)
    issuer = subject

    # Create validity period (e.g., 365 days)
    valid_from = datetime.datetime.utcnow()
    valid_to = valid_from + datetime.timedelta(days=365)

    # Create certificate builder
    builder = x509.CertificateBuilder()
    builder = builder.subject_name(subject)
    builder = builder.issuer_name(issuer)
    builder = builder.public_key(private_key.public_key())
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.not_valid_before(valid_from)
    builder = builder.not_valid_after(valid_to)

    if dns_name:
        san = SubjectAlternativeName([DNSName(dns_name)])
        builder = builder.add_extension(san, critical=False)

    certificate = builder.sign(private_key, hashes.SHA256(), default_backend())

    with open("server.crt", "wb") as f:
        f.write(certificate.public_bytes(encoding=serialization.Encoding.PEM))

    # Write private key to file (for server use)
    with open("server.key", "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

if __name__ == "__main__":
    common_name = "servername"  # Replace with your desired server name
    dns_name = "https://www.visage.com"  # Optional DNS name for the server (replace with your actual domain name if applicable)
    generate_self_signed_cert(common_name, dns_name)