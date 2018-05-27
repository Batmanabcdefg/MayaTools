from functools import partial
import os
from PyQt4 import QtGui, QtCore, uic
import shutil
import sys
import logging
import pickle

cwd = os.path.dirname(os.path.abspath(__file__))
qtDir = os.path.join(os.environ['REPOSDIR'],'artpipeline/asset_manager/ui/qt')
if cwd not in sys.path:
    sys.path.append(cwd)
if qtDir not in sys.path:
    sys.path.append(qtDir)

#--- Import from library
libDir = os.environ['REPOSDIR'] + '/artpipeline/library'
if libDir not in sys.path:
    sys.path.insert(0,libDir)

from names import assets as asset_names
reload( asset_names )
import projects
reload( projects )
import users
reload( users )
from qt import tab as qtTabLib
reload( qtTabLib )
from qt import FlowLayout

#--- Ui components
from SettingsPage import SettingsPage
reload( SettingsPage )
from CreateAssetPage import CreateAssetPage
reload( CreateAssetPage )
from CreateAnimPage import CreateAnimPage
reload( CreateAnimPage )
from AssetWidget import AssetWidget
reload( AssetWidget )
from AnimInfoPage import AnimInfoPage
reload( AnimInfoPage )

import ignore
reload( ignore )

#------ Pick .ui file based on running conditions: Maya or OS
path = __file__.replace('MainPage.py','')[:-1]
try:
    import maya.OpenMayaUI as apiUI
    import sip
    form, base = uic.loadUiType(path+'/main_page.ui')
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
    parent = getMayaWindow()
    INMAYA = True

except ImportError,e:
    form, base = uic.loadUiType(path+'/main_page.ui')
    parent = None
    INMAYA = False
#--------------------------------------------------------------


class MainPage(form, base):
    #UI for MainPage of asset_manager
    def __init__(self, parent = parent, **keywords):
        super(MainPage, self).__init__(parent)

        #--- Determine how much feedback in log file
        if keywords.has_key('v'):
            self.verbosity = keywords['v']
        else:
            # Default. Higher verbosity reveals more info in log file. 1 - 5
            self.verbosity = 1

        #--- Setup logging
        self.logger = logging.getLogger(__name__)
        cwd = os.path.dirname(__file__)
        fh = logging.FileHandler(os.path.join(cwd,'MainPage.log'),'w')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s : [%(name)s] : [%(levelname)s] : %(message)s',
                                      datefmt='%m/%d/%Y %I:%M:%S %p')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)
        self.logger.debug('MainPage.__init__(): Initializing...')

        self.setupUi(self)
        self.setupComboMenus()
        self.setupSettingsPage()
        self.setupCreateTabs()

        self.projectsCC()
        #self._restoreState()

    def setupComboMenus(self):
        projs = projects.projects.keys()
        projs.sort()
        self.projComboBox.addItems(projs)
        self.projComboBox.currentIndexChanged['QString'].connect(self.projectsCC)
        usrs = users.users
        usrs.sort()
        #self.userComboBox.addItems(usrs)

    def setupSettingsPage(self):
        self.settingsPage = SettingsPage.SettingsPage( self.settingsTab )
        self.settingsVLayout.addWidget(self.settingsPage)

    def setupCreateTabs(self):
        # Create tab layout
        tabs = ['Asset','Animation']
        newTabs = qtTabLib.createTabs(tabLayout=self.createPageTabs,tabs=tabs)

        layout = QtGui.QVBoxLayout()
        self.createAssetPage = CreateAssetPage.CreateAssetPage( newTabs[0] )
        layout.addWidget(self.createAssetPage)
        newTabs[0].setLayout(layout)

        layout = QtGui.QVBoxLayout()
        self.createAnimPage = CreateAnimPage.CreateAnimPage( newTabs[1] )
        layout.addWidget(self.createAnimPage)
        newTabs[1].setLayout(layout)

    def setupBrowsePage(self):
        try:
            root = str(self.settingsPage.assetLibPathLineEdit.text())
            unityPath = str(self.settingsPage.unityPathLineEdit.text())

            # if root happens to not be in assetlib
            # it will not work
            assetLibVar = '$ASSETLIB'
            if assetLibVar in root:

                root = root.replace( assetLibVar, os.environ['ASSETLIB'])
                unityPath = unityPath.replace('$REPOSDIR', os.environ['REPOSDIR'])
                dirs = next(os.walk(root))[1]

                for d in ignore.assetmanager_ignore:
                    try: dirs.remove(d)
                    except: pass

                qtTabLib.removeTabs(layout=self.browseTabs)
                newTabs = qtTabLib.createTabs(tabLayout=self.browseTabs,tabs=dirs)

                for t,d in zip(newTabs,dirs):
                    if d == 'animation':
                        hl2 = QtGui.QHBoxLayout(t)
                        hl2.setSpacing(0)
                        hl2.setContentsMargins(0,0,0,0)
                        tabWidget = QtGui.QTabWidget(t)
                        hl2.addWidget(tabWidget)

                        animDirs = next(os.walk(os.path.join(root,d)))[1]
                        for ig in ignore.assetmanager_ignore:
                            try: animDirs.remove(ig)
                            except: pass
                        animTabs = qtTabLib.createTabs(tabLayout=tabWidget,tabs=animDirs)

                        for at,ad in zip(animTabs,animDirs):
                            hl3 = QtGui.QHBoxLayout(at)

                            scrolly = QtGui.QScrollArea(at)
                            scrolly.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                            scrolly.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
                            scrolly.setFrameShape(QtGui.QFrame.NoFrame)
                            scrolly.setWidgetResizable(True)

                            scrollAreaWidgetContents = QtGui.QWidget()
                            scrolly.setWidget(scrollAreaWidgetContents)
                            hl3.addWidget(scrolly)

                            f = FlowLayout.FlowLayout(parent=scrollAreaWidgetContents)
