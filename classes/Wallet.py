import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
import binascii



class Wallet:
    """
    A wallet is a private/public key pair
    """

    def __init__(self, data):
        random_gen = Crypto.Random.new().read
        self.private_key = RSA.generate(1024, random_gen)
        self.public_key = self.private_key.publickey()
        self.signer = PKCS1_v1_5.new(self.private_key)
        self.balance = 0


    @property
    def address(self):
        """We take a shortcut and say address is public key"""
        return binascii.hexlify(self.public_key.exportKey(format='DER')).decode('ascii')


    def sign(self, message):
        """
        Sign a message with this wallet
        """
        h = SHA.new(message.encode('utf8'))
        return binascii.hexlify(self.signer.sign(h)).decode('ascii')
