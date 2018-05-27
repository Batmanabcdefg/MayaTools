import unittest
import os
import sys
import platform
import shutil
from itertools import chain

from mock import MagicMock, patch, call

if platform.system() == 'Darwin':
    modDir = os.path.dirname(os.path.abspath(__file__).replace('tests/api/asset/test_Export.py', 'api/asset/'))
elif platform.system() == 'Windows':
    modDir = os.path.dirname(os.path.abspath(__file__).replace('tests\\api\\asset\\test_Export.py', 'api\\asset\\'))
if modDir not in sys.path:
    sys.path.insert(0,modDir)
    
#--- Mock out fbxExport import that Export does
fbx_mock = MagicMock()
sys.modules['fbxExport'] = fbx_mock
import Export
reload( Export ) 
setattr(Export, 'fbxExport', fbx_mock)

class test_Export(unittest.TestCase):
    def setUp(self):
        self.results = []
        self.unityPath = os.environ['REPOSDIR']+\
            '/UnityProject/testing/Assets/art'

    @patch('Export.os.path.exists')
    def test_exportAnim(self, os_stub):
      
        # Arrange
        fbx_mock.fbxExport().exportAnim.return_value = True
        export = Export.Export()
        fileName = os.environ['REPOSDIR']+\
            '/arttools/Maya/testing/DevAssetLib/testing/animation/biped/library/clip/female_sitting_typing_01/female_sitting_typing_01.ma'
        if os.name == 'nt':
            fileName = fileName.split(os.sep)
            fileName = os.path.join(fileName[0],'/',fileName[1])
        assetPath = os.path.dirname(fileName)+'/fbx'
        
        # Act
        self.results = export.exportAnim( fileName=fileName, assetPath=assetPath, 
                                          unityPath=self.unityPath )
        
        # Assert
        self.assertTrue( call.fbxExport().exportAnim(fileName=fileName, assetPath=assetPath, 
                                         unityPath=self.unityPath) in fbx_mock.mock_calls )
        
    @patch('Export.os.path.isdir')    
    @patch('Export.os.walk')
    @patch('Export.Export.exportAnim')
    def test_batchExportAnims(self, expAnim_mock,os_walk_stub, os_isdir_stub):
        # Arrange
        test_dir = [('testDir', ['d1, d2'], ['female_sitting_typing_01.ma'])]        
        export = Export.Export()
        os_isdir_stub.return_value = True
        os_walk_stub.return_value = test_dir
        
        animDir = os.environ['REPOSDIR']+'/arttools/Maya/testing/DevAssetLib/testing/animation'
        if os.name == 'nt':
            animDir = animDir.split(os.sep)
            animDir = os.path.join(animDir[0],'/',animDir[1])
        
        # Act
        self.results = export.batchExportAnims(directory=animDir, unityPath=self.unityPath)

        # Assert
        self.assertTrue( call(unityPath='/Users/3mo/Documents/repos/UnityProject/testing/Assets/art', 
                          assetPath='testDir/fbx', fileName='testDir/female_sitting_typing_01.ma')\
                         in expAnim_mock.mock_calls )
           
    @patch('Export.os.path.isfile')
    def test_exportAsset(self,os_stub):
        # Arrange
        export = Export.Export()
        fileName = os.environ['REPOSDIR']+'/AssetLib/testing/hair/hair_carol_01/rig/hair_carol_01_rig.ma'
        assetPath = os.path.dirname(fileName).replace('rig','fbx')
        assetFbxFile = assetPath + '/hair_carol_01_rig.fbx'
        unityFbxFile = self.unityPath + '/hair_carol_01_rig.fbx'
        
        os_stub.return_value = True
        fbx_mock.fbxExport().exportAsset.return_value = [True, True]
        
        if os.name == 'nt':
            fileName = fileName.split(os.sep)
            fileName = os.path.join(fileName[0],'/',fileName[1])

        # Act
        self.results = export.exportAsset(fileName=fileName, assetPath=assetPath, unityPath=self.unityPath)
        
        # Assert
        self.assertTrue(call.fbxExport.fbx().exportAsset(fileName=fileName, 
                                       assetPath=assetPath, 
                                       unityPath=self.unityPath) in fbx_mock.mock_calls)
    
    @patch('Export.os.path.isdir')    
    @patch('Export.os.walk')
    @patch('Export.Export.exportAsset')   
    def test_batchExportAssets(self, expAsset_mock, os_walk_stub, os_path_isdir_stub):
        # Arrange
        test_dir = [('/testDir/rig', ['d1, d2'], ['hair_carol_01_rig.ma'])] 
        export = Export.Export()
        os_path_isdir_stub.return_value = True
        os_walk_stub.return_value = test_dir
        assetDir = '/testDir'
        if os.name == 'nt':
            assetDir = assetDir.split(os.sep)
            assetDir = os.path.join(assetDir[0],'/',assetDir[1])
        
        # Act
        self.results = export.batchExportAssets(directory=assetDir, unityPath=self.unityPath)


        # Assert
        self.assertTrue( call(unityPath=self.unityPath, 
                          assetPath='/testDir/fbx', 
                          fileName='/testDir/rig/hair_carol_01_rig.ma')\
                         in expAsset_mock.mock_calls )

    
    