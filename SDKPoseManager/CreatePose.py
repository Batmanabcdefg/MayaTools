'''
Create a pose.
Pose: SDK'd transform nodes driven by Control.attr
'''

import maya.OpenMayaUI as apiUI
from PySide import QtGui, QtCore
from shiboken import wrapInstance
import pysideuic
import xml.etree.ElementTree as xml
from cStringIO import StringIO
import os
import pymel.core as pm
import pdb

from functools import partial

def loadUiType(uiFile):
    'load a .ui file in memory'
    parsed = xml.parse(uiFile)
    widget_class = parsed.find('widget').get('class')
    form_class = parsed.find('class').text

    with open(uiFile, 'r') as f:
        o = StringIO()
        frame = {}

        pysideuic.compileUi(f, o, indent=0)
        pyc = compile(o.getvalue(), '<string>', 'exec')
        exec pyc in frame

        # Fetch the base_class and form class based on their type
        # in the xml from designer
        form_class = frame['Ui_%s'%form_class]
        base_class = eval('QtGui.%s'%widget_class)

    return form_class, base_class

cwd = os.path.dirname(os.path.abspath(__file__))
uifile = cwd+'/qt/CreatePose_ui.ui'
form, base = loadUiType(uifile)

class CreatePose(form, base):
    '''
    Add attribute to selected. Can set min and max values.
    '''
    def __init__(self, parent = None):
        self.parent = parent
        super(CreatePose,self).__init__(parent)
        self.setupUi(self)

        self.loadDriverBtn.clicked.connect(partial(self.loadCtrl,
                                                   self.driverNameLineEdit))
        self.createPoseBtn.clicked.connect(self.createPose)

    def createPose(self):
        driver = str(self.driverNameLineEdit.text())
        poseName = str(self.poseNameLineEdit.text())
        minV = float(self.minValueLineEdit.text())
        maxV = float(self.maxValueLineEdit.text())

        try:
            for each in pm.ls(sl=1):
                pm.addAttr(each,longName=poseName,minValue=minV,maxValue=maxV,k=True)
        except Exception,e:
            raise Exception(e)

    def loadCtrl(self,fld=None):
        sel = pm.ls(sl=True)
        fld.setText(str(sel))

def main():
    global win
    try:
        win.close()
    except:
        pass
    win = CreatePose()
    win.show()