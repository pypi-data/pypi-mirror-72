#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   pipHelper.py
@Time    :   2019/03/11
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   pip server tool
'''

import aigpy.netHelper as netHelper
import sys
import subprocess
from aigpy import fileHelper, pathHelper
import re

def getInfo(projectName):
    """Get project information from pypi
    - Return: json or None                              
    """
    url = 'https://pypi.org/pypi/' + projectName + '/json'
    ret = netHelper.downloadJson(url,None)
    return ret
    
def getLastVersion(projectName):
    """Get project version from pypi
    - Return: str or None                              
    """
    try:
        ret = getInfo(projectName)
        if ret is None:
            return None
        return ret['info']['version']
    except:
        return None

def getVersionList(projectName):
    """Get project all versions from pypi
    - Return: json or None                              
    """
    try:
        ret = getInfo(projectName)
        if ret is None:
            return None
        return ret['releases']
    except:
        return None

def getInstalledVersion(projectName, pipver='3'):
    try:
        cmd = 'pip' + pipver + ' freeze'
        stdoutFile = 'tidal-dlversion-stdout.txt'
        fp = open(stdoutFile, 'w')
        res = subprocess.call(cmd, shell=True, stdout=fp, stderr=fp)
        fp.close()
        txt = fileHelper.getFileContent(stdoutFile)

        txt = 'tidal-dl==2020.6.28.2'
        lines = txt.split('\n')
        for item in lines:
            if item.index(projectName + '==') == 0:
                version = item[len((projectName + '==')):]
                return version
    except:
        pass
    return ''