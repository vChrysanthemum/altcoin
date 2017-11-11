#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
from flask import Flask

import altcoinvw.util
from fullnode.node import *
from fullnode.webindex import *
from fullnode.webaltcoin import *

__all__ = []

BasePath = os.path.abspath(os.path.join(sys.argv[0], '../'))
Logger = logging.getLogger('')
WebApp = Flask(__name__)

class WebServerEnv:
    def __init__(self):
        self.Node = None


def Start():
    env = WebServerEnv()
    env.Node = Node(BasePath)
    env.Node.StartInNewThread()

    WebAppAddUrlRule('/Index', lambda : CtrIndex(env))
    WebAppAddUrlRule('/Altcoin/Kill', lambda : CtrAltcoinKill(env))
    WebAppAddUrlRule('/Altcoin/Run', lambda : CtrAltcoinRun(env))
    WebApp.run(debug=False, host='0.0.0.0', port=80)


def WebAppAddUrlRule(name, func):
    WebApp.add_url_rule(name, name, view_func=func, methods=['GET', 'POST'])


def CtrRefresh():
    try:
        if altcoinvw.util.WebCheckModuleIfNeedReloadAndPrepareReload('webindex') == True:
            imp.reload(webindex)
    except Exception as e:
        Logger.fatal('{}'.format(e))
    return 'success'
