#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

BasePath = os.path.abspath(os.path.join(sys.argv[0], '../../'))
sys.path.append(BasePath)

import unittest

import altcoinvw.util

class TestSerialize(unittest.TestCase):
    def testMain(self):
        class Test:
            def __init__(self):
                self.Data = 'test'
        
        t0 = Test()
        sdata = altcoinvw.util.WebSerializeObject(t0)
        self.assertEqual(type(sdata), str)
        t1 = altcoinvw.util.WebUnserializeObject(sdata, Test)
        self.assertEqual(t0.Data, t1.Data)

if __name__ == '__main__':
    unittest.main()
