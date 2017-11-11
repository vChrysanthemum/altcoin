#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import threading
from altcoinvw import node

class VirtualWorld:
    def __init__(self, basepath):
        return
        basepath = basepath.strip()
        if basepath == '':
            basepath = os.getcwd()

        pwd = os.getcwd()
        self.DataBasePath = os.path.join(basepath, 'data')
        self.AltcoindPath = os.path.realpath(os.path.join(basepath, 'bin', 'altcoind'))
        print(self.AltcoindPath)

        self.LogName = 'VirtualWorld'
        self.LogFormat = logging.Formatter('%(pathname)s:%(lineno)d %(asctime)s%(levelname)-8s: %(message)s')
        self.LogFilePath = os.path.join(self.DataBasePath, 'altcoinvw.log')
        self.LogLevel = logging.ERROR
        self.LoggerHandler = None
        self.Logger = None

        self.NodeMutex = threading.Lock()
        self.NodesMaxID = 0
        self.Nodes = {}


    def Init(self):
        return
        if os.path.exists(self.DataBasePath) == False:
            os.makedirs(self.DataBasePath)

        if os.path.exists(self.AltcoindPath) == False:
            raise Exception('altcoind not exists')

        self.Logger = logging.getLogger(self.LogName)
        self.LoggerHandler = logging.FileHandler(self.LogFilePath, mode='a+')
        self.LoggerHandler.setLevel(self.LogLevel)
        self.LoggerHandler.setFormatter(self.LogFormat)
        self.Logger.addHandler(self.LoggerHandler)

        print(self.LogLevel, self.LogName)
        self.Logger.info('init success')


    def NewNode(self):
        with self.NodeMutex:
            self.NodesMaxID += 1
            result = node.Node(self, self.NodesMaxID)
            self.Nodes[result.ID] = result

        return result


    def StartNodes(self):
        for nodeID, node in self.Nodes.items():
            node.Init()
            node.Run()


    def StopNodes(self):
        for nodeID, node in self.Nodes.items():
            node.Kill()
        for nodeID, node in self.Nodes.items():
            node.Wait()
