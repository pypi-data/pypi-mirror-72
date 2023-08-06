#!/usr/bin/python3.8

import random
import time
import hmac
import base64
import hashlib

class TwoFactor:

    def __init__(self, digits : int=6, digest : any=hashlib.sha1):

        self.digits = digits
        self.digest = digest

    def getcodes(self, *secrets):

        codes = {}

        if isinstance(secrets, tuple) == True or isinstance(secrets, list) == True:

            for secret in secrets[0]:

                if not secret in codes.keys():
                    codes[secret] = self.getcode(secret)

            return codes

        else:
            raise Exception('Secrets is not a tuple or list.')

    def getcode(self, secret, input: int=int(time.time()), padding: int=8):

        if isinstance(secret, str) == False:
            raise Exception('Secret is not a string.')

        if isinstance(input, int) == False:
            raise Exception('Time is not a int.')

        input = input // 30

        if input < 0:
            raise ValueError('input must be positive integer')

        signature = bytearray(self.signature(secret, input))

        offset = signature[-1] & 0xf

        code = ((signature[offset]) << 24 | (signature[offset+1] & 0xff) << 16 | (signature[offset+2] & 0xff) << 8 | (signature[offset + 3] & 0xff))
        code = str(code % 10 ** self.digits)

        while len(code) < self.digits:
            code = '0' + code

        return code

    def signature(self, secret : str, input : int):

        return hmac.new(self.byte_secret(secret), self.int_to_bytestring(input), self.digest).digest()

    def getsecret(self, lenght: int=16, chars : str=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567')):

        if lenght < 16:
            raise Exception('Secrets should be at least 128 bits.')

        return ''.join(random.choice(chars) for p in range(lenght))

    def getsecrets(self, amount: int=1, lenght: int=16, chars : str=list('ABCDEFGHIJKLMNOPQRSTUVWXYZ234567')):

        if lenght < 16:
            raise Exception('Secrets should be at least 128 bits.')

        secrets = []
        amount = amount

        while amount != 0:

            secrets.append(self.getsecret(lenght, chars))
            amount = amount - 1

        return secrets

    def byte_secret(self, secret):

        padding = len(secret) % 8

        if padding != 0:
            secret += '=' * (8 - padding)

        return base64.b32decode(secret, casefold=True)

    def int_to_bytestring(self, input: int, padding: int=8):

        result = bytearray()

        while input != 0:

            result.append(input & 0xFF)
            input >>= padding

        return bytes(bytearray(reversed(result)).rjust(padding, b'\0'))

    def checkcode2fa(self, secret, code):

        if len(str(secret)) < 16:
            raise Exception('Secrets should be at least 128 bits.')

        return self.getcode(secret) == code
