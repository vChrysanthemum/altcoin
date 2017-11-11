#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import requests
import time

import fullnode
import altcoinvw.util
import altcoinvw.altcoinrpc
import altcoinvw.node

class Node(altcoinvw.node.Node):
    def __init__(self, basePath):
        altcoinvw.node.Node.__init__(self, basePath)
        self.MetaNode.Role = 'fullnode'
        self.Init()
        self.Thread = None


    def ensureAccountRice(self):
        result, err = self.AltcoinProxy.Call('listaccounts', [])
        if err != None:
            self.Logger.error(err)
        if (result[""] == 0):
            self.AltcoinProxy.Call('generate', [102])


    def loopJob(self):
        while True:
            time.sleep(2)
            self.ensureAccountRice()


    def StartInNewThread(self):
        self.Thread = threading.Thread(target=self.Run)
        self.Thread.start()
        self.Thread = threading.Thread(target=self.loopJob)
        self.Thread.start()
        self.RegisterInManager()
        return self.Thread


    def RegisterInManager(self):
        postData = {}
        postData['Node'] = altcoinvw.util.WebSerializeObject(self.MetaNode)
        try:
            response = requests.post('http://manager/RegisterNode', data=postData)
            self.Logger.fatal(response.text)
        except Exception as e:
            self.Logger.error(e)
