#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import subprocess

class Node:
    def __init__(self, vw, nodeID):
        self.ID = nodeID
        self.VirtualWorld = vw
        self.DataBaseDir = os.path.join(vw.DataBaseDir,
                'node.{nodeid}'.format(nodeid=self.ID))

        self.LogName = 'Node.{nodeID}'.format(nodeID=nodeID)
        self.LogFormat = logging.Formatter('%(pathname)s:%(lineno)d '
                '%(asctime)s '
                '%(levelname)s: %(message)s')
        self.LogFilePath = os.path.join(self.DataBaseDir, 'node.log')
        self.LogLevel = logging.ERROR
        self.LoggerHandler = None
        self.Logger = None

        self.ProcessStdOutFilePath = os.path.join(self.DataBaseDir, 'stdout.log')
        self.ProcessStdErrFilePath = os.path.join(self.DataBaseDir, 'stderr.log')
        self.ProcessArgs = []
        self.Process = None


    def Init(self):
        if os.path.exists(self.DataBaseDir) == False:
            os.makedirs(self.DataBaseDir)
        self.Logger = logging.getLogger(self.LogName)
        self.LoggerHandler = logging.FileHandler(self.LogFilePath, mode='a+')
        self.LoggerHandler.setLevel(self.LogLevel)
        self.LoggerHandler.setFormatter(self.LogFormat)
        self.Logger.addHandler(self.LoggerHandler)

        self.Logger.info('init success')
            

    def Run(self):
        cmd = [self.VirtualWorld.AltcoindPath] + self.ProcessArgs
        print(cmd)
        fout = open(self.ProcessStdOutFilePath, 'a')
        ferr = open(self.ProcessStdErrFilePath, 'a')
        self.Process = subprocess.Popen(cmd, shell=False,
                stdout=fout, stderr=ferr)
        self.Logger.info(self.Process)


    def Kill(self):
        try:
            self.Logger.info(self.Process.kill())
        except Exception as e:
            self.Logger.error(e)


    def Wait(self):
        try:
            self.Logger.info(self.Process.wait())
        except Exception as e:
            self.Logger.error(e)
