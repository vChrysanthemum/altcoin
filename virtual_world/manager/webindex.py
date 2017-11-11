#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request

import manager

def CtrIndex(env):
    return 'hello {ip}'.format(ip=request.remote_addr)
