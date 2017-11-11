#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import base64
import json
import decimal

#  USER_AGENT = "AuthServiceProxy/0.1"
USER_AGENT = "AltcoinProxy/0.1"
HTTP_TIMEOUT = 30

def ReadConfigFile(filename):
    cfg = {}
    f = open(filename)
    try:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('#'):
                continue
            off = line.find('=')
            if off <= 0:
                continue
            key = line[0:off].strip(' ')
            value = line[off+1:].strip(' ')
            cfg[key] = value
    finally:
        f.close()
    return cfg


class JSONRPCException(Exception):
    def __init__(self, rpcError):
        Exception.__init__(self)
        self.error = rpcError

    def __str__(self):
        if (isinstance(self.error, dict)):
            return json.dumps(self.error)
        return str(self.error)


class AltcoinProxy:
    def __init__(self, configFilePath):
        self.Config = ReadConfigFile(configFilePath)
        self.__idcnt = 0

        authpair = '%s:%s' % (self.Config['rpcuser'], self.Config['rpcpassword'])
        authpair = authpair.encode('utf8')
        self.AuthHdr = 'Basic '.encode('utf8') + base64.b64encode(authpair)

        self.Hostname = self.Config['rpcconnect']
        self.Port = self.Config['rpcport']
        self.UrlBase = 'http://{}:{}'.format(
                self.Hostname, self.Port)
    

    def Call(self, method, args=[]):
        requestUrl = 'http://{}:{}'.format(self.Hostname, self.Port)
        headers = {'Host' : self.Hostname,
                'User-Agent' : USER_AGENT,
                'Authorization' : self.AuthHdr,
                'Content-type' : 'application/json'}
        postData = json.dumps({
               'version': '1.1',
               'method': method,
               'params': args,
               'id': self.__idcnt})

        response = requests.post(requestUrl, data=postData, headers=headers)
        if response is None:
            return None, JSONRPCException({
                'code' : -342, 'message' : 'missing HTTP response from server'})

        #  return json.loads(response.text, parse_float=decimal.Decimal)
        response = json.loads(response.text)
        if 'error' in response and response['error'] != None:
            return None, JSONRPCException(response['error'])
        elif 'result' not in response:
            return None, JSONRPCException({
                    'code' : -343, 'message' : 'missing JSON-RPC result'})
        return response['result'], None
