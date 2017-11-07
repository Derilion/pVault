from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto import Random
from sys import getsizeof
import hashlib
import base64


class encryptior():
    """collects methods to encode strings, is a singleton"""

    class __encryptior:

        # AES key saved persistently
        aeskey = 0
        aeskeylength = 0

        def __init__(self):
            """embedded singleton constructor"""
            self.aeskeylength = 16
            print("created")

        def __str__(self):
            return repr(self)

    # describes the singletons instance
    __instance = None
    # AES blocksize to which it will be encoded
    __blocksize = 16

    def __init__(self):
        """singleton constructor"""
        if not encryptior.__instance:
            encryptior.__instance = encryptior.__encryptior()

    def setAES(self, key):
        """set 128bit AES key"""
        # # create random session key
        # key = get_random_bytes(self.__instance.aeskeylength)
        # self.__instance.aeskey = key
        print("setting key to: ", key)
        self.__instance.aeskey = key

    def setAESfromPW(self, string, salt=0):
        """creates an AES key from a password"""

        if salt == 0:
            # get salt
            salt = self._createSalt()

        # hash password and salt
        hashed = hashlib.sha3_256(salt + string.encode()).hexdigest()

        # take first 16 byte of hash as aes key
        hashed = self.unicode_truncate(hashed, 16)
        return hashed.encode("utf-8"), salt

    def _createSalt(self):
        """creates salt for the creation of safe hashed passwords"""
        salt = get_random_bytes(self.__instance.aeskeylength)
        return salt

    @staticmethod
    def unicode_truncate(string, length, encoding='utf-8'):
        encoded = string.encode(encoding)[:length]
        return encoded.decode(encoding, 'ignore')

    def encryptAES(self, string):
        """encrypts data in AES"""

        # pad data to AES blocksize
        string = self._pad(string)
        # calculate iv
        iv = Random.new().read(AES.block_size)
        # create AES object in CBC mode
        cipher = AES.new(self.__instance.aeskey, AES.MODE_CBC, iv)
        # WORKAROUND encode string in UTF-8 (unknown why it is neccessary)
        string = string.encode('utf-8')
        # encrypt string and encode it in base64 byte format
        ciphertext = base64.b64encode(iv + cipher.encrypt(string))
        return ciphertext

    def alternateencryptAES(self, serial):
        serial = serial + (self.__blocksize - len(serial) % self.__blocksize) * chr(self.__blocksize - len(serial) % self.__blocksize)
        print(serial)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.__instance.aeskey, AES.MODE_CBC, iv)
        ciphertext = base64.b64encode(iv + cipher.encrypt(serial))
        return ciphertext

    def decryptAES(self, enc):
        """decrypts AES encrypted data"""

        # encode bytes in base64
        enc = base64.b64decode(enc)
        # calculate iv from AES blocksize
        iv = enc[:AES.block_size]
        # create AES object in CBC mode
        cipher = AES.new(self.__instance.aeskey, AES.MODE_CBC, iv)
        # encrypt data
        cleartext = self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
        return cleartext

    def _pad(self, string):
        """resizes data to AES blocksize"""
        return string + (self.__blocksize - len(string) % self.__blocksize) * chr(self.__blocksize - len(string) % self.__blocksize)

    @staticmethod
    def _unpad(string):
        """removes padded data from AES blocksize"""
        return string[:-ord(string[len(string)-1:])]


