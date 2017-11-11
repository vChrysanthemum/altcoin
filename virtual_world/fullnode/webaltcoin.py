#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from flask import Flask
from flask import request

from fullnode import *

def CtrAltcoinKill(webServerEnv):
    webServerEnv.Node.Kill()
    return '{}'.format(webServerEnv.Node.Wait())


def CtrAltcoinRun(webServerEnv):
    return '{}'.format(webServerEnv.Node.Run())


def CtrAltcoinCall(webServerEnv):
    method, args = None, None
    try:
        method = request.args.get('method', '')
        args = json.loads(request.args.get('args', ''))
    except Exception as e:
        pass

    result, err = webServerEnv.Node.AltcoinProxy.Call(method, args)
    if err != None:
        return str(err)

    return json.dumps(result)
