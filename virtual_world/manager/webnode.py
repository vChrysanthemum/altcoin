#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
import json

import manager
import altcoinvw.util
import altcoinvw.node

def CtrRegisterNode():
    paramNode = request.form.get('Node', altcoinvw.util.WebSerializeObject({}))
    node = altcoinvw.util.WebUnserializeObject(paramNode, altcoinvw.node.MetaNode)
    if not node.ID:
        return altcoinvw.util.WebApiOutput(-1, 'node not valid')
    node.IP = request.remote_addr
    manager.Logger.fatal(node)

    manager.Nodes[node.ID] = node
    return altcoinvw.util.WebApiOutput(0)

def CtrListNodes():
    return json.dumps(manager.Nodes)
