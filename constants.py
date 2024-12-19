from Crypto.Cipher import AES

BD_ADDR = "2D4DE701-9160-935E-C351-707F30C5709C"
BD_NAME = "GLASSES-02FB6E"
AES_KEY = b'\x32\x67\x2f\x79\x74\xad\x43\x45\x1d\x9c\x6c\x89\x4a\x0e\x87\x64'
AES_MODE = AES.MODE_ECB
DEFAULT_ATTEMPTS = 3

cipher = AES.new(AES_KEY, AES_MODE)
def encrypt(value):
    return cipher.encrypt(value)

EXAMPLE_MSGS = [
    encrypt(b'\x06PLAY\x01\x00;\x97\xf2\xf3U\xa9r\x13\x8b'),
    encrypt(b'\x06PLAY\x01\x04;\x97\xf2\xf3U\xa9r\x13\x8b'),
    encrypt(b'\x06PLAY\x01\x03;\x97\xf2\xf3U\xa9r\x13\x8b')]
