#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import logging
import time
import imp
from flask import Flask

import altcoinvw.util
from manager import webindex
from manager import webnode

__all__ = []

BasePath = os.path.abspath(os.path.join(sys.argv[0], '../'))
Logger = logging.getLogger('')
ModuleReloadTime = {}
Nodes = {}
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

    WebAppAddUrlRule('/Index', lambda : webindex.CtrIndex())
    WebAppAddUrlRule('/RegisterNode', lambda : webnode.CtrRegisterNode())
    WebAppAddUrlRule('/ListNodes', lambda : webnode.CtrListNodes())
    WebAppAddUrlRule('/Refresh', CtrRefresh)
    WebApp.run(debug=False, host='0.0.0.0', port=80)


def WebAppAddUrlRule(name, func):
    WebApp.add_url_rule(name, name, view_func=func, methods=['GET', 'POST'])


def WebCheckModuleIfNeedReloadAndPrepareReload(modulename):
    return altcoinvw.util.WebCheckModuleIfNeedReloadAndPrepareReload(BasePath, 
            'manager',
            ModuleReloadTime,
            modulename)


def CtrRefresh():
    try:
        if WebCheckModuleIfNeedReloadAndPrepareReload('webindex') == True:
            imp.reload(webindex)
        if WebCheckModuleIfNeedReloadAndPrepareReload('webnode') == True:
            imp.reload(webnode)

    except Exception as e:
        Logger.fatal('{}'.format(e))
    return 'success'
