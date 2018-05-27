import unittest
import os
import sys
import platform

from mock import MagicMock, patch, call

if platform.system() == 'Darwin':
    modDir = os.path.dirname(os.path.abspath(__file__).replace('tests/api/asset/test_Create.py', 'api/asset/'))
elif platform.system() == 'Windows':
    modDir = os.path.dirname(os.path.abspath(__file__).replace('tests\\api\\asset\\test_Create.py', 'api\\asset\\'))
if modDir not in sys.path:
    sys.path.insert(0,modDir)

import Create
reload( Create )

class test_Create(unittest.TestCase):
    def test_main_1(self):
        failMsg = 'Failed to create asset.' 
        
        #------------------------ Arrange  
        # Act
        inst = Create.Create()
        result = inst.main()
        # Assert
        self.assertEqual( result, {'AssetLibStubs':failMsg,
                                  'UnityLibStubs':failMsg,
                                  'MetaData':failMsg} )

    @patch('Create.Create.createAssetLibStubFiles')      
    @patch('Create.Create.createUnityStubFiles')  
    @patch('Create.Create.createMetaDataFiles')    
    def test_main_2(self, meta_stub, unity_stub, assetLib_stub):
        successMsg = 'Created asset successfully.'
        failMsg = 'Failed to create asset.' 
        
        #------------------------  Arrange
        project = 'testing'
        unityPath = '/temp/testing/dir'
        assetLibPath = '/temp/testing/unityDir'
        user = 'unassigned'
        name = 'Asset_01'
        description = 'A test asset.'
        typ = 'character'
        subType = 'main'
        
        meta_stub.return_value = True
        unity_stub.return_value = True
        assetLib_stub.return_value = True
        
        # Act
        inst = Create.Create()
        result = inst.main(  project=project,
                             unityPath=unityPath,
                             assetLibPath=assetLibPath,
                             user=user,
                             name=name,
                             description=description,
                             typ=typ,
                             subType=subType )
        
        # Assert
        self.assertEqual( result, {'AssetLibStubs':successMsg,
                                  'UnityLibStubs':successMsg,
                                  'MetaData':successMsg} )
        
    @patch('Create.Create.createAssetLibStubFiles')      
    @patch('Create.Create.createUnityStubFiles')  
    @patch('Create.Create.createMetaDataFiles') 
    def test_main_3(self, meta_stub, unity_stub, assetLib_stub):
        successMsg = 'Created asset successfully.'
        failMsg = 'Failed to create asset.' 
        
        #------------------------ Arrange
        project = 'testing'
        unityPath = '/temp/testing/dir'
        assetLibPath = '/temp/testing/unityDir'
        user = 'unassigned'
        name = 'Ass' # Name too short test
        description = 'A test asset.'
        typ = 'character'
        subType = 'main'    
        
        meta_stub.return_value = False
        unity_stub.return_value = False
        assetLib_stub.return_value = False
        
        # Act
        inst = Create.Create()
        result = inst.main( project=project,
                            unityPath=unityPath,
                            assetLibPath=assetLibPath,
                            user=user,
                            name=name,
                            description=description,
                            typ=typ,
                            subType=subType )
        
        # Assert
        self.assertEqual( result, {'AssetLibStubs':failMsg,
                                  'UnityLibStubs':failMsg,
                                  'MetaData':failMsg} )
        
    @patch('Create.Create.createAssetLibStubFiles')      
    @patch('Create.Create.createUnityStubFiles')  
    @patch('Create.Create.createMetaDataFiles')    
    def test_main_4(self, meta_stub, unity_stub, assetLib_stub):
        successMsg = 'Created asset successfully.'
        failMsg = 'Failed to create asset.' 
        
        #------------------------  Arrange
        project = 'testing'
        unityPath = '/temp/testing/dir'
        assetLibPath = '/temp/testing/unityDir'
        user = 'userX' # Invalid user
        name = 'Asset_01'
        description = 'A test asset.'
        typ = 'character'
        subType = 'main'
        
        meta_stub.return_value = True
        unity_stub.return_value = True
        assetLib_stub.return_value = True
        
        # Act
        inst = Create.Create()
        result = inst.main(  project=project,
                             unityPath=unityPath,
                             assetLibPath=assetLibPath,
                             user=user,
                             name=name,
                             description=description,
                             typ=typ,
                             subType=subType )
        
        # Assert
        self.assertEqual( result, {'AssetLibStubs':failMsg,
                                  'UnityLibStubs':failMsg,
                                  'MetaData':failMsg} )
        
        
    @patch('Create.Create.createAssetLibStubFiles')      
    @patch('Create.Create.createUnityStubFiles')  
    @patch('Create.Create.createMetaDataFiles')    
    def test_main_5(self, meta_stub, unity_stub, assetLib_stub):
        successMsg = 'Created asset successfully.'
        failMsg = 'Failed to create asset.' 
        
        #------------------------  Arrange
        project = 'testing'
        unityPath = '/temp/testing/dir'
        assetLibPath = '/temp/testing/unityDir'
        user = 'unassigned'
        name = 'Asset_01'
        description = 'A test asset.'
        typ = 'characterX' # Invalid type
        subType = 'main'
        
        meta_stub.return_value = True
        unity_stub.return_value = True
        assetLib_stub.return_value = True
        
        # Act
        inst = Create.Create()
        result = inst.main(  project=project,
                             unityPath=unityPath,
                             assetLibPath=assetLibPath,
                             user=user,
                             name=name,
                             description=description,
                             typ=typ,
                             subType=subType )
        
        # Assert
        self.assertEqual( result, {'AssetLibStubs':failMsg,
                                  'UnityLibStubs':failMsg,
                                  'MetaData':failMsg} )
        
    @patch('Create.Create._createFile')
    @patch('Create.Create._getAnimDir') 
    def test_createMetaDataFiles_1(self, getAnimDirs_stub, create_file_stub):
        #------------------------  Arrange
        project = 'testing'
        unityPath = '/temp/testing/unityDir'
        assetLibPath = '/temp/testing/AssetLib'
        user = 'unassigned'
        name = 'Asset_01'
        description = 'A test asset.'
        typ = 'character'
        subType = 'main'
        
        create_file_stub.return_value = True
        getAnimDirs_stub.return_value = True
        
        # Act
        inst = Create.Create()
        result = inst.createMetaDataFiles(  project=project,
                                            assetLibPath=assetLibPath,
                                            name=name,
                                            typ=typ )
        
        # Assert
        self.assertEqual( result, True )

    @patch('Create.shutil')
    @patch('Create.Create._getAnimDir')
    def test_createUnityStubFiles(self, getAnimDirs_stub, shutil_mock):
        #------------------------  Arrange
        asset_stub = os.path.join(os.environ['REPOSDIR'],'artpipeline/library/stub_files/asset_stub.fbx')
        project = 'testing'
        unityPath = '/temp/UnityDir/testing/Assets/art'
        name = 'Asset_01'
        typ = 'character'
        
        expected_path = '/temp/UnityDir/testing/Assets/art/Asset_01'
        getAnimDirs_stub.return_value = expected_path
        
        # Act
        inst = Create.Create()
        result = inst.createUnityStubFiles( project=project,
                                             unityPath=unityPath,
                                             name=name,
                                             typ=typ )
        
        # Assert
        self.assertEqual( result, True )
        self.assertTrue(call.os.makedirs(expected_path) in shutil_mock.mock_calls)
        self.assertTrue(call.copyfile(asset_stub, expected_path+'/Asset_01.fbx') in shutil_mock.mock_calls)
    
    @patch('Create.Create._getAnimDir')
    @patch('Create.Create._makeDir')
    @patch('Create.shutil') 
    @patch('Create.os')
    def test_createAssetLibStubFiles(self, os_stub, 
                                     shutil_mock, makeDir_mock,
                                     getAnimDir_stub):
        #------------------------  Arrange
        project = 'testing'
        assetPath = '/temp/AssetLib/testing'
        name = 'Asset_01'
        typ = 'character'    
        os_stub.path.isdir.return_value = False
        os_stub.path.join.return_value = 'path'
        getAnimDir_stub.return_value = 'path'
        
        # Act
        inst = Create.Create()
        result = inst.createAssetLibStubFiles( project=project,
                                             assetPath=assetPath,
                                             name=name,
                                             typ=typ )
        
        # Assert
        self.assertTrue( result )
        self.assertTrue(call(path='path',dirName='model') in makeDir_mock.mock_calls)
        self.assertTrue(call(path='path',dirName='rig') in makeDir_mock.mock_calls)
        self.assertTrue(call(path='path',dirName='texture') in makeDir_mock.mock_calls)
        self.assertTrue(call(path='path',dirName='concept') in makeDir_mock.mock_calls)
        self.assertTrue(call(path='path',dirName='fbx') in makeDir_mock.mock_calls)
        self.assertTrue(call(path='path',dirName='meta') in makeDir_mock.mock_calls)
        self.assertTrue(call(path='path',dirName='reference') in makeDir_mock.mock_calls)
        self.assertTrue(call(path='path',dirName='notes') in makeDir_mock.mock_calls)
        self.assertTrue(call(path='path',dirName='reports') in makeDir_mock.mock_calls)
        self.assertTrue(call(path='path',dirName='unity_proj') in makeDir_mock.mock_calls)
    
    @patch('Create.shutil')
    def test_makeDirs(self, shutil_mock):
        path = 'path'
        dirName = 'test'
        
        inst = Create.Create()
        inst._makeDir(path=path, dirName=dirName)
        
        self.assertTrue(call.os.makedirs(os.path.join(path,dirName)) in shutil_mock.mock_calls)
        
        
    def test_getAnimDir(self):
        project = 'testing'
        typ = 'biped_animcycle'
        name = 'Anim_01'
        
        inst = Create.Create()
        
        path = '/repos/AssetLib'
        result = inst._getAnimDir(project=project,path=path,typ=typ,name=name)
        self.assertEqual(result, '/repos/AssetLib/testing/animation/biped/library/cycle/Anim_01')
        
        path = '/repos/UnityProject/Assets/art'
        result = inst._getAnimDir(unity=True, project=project, path=path, typ=typ, name=name)
        self.assertEqual(result, '/repos/UnityProject/Assets/art/animation/Anim_01')
        
        
    
    
