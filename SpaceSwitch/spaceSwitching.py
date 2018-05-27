'''
Use:
import sys
path = '/Users/mauricioptkvp/Desktop/SpaceSwitch'
if path not in sys.path:
	sys.path.insert(0,path)

import spaceSwitching
reload( spaceSwitching )
spaceNode = spaceSwitching.setupSpaces(name='locSpace',parent='pCube1',child='locator1')

spaceSwitching.spaceSwitch(spaceNode=spaceNode, newParent='pSphere1')

spaceSwitching.spaceSwitch(spaceNode=spaceNode, newParent='pCube1')
'''

import maya.cmds as cmds
import maya.mel as mel
import maya.OpenMaya as om

def setupSpaces(name=None,parent=None,child=None):
    if not name: raise Exception('No name passed in by caller')
    if not parent: raise Exception('No parent passed in by caller')
    if not child: raise Exception('No child passed in by caller')
    
    cmds.loadPlugin( 'decomposeMatrix.bundle' )
    
    spaceNode = _createSpaceNode(name=name)
    
    multMatrix = cmds.createNode('multMatrix',n='%s_multMatrix'%name)
    rpPointMatrixMult = cmds.createNode('pointMatrixMult',n='%s_rpPointMatrixMult'%name)
    decomp = cmds.createNode('decomposeMatrix',n='%s_decomposeMatrix'%name)
    rpDecomp = cmds.createNode('decomposeMatrix',n='%s_rpDecomposeMatrix'%name)
    offsetMatrix = cmds.createNode('fourByFourMatrix',n='%s_offsetMatrix'%name)
    rpOffsetMatrix = cmds.createNode('fourByFourMatrix',n='%s_rpOffsetMatrix'%name)
    
    # Connect Parent to message attribute
    cmds.connectAttr('%s.message'%parent,'%s.pn'%spaceNode,f=True)  
    
    # Connect Parent to message attribute
    cmds.connectAttr('%s.message'%child,'%s.cn'%spaceNode,f=True)     
    
    # Connect multMatrix to message attribute
    cmds.connectAttr('%s.message'%multMatrix,'%s.mmn'%spaceNode,f=True) 
    
    # Connect rpPointMatrixMult to message attribute
    cmds.connectAttr('%s.message'%rpPointMatrixMult,'%s.rppmmn'%spaceNode,f=True)     
    
    # Connect decomp to message attribute
    cmds.connectAttr('%s.message'%decomp,'%s.dcn'%spaceNode,f=True)     
    
    # Connect offsetMatrix to message attribute
    cmds.connectAttr('%s.message'%offsetMatrix,'%s.omn'%spaceNode,f=True)    
    
    
    # Set offsetMatrix value
    offsetM = _getOffsetMatrix(parent,child)  
    matrix_write_4x4Node(offsetMatrix,offsetM)
    
    # Make connections 
    # Transformations
    cmds.connectAttr('%s.output'%offsetMatrix,'%s.matrixIn[0]'%multMatrix,f=True)
    cmds.connectAttr('%s.wm'%parent,'%s.matrixIn[1]'%multMatrix,f=True)
    cmds.connectAttr('%s.pim'%child,'%s.matrixIn[2]'%multMatrix,f=True)
    
    cmds.connectAttr('%s.matrixSum'%multMatrix,'%s.inputMatrix'%decomp,f=True)
    
    cmds.connectAttr('%s.outputTranslate'%decomp,'%s.translate'%child,f=True)    
    cmds.connectAttr('%s.outputRotate'%decomp,'%s.rotate'%child,f=True)    
    cmds.connectAttr('%s.outputScale'%decomp,'%s.scale'%child,f=True)    
    cmds.connectAttr('%s.outputShear'%decomp,'%s.shear'%child,f=True)
    
    # Rotation   
    cmds.connectAttr('%s.rotatePivot'%parent,'%s.rotatePivot'%child,f=True)
    cmds.connectAttr('%s.scalePivot'%parent,'%s.scalePivot'%child,f=True)    
    cmds.connectAttr('%s.rotateOrder'%parent,'%s.rotateOrder'%child,f=True)
    cmds.connectAttr('%s.rotatePivotTranslate'%parent,'%s.rotatePivotTranslate'%child,f=True)   
    
    return spaceNode
    
def _createSpaceNode(name=None):
    ''' Create node with attributes to be connected for space connections '''
    if not name: raise Exception('No name passed in by caller')    
    spaceNode = cmds.createNode('null',n=name)
    
    # ParentNode message attribute
    cmds.addAttr( spaceNode, shortName='pn', longName='parentNode', at='message' )
    
    # ChildNode message attribute
    cmds.addAttr( spaceNode, shortName='cn', longName='childNode', at='message' )    
    
    # multMatrixNode message attribute
    cmds.addAttr( spaceNode, shortName='mmn', longName='multMatrixNode', at='message' ) 
    
    # rpMultMatrixNode message attribute
    cmds.addAttr( spaceNode, shortName='rppmmn', longName='rpPointMatrixMult', at='message' )     
    
    # decompNode message attribute
    cmds.addAttr( spaceNode, shortName='dcn', longName='decompNode', at='message' )   
    
    # switchMatrixNode message attribute
    cmds.addAttr( spaceNode, shortName='omn', longName='offsetMatrixNode', at='message' )  
    
    return spaceNode

