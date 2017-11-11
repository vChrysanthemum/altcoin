#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request

from fullnode import *

def CtrAltcoinKill(webServerEnv):
    webServerEnv.Node.VWNode.Kill()
    return '{}'.format(webServerEnv.Node.VWNode.Wait())

def CtrAltcoinRun(webServerEnv):
    return '{}'.format(webServerEnv.Node.VWNode.Run())
