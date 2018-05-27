from functools import partial
import os
from PyQt4 import QtGui, QtCore, uic
import maya.OpenMayaUI as apiUI
import sip
import shutil
import sys
import pymel.core as pm
import logging

#--- Logging
from pymel.tools import loggingControl
loggingControl.initMenu()
from pymel.internal.plogging import pymelLogger
pymelLogger.setLevel(logging.DEBUG)

#--- Add cwd
cwd = os.path.dirname(os.path.abspath(__file__))
if cwd not in sys.path:
    sys.path.append(cwd)

import WerewolfRig
reload( WerewolfRig )
import CurveUtils
reload( CurveUtils )
dir(CurveUtils)

path = __file__.replace('RigBuilder.py','')[:-1]
form, base = uic.loadUiType(path+'/RigBuilder_ui.ui')

#--------------------------------------------------------------
def getMayaWindow():
    """
    Get the main Maya window as a QtGui.QMainWindow instance
    @return: QtGui.QMainWindow instance of the top level Maya windows
    """
    ptr = apiUI.MQtUtil.mainWindow()
    if ptr is not None:
        return sip.wrapinstance(long(ptr), QtCore.QObject)
#--------------------------------------------------------------

#--------------------------------------------------------------
class RigBuilder(form, base):
    ''' Maya UI to build Rigs '''
    def __init__(self, parent = getMayaWindow()):
        super(RigBuilder, self).__init__(parent)
        pymelLogger.debug('Starting: RigBuilder.__init__()...') 
            
        # Setup here
        self.setupUi(self)
        self.buildHeadRigBtn.clicked.connect(WerewolfRig.build_head)
        self.buildBodyRigBtn.clicked.connect(WerewolfRig.build_body)
        self.importHeadRigBtn.clicked.connect(WerewolfRig.import_head_rig)
        
        self.importHeadSkeletonBtn.clicked.connect(self.importFile)
        self.importBodySkeletonBtn.clicked.connect(self.importFile)
        
        self.exportCurvesBtn.clicked.connect(CurveUtils.exportCrvs)
        self.importCurvesBtn.clicked.connect(CurveUtils.importCrvs)
        
        self.mirrorCurvesBtn.clicked.connect(CurveUtils.mirrorCurves)
        
        
        
        pymelLogger.debug('End: RigBuilder.__init__()...') 
        
    def importFile(self):
        ''' Import a maya scene into the current scene using UI dialog'''
        try:
            pm.importFile( pm.fileDialog() )
        except Exception,e:
            raise Exception(e)

def main():
    global win
    try:
        win.close()
    except:
        pass
        
    win = RigBuilder()
    win.show()
    
if __name__=="RigBuilder.RigBuilder":
    main()
    