def _getOffsetMatrix(obj1,obj2):
    ''' Return offset MMatrix from obj1 to obj2'''
    obj1_m = cmds.xform(obj1,q=True,matrix=True)
    obj2_m = cmds.xform(obj2,q=True,matrix=True)
    obj1WM = om.MMatrix()
    obj2WM = om.MMatrix()
    om.MScriptUtil.createMatrixFromList( obj1_m, obj1WM)     
    om.MScriptUtil.createMatrixFromList( obj2_m, obj2WM) 
    
    return obj1WM.inverse() * obj2WM

def spaceSwitch(spaceNode=None, newParent=None):
    ''' Pass in constrained node and new target transform. '''
    if not spaceNode: raise Exception('No spaceNode passed in by caller')
    if not newParent: raise Exception('No newParentpassed in by caller')
    
    # Get nodes connected to message attrs
    currentParent = cmds.listConnections('%s.parentNode'%spaceNode)[0]
    child = cmds.listConnections('%s.childNode'%spaceNode)[0]
    multMatrix = cmds.listConnections('%s.multMatrixNode'%spaceNode)[0]
    decomp = cmds.listConnections('%s.decompNode'%spaceNode)
    offsetMatrix = cmds.listConnections('%s.offsetMatrixNode'%spaceNode)[0]
    
    currentParentWM = om.MMatrix()
    om.MScriptUtil.createMatrixFromList( cmds.getAttr('%s.wm'%currentParent), currentParentWM)
    
    newParentWIM = om.MMatrix()
    om.MScriptUtil.createMatrixFromList( cmds.getAttr('%s.wim'%newParent), newParentWIM)
    
    childWM = om.MMatrix()
    om.MScriptUtil.createMatrixFromList( cmds.getAttr('%s.wm'%child), childWM)    
    
    # Get transformation difference from newParent to currentParent
    TM = newParentWIM * childWM
    matrix_write_4x4Node(offsetMatrix,TM)
    
    # Swap parents in multMatrix node
    cmds.disconnectAttr('%s.wm'%currentParent,'%s.matrixIn[1]'%multMatrix)
    cmds.connectAttr('%s.wm'%newParent,'%s.matrixIn[1]'%multMatrix,f=True)
    
    # Point parent message attr to new parent
    cmds.connectAttr('%s.message'%newParent,'%s.parentNode'%spaceNode,f=True) 
    
    # Update rotate pivot
    cmds.connectAttr('%s.rotatePivot'%newParent,'%s.rotatePivot'%child,f=True)
    cmds.connectAttr('%s.scalePivot'%newParent,'%s.scalePivot'%child,f=True)    
    cmds.connectAttr('%s.rotateOrder'%newParent,'%s.rotateOrder'%child,f=True)
    cmds.connectAttr('%s.rotatePivotTranslate'%newParent,'%s.rotatePivotTranslate'%child,f=True)  

def matrix_read_4x4Node( m1 ):
    ''' Read data from a fourByFourMatrix node into an MMatrix object. '''
    resultM = om.MMatrix()
    try:
        for r in range(4):
            for c in range(4):
                om.MScriptUtil.setDoubleArray(resultM[r], c, cmds.getAttr('%s.in%s%s'%(m1,r,c)) )
        return resultM
        
    except Exception,e:
        raise Exception(e)    

def matrix_write_4x4Node( matrixNode, m1 ):
    ''' Write data from an MMatrix object (m1) to a fourByFourMatrix node. '''
    try:
        for r in range(4):
            for c in range(4):
                cmds.setAttr('%s.in%s%s'%(matrixNode,r,c), m1(r,c))

    except Exception,e:
        raise Exception(e)
    
def matrix_translate_4x4Node( matrixNode, mvValues=[0,0,0], mode='add'):
    ''' matrixNode = multMatrix, values = MVector '''
    values = []
    values.append(cmds.getAttr('%s.in30'%matrixNode))
    values.append(cmds.getAttr('%s.in31'%matrixNode))
    values.append(cmds.getAttr('%s.in32'%matrixNode))
    
    if mode == 'add':
        cmds.setAttr('%s.in30'%(matrixNode), (values[0]+mvValues[0]) )
        cmds.setAttr('%s.in31'%(matrixNode), (values[1]+mvValues[1]) )
        cmds.setAttr('%s.in32'%(matrixNode), (values[2]+mvValues[2]) )
        
    if mode == 'subtract':
        cmds.setAttr('%s.in30'%(matrixNode), (values[0]-mvValues[0]) )
        cmds.setAttr('%s.in31'%(matrixNode), (values[1]-mvValues[1]) )
        cmds.setAttr('%s.in32'%(matrixNode), (values[2]-mvValues[2]) )
        
    if mode == 'replace':
        cmds.setAttr('%s.in30'%(matrixNode), mvValues[0] )
        cmds.setAttr('%s.in31'%(matrixNode), mvValues[1] )
        cmds.setAttr('%s.in32'%(matrixNode), mvValues[2] )
        

    