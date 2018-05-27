import unittest
import os
import sys
import platform
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt

from mock import MagicMock, patch, call

if platform.system() == 'Darwin':
    modDir = os.path.dirname(os.path.abspath(__file__).replace('tests/ui/qt/test_AnimInfoPage.py', 'ui/qt/'))
elif platform.system() == 'Windows':
    modDir = os.path.dirname(os.path.abspath(__file__).replace('tests\\ui\\qt\\test_AnimInfoPage.py', 'ui\\qt\\'))
if modDir not in sys.path:
    sys.path.insert(0,modDir)

from AnimInfoPage import AnimInfoPage
reload( AnimInfoPage )

class test_AnimInfoPage(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Launch UI
        self.app = QApplication(sys.argv)
        self.form = AnimInfoPage.AnimInfoPage()

    @classmethod
    def tearDownClass(self):
        # Close UI
        self.form.close()
        
    def test_getProject(self):
        path = '$ASSETLIB/facecreator/blah'
        result = self.form.getProject(path=path)
        self.assertEqual(result,'facecreator')
    
    def test_labels(self):
        self.assertEqual(str(self.form.assetLibPathLabel.text()),'Asset Library Directory: /assetLib/assset')
        self.assertEqual(str(self.form.unityPathLabel.text()),'Unity Directory: /unity/Assets/art')
        
    def test_infoTextEdit(self):
        textString = 'Project:\n'+\
        'Name:\n'+\
        'Status:\n'+\
        'Assginee:\n'+\
        'Date Created:\n'+\
        'Date Modified:\n'+\
        'Framerate:\n'+\
        'StartFrame:\n'+\
        'EndFrame:\n'+\
        'Rigs:\n'+\
        'Camera:\n'+\
        'Latest Export:\n'+\
        'Latest Commit:'
        
        self.assertEqual(str(self.form.infoTextEdit.toPlainText()),textString)        
        
        