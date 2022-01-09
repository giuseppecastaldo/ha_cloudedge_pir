import json

import requests
from urllib.parse import urlencode

import time
import random

from .utils.cryptoutil import (
    make_digest,
    make_digest_hex,
    triple_des_encrypt,
)


class MeariSDK:
    def __init__(self, account, password, phone_code, country_code):
        self.account = account
        self.password = password
        self.country_code = country_code
        self.phone_code = phone_code
        self._cloud_data = None

        self._BASE_URL = "https://apis.cloudedge360.com/meari/app/login"

    def login(self):
        response = requests.post(
            self._BASE_URL, data=self.__data(), headers=self.__headers()
        )
        self._cloud_data = json.loads(response.text)
        return self._cloud_data

    def mqtt_credentials(self):
        mqtt_data = self._cloud_data["result"]["iot"]["mqtt"]

        client_id = "{client_id}|securemode=2,signmethod=hmacsha1|".format(
            client_id=mqtt_data["clientId"]
        )

        username = "{device_name}&{product_key}".format(
            device_name=mqtt_data["dn"], product_key=mqtt_data["pk"]
        )

        password = make_digest_hex(
            "clientId{client_id}deviceName{device_name}productKey{product_key}".format(
                client_id=mqtt_data["clientId"],
                device_name=mqtt_data["dn"],
                product_key=mqtt_data["pk"],
            ),
            mqtt_data["deviceSecret"],
        )

        mqtt_credentials = {
            "client_id": client_id,
            "username": username,
            "password": password,
            "host": mqtt_data["host"],
            "port": int(mqtt_data["port"]),
            "keepalive": mqtt_data["keepalive"],
            "topic": mqtt_data["subTopic"],
        }

        return mqtt_credentials

    def __current_milli_time(self):
        return round(time.time() * 1000)

    def __headers(self):
        time = str(self.__current_milli_time())
        nonce = random.randint(100000, 999999)
        key = "bc29be30292a4309877807e101afbd51"

        sign = "api=/ppstrongs//meari/app/login|X-Ca-Key={key}|X-Ca-Timestamp={timestamp}|X-Ca-Nonce={nonce}".format(
            key=key, timestamp=time, nonce=str(nonce)
        )

        headers = {
            "X-Ca-Key": key,
            "X-Ca-Nonce": str(nonce),
            "X-Ca-Sign": make_digest(sign, "35a69fd1-6527-4566-b190-921f9a651488"),
            "X-Ca-Timestamp": time,
            "content-type": "application/x-www-form-urlencoded",
        }

        return headers

    def __data(self):
        data = {
            "phoneType": "a",
            "sourceApp": 8,
            "appVer": "4.0.4",
            "iotType": 3,
            "lngType": "en",
            "userAccount": self.account,
            "password": triple_des_encrypt(self.password),
            "phoneCode": self.phone_code,
            "appVerCode": 404,
            "t": str(self.__current_milli_time()),
            "countryCode": self.country_code,
        }

        return urlencode(data)