#                            assets = AssetWidget.AssetWidget().getAssets(os.path.join(root,d,ad),
#                                                                         unityPath=unityPath)
#
                            assets = AssetWidget.AssetWidget().getAssets(root+'/'+d+'/'+ad,
                                                                         unityPath=unityPath)

                            for a in assets:
                                f.addWidget(a)
                    else:
                        hl = QtGui.QHBoxLayout(t)
                        scrolly = QtGui.QScrollArea(t)
                        scrolly.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                        scrolly.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
                        scrolly.setFrameShape(QtGui.QFrame.NoFrame)
                        scrolly.setWidgetResizable(True)

                        scrollAreaWidgetContents = QtGui.QWidget()
                        scrolly.setWidget(scrollAreaWidgetContents)
                        hl.addWidget(scrolly)

                        f = FlowLayout.FlowLayout(parent=scrollAreaWidgetContents)
                        #assets = AssetWidget.AssetWidget().getAssets(os.path.join(root,d),
                        assets = AssetWidget.AssetWidget().getAssets(root+'/'+d,
                                                                     unityPath=unityPath)

                        for a in assets:
                            f.addWidget(a)

            else:
                # getting rig of tabs if project does not have content
                qtTabLib.removeTabs(layout=self.browseTabs)
                return False


        except Exception,e:
            self.logger.error(e)
            raise Exception( e )

    def projectsCC(self):
        ''' Update paths in settings when project chages. '''
        proj = str(self.projComboBox.currentText())
        self.settingsPage.assetLibPathLineEdit.setText(projects.projects[proj][0])
        self.settingsPage.unityPathLineEdit.setText(projects.projects[proj][1])
        self.setupBrowsePage()

    def _saveState(self):
        ''' Write data from UI to file '''
        self.logger.info('Starting: _saveState()...')

        project = str( self.projComboBox.currentText() ).lower()
        user = 'None'#str(self.userComboBox.currentText()).lower()
        svnAcct = str(self.settingsPage.svnUserLineEdit.text()).lower()
        svnPW = str(self.settingsPage.svnPwLineEdit.text() ).lower()
        sgAcct = str(self.settingsPage.sgUserLineEdit.text()).lower()
        sgPW = str(self.settingsPage.sgPwLineEdit.text() ).lower()
        ggAcct = str(self.settingsPage.gMailAddrLineEdit.text()).lower()
        ggPW = str(self.settingsPage.gMailPwLineEdit.text() ).lower()

        data = [project, user, svnAcct, svnPW, sgAcct, sgPW, ggAcct, ggPW]
        f = open(os.path.join(os.environ['REPOSDIR'],'artpipeline/asset_manager/asset_manager_user.data'), 'wb')
        pickle.dump(data, f)
        f.close()

        self.logger.info('End: _saveState().')

    def _restoreState(self):
        ''' Load data from saveState file to Browser tab '''
        self.logger.info('Starting: _restoreState()...')
        fileName = os.path.join(os.environ['REPOSDIR'],'artpipeline/asset_manager/asset_manager_user.data')

        if os.path.isfile(fileName):
            self.logger.info('Found state file. Restoring state...')
            data = pickle.load( open( fileName, "rb" ) )

            self.projComboBox.setCurrentIndex(self.projComboBox.findText(data[0].title()))
            #self.userComboBox.setCurrentIndex(self.userComboBox.findText(data[1].title()))
            self.svnUserLineEdit.setText(data[2])
            self.svnPwLineEdit.setText(data[3])
            self.sgUserLineEdit.setText(data[4])
            self.sgPwLineEdit.setText(data[5])
            self.gMailAddrLineEdit.setText(data[6])
            self.gMailPwLineEdit.setText(data[7])

            self.logger.info('Restoring state done.')

        self.logger.info('End: _restoreState().')

    '''
    def closeEvent(self, event):
        self._saveState()
        event.accept()
    '''

def main():
    global am_win
    try:
        am_win.close()
    except:
        pass
    if not INMAYA:
        am_app = QtGui.QApplication(sys.argv)

    am_win = MainPage()
    am_win.show()

    if not INMAYA:
        sys.exit(am_app.exec_())

if __name__ == "__main__":
    main()

