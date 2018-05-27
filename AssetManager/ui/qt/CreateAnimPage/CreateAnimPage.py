from functools import partial
import os
from PyQt4 import QtGui, QtCore, uic
import shutil
import sys
import logging

cwd = os.path.dirname(os.path.abspath(__file__))

if cwd not in sys.path:
    sys.path.append(cwd)
    
#--- Import from library
libDir = os.environ['REPOSDIR'] + '/artpipeline/library'
apiDir = os.environ['REPOSDIR'] + '/artpipeline/asset_manager/api/asset'
if libDir not in sys.path:
    sys.path.insert(0,libDir)
if apiDir not in sys.path:
    sys.path.insert(0,apiDir)
    
from names import assets as asset_names
reload( asset_names )
import projects
reload( projects )
import users
reload( users )
import SetData as SetData
reload( SetData )

#------ Pick .ui file based on running conditions: Maya or OS
path = __file__.replace('CreateAnimPage.py','')[:-1]
try:
    import maya.OpenMayaUI as apiUI
    import sip
    form, base = uic.loadUiType(path+'/create_anim_page.ui')

    parent = None
    INMAYA = True
    
except ImportError,e:
    form, base = uic.loadUiType(path+'/create_anim_page.ui')
    parent = None
    INMAYA = False
#--------------------------------------------------------------

