#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

import fullnode
import altcoinvw.util
import altcoinvw.node

MetaNode = altcoinvw.node.TemplateInitNode()

def Start():
    MetaNode.Role = 'fullnode'
    postData = {}
    postData['Node'] = altcoinvw.util.WebSerializeObject(MetaNode)
             
    r = requests.post('http://manager/RegisterNode', data=postData)
    fullnode.Logger.fatal(r.text)
