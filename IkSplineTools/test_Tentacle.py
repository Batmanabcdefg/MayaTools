import unittest
import sys
import os

import maya.cmds as cmds
import maya.mel as mel

import maya.standalone as standalone
standalone.initialize(name='python')

class test_Tentacle(unittest.TestCase):
    def setUp(self):
        cmds.file(newFile=True,f=True)
        
        # Draw curve
        self._drawCurve()
        
        # DrawJoints
        