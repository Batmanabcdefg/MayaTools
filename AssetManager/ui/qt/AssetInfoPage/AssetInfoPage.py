from functools import partial
import os
from PyQt4 import QtGui, QtCore, uic
import shutil
import sys
import logging


cwd = os.path.dirname(os.path.abspath(__file__))
apiDir = os.path.join(os.environ['REPOSDIR'],'artpipeline','asset_manager','api')

if cwd not in sys.path:
    sys.path.insert(0,cwd)
if apiDir not in sys.path:
    sys.path.insert(0,apiDir)
    
#--- Import from library
libDir = os.environ['REPOSDIR'] + '/artpipeline/library'
if libDir not in sys.path:
    sys.path.insert(0,libDir)
    
import projects
reload( projects )
import users
reload( users )

from asset.GetData import GetData

#------ Pick .ui file based on running conditions: Maya or OS
path = __file__.replace('AssetInfoPage.py','')[:-1]
try:
    import maya.OpenMayaUI as apiUI
    import sip
    form, base = uic.loadUiType(path+'/asset_info_page.ui')
    parent = None
    INMAYA = True
    
except ImportError,e:
    form, base = uic.loadUiType(path+'/asset_info_page.ui')
    parent = None
    INMAYA = False
#--------------------------------------------------------------


class AssetInfoPage(form, base):
    #UI for MainPage of asset_manager
    def __init__(self, parent = parent, **keywords):
        super(AssetInfoPage, self).__init__(parent)

        self.setupUi(self)
        
        self.concept_createNotePushButton.clicked.connect(self.createNote)
        
    def getProject(self,path=None):
        ''' Given a path with $ASSETLIB, return the project name '''
        path = path.replace('$ASSETLIB','')
        elems = os.path.split(path)
        for proj in projects.projects.keys():
            if proj in elems[0]:
                return proj
        return False
    
    def launchPage(self, parent=None):
        ''' 
        Launch the asset info page with the assets data.
        '''
        # Launch UI
        self.app = QtGui.QApplication(sys.argv)
        self.form = AssetInfoPage(parent=parent)
        self.setupWin()
    
    def setupWin(self):
        # Get asset data
        name = os.path.split(path)[-1]
        icon = path+'/icon.png'
        project = self.getProject(path=path)
        data = {'notes':{},
         'status':'ip',
         'assignee':'msantos',
         'lastExported':'3'}#GetData().allData(xmlFile=path)
        
        # Setup UI
        self.setupInfoTextEdit(project=project,
                               name=name,
                               status=data['status'],
                               assignee=data['assignee'],
                               dateCreated='N/A',
                               dateModified='N/A',
                               framerate='N/A',
                               startFrame='N/A',
                               endFrame='N/A',
                               rigs='N/A',
                               camera='N/A',
                               lastExported=data['lastExported'],
                               lastCommit='N/A')
        
        #self.setupNotes(notes=notes)
        
    

        
    def setupInfoTextEdit(self,project=None,
                               name=None,
                               status=None,
                               assignee=None,
                               dateCreated=None,
                               dateModified=None,
                               framerate=None,
                               startFrame=None,
                               endFrame=None,
                               rigs=None,
                               camera=None,
                               lastExported=None,
                               lastCommit=None):
        text = QtCore.QString('<b>Project:</b> %s\n'%project)
        text.append(QtCore.QString('<b>Name:</b> %s\n'%name))
        text.append(QtCore.QString('<b>Status:</b> %s\n'%status))
        text.append(QtCore.QString('<b>Assignee:</b> %s\n'%assignee))
        text.append(QtCore.QString('<b>Date Created:</b> %s\n'%dateCreated))
        text.append(QtCore.QString('<b>Date Modified:</b> %s\n'%dateModified))
        text.append(QtCore.QString('<b>Framerate:</b> %s\n'%framerate))
        text.append(QtCore.QString('<b>Start Frame:</b> %s\n'%startFrame))
        text.append(QtCore.QString('<b>End Frame:</b> %s\n'%endFrame))
        text.append(QtCore.QString('<b>Rigs:</b> %s\n'%rigs))
        text.append(QtCore.QString('<b>Camera:</b> %s\n'%camera))
        text.append(QtCore.QString('<b>Last Exported:</b> %s\n'%lastExported))
        text.append(QtCore.QString('<b>Last Commit:</b> %s'%lastCommit))
        
        #self.infoTextEdit.setHtml(text)
        
    def createNote(self):
        print 'Note!'
        
        
        