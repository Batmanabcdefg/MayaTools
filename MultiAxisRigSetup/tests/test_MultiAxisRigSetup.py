import unittest
import os
import sys

import maya.cmds as cmds
import maya.standalone as standalone
standalone.initialize(name='python')

cwd = os.path.dirname(os.path.abspath(__file__).replace('tests',''))
if cwd not in sys.path:
    sys.path.append(cwd)
import MultiAxisRigSetup
reload( MultiAxisRigSetup )

class test_MultiAxisRigSetup(unittest.TestCase):
    def setUp(self):
        self.rig = MultiAxisRigSetup.MultiAxisRigSetup(log=True)
        
    def tearDown(self):
        # Close without saving to reset the test scene
        cmds.file(newFile=True,f=True)
    
    def test_createRig(self):
        scene = cwd+os.sep+'tests/scenes/test_createRig.ma'
        cmds.file(scene,o=True,f=True)
        
        self.rig.createRig(name='test',
                        baseTransform='joint2',
                        targetTransform='joint3',
                        control='control',
                        aim='y',up='z',wup='y')
        
        self.assertTrue(cmds.objExists('test_multiAxisRigGrp'))
        self.assertTrue(cmds.objExists('test_multiAxisRigGrpParentConst'))
        self.assertTrue(cmds.objExists('test_multiAxisRigPlane'))
        self.assertTrue(cmds.objExists('test_multiAxisRigPlanePointConst'))
        self.assertTrue(cmds.objExists('test_multiAxisRigLoc'))
        self.assertTrue(cmds.objExists('test_multiAxisRigCPOS'))
        self.assertTrue(cmds.objExists('test_multiAxisRigLocGeoConst'))
        self.assertTrue(cmds.objExists('test_multiAxisRigLocPointConst'))        
        self.assertTrue(cmds.objExists('control.test_u'))
        self.assertTrue(cmds.objExists('control.test_v'))
        
        self.assertEqual(cmds.getAttr('control.test_u'),.5)
        self.assertEqual(cmds.getAttr('control.test_v'),.5) 
        cmds.rotate(0,90,0,'joint2',a=True)
        self.assertEqual(cmds.getAttr('control.test_u'),0)
        cmds.rotate(0,0,90,'joint2',a=True)
        self.assertEqual(cmds.getAttr('control.test_v'),0)   
        cmds.rotate(0,-90,0,'joint2',a=True)
        self.assertEqual(cmds.getAttr('control.test_u'),1)
        cmds.rotate(0,0,-90,'joint2',a=True)
        self.assertEqual(cmds.getAttr('control.test_v'),1)    
        
    def test_createPlane(self):
        scene = cwd+os.sep+'tests/scenes/test_createPlane.ma'
        cmds.file(scene,o=True,f=True)
        
        result = self.rig._createPlane(name='test',
                                baseTransform='joint2',
                                targetTransform='joint3',
                                aim='y',up='z',wup='y')
        
        self.assertTrue(cmds.objExists('test_multiAxisRigPlanePointConst'))
        self.assertEqual(result,'test_multiAxisRigPlane')
        self.assertTrue(cmds.objExists('test_multiAxisRigPlane'))
        self.assertEqual(cmds.xform('joint2',q=1,ws=1,rp=1),
                         cmds.xform('test_multiAxisRigPlane',q=1,ws=1,rp=1))
        self.assertTrue(cmds.getAttr('test_multiAxisRigPlane.scaleX'),4)
        self.assertTrue(cmds.getAttr('test_multiAxisRigPlane.scaleY'),4)
        self.assertTrue(cmds.getAttr('test_multiAxisRigPlane.scaleZ'),4)
        self.assertTrue(cmds.getAttr('test_multiAxisRigPlane.rotateX'),-90)
        self.assertTrue(cmds.getAttr('test_multiAxisRigPlane.rotateY'),-90)      

    def test_createLoc(self):
        scene = cwd+os.sep+'tests/scenes/test_createLoc.ma'
        cmds.file(scene,o=True,f=True)
        
        result = self.rig._createLoc(name='test',
                                        baseTransform='joint2',
                                        targetTransform='joint3',
                                        plane='test_multiAxisRigPlane')
        
        self.assertEqual(result,'test_multiAxisRigLoc')
        self.assertTrue(cmds.objExists('test_multiAxisRigLoc'))
        expectedPos = cmds.xform('joint2',q=1,ws=1,rp=1)
        resultPos = cmds.xform('test_multiAxisRigLoc',q=1,ws=1,rp=1)
        self.assertAlmostEqual(expectedPos[0],resultPos[0]) 
        self.assertAlmostEqual(expectedPos[1],resultPos[1]) 
        self.assertAlmostEqual(expectedPos[2],resultPos[2]) 
        self.assertTrue(cmds.objExists('test_multiAxisRigLocGeoConst'))
        self.assertTrue(cmds.objExists('test_multiAxisRigLocPointConst'))
        
    
    def test_setupCPOS(self):
        scene = cwd+os.sep+'tests/scenes/test_setupCPOS.ma'
        cmds.file(scene,o=True,f=True)

        result = self.rig._setupCPOS(name='test',plane='test_multiAxisRigPlane',
                                    loc='test_multiAxisRigLoc')
        
        self.assertEqual(result,'test_multiAxisRigCPOS')
        self.assertTrue(cmds.objExists('test_multiAxisRigCPOS'))
        self.assertEqual(cmds.listConnections('test_multiAxisRigCPOS.inputSurface')[0],
                        'test_multiAxisRigPlane')
        self.assertEqual(cmds.listConnections('test_multiAxisRigCPOS.inPosition')[0],
                        'test_multiAxisRigLoc')      
        
    def test_setupRigHeirarchy(self):
        scene = cwd+os.sep+'tests/scenes/test_setupRigHeirarchy.ma'
        cmds.file(scene,o=True,f=True)
        
        result = self.rig._setupRigHeirarchy(name='test',
                                             baseTransform='joint2',
                                             plane='test_multiAxisRigPlane',
                                             loc='test_multiAxisRigLoc')
        
        self.assertEqual(result,'test_multiAxisRigGrp')
        self.assertTrue(cmds.objExists('test_multiAxisRigGrp'))
        self.assertTrue(cmds.objExists('test_multiAxisRigGrpParentConst'))
        self.assertTrue(cmds.listRelatives('test_multiAxisRigPlane',parent=True)[0],
                        'test_multiAxisRigGrp')
        self.assertTrue(cmds.listRelatives('test_multiAxisRigLoc',parent=True)[0],
                        'test_multiAxisRigGrp')        
    
    def test_createAttrs(self):
        scene = cwd+os.sep+'tests/scenes/test_createAttrs.ma'
        cmds.file(scene,o=True,f=True)
        
        self.rig._createAttrs(name='test', control='control', node='test_multiAxisRigCPOS')
        
        self.assertTrue(cmds.objExists('control.test_u'))
        self.assertTrue(cmds.objExists('control.test_v'))
        self.assertEqual(cmds.listConnections('control.test_u')[0],
                        'test_multiAxisRigCPOS')
        self.assertEqual(cmds.listConnections('control.test_v')[0],
                        'test_multiAxisRigCPOS')    
        
        
        
        
    