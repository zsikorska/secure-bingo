import datetime

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.x509.oid import NameOID

from crypto.asymmetric.signature_manager import SignatureManager
from logger.logger import Logger


class SmartCard:

    def __init__(self, pin: str, keys, signature_manager: SignatureManager, logger: Logger):
        self.session = None
        self.logger = logger
        self._private_key = keys['private_key']
        self._public_key = keys['public_key']
        self.signature_manager = signature_manager
        self.pin = pin

    def is_session(self):
        if self.session is None:
            self.logger.error("Smart card", "OUT OF SESSION")
            return False
        return True

    def load_session(self):
        if self.session is not None:
            return

        self.session = True

        return True

    def logout(self):
        self.session = None

    def get_keys(self):
        if not self.is_session():
            return None
        return self._get_private_key(), self.get_certificate().public_key()

    def _get_private_key(self):
        if not self.is_session():
            return None
        return self._private_key

    def get_certificate(self):
        if not self.is_session():
            return None

        one_day = datetime.timedelta(1, 0, 0)
        builder = x509.CertificateBuilder()
        builder = builder.subject_name(x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u'cryptography.io'),
        ]))
        builder = builder.issuer_name(x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, u'cryptography.io'),
        ]))
        builder = builder.not_valid_before(datetime.datetime.today() - one_day)
        builder = builder.not_valid_after(datetime.datetime.today() + (one_day * 30))
        builder = builder.serial_number(x509.random_serial_number())
        builder = builder.public_key(self._public_key)
        builder = builder.add_extension(
            x509.SubjectAlternativeName(
                [x509.DNSName(u'cryptography.io')]
            ),
            critical=False
        )
        builder = builder.add_extension(
            x509.BasicConstraints(ca=False, path_length=None), critical=True,
        )
        certificate = builder.sign(
            private_key=self._private_key, algorithm=hashes.SHA256(),
        )

        return certificate

    def get_certificate_serialized(self):
        return self.get_certificate().public_bytes(encoding=serialization.Encoding.DER)

    def sign_message(self, message: bytes):
        if not self.is_session():
            return None
        private_key = self._private_key

        return self.signature_manager.create_signature(message, private_key)

    @staticmethod
    def verify_signature(signature, message, public_key):
        try:
            public_key.verify(signature, message,
                              padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                              hashes.SHA256())
            return True
        except Exception:
            return False

    @staticmethod
    def deserialize_certificate(certificate):
        return x509.load_der_x509_certificate(certificate)
