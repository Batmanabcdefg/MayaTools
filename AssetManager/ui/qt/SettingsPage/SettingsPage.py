from functools import partial
import os
from PyQt4 import QtGui, QtCore, uic
import shutil
import sys
import logging

cwd = os.path.dirname(os.path.abspath(__file__))

if cwd not in sys.path:
    sys.path.append(cwd)

#------ Pick .ui file based on running conditions: Maya or OS
path = __file__.replace('SettingsPage.py','')[:-1]
try:
    import maya.OpenMayaUI as apiUI
    import sip
    form, base = uic.loadUiType(path+'/settings_page.ui')

    parent = None
    INMAYA = True
    
except ImportError,e:
    form, base = uic.loadUiType(path+'/settings_page.ui')
    parent = None
    INMAYA = False
#--------------------------------------------------------------


class SettingsPage(form, base):
    #UI for MainPage of asset_manager
    def __init__(self, parent = parent, **keywords):
        super(SettingsPage, self).__init__(parent)
        
        #--- Determine how much feedback in log file
        if keywords.has_key('v'):
            self.verbosity = keywords['v']
        else:
            # Default. Higher verbosity reveals more info in log file. 1 - 5
            self.verbosity = 1

        #--- Setup logging
        self.logger = logging.getLogger(__name__)
        cwd = os.path.dirname(__file__)
        fh = logging.FileHandler(os.path.join(cwd,'SettingsPage.log'),'w')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s : [%(name)s] : [%(levelname)s] : %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh) 
        self.logger.debug('SettingsPage.__init__(): Initializing...')
        
        self.setupUi(self)
    