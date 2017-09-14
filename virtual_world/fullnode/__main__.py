#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

BasePath = os.path.abspath(os.path.join(sys.argv[0], '../'))
sys.path.append(BasePath)

import logging
import time
import altcoinvw.vw
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'

if __name__ ==  '__main__':
    cfg = {
            'loggingLevel': logging.DEBUG,
            }

    logger = logging.getLogger('')
    logger.setLevel(cfg['loggingLevel'])

    #  app.run(debug=True, port=10021)
    vw = altcoinvw.vw.VirtualWorld(BasePath)
    vw.LogLevel = cfg['loggingLevel']
    vw.Init()

    node = vw.NewNode()
    node.LogLevel = cfg['loggingLevel']

    vw.StartNodes()
    time.sleep(3)
    vw.StopNodes()
