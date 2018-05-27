'''
Create and manage poses set via SDK on selected controls.
- A pose is represented as an attribute on a user designated control curve
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

import CreatePose
reload( CreatePose )
import PoseWidget
reload( PoseWidget )

def getMayaWindow():
    """
    Get the main Maya window as a QtGui.QMainWindow instance
    @return: QtGui.QMainWindow instance of the top level Maya windows
    """
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return wrapInstance(long(ptr), QtGui.QWidget)

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
uifile = cwd+'/qt/SDKPoseManager_ui.ui'
form, base = loadUiType(uifile)

'''
# Run the code in Maya
import sys
path = '/Users/3mo/Desktop/GC_Academy/MayaRiggingTools'
if path not in sys.path:
    sys.path.append(path)

from SDKPoseManager import SDKPoseManager
reload(SDKPoseManager)
'''
class SDKPoseManager(form, base):
    '''
    Tool for managing SDKed poses.
    '''
    def __init__(self, parent = getMayaWindow()):
        super(SDKPoseManager,self).__init__(parent)
        self.setupUi(self)
        self.controls = []
        self.controlNameFlds = []
        self.poses = []

        self.createPoseBtn.clicked.connect(CreatePose.main)
        self.controlsSlider.sliderReleased.connect( self.ui_controlFields )

        self.zeroBtn.clicked.connect(self._zero)
        self.selBtn.clicked.connect(self._sel)
        self.keyBtn.clicked.connect(self._key)
        self.muteBtn.clicked.connect(self._mute)
        self.clearBtn.clicked.connect(self._clear)
        self.mirrorPoseBtn.clicked.connect(self.mirrorPose)
        self.refreshBtn.clicked.connect(self.refresh)

        selected = pm.ls(sl=True)#,type='transform')
        self.ui_controlFields( selected = selected )
        if len(selected):
            self.refresh()

    def ui_controlFields( self, selected=None ):
        if selected:
            num = len( selected )
            self.controlsSlider.setValue( num )
            self.controlsNum.display( str(num) )
        else:
            num = int( self.controlsNum.value() )

        self.controlNameFlds = []
        self.poses = []

        self.ui_clearLayout( self.controlsVLayout )
        self.ui_clearLayout( self.poseVLayout )

        for i in range(num):
            grp = QtGui.QGroupBox()
            self.controlsVLayout.addWidget( grp )
            hLayout = QtGui.QHBoxLayout( grp )
            hLayout.addWidget(QtGui.QLabel( text='Control %s'%str(i+1)) )
            controlNameFld = QtGui.QLineEdit()
            if selected:
                controlNameFld.setText(str(selected[i]))
            hLayout.addWidget( controlNameFld )
            self.controlNameFlds.append( controlNameFld )
            btn = QtGui.QPushButton( text='<<<Load' )
            hLayout.addWidget( btn )
            btn.clicked.connect( partial( self.loadCtrl, controlNameFld ) )


    def ui_clearLayout(self,layout=None):
        for cnt in reversed(range(layout.count())):
            # removes an item and returns it
            widget = layout.takeAt(cnt).widget()

            if widget is not None:
                # widget will be None if the item is a layout
                widget.deleteLater()

    def loadCtrl(self,fld=None):
        sel = pm.ls(sl=True)[0]
        fld.setText(str(sel))

    def refresh(self):
        self.poses = []
        self.ui_clearLayout(self.poseVLayout)
        for each in self.controlNameFlds:
            if each:
                self.drawPoses(ctrl=str(each.text()))

    def mirrorPose(self):
        lf='lf_'
        rt='rt_'
        center = 'ctr_'
        sel = pm.ls(sl=1)
        pm.select(clear=True)
        commands = []
        for s in sel:

            mirrorObject = ""
            if str(s).startswith(lf):
                mirrorObject = rt + s[3:]
            elif str(s).startswith(rt):
                mirrorObject = lf + s[3:]
            elif str(s).startswith(center):
                mirrorObject = center + s[4:]

            pos = pm.xform(s, q=1, ws=1, rp=1)
            rot = pm.xform(s, q=1, ws=1, ro=1)
            scale = pm.xform(s, q=1, r=1, s=1)

            commands.append( 'move %s %s %s  -ws -rpr "%s"'%(-pos[0],pos[1],pos[2],mirrorObject) )
            commands.append( 'rotate -a %s %s %s -ws "%s" '%(rot[0],-rot[1],-rot[2],mirrorObject) )
            commands.append( 'scale %s %s %s "%s"'%(scale[0],scale[1],scale[2],mirrorObject) )

            pm.select(mirrorObject,add=True)

        for c in commands:
            pm.mel.eval(c)

    def getControlAttrs(self,ctrl=None):
        if pm.objectType(ctrl) == 'transform':
            return pm.listAttr(ctrl,unlocked=True,k=True)
        else:
            attrs = pm.listAttr(ctrl,connectable=True)
            for attr in attrs:
                if attr == 'distance':
                    return ['distance']
            return None

    def drawPoses(self,ctrl=None):
        """ Create individual control fields """
        attrs = self.getControlAttrs(ctrl=ctrl)
        self.poseVLayout.addWidget(QtGui.QLabel(str(ctrl)))
        for attr in attrs:
            if attr:
                try:
                    if attr == 'distance':
                        minV,maxV = -20, 20
                        pose = PoseWidget.PoseWidget( self.poseScrollArea, sliderEnabled=False )
                        pose.setup(ctrl,attr,minV,maxV)
                    else:
                        minV,maxV = pm.attributeQuery( attr, node=ctrl, range=True )
                        pose = PoseWidget.PoseWidget( self.poseScrollArea )
                        pose.setup(ctrl,attr,minV,maxV)
                except Exception,e:
                    pose = PoseWidget.PoseWidget( self.poseScrollArea, sliderEnabled=False )
                    pose.setup(ctrl,attr,-1000,1000)

                self.poseVLayout.addWidget( pose )
                self.poses.append(pose)



        line = QtGui.QFrame()
        line.setObjectName("line")
        line.setGeometry(QtCore.QRect(300, 0, 0, 3))
        line.setFrameShape(QtGui.QFrame.HLine)
        line.setFrameShadow(QtGui.QFrame.Sunken)
        self.poseVLayout.addWidget(line)

    def _zero(self):
        if len(self.poses):
            for p in self.poses:
                if p.poseCheckBox.isChecked():
                    p._zero()

    def _sel(self):
        if len(self.poses):
            if self.selBtn.text() == 'Select -All- / None':
                state = False
                text = 'Select All / -None-'
            else:
                state = True
                text = 'Select -All- / None'

            for p in self.poses:
                p.poseCheckBox.setCheckState(state)
                self.selBtn.setText(text)

    def _key(self):
        if len(self.poses):
            for p in self.poses:
                if p.poseCheckBox.isChecked():
                    p._key()

    def _mute(self):
        if len(self.poses):
            state = None
            if self.muteBtn.text() == 'Mute Selected: -On- / Off':
                state = False
            else:
                state = True
            for p in self.poses:
                if p.poseCheckBox.isChecked():
                    if state:
                        self.muteBtn.setText('Mute Selected: -On- / Off')
                        p.muteBtn.setText('Mute: Off')
                        p._mute()
                    else:
                        self.muteBtn.setText('Mute Selected: On / -Off-')
                        p.muteBtn.setText('Mute: On')
                        p._mute()

    def _clear(self):
        if len(self.poses):
            for p in self.poses:
                if p.poseCheckBox.isChecked():
                    p._clear()

def main():
    global win
    try:
        win.close()
    except:
        pass
    win = SDKPoseManager()
    win.show()


if __name__=="SDKPoseManager.SDKPoseManager":
    main()