class CreateAnimPage(form, base):
    #UI for MainPage of asset_manager
    def __init__(self, parent = parent, **keywords):
        super(CreateAnimPage, self).__init__(parent)
        
        #--- Determine how much feedback in log file
        if keywords.has_key('v'):
            self.verbosity = keywords['v']
        else:
            # Default. Higher verbosity reveals more info in log file. 1 - 5
            self.verbosity = 1

        #--- Setup logging
        self.logger = logging.getLogger(__name__)
        cwd = os.path.dirname(__file__)
        fh = logging.FileHandler(os.path.join(cwd,'CreateAnimPage.log'),'w')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s : [%(name)s] : [%(levelname)s] : %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh) 
        self.logger.debug('CreateAnimPage.__init__(): Initializing...')
        
        self.setupUi(self)
        
        self.previewPushButton.clicked.connect(self.preview)
        self.createPushButton.clicked.connect(self.create)
        self.typeComboBox.currentIndexChanged['QString'].connect(self.type_cc)
        self.setupTypeMenu()
        
        # Used for QMessageBoxes
        self.prompt = None
        
    def setupTypeMenu(self):
        animTypes = [ x for x in asset_names.types if 'anim' in x ]
        animTypes.sort()
        self.typeComboBox.addItems(animTypes) 
        
    def type_cc(self):
        ''' Call-back for type menu change. '''
        self.logger.info('Starting: ac_typeFilterCallback()...')
        self.subTypeComboBox.clear()
        typ = str(self.typeComboBox.currentText() )
        for styp in asset_names.subtypes[typ]:
            self.subTypeComboBox.addItem(styp)
      
    def preview(self):
        ''' Generate preview given current data in ui '''
        parent = self.parent().parent().parent().parent().parent().parent().parent().parent()
        project = str(parent.projComboBox.currentText())
        #user = str(parent.userComboBox.currentText())
        name = str(self.nameLineEdit.text())
        desc = str(self.descLineEdit.text())
        typ = str(self.typeComboBox.currentText())
        subTyp = str(self.subTypeComboBox.currentText())
        assetLibPath = str(parent.settingsPage.assetLibPathLineEdit.text())
        unityPath = str(parent.settingsPage.unityPathLineEdit.text())
        
        text = QtCore.QString('<p><b>Project:</b> %s</br></p>'%project)
        text.append(QtCore.QString('<p><b>Name:</b> %s</p>'%name))
        text.append(QtCore.QString('<p><b>Description:</b> %s</p>'%desc))
        text.append(QtCore.QString('<p><b>Status:</b> wts</p>'))
        #text.append(QtCore.QString('<p><b>Assginee:</b> %s</p>'%user))
        text.append(QtCore.QString('<p><b>AssetLibPath:</b> %s/%s/%s/%s</p>'%(assetLibPath,'animation',typ,name)))
        text.append(QtCore.QString('<p><b>Unity Path:</b> %s/animation/%s/%s</p>'%(unityPath,typ,name)))
        text.append(QtCore.QString('<p><b>File name:</b> %s_%s.ma</p>'%(name,typ)))
        self.previewTextEdit.setText(text)
        
    def create(self):
        self.logger.info('Starting create()...')
        elems = self.previewTextEdit.toPlainText().split('\n')
        a,b,c = False, False, False
        for elem in elems:
            if 'AssetLibPath' in elem:
                assetLib = str(elem.split(':')[-1]).strip().replace('$ASSETLIB',os.environ['ASSETLIB'])
                a = True
            if 'Unity Path' in elem:
                unityPath = str(elem.split(':')[-1]).strip().replace('$REPOSDIR',os.environ['REPOSDIR'])  
                b = True
            if 'File name' in elem:
                fileName = str(elem.split(':')[-1]).strip().replace('$ASSETLIB',os.environ['ASSETLIB'])
                c = True
        if not a or not b or not c:
            msg = "Create failed. Ensure preview data is correct.\nNothing created."
            self.logger.error(msg)
            self.prompt = QtGui.QMessageBox(self)
            self.prompt.setText(msg)
            self.prompt.exec_()
            return False
        
        # Define file names
        assetLibFile = os.path.join(str(assetLib),str(fileName))
        unityFile = os.path.join(str(unityPath),str(fileName).replace('.ma','.fbx'))
       
        try:
            # Make directories
            os.makedirs(assetLib)
            for d in asset_names.anim_dirs:
                os.makedirs(os.path.join(assetLib, d))
            
            if not 'None' in unityPath: os.makedirs(unityPath)        
            
            # Create anim stubs
            stubDir = os.environ['REPOSDIR']+'/artpipeline/library/stub_files/'
            
            shutil.copyfile(stubDir+'anim_stub.ma', assetLibFile)
            if not 'None' in unityPath:
                shutil.copyfile(stubDir+'anim_stub.fbx',unityFile)
            shutil.copyfile(stubDir+'anim_stub.xml',assetLib+'/meta/anim_info.xml')
            shutil.copyfile(stubDir+'stub_icon.jpg',assetLib+'/icon.jpg')
            
        except Exception,e:
            msg = e
            self.logger.error(msg)
            self.prompt = QtGui.QMessageBox(self)
            self.prompt.setText(str(msg))
            self.prompt.exec_()  
            return
        
        #self._writeXmlData( xmlFile=assetLib+'/meta/anim_info.xml' )

        # Results prompt
        msg = "Created: %s\n"%assetLibFile
        if not 'None' in unityPath:
            msg += "Created: %s\n"%unityFile
        self.logger.info(msg)
        self.prompt = QtGui.QMessageBox(self)
        self.prompt.setText(msg)
        self.prompt.exec_()   
        
        self.logger.info('create(): End.')
        
    def _writeXmlData(self, xmlFile=None):
        ''' Write data to xml files for asset '''
        parent = self.parent().parent().parent().parent().parent().parent().parent().parent()
        project = str(parent.projComboBox.currentText())
        user = None#str(parent.userComboBox.currentText())
        name = str(self.nameLineEdit.text())
        typ = str(self.typeComboBox.currentText())
        
        sd = SetData.SetData()
        sd.setValue(typ = 'project', value = project, filePath = xmlFile, userName = user )
        sd.setValue(typ = 'assignee', value = user, filePath = xmlFile, userName = user )
        sd.setValue(typ = 'type', value = typ, filePath = xmlFile, userName = user )
        sd.setValue(typ = 'name', value = name, filePath = xmlFile, userName = user )
        sd.setValue(typ = 'status', value = 'wts', filePath = xmlFile, userName = user )
        
        
        
        