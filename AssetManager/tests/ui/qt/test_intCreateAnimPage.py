import unittest
import os
import sys
import platform
from PyQt4.QtGui import QApplication
from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt
from PyQt4 import QtCore

from mock import MagicMock, patch, call

if platform.system() == 'Darwin':
    modDir = os.path.dirname(os.path.abspath(__file__).replace('tests/ui/qt/test_intCreateAnimPage.py', 'ui/qt/'))
elif platform.system() == 'Windows':
    modDir = os.path.dirname(os.path.abspath(__file__).replace('tests\\ui\\qt\\test_intCreateAnimPage.py', 'ui\\qt\\'))
if modDir not in sys.path:
    sys.path.insert(0,modDir)

from MainPage import MainPage
reload( MainPage )

class test_intCreateAnimPage(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # Launch UI
        self.app = QApplication(sys.argv)
        self.form = MainPage.MainPage()
        
        # Global stub of previewTextEdit as it can't be mocked, since it 
        # is created at runtime by setupUi
        preview_stub = MagicMock(name='previewTextEdit')
        preview_stub.toPlainText.return_value = 'AssetLibPath: test\nUnity Path: test\nFile name: test'
        self.form.createAnimPage.previewTextEdit = preview_stub        

    @classmethod
    def tearDownClass(self):
        # Close UI
        self.form.close()
        
    def test_tabs(self):
        # Where Anim and Asset tabs created?
        self.assertEqual(self.form.createPageTabs.count(),2)
        self.assertEqual(str(self.form.createAnimPage.typeComboBox.currentText()),'biped_animclip')
    
    def test_previewButton(self):
        # Arrange
        self.form.createAnimPage.nameLineEdit.setText('Anim_01')
        self.form.createAnimPage.descLineEdit.setText('An animation.')
        self.form.createAnimPage.typeComboBox.currentIndex = 0
        self.form.createAnimPage.subTypeComboBox.currentIndex = 0
        
        # Act
        QTest.mouseClick(self.form.createAnimPage.previewPushButton, Qt.LeftButton)
        result = self.form.createAnimPage.previewTextEdit.toPlainText()
        
        # Assert
        expected = QtCore.QString('AssetLibPath: test\nUnity Path: test\nFile name: test')
        
        self.assertEqual(result, expected)

    @patch('os.makedirs')    
    @patch('shutil.copyfile')            
    @patch('os.path.join')                
    def test_createButton_1(self,
                            os_join_stub,
                            shutil_mock,
                            makedirs_mock):
        ''' No unity path '''
        # Arrange
        #- Ui 
        self.form.createAnimPage.nameLineEdit.setText('Anim_01')
        self.form.createAnimPage.descLineEdit.setText('An animation.')
        self.form.createAnimPage.typeComboBox.currentIndex = 0
        self.form.createAnimPage.subTypeComboBox.currentIndex = 0
        QTest.mouseClick(self.form.createAnimPage.previewPushButton, Qt.LeftButton)
        
        # Act
        QTest.mouseClick(self.form.createAnimPage.createPushButton, Qt.LeftButton)
        
        # Assert
        self.assertTrue(call('test') in makedirs_mock.mock_calls)
        self.assertTrue(call(os_join_stub()) in makedirs_mock.mock_calls)
        self.assertTrue(call(os.environ['REPOSDIR']+\
                            '/artpipeline/library/stub_files/anim_stub.ma',
                            os.path.join().replace()) in shutil_mock.mock_calls)
        self.assertTrue(call(os.environ['REPOSDIR']+\
                            '/artpipeline/library/stub_files/anim_stub.fbx',
                            os.path.join().replace()) in shutil_mock.mock_calls)
    