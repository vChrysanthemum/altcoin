#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

BasePath = os.path.abspath(os.path.join(sys.argv[0], '../'))
sys.path.append(BasePath)

import manager

if __name__ ==  '__main__':
    manager.Start()
