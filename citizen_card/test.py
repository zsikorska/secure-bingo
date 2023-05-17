from fake_smart_card import SmartCard
from logger.logger import Logger
# from smart_card import SmartCard
from cryptography.hazmat.primitives.hashes import SHA1, Hash, SHA256
from cryptography.hazmat.backends import default_backend as db

smartcard = SmartCard(Logger())

smartcard.load_session('1111')

# print(smartcard.get_certificate())


priv, pub = smartcard.get_keys()
print(priv)
print(pub)
text = b"Anna ma koteczka"

# textb =

s = smartcard.sign_message(text)
p = smartcard.get_certificate().public_key()
#
# message_to_bytes = bytes(text, 'ascii')
# md = Hash(SHA1(), backend=db(), )
# md.update(message_to_bytes)
# digest = md.finalize()

print(smartcard.verify_signature(s, text, p))
# print(SmartCard.validate_signature(s, digest, p))

# keys = smartcard.get_keys()
#
# print(keys[0])
# print(keys[1])

# print(smartcard.get_certificate())

print("###################")
print(type(smartcard.get_certificate().public_key()))
print("+++++++++++++++++++")


