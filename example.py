
import requests
from future.builtins import bytes
from urllib.parse import urlparse
import hmac
import hashlib
import time
import json


class Rest():
    def __init__(self, apiKey, apiSecret, base_url):
        self.apiKey = apiKey
        self.apiSecret = apiSecret
        self.base_url = base_url
        self.s = requests.Session()

    def generate_signature(self, apisecret, verb, url, expires, data):
        parsedURL = urlparse(url)
        path = parsedURL.path
        if parsedURL.query:
            path = path + '?' + parsedURL.query
        if isinstance(data, (bytes, bytearray)):
            data = data.decode('utf8')
        message = verb + path + str(expires) + data

        signature = hmac.new(bytes(apisecret, 'utf-8'), bytes(message, 'utf-8'), digestmod=hashlib.sha256).hexdigest()
        return signature

    def get_header(self, url, postdict, methods):
        data = json.dumps(postdict)
        expires = int(round(time.time()) + 3)
        header = {'api-expires': str(expires),'api-key':self.apiKey,'api-signature':self.generate_signature(self.apiSecret, methods, url, expires, data)}
        return header

    def place_order(self, postdict):
        path = self.base_url + '/order'
        header = self.get_header("/api/v1/order", postdict, 'POST')
        re = self.s.post(path, json=postdict, headers=header)
        return re

    def amend_order(self, postdict):
        path = self.base_url + "/order"
        header = self.get_header("/api/v1/order", postdict, 'PUT')
        re = self.s.put(path, json=postdict, headers=header)
        return re.json()

    def cancel_order(self, postdict):
        path = self.base_url + "/order"
        header = self.get_header("/api/v1/order", postdict, 'DELETE')
        re = self.s.delete(path, json=postdict, headers=header)
        return re.json()

    def get_depth(self, postdict):
        path = self.base_url + "/orderBook/L2"
        header = self.get_header("/api/v1/orderBook/L2", postdict, 'GET')
        re = requests.get(path, json=postdict, headers=header)
        return re
        
    def set_leverage(self, postdict):
        path = self.base_url + "/position/leverage"
        header = self.get_header("/api/v1/position/leverage", postdict, 'POST')
        re = self.s.post(path, json=postdict, headers=header)
        return re


if __name__ == '__main__':
    apiKey = ''
    apiSecret = ''
    base_url = 'https://testnet.bitmex.com/api/v1'
    ex = Rest(apiKey, apiSecret, base_url)
    postdict_buy = {"symbol": "XBTUSDT", "orderQty": "1000", "price": "10000", "side": "Buy"}
    

    st = time.time()
    re1 = ex.place_order(postdict_buy).text
    print(time.time() - st)
    print(re1)
    
    




















