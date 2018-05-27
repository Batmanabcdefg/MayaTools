import unittest
import sys
import os

import maya.cmds as cmds
import maya.standalone as standalone
standalone.initialize(name='python')

cwd = os.path.dirname(os.path.abspath(__file__).replace('tests',''))
if cwd not in sys.path:
    sys.path.append(cwd)
import ClusterLib
reload( ClusterLib )

class test_ClusterLib(unittest.TestCase):
    def setUp(self):
        cmds.file(newFile=True,f=True)
        
        self.sphere = cmds.polySphere()
        self.loc1 = cmds.spaceLocator()[0]
        self.loc2 = cmds.spaceLocator()[0]
        self.joint = cmds.joint()        
        
    def tearDown(self):
        pass
    
    def test_clusterSingleObject(self):
        name = 'test'
        deform = self.sphere[0]
        handle = self.loc1
        follow = self.loc2
        parent = self.joint
        
        result = ClusterLib.cluster(name=name, deform=deform, 
                           handle=handle, follow=follow, parent=parent)
        
        self.assertEqual(result,['test','locator1'])
        
        cmds.move(3,3,3,self.joint)
        pos = cmds.xform(result[1],q=1,ws=1,rp=1)
        self.assertAlmostEqual(3,pos[0])
        self.assertAlmostEqual(3,pos[1])
        self.assertAlmostEqual(3,pos[2])
        
    def test_clusterList(self):
        name = 'test'
        deform = ['%s.vtx[0]'%self.sphere[0],'%s.vtx[1]'%self.sphere[0],'%s.vtx[2]'%self.sphere[0]]
        handle = self.loc1
        follow = self.loc2
        parent = self.joint
        
        result = ClusterLib.cluster(name=name, deform=deform, 
                           handle=handle, follow=follow, parent=parent)
        
        self.assertEqual(result,['test','locator1'])
        
        cmds.move(3,3,3,self.joint)
        pos = cmds.xform(result[1],q=1,ws=1,rp=1)
        self.assertAlmostEqual(3,pos[0])
        self.assertAlmostEqual(3,pos[1])
        self.assertAlmostEqual(3,pos[2])
        
    
    