# import libraries
import hashlib
import random
import string
import json
import binascii
import numpy as np
import pandas as pd
import pylab as pl #pylab-sdk
import logging
import datetime
import collections

# following imports are required by PKI
import Crypto #pip install pycryptodome NO TIME BUG
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5


#Class del Client che genera la PKI privata e pubblica
class Client:
   def __init__(self):
      random = Crypto.Random.new().read
      self._private_key = RSA.generate(1024, random)
      self._public_key = self._private_key.publickey()
      self._signer = PKCS1_v1_5.new(self._private_key)

   @property
   def identity(self):
      return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')


# ##test che genera UTENTI E PKI
Cerberus = Client()
ciao=Client()
# print ("\ncerberus=\t"+Cerberus.identity)
# print("\nciao=\t"+ciao.identity)



#Class who create Transation file
class Transation:

    #metodo che salva pki public mittente e destinatario con ora della transazione
    def __init__(self, sender, recipient, value):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.time = datetime.datetime.now()

    #Metodo dizionario che crea utente Genesis
    def to_dict(self):
        if self.sender == "Genesis":
            identity = "Genesis"
        else:
            identity = self.sender.identity

            return collections.OrderedDict({'sender': identity,'recipient': self.recipient,'value': self.value,'time' : self.time})

    #dizionario chiave privata che firma la transazione
    def sign_transaction(self):
        private_key = self.sender._private_key
        signer = PKCS1_v1_5.new(private_key)
        h = SHA.new(str(self.to_dict()).encode('utf8'))
        return binascii.hexlify(signer.sign(h)).decode('ascii')




# #prova di transazione di 5 value
# t=Transation(Cerberus,ciao.identity,5.0)
# signature = t.sign_transaction()
# print(signature)
