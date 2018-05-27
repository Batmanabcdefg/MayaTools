import unittest
import os
import sys
import platform

from mock import MagicMock, patch, call

if platform.system() == 'Darwin':
    modDir = os.path.dirname(os.path.abspath(__file__).replace('tests/api/asset/test_GetData.py', 'api/asset/'))
elif platform.system() == 'Windows':
    modDir = os.path.dirname(os.path.abspath(__file__).replace('tests\\api\\asset\\test_GetData.py', 'api\\asset\\'))
if modDir not in sys.path:
    sys.path.insert(0,modDir)

import GetData
reload( GetData )

class test_GetData(unittest.TestCase):
    
    @patch('GetData.GetData.getValue')
    def test_allData(self, getValue_stub):
        # Arrange
        xmlFile = '/path/concept_info.xml'
        expected = {'notes':{},
         'status':'ip',
         'assignee':'msantos',
         'lastExported':'3'}
        getValue_stub.side_effect = [{},'ip','msantos','3']
        
        # Act
        inst = GetData.GetData()
        result = inst.allData(xmlFile=xmlFile)
        
        # Assert
        self.assertEqual(result, expected)
    
    @patch('GetData.os.path.exists')
    def test_check_metaFile_exists(self,os_mock):
        #------------------------ Arrange 
        path = '/temp/poo'
        os_mock.return_value = True
        
        # Act        
        inst = GetData.GetData()
        result = inst._check_metaFile_exists(filePath=path)
        
        # Assert
        self.assertEqual( result, True )
        self.assertTrue(call(path) in os_mock.mock_calls)
    
    @patch('tmxml.tmxml.tmXml')
    @patch('GetData.GetData._check_metaFile_exists')
    def test_getValue(self,
                      cmfe_stub, 
                      xml_stub):
        # Arrange
        typ = 'assignee'
        path = '/blah/temp.xml'
        returnValue = 'value'
        
        fake_xml = MagicMock( name = 'xmlFile' )
        fake_xml.getElementsByTagName.return_value = ['']
        xml_stub.readXml.return_value = fake_xml 
        xml_stub().getTagValue.return_value = returnValue
        cmfe_stub.return_value = True
        
        # Act
        inst = GetData.GetData()
        result = inst.getValue( typ=typ, filePath=path )
        
        # Assert
        self.assertEqual(result, 'value')    
    
    @patch('tmxml.tmxml.tmXml')
    def test_get_notes_from_xml(self, xml_stub):
        # Arrange
        notes = [{'dateCreated':'test',
                 'createdBy':'test',
                 'note':'Some note.'}]
        xmlFake = MagicMock(name='xmlFake')
        nodeFake = MagicMock(name='nodeFake')
        nodeFake.attributes['dateCreated'].value = 'test'
        xmlFake.getElementsByTagName.return_value = [nodeFake]
        xml_stub().getTagValue.return_value = 'Some note.'
        
        # Act
        inst = GetData.GetData()
        result = inst._get_notes_from_xml( xmlFile=xmlFake )
        
        # Assert
        self.assertListEqual(result, notes)
