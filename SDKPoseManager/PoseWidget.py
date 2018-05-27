'''
PoseWidget used by SDKPoseManager
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
uifile = cwd+'/qt/PoseWidget_ui.ui'
form, base = loadUiType(uifile)

class PoseWidget(form, base):
    '''
    Display pose slider and buttons.
    '''
    def __init__(self, parent = None, **kwargs):
        self.parent = parent
        super(PoseWidget,self).__init__(parent)
        if kwargs.has_key('sliderEnabled'):
            self.sliderEnabled = kwargs['sliderEnabled']
        else:
            self.sliderEnabled =  True
        self.setupUi(self)
        self.minV = 0
        self.maxV = 100
        self.zeroBtn.clicked.connect(self._zero)
        self.keyBtn.clicked.connect(self._key)
        self.muteBtn.clicked.connect(self._mute)
        self.clearBtn.clicked.connect(self._clear)

        self.zeroPoseBtn.clicked.connect(self._setZeroKey)

    def setup(self,obj,attr,minV,maxV):
        ''' Connect UI to scene objects '''
        self.obj = obj
        self.attr = attr
        self.minV = minV
        self.maxV = maxV
        if self.minV == 0:
            self.poseABtn.setEnabled(False)
        self.poseCheckBox.setText(attr)

        self.horizontalSlider.setRange(minV*1000,maxV*1000)
        self.horizontalSlider.valueChanged.connect(self._handleSlider)
        self.horizontalSlider.setValue(pm.getAttr('%s.%s'%(obj,attr))*1000)

        self.horizontalSlider.setEnabled(self.sliderEnabled)

        self.poseABtn.clicked.connect(partial(self._setPose,self.minV))
        self.poseBBtn.clicked.connect(partial(self._setPose,self.maxV))

    def _setZeroKey(self):
        if not self.sliderEnabled:
            return None

        poseName = self.attr
        sel = pm.ls(sl=True)
        for s in sel:
            for attr in ['tx','ty','tz','rx','ry','rz','sx','sy','sz']:
                try:
                    if 's' in attr:
                        self.horizontalSlider.setValue(1)
                        pm.mel.eval('setDrivenKeyframe -currentDriver %s.%s %s.%s;'%(self.obj,self.attr,s,attr))
                    else:
                        self.horizontalSlider.setValue(0)
                        pm.mel.eval('setDrivenKeyframe -currentDriver %s.%s %s.%s;'%(self.obj,self.attr,s,attr))

                except Exception,e:
                    raise Exception(e)

    def _setPose(self,value=None):
        sel = pm.ls(sl=True)
        for s in sel:
            for attr in ['tx','ty','tz','rx','ry','rz','sx','sy','sz']:
                try:
                    self.horizontalSlider.setValue(value*1000)
                    pm.mel.eval('setDrivenKeyframe -currentDriver %s.%s %s.%s;'%(self.obj,self.attr,s,attr))
                except Exception,e:
                    raise Exception(e)


    def _mute(self):
        if not self.sliderEnabled:
            return None

        state = self.muteBtn.text()
        if state == 'Mute: Off':
            # Mute if unmuted
            pm.mel.eval('mute %s.%s'%(self.obj,self.attr))
            self.muteBtn.setText('Mute: On')
        else:
            # Unmute if muted
            pm.mel.eval('mute -disable -force %s.%s'%(self.obj,self.attr))
            self.muteBtn.setText('Mute: Off')

    def _key(self):
        if not self.sliderEnabled:
            return None

        pm.setKeyframe('%s.%s'%(self.obj,self.attr))

    def _clear(self):
        if not self.sliderEnabled:
            return None

        pm.mel.eval('CBdeleteConnection "%s.%s";'%(self.obj,self.attr))

    def _handleSlider(self, val):
        self.attrLcd.display(float(val/1000.0))
        if not self.sliderEnabled:
            return None

        pm.setAttr('%s.%s'%(self.obj,self.attr),float(val/1000.0))

    def _zero(self):
        if not self.sliderEnabled:
            return None

        self.horizontalSlider.setValue(0)