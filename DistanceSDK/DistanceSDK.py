'''
Create and manage poses set via SDK on selected controls.
- A pose is represented as an attribute on a user designated control curve
'''

import maya.OpenMayaUI as apiUI
from PyQt4 import QtGui, QtCore, uic
import sip
import os
import pymel.core as pm
import pdb
from functools import partial

cwd = os.path.dirname(os.path.abspath(__file__))
uifile = cwd+'/qt/DistanceSDK_ui.ui'
form, base = uic.loadUiType(uifile)

def getMayaWindow():
    """
    Get the main Maya window as a QtGui.QMainWindow instance
    @return: QtGui.QMainWindow instance of the top level Maya windows
    """
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return sip.wrapinstance(long(ptr), QtCore.QObject)

'''
# Run the code in Maya
import sys
path = '/Users/3mo/Desktop/GC_Academy/MayaRiggingTools'
if path not in sys.path:
    sys.path.append(path)

from DistanceSDK import DistanceSDK
reload(DistanceSDK)
'''
class DistanceSDK(form, base):
    '''
    Tool for managing SDKed poses.
    '''
    def __init__(self, parent = getMayaWindow()):
        super(DistanceSDK,self).__init__(parent)
        self.setupUi(self)
        # Distance input
        self.baseLoadButton.clicked.connect( partial( self.loadCtrl, self.baseLineEdit ) )
        self.targetLoadButton.clicked.connect( partial( self.loadCtrl, self.targetLineEdit ) )
        self.parentLoadButton.clicked.connect( partial( self.loadCtrl, self.parentLineEdit ) )
        self.driverLoadButton.clicked.connect( partial( self.loadCtrl, self.driverLineEdit ) )
        self.driverSelectButton.clicked.connect(self.selectDriver)

        
    def loadCtrl(self,fld=None):
        sel = pm.ls(sl=True)[0]
        fld.setText(QtCore.QString(str(sel)))
        
    def loadDriver(self):
        sel = pm.ls(sl=True)[0]
        self.driverLineEdit.setText(QtCore.QString(str(sel)))
        attrs = pm.listAttr(sel, k=1, v=1, u=1)
        for each in attrs:
            
    
    def selectDriver(self):
        driver = str(QtCore.QString(self.driverLineEdit.text()))
        pm.select(driver,r=1)
        

def main():
    global win
    try:
        win.close()
    except:
        pass
    win = DistanceSDK()
    win.show()


if __name__=="DistanceSDK.DistanceSDK":
    main()
