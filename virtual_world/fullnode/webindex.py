#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request

import fullnode

def CtrIndex(webServerEnv):
    return 'hello {ip}'.format(ip=request.remote_addr)
