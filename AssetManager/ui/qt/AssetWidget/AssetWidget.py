from functools import partial
import os
from PyQt4 import QtGui, QtCore, uic
import shutil
import sys
import logging

import random

cwd = os.path.dirname(os.path.abspath(__file__))

if cwd not in sys.path:
    sys.path.append(cwd)

libDir = os.environ['REPOSDIR'] + '/artpipeline/library'
if libDir not in sys.path:
    sys.path.insert(0,libDir) 
      
import tmxml.tmxml as tmXml


assetDir = os.environ['REPOSDIR'] + '/artpipeline/asset_manager/api/asset'
if assetDir not in sys.path:
    sys.path.insert(0,assetDir)
    
import SetData
reload(SetData)
      


#--- Import from ui qt     
qtDir = os.environ['REPOSDIR'] + '/artpipeline/asset_manager/ui/qt'
if qtDir not in sys.path:
    sys.path.insert(0,qtDir)     
 
import AssetInfoPage.AssetInfoPage as AssetInfoPage
reload(AssetInfoPage)
import AnimInfoPage.AnimInfoPage as AnimInfoPage
reload(AnimInfoPage)


      
#--- Import from library
libDir = os.environ['REPOSDIR'] + '/artpipeline/library'
if libDir not in sys.path:
    sys.path.insert(0,libDir)

   
import projects
reload( projects )
import users
reload( users )
import ignore
from qt import ExtendedLabel
reload(ExtendedLabel)

