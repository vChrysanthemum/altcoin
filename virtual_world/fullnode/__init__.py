#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
from flask import Flask

import altcoinvw.util
from fullnode import webindex
from fullnode import node

__all__ = []

BasePath = os.path.abspath(os.path.join(sys.argv[0], '../'))
Logger = logging.getLogger('')
WebApp = Flask(__name__)

def Start():
    cfg = {
            'loggingLevel': logging.DEBUG,
            }
    #  loggerHandler = logging.FileHandler(self.LogFilePath, mode='a+')
    loggerHandler = logging.StreamHandler()
    loggerHandler.setLevel(cfg['loggingLevel'])
    loggerHandler.setFormatter(logging.Formatter('%(pathname)s:%(lineno)d %(asctime)s '
        '%(levelname)-8s: %(message)s'))
    Logger.addHandler(loggerHandler)

    node.Start()
    return

    WebAppAddUrlRule('/Index', lambda : webindex.CtrIndex())
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
