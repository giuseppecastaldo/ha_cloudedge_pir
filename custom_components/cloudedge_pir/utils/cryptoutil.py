import pyDes

import hashlib
import hmac
import base64

KEY = "123456781234567812345678"
IV = "01234567"


def triple_des_encrypt(text):
    des = pyDes.triple_des(key=KEY, mode=pyDes.CBC, padmode=pyDes.PAD_PKCS5, IV=IV)
    return base64.b64encode(des.encrypt(text)).decode()


def make_digest(message, key):
    key = bytes(key, "UTF-8")
    message = bytes(message, "UTF-8")

    digester = hmac.new(key, message, hashlib.sha1)
    signature1 = digester.digest()

    signature2 = base64.urlsafe_b64encode(signature1)
    return str(signature2, "UTF-8")


def make_digest_hex(message, key):
    key = bytes(key, "UTF-8")
    message = bytes(message, "UTF-8")

    digester = hmac.new(key, message, hashlib.sha1)
    return digester.digest().hex().upper()
