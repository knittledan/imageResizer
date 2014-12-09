# -*- coding: utf-8 -*-
#----------------------------------------------------------------------------------------
# __init__.py initialization file for PIL
#----------------------------------------------------------------------------------------

import os
import sys
import platform

#----------------------------------------------------------------------------------------
# Defines
#----------------------------------------------------------------------------------------

kMac     = 0
kLinux   = 1
kWindows = 2

currentDir = os.path.dirname(os.path.realpath(__file__))

#----------------------------------------------------------------------------------------
# Methods
#----------------------------------------------------------------------------------------

def getOs():
    name = platform.system()
    if name == 'Darwin':
        return kMac
    if name == 'Linux':
        return kLinux
    if name == 'Windows':
        return kWindows

if getOs() == kMac:
    module = os.path.join(currentDir, 'mac')

if getOs() == kLinux:
    module = os.path.join(currentDir, 'linux')

if getOs() == kWindows:
    module = os.path.join(currentDir, 'windows')

#----------------------------------------------------------------------------------------
# Package handler
#----------------------------------------------------------------------------------------
# insert os specific PIL package path into sys.path
sys.path.insert(0, module)
# delete empty PIL package
del sys.modules[__name__]
# import os specific PIL package
import PIL