class AssetWidget(object):
    """ """
    def __init__(self, **keywords):
        """
        #--- Determine how much feedback in log file
        if keywords.has_key('v'):
            self.verbosity = keywords['v']
        else:
            # Default. Higher verbosity reveals more info in log file. 1 - 5
            self.verbosity = 1

        #--- Setup logging
        
        self.logger = logging.getLogger(__name__)
        cwd = os.path.dirname(__file__)
        fh = logging.FileHandler(os.path.join(cwd,'AssetWidget.log'),'w')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s : [%(name)s] : [%(levelname)s] : %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh) 
        self.logger.debug('AssetWidget.__init__(): Initializing...')
        """
           
    def getAssets(self, root=None, unityPath=None):
        ''' 
        Given a root directory with asset directories in it,
        return a list of widgets that represent those assets. 
        '''
        try:
            widgets = []
            try:
                dirs = next(os.walk(root))[1]
            except:
                return widgets

            for d in ignore.assetmanager_ignore:
                try: dirs.remove(d)
                except: pass
            
            # if there is no content on dir don't proceed 
            if len(dirs)>0:
                if 'animation' not in root:
                    for each in dirs:
                        #widgets.append(self.setUpAssetWidget(path=os.path.join(root,each),
                        widgets.append(self.setUpAssetWidget(path=root+'/'+each,
                                                             unityPath=unityPath))
                else:
                    for each in dirs:
                        #widgets.append(self.setUpAnimWidget(path=os.path.join(root,each),
                        widgets.append(self.setUpAnimWidget(path=root+'/'+each,
                                                            unityPath=unityPath))
            return widgets
        except Exception, e:
            """
            self.logger.error('dirs: %s'%dirs)
            self.logger.error(e)
            """
            raise Exception(e)
        

    def setUpAssetWidget(self, path=None, unityPath=None):
        ''' 
        Given a path to an asset, create a widget with its' info 
        @todo: Read meta data
        '''
        name = os.path.basename(path)
        widget = self.createAW(name=name, typ='asset', path=path, unityPath=unityPath)
        
        launch = AssetInfoPage.AssetInfoPage()
        launch = launch.launchPage
        #widget.connect(widget, QtCore.SIGNAL('clicked'), partial( launch, path))         
        return widget
        
    def setUpAnimWidget(self, path=None, unityPath=None):
        ''' 
        Given a path to an animation, create a widget with its' info 
        @todo: Read meta data
        '''
        name = os.path.basename(path)
        widget = self.createAW(name=name, typ='anim', path=path, unityPath=unityPath)
        
        launch = AnimInfoPage.AnimInfoPage()
        launch = launch.launchPage
        #widget.connect(widget, QtCore.SIGNAL('clicked'), partial( launch, path))        
        return widget
    
    def _check_icon_exists(self, path=None):
        """ """
        iconPath = os.path.join(path, 'icon.jpg')
        if os.path.exists( iconPath ):
            return True
        else:
            return False
    
    def _status_color(self, status):
        """ """
        try:
            sColor = {'wts': '255,255,255',
                      'ip': '255,255,0',
                      'review': '100,100,255',
                      'final': '0,255,0',
                      'hold': '250,150,28'}[status]
            return sColor
        except:
            # status not valid
            return '0,0,0'

    def _status_labels(self, name=None, statusGroupBox=None, hl=None, path=None):
        """ """
        #read xml if it exists and set status
        # model_info.xml concept_info.xml texture_info.xml rig_info.xml
        #assetInfoFiles = ['model_info.xml','concept_info.xml','texture_info.xml','rig_info.xml']
        if 'animation' in path:
            pathToXml = os.path.join(path, 'meta','anim_info.xml')
        else:
            pathToXml = os.path.join(path, 'meta', name + '_info.xml')
        #setValue(typ = None, value = None, filePath = None, userName = None ):
        #SetData.SetData().setValue('status', value, pathToXml, 'msantos' )
        sd = SetData.SetData().setValue
        scMethod = self._status_color
        optList = [ ['wts',[sd,['status', 'wts', pathToXml, 'msantos',scMethod]]], 
                   ['ip',[sd,['status', 'ip', pathToXml, 'msantos',scMethod ]]], 
                   ['review',[sd,['status', 'review', pathToXml, 'msantos',scMethod ]]], 
                   ['final',[sd,['status', 'final', pathToXml, 'msantos',scMethod ]]],
                   ['hold',[sd,['status', 'hold', pathToXml, 'msantos',scMethod ]]] 
                 ]

        if os.path.exists(pathToXml):
            
            xmlObj = tmXml.tmXml()
            xmlFile = xmlObj.readXml(pathToXml)
            status = xmlObj.getTagValueByTagName(xmlFile, 'status')
            sColor = self._status_color(status)

            statusLabel = ExtendedLabel.ExtendedLabel( statusGroupBox, optList )
            statusLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            statusLabel.setAutoFillBackground(False)
            statusLabel.setStyleSheet("QLabel { background-color: rgb("+sColor+") } ")
            
            if 'animation' in path:
                statusLabel.setText(" ")
            else:
                statusLabel.setText(" %s"%name[0].title()) 
                
            #statusLabel.setPixmap(QtGui.QPixmap("../graphics/png/status_open_small.png"))
            #statusLabel.setScaledContents(True)
            statusLabel.setObjectName(name)
            hl.addWidget(statusLabel)
            
        else:
            # file could not be found

            statusLabel = ExtendedLabel.ExtendedLabel( statusGroupBox, optList )
            statusLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            statusLabel.setAutoFillBackground(False)
            statusLabel.setStyleSheet("background-color: rgb(10,10,10);")
            statusLabel.setText("")
            #statusLabel.setPixmap(QtGui.QPixmap("../graphics/png/status_open_small.png"))
            #statusLabel.setScaledContents(True)
            statusLabel.setObjectName(name)
            hl.addWidget(statusLabel)
            return False

    
    
    def createAW(self, name=None, typ=None, path=None, unityPath=None):
        """ creates assetwidget """

        if typ == 'asset':
            optList = [ ['Open File',[path,typ,unityPath]],
                        ['Open Directory',[path,typ,unityPath]],
                        ['Assign',[path,typ,unityPath]],
                        ['Assignments',[path,typ,unityPath]], 
                        ['WebPlayer',[path,None,unityPath]],
                        ['Export',[path,typ,unityPath]] ]
                        #['----------',[None,None]],
                        #['Delete',[None,None]] ]
            
        elif typ == 'anim':
            optList = [ ['Open File',[path,typ,unityPath]],
                        ['Open Directory',[path,typ,unityPath]],
                        ['Assign',[path,typ,unityPath]],
                        ['Assignments',[path,typ,unityPath]], 
                        ['WebPlayer',[None,None,unityPath]],
                        ['Export',[path,typ,unityPath]] ]
                        #['----------',[None,None,unityPath]], 
                        #['Delete',[None,None,unityPath]] ]
        else:
            raise Exception('createAW called without typ. Should be either "asset or "anim".')
        
        exTop = ExtendedLabel.ExtendedLabel( optList=optList )
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHeightForWidth(exTop.sizePolicy().hasHeightForWidth())
        exTop.setSizePolicy(sizePolicy)
        exTop.setMinimumSize(QtCore.QSize(168, 233))
        exTop.setMaximumSize(QtCore.QSize(168, 233))
        
        topGroupBox = QtGui.QGroupBox(exTop)
        topGroupBox.setMinimumSize(QtCore.QSize(100, 210))
        topGroupBox.setMaximumSize(QtCore.QSize(130, 210))
        topGroupBox.setToolTip(name)
        
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        topGroupBox.setFont(font)
        topGroupBox.setTitle("")
        topGroupBox.setCheckable(False)
        topGroupBox.setObjectName("topGroupBox")
        verticalLayout_5 = QtGui.QVBoxLayout(topGroupBox)
        verticalLayout_5.setObjectName("verticalLayout_5")
        nameLabel = QtGui.QLabel(topGroupBox)
        nameLabel.setMinimumSize(QtCore.QSize(100, 15))
        nameLabel.setMaximumSize(QtCore.QSize(100, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        
        nameLabel.setFont(font)
        nameLabel.setObjectName("nameLabel")
        nameLabel.setText(name)
        
        verticalLayout_5.addWidget(nameLabel)
        iconLabel = QtGui.QLabel(topGroupBox)
        iconLabel.setMinimumSize(QtCore.QSize(100, 100))
        iconLabel.setMaximumSize(QtCore.QSize(100, 100))
        iconLabel.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(15)
        iconLabel.setFont(font)
        iconLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        iconLabel.setAutoFillBackground(True)
        iconLabel.setFrameShape(QtGui.QFrame.Box)
        iconLabel.setFrameShadow(QtGui.QFrame.Plain)
     
        # asset icon
        if self._check_icon_exists(path):
            iconPath = os.path.join(path, 'icon.jpg')
        else: iconPath = os.path.join( libDir, 'stub_files', 'stub_icon.jpg' )
        iconLabel.setPixmap(QtGui.QPixmap( iconPath ))
        
        iconLabel.setScaledContents(True)
        iconLabel.setObjectName("iconLabel")
        verticalLayout_5.addWidget(iconLabel)
        
        '''
        statusGroupBox = QtGui.QGroupBox(topGroupBox)
        statusGroupBox.setMaximumSize(QtCore.QSize(16777215, 30))
        statusGroupBox.setObjectName("statusGroupBox")
        
        horizontalLayout_7 = QtGui.QHBoxLayout(statusGroupBox)
        horizontalLayout_7.setSpacing(0)
        horizontalLayout_7.setMargin(1)
        horizontalLayout_7.setObjectName("horizontalLayout_7")
        
        if typ == 'asset':
            lst = ['concept', 'model', 'texture', 'rig']
            for each in lst:
                self._status_labels(each, statusGroupBox, horizontalLayout_7, path)
        if typ == 'anim':
            lst = ['anim']
            for each in lst:
                self._status_labels(each, statusGroupBox, horizontalLayout_7, path)
           
        #, 'export' 

        verticalLayout_5.addWidget(statusGroupBox)
        '''
        return exTop
        
        