#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import uuid
import subprocess

class MetaNode:
    def __init__(self):
        self.ID = None
        self.Role = ''
        self.IP = ''


def TemplateInitNode():
    node = MetaNode()
    node.ID = uuid.uuid1().__str__()
    return node


class Node:
    def __init__(self, basePath):
        self.AltcoinBinPath = altcoindBinPath
        self.BasePath = basePath
        self.Logger = None

        self.ProcessStdOutFilePath = os.path.join(self.DataBaseDir, 'stdout.log')
        self.ProcessStdErrFilePath = os.path.join(self.DataBaseDir, 'stderr.log')
        self.ProcessArgs = []
        self.Process = None


    def Init(self):
        if os.path.exists(self.DataBaseDir) == False:
            os.makedirs(self.DataBaseDir)

        self.Logger.info('init success')
            

    def Run(self):
        cmd = os.path.join([self.AltcoinBinPath], "altcoind") + self.ProcessArgs
        print(cmd)
        fout = open(self.ProcessStdOutFilePath, 'a')
        ferr = open(self.ProcessStdErrFilePath, 'a')
        self.Process = subprocess.Popen(cmd, shell=False,
                stdout=fout, stderr=ferr)
        self.Logger.info(self.Process)


    def Kill(self):
        try:
            self.Logger.info(self.Process.kill())
        except Exception as e:
            self.Logger.error(e)


    def Wait(self):
        try:
            self.Logger.info(self.Process.wait())
        except Exception as e:
            self.Logger.error(e)
