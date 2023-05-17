from logger.logger import Logger
from crypto.asymmetric.asymmetric_key_generator import AsymmetricKeyGenerator
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_public_key


string = "b'-----BEGIN PUBLIC KEY-----\\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA1ler6tGc9GM5cuclitMQ\\nkJxyBuHVHfUHs9Zef1vQ14hkC34ZM8IhtaiceTqOF+P+/PM4ZirtfR7hmXgz0h9c\\nfuRL9ueidRt5JA+UucKKdwP7UrVg3zKTYCFM3WxgfURi+X7LiSufTLG2UFkS7w9k\\n8FWb+Ub7qkqjsn9ZgXmdN6qeiiYo+lZgqzLBDFqNR2Ao8wJjLwK9hqGwRSS7Ily8\\n4vETY5xWjE8OSHoWXRJ1K0T4l/Lyq9Egl1ye0q0QvxA6phW3BnG4zCj87MrXQ4Bh\\no9d5/7OOx0FWpVMJrhNtLdMEXcd3Ki0Y9zAqjefzGZnqwDtA4hgPgynnMvFhfAd9\\nNQIDAQAB\\n-----END PUBLIC KEY-----\\n’"
string = string.replace("\\\\", "\\")
print(string) 



# asymmetric_key_generator    = AsymmetricKeyGenerator()
# logger                      = Logger()
# key_pair                    = asymmetric_key_generator.generate_key_pair()
# serialized_public_key       = key_pair['serialized_public_key']

# print(type(serialized_public_key))
# print(serialized_public_key)

# public_key = load_pem_public_key(serialized_public_key, backend=default_backend())

# print(type(public_key))
# print(public_key)