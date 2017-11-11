#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import signal
import logging
import socket
import subprocess

from altcoinvw import altcoin

class MetaNode:
    def __init__(self):
        self.ID = None
        self.Role = ''
        self.IP = ''


def TemplateInitNode():
    node = MetaNode()
    node.ID = socket.gethostname()
    return node


class Node:
    def __init__(self, basePath):
        basePath = os.path.realpath(basePath)
        self.MetaNode = TemplateInitNode()
        self.DataBasePath = os.path.join(basePath, 'data', self.MetaNode.ID)
        self.AltcoinDaemonBinPath = os.path.realpath(os.path.join(
            basePath, '..', 'src', 'altcoind'))
        self.AltcoinCliBinPath = os.path.realpath(os.path.join(
            basePath, '..', 'src', 'altcoin-cli'))
        self.AltcoinTemplateConfPath = os.path.join(
                basePath, 'conf', 'altcoin0.template.conf')
        self.AltcoinConfPath = os.path.join(
                self.DataBasePath, '{}.conf'.format(self.MetaNode.ID))

        self.LogName = self.MetaNode.ID
        self.LogLevel = logging.DEBUG
        self.LogFilePath = os.path.join(self.DataBasePath,
                '{}.log'.format(self.MetaNode.ID))
        self.LogFormat = logging.Formatter('%(levelname)-6s %(pathname)s:%(lineno)d %(asctime)s: %(message)s')
        self.Logger = logging.getLogger(self.LogName)

        self.ProcessStdOutFilePath = os.path.join(self.DataBasePath, 'stdout.log')
        self.ProcessStdErrFilePath = os.path.join(self.DataBasePath, 'stderr.log')
        self.ProcessArgs = '-conf={}'.format(self.AltcoinConfPath)
        self.Process = None


    def Init(self):
        if os.path.exists(self.DataBasePath) == False:
            os.makedirs(self.DataBasePath)

        cfg = altcoin.ReadConfigFile(self.AltcoinTemplateConfPath)
        cfg['datadir'] = self.DataBasePath
        cfg['rpcconnect'] = socket.gethostbyname(socket.gethostname())
        altcoin.WriteConfigFile(self.AltcoinConfPath, cfg)

        self.LoggerHandler = logging.FileHandler(self.LogFilePath, mode='a+',
                delay=False)
        self.LoggerHandler.setLevel(self.LogLevel)
        self.LoggerHandler.setFormatter(self.LogFormat)
        self.Logger.addHandler(self.LoggerHandler)

        self.AltcoinProxy = altcoin.AltcoinProxy(self.AltcoinConfPath)


        self.Logger.info('init success')
            

    def Run(self):
        fout = open(self.ProcessStdOutFilePath, 'a')
        ferr = open(self.ProcessStdErrFilePath, 'a')
        result = self.Process = subprocess.Popen([self.AltcoinDaemonBinPath, self.ProcessArgs],
                shell=False, stdout=fout, stderr=ferr)
        self.Logger.info(result)


    def Kill(self):
        try:
            self.Logger.info(os.kill(self.Process.pid, signal.SIGINT))
        except Exception as e:
            self.Logger.error(e)


    def Wait(self):
        try:
            self.Logger.info(self.Process.wait())
        except Exception as e:
            self.Logger.error(e)
