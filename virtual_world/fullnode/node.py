#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import threading
import time
import json

import fullnode
import altcoinvw.util
import altcoinvw.altcoin
import altcoinvw.node

class Node(altcoinvw.node.Node):
    def __init__(self, basePath):
        altcoinvw.node.Node.__init__(self, basePath)
        self.MetaNode.Role = 'fullnode'
        self.Init()
        self.Thread = None
        self.MemberNodes = {}


    def loopJob(self):
        while True:
            time.sleep(2)
            self.registerInManager()
            self.refreshMemberNodes()
            #  self.ensureAccountRich()


    def StartInNewThread(self):
        self.Thread = threading.Thread(target=self.Run)
        self.Thread.start()
        self.Thread = threading.Thread(target=self.loopJob)
        self.Thread.start()
        return self.Thread


    def registerInManager(self):
        postData = {}
        postData['Node'] = altcoinvw.util.WebSerializeObject(self.MetaNode)
        try:
            response = altcoinvw.util.RequestPost('http://manager/RegisterNode', data=postData)
            self.Logger.debug(response)
        except Exception as e:
            self.Logger.error(e)


    def refreshMemberNodes(self):
        try:
            response = altcoinvw.util.RequestPost('http://manager/ListNodes')
            memberNodes = json.loads(response)
            for memberNode in memberNodes:
                if memberNode['ID'] == self.MetaNode.ID:
                    continue
                if memberNode['ID'] in self.MemberNodes:
                    continue
                result, err = self.AltcoinProxy.Call('addnode',
                        ['{}:{}'.format(memberNode['IP'],
                            altcoinvw.ALTCOIN_PORT), "add"])
                if err != None:
                    self.Logger.error(str(err))
                    continue
                self.Logger.info(result)
                self.MemberNodes[memberNode['ID']] = memberNode
        except Exception as e:
            print(str(e))
            self.Logger.error(e)


    def ensureAccountRich(self):
        result, err = self.AltcoinProxy.Call('listaccounts', [])
        if err != None:
            self.Logger.error(err)
        if (result[""] == 0):
            self.AltcoinProxy.Call('generate', [102])
