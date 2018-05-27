import unittest
import os
import sys
import platform

from mock import MagicMock, patch, call

if platform.system() == 'Darwin':
    modDir = os.path.dirname(os.path.abspath(__file__).replace('tests/api/asset/test_SetData.py', 'api/asset/'))
elif platform.system() == 'Windows':
    modDir = os.path.dirname(os.path.abspath(__file__).replace('tests\\api\\asset\\test_SetData.py', 'api\\asset\\'))
if modDir not in sys.path:
    sys.path.insert(0,modDir)

import SetData
reload( SetData )

class test_SetData(unittest.TestCase):
    
    @patch('SetData.os.path.exists')
    def test_check_metaFile_exists(self,os_mock):
        #------------------------ Arrange 
        path = '/temp/poo'
        os_mock.return_value = True
        
        # Act        
        inst = SetData.SetData()
        result = inst._check_metaFile_exists(filePath=path)
        
        # Assert
        self.assertEqual( result, True )
        self.assertTrue(call(path) in os_mock.mock_calls)
    
    @patch('SetData.SetData._set_value_to_xml')
    @patch('SetData.SetData._check_existing_value')
    @patch('tmxml.tmxml.tmXml')
    @patch('SetData.SetData._check_metaFile_exists')
    def test_setValue_1(self,
                      cmfe_stub, 
                      xml_stub,
                      check_value_stub,
                      set_value_stub):
        # Arrange
        userName = 'msantos'
        typ = 'assignee'
        value = 'msantos'
        path = '/blah/temp.xml'
        
        fake_xml = MagicMock( name = 'xmlFile' )
        fake_xml.getElementsByTagName.return_value = ['']
        xml_stub.readXml.return_value = fake_xml 
        xml_stub.getTagValue.return_value = 'msantos'
        cmfe_stub.return_value = True
        check_value_stub.return_value = True
        set_value_stub.return_value = True
        
        # Act
        inst = SetData.SetData()
        result = inst.setValue(typ=typ, value=value, filePath=path, userName=userName)
        
        # Assert
        self.assertEqual(result, 'Added assignee:msantos to meta file')
        self.assertTrue(call('assignee', 'msantos', '/blah/temp.xml') in set_value_stub.mock_calls) 
        self.assertTrue(call().readXml('/blah/temp.xml') in xml_stub.mock_calls)
        self.assertTrue(call().readXml().getElementsByTagName('assignee') in xml_stub.mock_calls)      
        
    @patch('SetData.SetData._set_value_to_xml')
    @patch('SetData.SetData._check_existing_value')
    @patch('tmxml.tmxml.tmXml')
    @patch('SetData.SetData._check_metaFile_exists')
    def test_setValue_2(self,
                      cmfe_stub,
                      xml_mock,
                      check_value_stub,
                      set_value_mock):
        # Arrange
        userName = 'msantos'
        typ = 'status'
        value = 'ip'
        path = '/blah/temp.xml'
        
        fake_xml = MagicMock( name = 'xmlFile' )
        fake_xml.getElementsByTagName.return_value = ['']
        xml_mock.readXml.return_value = fake_xml 
        xml_mock.getTagValue.return_value = 'msantos'
        cmfe_stub.return_value = True
        check_value_stub.return_value = True
        set_value_mock.return_value = True
        
        # Act
        inst = SetData.SetData()
        result = inst.setValue(typ=typ, value=value, filePath=path, userName=userName)
        
        # Assert
        self.assertEqual(result, 'Added status:ip to meta file')
        self.assertTrue(call('status', 'ip', '/blah/temp.xml') in set_value_mock.mock_calls) 
        self.assertTrue(call().readXml('/blah/temp.xml') in xml_mock.mock_calls)
        self.assertTrue(call().readXml().getElementsByTagName('status') in xml_mock.mock_calls)    
        
        
    @patch('tmxml.tmxml.tmXml')
    def test_set_value_to_xml(self, xml_mock):
        # Arrange
        typ = 'assignee'
        value = 'msantos'
        path = '/blah/temp.xml'
        
        fakeXmlFile = MagicMock(name='fakeXmlfile')
        fakeXmlFile.toxml.return_value = 'Front<assignee></assignee>Back'
        xml_mock().readXml.return_value = fakeXmlFile
        
        # Act
        inst = SetData.SetData()
        result = inst._set_value_to_xml(typ=typ, value=value, filePath=path)  
        
        # Assert
        self.assertTrue(result)
        self.assertTrue(call().saveXml( path, 'Front<assignee>msantos</assignee>Back' ) in xml_mock.mock_calls)
        self.assertTrue(call().readXml( path ) in xml_mock.mock_calls )
     
    @patch('tmxml.tmxml.tmXml') 
    @patch('datetime.datetime')    
    def test_add_note_to_xml(self, dt_stub, xml_mock):
        # Arrange
        value = 'This is a note!'
        path = '/blah/temp.xml'
        userName = 'msantos'

        dt_now_stub = MagicMock(name='dt_now_stub')
        dt_now_stub.day = 9
        dt_now_stub.month = 9
        dt_now_stub.year = 9
        
        fakeXmlFile = MagicMock(name='fakeXmlFile')
        
        xml_mock().readXml.return_value = fakeXmlFile
        dt_stub.now.return_value = dt_now_stub
        
        # Act
        inst = SetData.SetData()
        result = inst._add_note_to_xml(value=value, filePath=path, userName=userName)  
        
        # Assert
        self.assertTrue(result) 
        self.assertTrue(call().readXml(path) in xml_mock.mock_calls)
        self.assertTrue(call().saveXml(path,fakeXmlFile) in xml_mock.mock_calls)
        
    def test_check_existing_value(self):
        currentValue = 'msantos'
        value = 'jcalduch'

        inst = SetData.SetData()
        result = inst._check_existing_value(value=value, currentValue=currentValue)  
        
        self.assertTrue(result)
        
        #----
        currentValue = 'msantos'
        value = 'msantos'

        inst = SetData.SetData()
        result = inst._check_existing_value(value=value, currentValue=currentValue)  
        
        self.assertFalse(result)        
        
        
    
