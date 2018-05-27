import unittest
import os
import sys
import platform
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt

from mock import MagicMock, patch, call

if platform.system() == 'Darwin':
    modDir = os.path.dirname(os.path.abspath(__file__).replace('tests/ui/qt/test_MainPage.py', 'ui/qt/'))
elif platform.system() == 'Windows':
    modDir = os.path.dirname(os.path.abspath(__file__).replace('tests\\ui\\qt\\test_MainPage.py', 'ui\\qt\\'))
if modDir not in sys.path:
    sys.path.insert(0,modDir)

from MainPage import MainPage
reload( MainPage )

class test_MainPage(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Launch UI
        self.app = QApplication(sys.argv)
        self.form = MainPage.MainPage()

    @classmethod
    def tearDownClass(self):
        # Close UI
        self.form.close()
        
    def test_currentProjectMenu(self):
        # Arrange
        projects = ['testing','facecreator','startrek','fearnet','diabetes']
        users = ['unassigned','chipple','ckong','vhao','jqi',
                 'jcalduch','bwilson','sbaittle','msantos']   
        
        # Assert
        self.assertEqual( len(projects), int(self.form.projComboBox.count()) )
        self.assertEqual( len(users), int(self.form.userComboBox.count()) )
        
    def test_projectsCC(self):
        # Act
        self.form.projComboBox.setCurrentIndex(2)
        
        # Assert
        self.assertEqual(str(self.form.settingsPage.assetLibPathLineEdit.text()),
                         '$ASSETLIB/fearnet')
        self.assertEqual(str(self.form.settingsPage.unityPathLineEdit.text()),
                         '$REPOSDIR/zombies/unityprojects/fearnet/Assets/art')

    
    