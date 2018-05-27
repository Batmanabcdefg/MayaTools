import unittest
import os
import sys

import maya.cmds as cmds
import maya.mel as mel
import pymel.core as pm

#import maya.standalone as standalone
#standalone.initialize(name='python')

cwd = os.path.dirname(os.path.abspath(__file__).replace('tests', ''))
if cwd not in sys.path:
    sys.path.append(cwd)
    
packageDir = os.path.dirname(os.path.abspath(cwd).replace('RibbonRig', ''))
if packageDir not in sys.path:
    sys.path.append(packageDir)
    
from UnittestLib import UnittestLib
reload( UnittestLib )
    
import RibbonRig
reload( RibbonRig )

class test_RibbonRig(unittest.TestCase):
    def setUp(self):
        self.test = UnittestLib.UnittestLib()
        self.rig = RibbonRig.RibbonRig(log=True)
        cmds.file(newFile=True,f=True)
    
    def tearDown(self):
        pass
    
    def test_createRig(self):
        #--- Setup the scene
        startJnt = cmds.joint(n='startJnt',p=(-3, 1, 5))
        endJnt = cmds.joint(n='endJnt',p=(2, 3, 2)) 
        upObj = cmds.joint(n='upJnt',p=(-5.723, 2.384, 1.69))

        #--- Call methods, get results
        name = 'test'
        normal=[0, 0, 1]
        up=[1, 0, 0]
        aim=[0, 1, 0]
        numJnts=6
        self.rig.createRig(name=name, startObj=startJnt, endObj=endJnt, startUpObj=upObj,
                          normal=normal, up=up, aim=aim, numJnts=numJnts)       
        
        #--- Check Results
        expectedTopNode = 'test_rbbnTopNode'
        self.assertTrue(cmds.objExists(expectedTopNode))
        self.test.assertFloatListAlmostEqual(cmds.xform('test_btmLoc_up', q=1,ws=1,rp=1), (-9.04, 4.07, -2.349))
    
    def test_createPlane(self):
        #--- Setup the scene
        startJnt = cmds.joint(n='startJnt',p=(0, 0, 0))
        endJnt = cmds.joint(n='endJnt',p=(0, 5, 0))
        
        #--- Call method, get results
        result = self.rig._createPlane(name='test',
                                       start=startJnt,
                                       end=endJnt,
                                       normal=[0, 0, 1],
                                       up=[1, 0, 0],
                                       aim=[0, 1, 0],
                                       spans=6)
        
        #--- Check Results
        self.assertEqual(result,'test_rbbnPlane')
        self.assertTrue(cmds.objExists('test_rbbnPlane'))
        self.assertEqual(cmds.getAttr('%sShape.spansU'%result), 1)
        self.assertEqual(cmds.getAttr('%sShape.spansV'%result), 6)
        self.assertEqual(cmds.getAttr('%sShape.degreeU'%result), 1)
        self.assertEqual(cmds.getAttr('%sShape.degreeV'%result), 3)        
        
    def test_createLocators(self):
        #--- Setup the scene
        startJnt = cmds.joint(n='startJnt',p=(3, 0, 0))
        endJnt = cmds.joint(n='endJnt',p=(3, 5, -2))
        upObj = cmds.joint(n='upJnt',p=(4, 0, 0))
        
        #--- Call method, get result
        result = self.rig._createLocators(name='test', start=startJnt, end=endJnt, startUpObj=upObj)
        
        #--- Check Results
        startPos = cmds.xform(startJnt, q=1, ws=1, rp=1)
        endPos = cmds.xform(endJnt, q=1, ws=1, rp=1)
        avgPos = [ (endPos[0]+startPos[0])/2.0, (endPos[1]+startPos[1])/2.0, (endPos[2]+startPos[2])/2.0 ]
        
        for locGrp in result.keys():
            if 'topLocs' in locGrp:
                try:
                    for loc in result[locGrp]:
                        locPos = cmds.xform(loc[0], q=1, ws=1, rp=1)
                        if loc[0].endswith('_up'):
                            self.test.assertFloatListAlmostEqual(l1=[ endPos[0]+10, endPos[1], endPos[2] ], l2=locPos)
                            continue
                        self.test.assertFloatListAlmostEqual(l1=endPos, l2=locPos)
                except AssertionError,e:
                    print 'loc: ', loc
                    print 'endPos: ', endPos
                    print 'locPos: ', locPos
                    raise AssertionError(e)
                    
            if 'mid' in locGrp:
                try:
                    for loc in result[locGrp]:
                        locPos = cmds.xform(loc[0], q=1, ws=1, rp=1)
                        if loc[0].endswith('_up'):                           
                            self.test.assertFloatListAlmostEqual(l1=[ avgPos[0]+10, avgPos[1], avgPos[2] ], l2=locPos)
                        else:                           
                            self.test.assertFloatListAlmostEqual(l1=avgPos, l2=locPos)
                except AssertionError,e:
                    print 'loc: ', loc
                    print 'avgPos: ', avgPos
                    print 'locPos: ', locPos                    
                    raise AssertionError(e)
                
            if 'btm' in locGrp:
                try:
                    for loc in result[locGrp]:
                        locPos = cmds.xform(loc[0], q=1, ws=1, rp=1)
                        if loc[0].endswith('_up'):
                            self.test.assertFloatListAlmostEqual(l1=[ startPos[0]+10, startPos[1], startPos[2] ], l2=locPos)
                            continue
                        self.test.assertFloatListAlmostEqual(l1=startPos, l2=locPos)
                except AssertionError,e:
                    print 'loc: ', loc
                    print 'startPos: ', startPos
                    print 'locPos: ', locPos    
                    raise AssertionError(e)
    
    def test_createFollicles(self):
        #--- Setup the scene
        plane = cmds.nurbsPlane( w=1, lengthRatio=5, d=3, u=1, v=6, ax=[0, 0, 1])[0]
        
        #--- Call method, get results
        result = self.rig._createFollicles(name='test', plane=plane, num=6)
        
        #--- Check Results
        expected = ['test_'+(plane+'ShapeFollicle_')+str(x+1).zfill(2) for x in range(6)]
        self.test.assertListEqual(l1=result, l2=expected)
        
        for each in result:
            self.assertTrue(cmds.objExists(each))
            transform = cmds.listRelatives(each,parent=True)[0]
            self.assertEqual(cmds.listRelatives(transform,parent=True)[0], 'test_rbbnFollicles_grp')
            self.assertFalse(cmds.listRelatives(each,c=True))
        
    
    def test_constrainLocators(self):
        #--- Setup the scene
        startJnt = cmds.joint(n='startJnt',p=(3, 0, 0))
        endJnt = cmds.joint(n='endJnt',p=(3, 5, -2))
        upObj = cmds.joint(n='upJnt',p=(4, 0, 0))
        
        #--- Create the locators... tsk, tsk, external dependency, but why repo so much code here!?
        result = self.rig._createLocators(name='test', start=startJnt, end=endJnt, startUpObj=upObj)
        
        #--- Call method, get results
        result = self.rig._constrainLocators(locators=result)
        
        #--- Check Results
        self.test.assertConstrained('test_btmLoc_pos','test_topLoc_aim',type='aim')
        self.test.assertConstrained('test_topLoc_pos','test_btmLoc_aim',type='aim')
        self.test.assertConstrained('test_topLoc_pos','test_midLoc_aim',type='aim')
        
        self.test.assertConstrained('test_topLoc_pos','test_midLoc_pos',type='point')      
        self.test.assertConstrained('test_btmLoc_pos','test_midLoc_pos',type='point')       
        
        self.test.assertConstrained('test_topLoc_up','test_midLoc_up',type='point')       
        self.test.assertConstrained('test_btmLoc_up','test_midLoc_up',type='point')
        
        btmPos = cmds.xform('test_btmLoc_up', q=1,ws=1, rp=1)
        self.test.assertFloatListAlmostEqual(btmPos,[13,0,0])
        
        # Twist the top
        cmds.rotate(0,45,0,'test_topLoc_pos')
        topPos = cmds.xform('test_topLoc_up', q=1,ws=1, rp=1)
        midPos = cmds.xform('test_midLoc_up', q=1,ws=1, rp=1)
        avgPos = [(topPos[0]+btmPos[0])/2.0, (topPos[1]+btmPos[1])/2.0, (topPos[2]+btmPos[2])/2.0]
        self.test.assertListEqual(avgPos, midPos)
        
    def test_createBindJoints(self):
        #--- Setup the scene
        plane = cmds.nurbsPlane( w=1, lengthRatio=5, d=3, u=1, v=6, ax=[0, 0, 1])[0]
        follicles = self.rig._createFollicles(name='test', plane=plane, num=6)
        
        #--- Call method, get results
        result = self.rig._createBindJoints(name='test', parents=follicles)
        
        #--- Check Results
        joints = ['test_'+str(x+1).zfill(2)+'_jnt_deform' for x in range(6)]
        self.test.assertListEqual(result, joints)
        for j in result:
            self.assertTrue(cmds.objExists(j))

    def test_createPlaneJoints(self):
        #--- Setup the scene
        locs = []
        locs.append(cmds.spaceLocator(p=(0, 0, 1))[0])
        locs.append(cmds.spaceLocator(p=(1, 2, 2))[0])
        locs.append(cmds.spaceLocator(p=(2, 4, 3))[0])
        
        #--- Call method, get results
        result = self.rig._createPlaneJoints(locs=locs)
        
        #--- Check Results
        joints = [x+'_rbbn_jnt' for x in locs]
        self.test.assertListEqual(result, joints)
        self.test.assertListEqual(cmds.xform(result[0],q=1,ws=1,rp=1), cmds.xform(locs[0],q=1,ws=1,rp=1))
        self.test.assertListEqual(cmds.xform(result[1],q=1,ws=1,rp=1), cmds.xform(locs[1],q=1,ws=1,rp=1))
        self.test.assertListEqual(cmds.xform(result[2],q=1,ws=1,rp=1), cmds.xform(locs[2],q=1,ws=1,rp=1))
    
    def test_skinPlane(self):    
        #--- Setup the scene
        plane = cmds.nurbsPlane( w=1, lengthRatio=5, d=3, u=1, v=6, ax=[0, 0, 1])[0]
        joints = []
        joints.append(cmds.joint(p=(0, 0, 0)))
        joints.append(cmds.joint(p=(0, 2.5, 0)))
        joints.append(cmds.joint(p=(0, 5, 0)))        

        #--- Call method, get results
        result = self.rig._skinPlane(plane=plane, joints=joints)
        
        #--- Check Results        
        sc = mel.eval('findRelatedSkinCluster("%s");'%plane)
        self.assertEqual(sc,'skinCluster1')

    def test_setupHeirarchy(self):
        #--- Setup the scene
        startJnt = cmds.joint(n='startJnt',p=(3, 0, 0))
        endJnt = cmds.joint(n='endJnt',p=(3, 5, -2))        
        locs = []
        locs.append(cmds.spaceLocator(n='test_topLoc_pos', p=(0, 0, 1))[0])
        locs.append(cmds.spaceLocator(n='test_midLoc_pos',p=(1, 2, 2))[0])
        locs.append(cmds.spaceLocator(n='test_btmLoc_pos',p=(2, 4, 3))[0])
        
        locGrp = cmds.group(em=True)
        fGrp = cmds.group(em=True)
        plane = cmds.nurbsPlane( w=1, lengthRatio=5, d=3, u=1, v=6, ax=[0, 0, 1])[0]
        
        for each in locs:
            cmds.parent(each,locGrp)
        
        #--- Call method, get results
        result = self.rig._setupHeirarchy(name='test', startObj=startJnt, endObj=endJnt, 
                                          locGrp=locGrp, plane=plane, follicleGrp=fGrp)
        
        #--- Check Results
        expectedTopNode = 'test_rbbnTopNode'
        self.assertEqual(result, expectedTopNode)
        self.assertTrue(cmds.objExists(expectedTopNode))
        self.assertEqual(cmds.listRelatives(fGrp,parent=True)[0], expectedTopNode) 
        self.assertEqual(cmds.listRelatives(plane,parent=True)[0], expectedTopNode) 
        self.test.assertConstrained(startJnt,locs[2],type='parent')
        self.test.assertConstrained(endJnt,locs[0],type='parent')
    
    def test_angleBetween(self):
        v1 = [0,1,0]
        v2 = [1,0,0]
        angle = self.rig._angleBetween(v1,v2)
        self.assertAlmostEqual(90.0,angle,places=2)
        
        v1 = [0,1,0]
        v2 = [.5,.5,0]
        angle = self.rig._angleBetween(v1,v2)
        self.assertAlmostEqual(45.0,angle,places=2)   
        
    def test_zeroNode(self):
        node = pm.group()
        node.t.set(2,4,6)
        node.r.set(34,46,74)
        node.s.set(3,5,4)
        
        self.rig._zeroNode(node)
        
        self.test.assertFloatListAlmostEqual(node.t.get(),[0,0,0])
        self.test.assertFloatListAlmostEqual(node.r.get(),[0,0,0])
        self.test.assertFloatListAlmostEqual(node.s.get(),[0,0,0])
        
    def test_lockAndHide(self):
        node = pm.group()
        node.t.set(2,4,6)
        node.r.set(34,46,74)
        node.s.set(3,5,4)
        
        self.rig._lockAndHide(node)
        
        self.assertTrue( node.attr('tx').isLocked() )
        self.assertTrue( node.attr('ty').isLocked() )
        self.assertTrue( node.attr('tz').isLocked() )
        
        self.assertTrue( node.attr('rx').isLocked() )
        self.assertTrue( node.attr('ry').isLocked() )
        self.assertTrue( node.attr('rz').isLocked() )
        
        self.assertTrue( node.attr('sx').isLocked() )
        self.assertTrue( node.attr('sy').isLocked() )
        self.assertTrue( node.attr('tz').isLocked() )