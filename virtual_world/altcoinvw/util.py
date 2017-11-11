#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import imp
import json
import os
import time
import base64
import requests

def WebCheckModuleIfNeedReloadAndPrepareReload(basePath, parentModule, moduleReloadTime, modulename):
    path = os.path.join(basePath, parentModule, '{}.py'.format(modulename))
    if (modulename in moduleReloadTime) == False or \
            os.stat(path).st_mtime > moduleReloadTime[modulename]:
        moduleReloadTime[modulename] = time.time()
        return True
    return False


def WebSerializeObject(obj):
    if obj == None:
        d = None
    elif type(obj) == dict:
        d = obj
    else:
        d = {}
        d.update(vars(obj))
    d = json.dumps(d).__str__()
    d = bytes(d, 'utf-8')
    d = base64.b64encode(d)
    d = str(d, 'utf-8')
    return d


def WebUnserializeObject(d, objType):
    d = bytes(d, 'utf-8')
    d = base64.b64decode(d)
    d = str(d, 'utf-8')
    d = json.loads(d)
    obj = objType()
    for key, value in d.items():
        setattr(obj, key, value)
    return obj


def WebApiOutput(errno, errmsg='', obj=None):
    return json.dumps({
        'errno' : errno,
        'obj' : obj,
        'errmsg' : errmsg,
        })


def RequestPost(url, data={}, headers={}):
    responseText = None
    response = requests.post(url, data=data, headers=headers, stream=True)
    responseText = response.text
    response.close()
    return responseText
