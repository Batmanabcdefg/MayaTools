import unittest
import os

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om

import maya.standalone
maya.standalone.initialize(name='python')

import spaceSwitching
reload(spaceSwitching)

class test_spaceSwitching(unittest.TestCase):
    def setUp(self):
        cmds.file(newFile=True,f=True)
        
    def tearDown(self):
        pass
        
    def test_setupSpaces(self):
	name = 'Test'
        cube = cmds.polyCube()[0]
        loc = cmds.spaceLocator()[0]
	standardLoc = cmds.spaceLocator()[0]
        
        # Connect loc to cube
        spaceNode = spaceSwitching.setupSpaces(name=name,parent=cube,child=loc)
	cmds.parentConstraint(cube,standardLoc,mo=True)
        
        # Move/Rotate cube
        cmds.move(3,3,3,'%s.translate'%cube)
        cmds.rotate(45,45,45,'%s.rotate'%cube)
        
        # Assert that loc followed along exactlly
        self.assertEqual(cmds.getAttr('%s.translate'%cube),cmds.getAttr('%s.translate'%loc))
        self.assertEqual(cmds.getAttr('%s.rotate'%cube),cmds.getAttr('%s.rotate'%loc)) 
        
        # Assert connections
	self.assertTrue(cmds.isConnected('%s.message'%cube, '%s.parentNode'%spaceNode))
	self.assertTrue(cmds.isConnected('%s.message'%loc, '%s.childNode'%spaceNode))
	self.assertTrue(cmds.isConnected('%s_multMatrix.message'%name, '%s.multMatrixNode'%spaceNode))
	self.assertTrue(cmds.isConnected('%s_rpPointMatrixMult.message'%name, '%s.rpPointMatrixMult'%spaceNode))
	self.assertTrue(cmds.isConnected('%s_decomposeMatrix.message'%name, '%s.decompNode'%spaceNode))
	self.assertTrue(cmds.isConnected('%s_offsetMatrix.message'%name, '%s.offsetMatrixNode'%spaceNode))
	
	# Assert rotatePivot and scalePivot match parent
	childRp = cmds.xform(loc,q=True,ws=True,rp=True)
	childSp = cmds.xform(loc,q=True,ws=True,sp=True)
	parentRp = cmds.xform(cube,q=True,ws=True,rp=True)
	parentSp = cmds.xform(cube,q=True,ws=True,sp=True)
	self.assertEquals(childRp,parentRp)
	self.assertEquals(childSp,parentSp)

    def test_createSpaceNode(self):
        spaceNode = spaceSwitching._createSpaceNode(name='Test')
        
        # Assert that switch node exists
        self.assertTrue(cmds.objExists(spaceNode))
	
	# Assert attributes exist
	self.assertTrue(cmds.attributeQuery( 'parentNode', node=spaceNode, ex=True ))
        self.assertTrue(cmds.attributeQuery( 'childNode', node=spaceNode, ex=True ))
	self.assertTrue(cmds.attributeQuery( 'multMatrixNode', node=spaceNode, ex=True ))
	self.assertTrue(cmds.attributeQuery( 'rpPointMatrixMult', node=spaceNode, ex=True ))
	self.assertTrue(cmds.attributeQuery( 'decompNode', node=spaceNode, ex=True ))
	self.assertTrue(cmds.attributeQuery( 'offsetMatrixNode', node=spaceNode, ex=True ))
	
    def test_getOffsetMatrix(self):
	obj1 = cmds.polyCube()[0]
	obj2 = cmds.polySphere()[0]
	
	cmds.move(1,1,1,obj1)
	
	result = om.MMatrix()
	result = spaceSwitching._getOffsetMatrix(obj1,obj2)
	
	expectedVals = [1.0,0,0,0,  0,1.0,0,0,  0,0,1.0,0,  -1,-1,-1,1.0]
	expected = om.MMatrix()
	om.MScriptUtil.createMatrixFromList( expectedVals, expected)  
	
	self.assertEquals(result,expected)
	
    def test_spaceSwitch(self):
        name = 'Test'
        cube = cmds.polyCube()[0]
	sphere = cmds.polySphere()[0]
        loc = cmds.spaceLocator()[0]
        
        # Connect loc to cube
        spaceNode = spaceSwitching.setupSpaces(name=name,parent=cube,child=loc)
	
	# Move parent and ensure child follows
	cmds.move(343,35.45,164,cube,a=True)
	self.assertEquals(cmds.getAttr('%s.translateX'%loc),cmds.getAttr('%s.translateX'%cube))
	self.assertEquals(cmds.getAttr('%s.translateY'%loc),cmds.getAttr('%s.translateY'%cube))
	self.assertEquals(cmds.getAttr('%s.translateZ'%loc),cmds.getAttr('%s.translateZ'%cube))
	
	# Assert rotatePivot and scalePivot match parent after rotation
	cmds.rotate(453,-762,173,cube)
	childRp = cmds.xform(loc,q=True,ws=True,rp=True)
	childSp = cmds.xform(loc,q=True,ws=True,sp=True)
	parentRp = cmds.xform(cube,q=True,ws=True,rp=True)
	parentSp = cmds.xform(cube,q=True,ws=True,sp=True)
	self.assertAlmostEqual(childRp[0],parentRp[0])
	self.assertAlmostEqual(childRp[1],parentRp[1])
	self.assertAlmostEqual(childRp[2],parentRp[2])
	self.assertAlmostEqual(childSp[0],parentSp[0])	
	self.assertAlmostEqual(childSp[1],parentSp[1])
	self.assertAlmostEqual(childSp[2],parentSp[2])	
	
	# Switch space
	spaceSwitching.spaceSwitch(spaceNode, sphere)
	
	# Move new parent and ensure child follows with offet from last translation
	cmds.move(10,16.2,3.54,sphere,a=True)
	self.assertEquals(cmds.getAttr('%s.translateX'%loc),cmds.getAttr('%s.translateX'%sphere)+343)
	self.assertEquals(cmds.getAttr('%s.translateY'%loc),cmds.getAttr('%s.translateY'%sphere)+35.45)
	self.assertEquals(cmds.getAttr('%s.translateZ'%loc),cmds.getAttr('%s.translateZ'%sphere)+164)

	# Assert rotatePivot and scalePivot match parent after rotation
	#cmds.rotate(389,-432,564,sphere)
	childRp = cmds.xform(loc,q=True,ws=True,rp=True)
	childSp = cmds.xform(loc,q=True,ws=True,sp=True)
	parentRp = cmds.xform(sphere,q=True,ws=True,rp=True)
	parentSp = cmds.xform(sphere,q=True,ws=True,sp=True)
	self.assertAlmostEqual(childRp[0],parentRp[0])
	self.assertAlmostEqual(childRp[1],parentRp[1])
	self.assertAlmostEqual(childRp[2],parentRp[2])
	self.assertAlmostEqual(childSp[0],parentSp[0])	
	self.assertAlmostEqual(childSp[1],parentSp[1])
	self.assertAlmostEqual(childSp[2],parentSp[2])
	
	# Assert parentNode attr points to new parent, sphere
	self.assertTrue(cmds.isConnected('%s.message'%sphere, '%s.parentNode'%spaceNode))
    
    def test_matrix_read_4x4Node(self):
        mNode = cmds.createNode('fourByFourMatrix')
        for r in range(4):
            for c in range(4):
                cmds.setAttr('%s.in%s%s'%(mNode,r,c),3)
        
        resultM = spaceSwitching.matrix_read_4x4Node(mNode)
        
        for r in range(4):
            for c in range(4):
                self.assertEqual( resultM(r,c), (cmds.getAttr('%s.in%s%s'%(mNode,r,c))) ) 
            
    def test_matrix_write_4x4Node(self):
        matrixNode = cmds.createNode('fourByFourMatrix')
        m1 = om.MMatrix()
        for r in range(4):
            for c in range(4):
                om.MScriptUtil.setDoubleArray(m1[r], c, 5 )
        
        spaceSwitching.matrix_write_4x4Node( matrixNode, m1 )
    
        for r in range(4):
            for c in range(4):
                self.assertEqual( m1(r,c), (cmds.getAttr('%s.in%s%s'%(matrixNode,r,c))) )       
                
    def test_matrix_translate_4x4Node(self):
        mNode = cmds.createNode('fourByFourMatrix')
        vec = om.MVector(3,3,3)
        
        orig_mNodeValuesX = cmds.getAttr('%s.in30'%mNode)
        orig_mNodeValuesY = cmds.getAttr('%s.in31'%mNode)
        orig_mNodeValuesZ = cmds.getAttr('%s.in32'%mNode)        
        spaceSwitching.matrix_translate_4x4Node(mNode, vec, mode='add')
        mNodeValuesX = cmds.getAttr('%s.in30'%mNode)
        mNodeValuesY = cmds.getAttr('%s.in31'%mNode)
        mNodeValuesZ = cmds.getAttr('%s.in32'%mNode)
        self.assertEqual(mNodeValuesX, (orig_mNodeValuesX+vec[0]))
        self.assertEqual(mNodeValuesY, (orig_mNodeValuesX+vec[1]))
        self.assertEqual(mNodeValuesZ, (orig_mNodeValuesX+vec[2]))
        
        orig_mNodeValuesX = cmds.getAttr('%s.in30'%mNode)
        orig_mNodeValuesY = cmds.getAttr('%s.in31'%mNode)
        orig_mNodeValuesZ = cmds.getAttr('%s.in32'%mNode)         
        spaceSwitching.matrix_translate_4x4Node(mNode, vec, mode='subtract')
        mNodeValuesX = cmds.getAttr('%s.in30'%mNode)
        mNodeValuesY = cmds.getAttr('%s.in31'%mNode)
        mNodeValuesZ = cmds.getAttr('%s.in32'%mNode)
        self.assertEqual(mNodeValuesX, (orig_mNodeValuesX-vec[0]))
        self.assertEqual(mNodeValuesY, (orig_mNodeValuesX-vec[1]))
        self.assertEqual(mNodeValuesZ, (orig_mNodeValuesX-vec[2]))   
        
        spaceSwitching.matrix_translate_4x4Node(mNode, vec, mode='replace')
        mNodeValuesX = cmds.getAttr('%s.in30'%mNode)
        mNodeValuesY = cmds.getAttr('%s.in31'%mNode)
        mNodeValuesZ = cmds.getAttr('%s.in32'%mNode)
        self.assertEqual(mNodeValuesX, (vec[0]))
        self.assertEqual(mNodeValuesY, (vec[1]))
        self.assertEqual(mNodeValuesZ, (vec[2]))   
        
if __name__ == '__main__':
    unittest.main()