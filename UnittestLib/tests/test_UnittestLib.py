import unittest
import os
import sys

import maya.cmds as cmds
import maya.standalone as standalone
standalone.initialize(name='python')

cwd = os.path.dirname(os.path.abspath(__file__).replace('tests', ''))
if cwd not in sys.path:
    sys.path.append(cwd)
import UnittestLib
reload( UnittestLib )

class test_UnittestLib(unittest.TestCase):
    def setUp(self):
        self.lib = UnittestLib.UnittestLib(log=True)
        cmds.file(newFile=True,f=True)
    
    def test_assertListEqual(self):
        listA = ['a','b','c','d']
        listB = ['a','b','c','d']
        listC = ['f','f','f','f']
        listD = ['a','b']
        
        self.assertTrue(self.lib.assertListEqual(listA, listB))
        
        try:
            self.lib.assertListEqual(listA, listC)
        except AssertionError:
            pass
        
        try:
            self.lib.assertListEqual(listA, listD)
        except AssertionError:
            pass   
        
    def test_assertFloatListAlmostEqual(self):
        listA = [1.1,1.1,1.1,1.1]
        listB = [1.11,1.09,1.11,1.09]
        listC = [1.12,1.08,1.12,1.08]
        listD = [3,1.73452]
        
        self.assertTrue(self.lib.assertFloatListAlmostEqual(listA, listB))
        
        try:
            self.lib.assertFloatListAlmostEqual(listA, listC)
        except AssertionError:
            pass
        
        try:
            self.lib.assertFloatListAlmostEqual(listA, listD)
        except AssertionError:
            pass 
    
    def test_assertConstrained(self):
        a = cmds.polySphere()[0]
        b = cmds.polySphere()[0]
        
        temp = cmds.parentConstraint(a,b)
        self.assertTrue( self.lib.assertConstrained(a, b, type='parent') )
        cmds.delete(temp)
        
        temp = cmds.aimConstraint(a,b)
        self.assertTrue( self.lib.assertConstrained(a, b, type='aim') )
        cmds.delete(temp)        
        
        temp = cmds.pointConstraint(a,b)
        self.assertTrue( self.lib.assertConstrained(a, b, type='point') )
        cmds.delete(temp)  
        
        temp = cmds.orientConstraint(a,b)
        self.assertTrue( self.lib.assertConstrained(a,b,type='orient') )
        cmds.delete(temp)      
        
        temp = cmds.scaleConstraint(a,b)
        self.assertTrue( self.lib.assertConstrained(a,b,type='scale') )
        cmds.delete(temp)    
        
        temp = cmds.geometryConstraint(a,b)
        self.assertTrue( self.lib.assertConstrained(a,b,type='geometry') )
        cmds.delete(temp)       
        
        try:
            self.lib.assertConstrained(a,b,type='parent')
        except AssertionError:
            pass
        