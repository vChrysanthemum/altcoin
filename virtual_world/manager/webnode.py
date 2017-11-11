#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import time

from flask import Flask
from flask import request

import altcoinvw.util
import altcoinvw.node

def CtrRegisterNode(env):
    paramNode = request.form.get('Node', altcoinvw.util.WebSerializeObject({}))
    node = altcoinvw.util.WebUnserializeObject(paramNode, altcoinvw.node.MetaNode)
    if not node.ID:
        return altcoinvw.util.WebApiOutput(-1, 'node not valid')
    node.IP = request.remote_addr

    if node.ID in env.Nodes:
        node = env.Nodes[node.ID]

    node.RegisterTime = time.time()
    env.Nodes[node.ID] = node

    env.Logger.info(node.ID)
    env.Logger.info(env.Nodes)
    return altcoinvw.util.WebApiOutput(0)


def CtrListNodes(env):
    ret = []
    for nodeID, node in env.Nodes.items():
        ret.append({
            'ID':   nodeID,
            'Role': node.Role,
            'IP':   node.IP,
            })
    return json.dumps(ret)
