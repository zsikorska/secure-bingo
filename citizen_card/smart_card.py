import PyKCS11
from PyKCS11 import PyKCS11Error
from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend as db
from cryptography.hazmat.primitives.asymmetric.padding import PKCS1v15
from cryptography.hazmat.primitives.hashes import SHA1, Hash

from logger.logger import Logger


class SmartCard:
    AUTH_SLOT = 0
    SIGN_SLOT = 1
    ADDRESS_SLOT = 2
    # OPENSC_PKCS_LIB = '/opt/homebrew/Cellar/opensc/0.22.0/lib/opensc-pkcs11.so'
    OPENSC_PKCS_LIB = '/usr/lib/x86_64-linux-gnu/pkcs11/opensc-pkcs11.so'

    def __init__(self, pin: str, logger: Logger):
        self.session = None
        self.pin = pin
        self.logger = logger

    def is_session(self):
        if self.session is None:
            self.logger.info("Smart card", "OUT OF SESSION")
            return False
        return True

    def load_session(self):
        if self.session is not None:
            return

        pkcs11 = PyKCS11.PyKCS11Lib()
        pkcs11.load(SmartCard.OPENSC_PKCS_LIB)
        session = None

        try:
            session = pkcs11.openSession(SmartCard.AUTH_SLOT)
        except PyKCS11Error:
            self.logger.info("Smart card", "CARD IS NOT IN READER")
            return False

        if session is not None and self.pin is not None:
            try:
                session.login(self.pin)
            except PyKCS11Error:
                self.logger.info("Smart card", "PIN EXCEPTION")
                return False

        self.session = session
        return True

    def logout(self):
        self.session.logout()
        self.session.closeSession()
        self.session = None

    def get_keys(self):
        if not self.is_session():
            return None
        return self._get_private_key(), self.get_certificate().public_key()

    def _get_private_key(self):
        if not self.is_session():
            return None
        private_key = self.session.findObjects([
            (PyKCS11.CKA_CLASS, PyKCS11.CKO_PRIVATE_KEY)
        ])[0]

        return private_key

    def get_certificate(self):
        if not self.is_session():
            return None
        cert_obj = self.session.findObjects([
            (PyKCS11.CKA_CLASS, PyKCS11.CKO_CERTIFICATE),
            (PyKCS11.CKA_LABEL, 'CITIZEN AUTHENTICATION CERTIFICATE')
        ])[0]

        cert_der_data = bytes(cert_obj.to_dict()['CKA_VALUE'])
        cert = x509.load_der_x509_certificate(cert_der_data, backend=db())

        return cert

    def sign_message(self, message: bytes):
        if not self.is_session():
            return None
        private_key = self._get_private_key()

        mechanism = PyKCS11.Mechanism(PyKCS11.CKM_SHA1_RSA_PKCS, None)
        signature = bytes(self.session.sign(private_key, message, mechanism))

        return signature

    @staticmethod
    def validate_signature(signature, message: bytes, public_key):
        md = Hash(SHA1(), backend=db())
        md.update(message)
        digest = md.finalize()
        try:
            return public_key.verify(
                signature,
                digest,
                PKCS1v15(),
                SHA1()
            ) is None
        except InvalidSignature:
            return False
