import unittest
import os
import sys
import platform

from mock import MagicMock, patch, call

if platform.system() == 'Darwin':
    modDir = os.path.dirname(os.path.abspath(__file__).replace('tests/api/asset', 'api/asset'))
elif platform.system() == 'Windows':
    modDir = os.path.dirname(os.path.abspath(__file__).replace('tests\\api\\asset', 'api\\asset'))
    
if modDir not in sys.path:
    sys.path.append(modDir)

import ProjectNamesList
reload( ProjectNamesList )

class test_ProjectNamesList(unittest.TestCase):
    @patch('ProjectNamesList.ProjectNamesList._check_length')
    @patch('ProjectNamesList.ProjectNamesList._add_to_xml_names')
    @patch('ProjectNamesList.ProjectNamesList._check_unique')
    def test_add(self, check_unique_mock, add_xml_stub, len_stub):
        # Arrange
        addToNames = ProjectNamesList.ProjectNamesList()
        fakeFile = MagicMock(name='proj_names.xml') 
        
        namePass = 'Asset_01'
        nameNotUnique = 'Asset_00'
        nameTooBig = 'DeffgetshdjifugheitheyKuthri'        

        len_stub.return_value = True
        # Set what to return on 1st, 2nd, and 3rd calls
        check_unique_mock.side_effect = [True, False, True]
        # Set what to return on 1st and 2nd calls
        add_xml_stub.side_effect = [True, False]
        
        # Act
        resultPass = addToNames.add(assetName=namePass, fileName=fakeFile)
        resultNotUnique = addToNames.add(assetName=nameNotUnique, fileName=fakeFile)
        resultTooBig = addToNames.add(assetName=nameTooBig, fileName=fakeFile)
        
        # Assert
        self.assertTrue( call(name=namePass, fileName=fakeFile) in check_unique_mock.mock_calls)
        self.assertTrue( call(name=nameNotUnique, fileName=fakeFile) in check_unique_mock.mock_calls)
        self.assertTrue( call(name=nameTooBig, fileName=fakeFile) in check_unique_mock.mock_calls)
        
        self.assertEqual( resultPass, 'Added %s to proj_names.xml'%namePass )
        self.assertEqual( resultNotUnique, False )
        self.assertEqual( resultTooBig, False )
    
    @patch('ProjectNamesList.ProjectNamesList._read_xml_names')
    def test_check_unique(self, read_stub):
        read_stub.method()
        # Arrange 
        addToNames = ProjectNamesList.ProjectNamesList()
        name = 'Asset_01'
        fakeFile = MagicMock(name='proj_names.xml')
        read_stub.side_effect = [ [], ['Asset_01'] ]
        
        # Act
        result1 = addToNames._check_unique(name=name, fileName=fakeFile)
        result2 = addToNames._check_unique(name=name, fileName=fakeFile)
        
        # Assert
        self.assertTrue(result1)
        self.assertFalse(result2)
        
    def test_check_length(self):
        addToNames = ProjectNamesList.ProjectNamesList()
        self.assertFalse( addToNames._check_length('aaaa') ) #4
        self.assertFalse( addToNames._check_length('aaaaaaaaaaaaaaaaaaaaa') ) #21
        self.assertTrue( addToNames._check_length('aaaaaaaaaaaa') ) #12
        
    @patch('ProjectNamesList.xml')
    def test_read_xml_names(self,xml_stub):
        # Arrange 
        addToNames = ProjectNamesList.ProjectNamesList()
        name = 'Asset_01'
        fakeFile = MagicMock(name='proj_names.xml')
        xmlParseStub = MagicMock(name='xmlParseStub')
        xmlNodeStub = MagicMock(name='xmlNodeStub')
      
        
        
        xmlParseStub.getElementsByTagName.return_value = [xmlNodeStub]
        xmlNodeStub.attributes['name'].value = 'Asset_01'
        xml_stub.parse.return_value = xmlParseStub

        # Act
        result = addToNames._read_xml_names( fileName=fakeFile )
        
        # Assert
        self.assertEqual(result[0],'Asset_01')
    
  
    @patch('ProjectNamesList.xml')
    def test_add_to_xml_names(self, xml_stub):
        # Arrange 
        import __builtin__
        open_mock = MagicMock( name = 'mockOpen' )
        xmlDocMock = MagicMock( name = 'xmlDocMock' )
        __builtin__.open = open_mock
        open_mock.return_value = xmlDocMock
        
        addToNames = ProjectNamesList.ProjectNamesList()
        name = 'Asset_01'
        fakeFile = MagicMock(name='proj_names.xml')
        xmlFileMock = MagicMock( name = 'xmlFileMock' )
        childNameMock = MagicMock( name = 'childNameMock' )
         
        xml_stub.parse.return_value = xmlFileMock 
        xmlFileMock.createElement.return_value = childNameMock 

        # Act
        result = addToNames._add_to_xml_names( name=name, fileName=fakeFile )
        
        # Assert
        self.assertEqual( result, True )
        self.assertTrue( call.parse(fakeFile) in xml_stub.mock_calls)
        
    @patch('ProjectNamesList.ProjectNamesList._remove_from_xml_names')
    def test_remove(self, removeFromNames_mock ):
        # Arrange
        removeFromNames = ProjectNamesList.ProjectNamesList()
        fakeFile = MagicMock(name='proj_names.xml') 
        namePass = 'Asset_01'

        # Set what to return 
        removeFromNames_mock.return_value = True

        # Act
        resultPass = removeFromNames.remove(assetName=namePass, fileName=fakeFile)

        # Assert
        self.assertTrue( call(name=namePass, fileName=fakeFile) in removeFromNames_mock.mock_calls)
        self.assertNotEqual( resultPass, None )

    
    
    @patch('ProjectNamesList.xml')
    def test_remove_from_xml_names(self, xml_stub):
        # Arrange 
        import __builtin__
        open_mock = MagicMock( name = 'mockOpen' )
        xmlDocMock = MagicMock( name = 'xmlDocMock' )
        __builtin__.open = open_mock
        open_mock.return_value = xmlDocMock
        
        removeFromNames = ProjectNamesList.ProjectNamesList()
        name = 'Asset_01'
        
        fakeFile = MagicMock(name='proj_names.xml')
        xmlFileMock = MagicMock( name = 'xmlFileMock' )
        
        parentNodeMock = MagicMock( name = 'parentNameMock' )
        childNodeMock = MagicMock( name = 'childNameMock' )
         
        xml_stub.parse.return_value = xmlFileMock 
        
        xmlFileMock.childNodes[0] = parentNodeMock
        xmlFileMock.childNodes[0].childNodes = [childNodeMock]
        childNodeMock.nodeType = 2
        childNodeMock.attributes['name'].value = name
        
        parentNodeMock.removeChild.return_value = childNodeMock 
        #xmlFileMock.createElement.return_value = childNameMock 

        # Act
        result = removeFromNames._remove_from_xml_names( name=name, fileName=fakeFile )
        
        # Assert
        self.assertTrue( call.parse(fakeFile) in xml_stub.mock_calls)
        self.assertEqual( result, True )
          