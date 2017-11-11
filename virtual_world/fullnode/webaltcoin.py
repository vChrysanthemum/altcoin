#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json

from flask import Flask
from flask import request

from fullnode import *

def CtrAltcoinKill(env):
    env.Node.Kill()
    return '{}'.format(env.Node.Wait())


def CtrAltcoinRun(env):
    return '{}'.format(env.Node.Run())


def CtrAltcoinCall(env):
    method, args = None, None
    try:
        method = request.args.get('method', '')
        args = json.loads(request.args.get('args', ''))
    except Exception as e:
        pass

    result, err = env.Node.AltcoinProxy.Call(method, args)
    if err != None:
        return str(err)

    return json.dumps(result)
