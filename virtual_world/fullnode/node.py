#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import requests

import fullnode
import altcoinvw.util
import altcoinvw.node

class Node:
    def __init__(self, basePath):
        self.VWNode = altcoinvw.node.Node(basePath)
        self.VWNode.MetaNode.Role = 'fullnode'
        self.VWNode.Init()
        self.Thread = None


    def doStartInNewThread(self):
        self.RegisterInManager()
        self.VWNode.Run()


    def StartInNewThread(self):
        self.Thread = threading.Thread(target=self.doStartInNewThread)
        self.Thread.start()
        return self.Thread


    def RegisterInManager(self):
        postData = {}
        postData['Node'] = altcoinvw.util.WebSerializeObject(self.VWNode.MetaNode)
         
        try:
            r = requests.post('http://manager/RegisterNode', data=postData)
            self.VWNode.Logger.fatal(r.text)
        except Exception as e:
            self.VWNode.Logger.error(e)
