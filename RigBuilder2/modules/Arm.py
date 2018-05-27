import os
import sys
import logging

import pymel.core as pm

#--- Add cwd and lib
cwd = os.path.dirname(os.path.abspath(__file__))
lib = cwd.replace('modules','library')
if cwd not in sys.path:
    sys.path.append(cwd)
if lib not in sys.path:
    sys.path.append(lib)

import Names
reload( Names )
import Control
reload( Control )

#--- Logging
from pymel.tools import loggingControl
loggingControl.initMenu()
from pymel.internal.plogging import pymelLogger
pymelLogger.setLevel(logging.DEBUG)

def build(side=None):
    pymelLogger.debug('Starting: build()...') 

    # Define names
    if side == Names.prefixes['left']:
        follow_chain = [ '%s%s_%s'%(Names.prefixes['left'], jnt, Names.suffixes['follow']) for jnt in Names.joints_arm]
        fk_chain = [ '%s%s_%s'%(Names.prefixes['left'], jnt, Names.suffixes['fk']) for jnt in Names.joints_arm]
        ik_chain = [ '%s%s_%s'%(Names.prefixes['left'], jnt, Names.suffixes['ik']) for jnt in Names.joints_arm]
        fkControls = Names.controls_leftArmFk
        ikControls = Names.controls_leftArmIk
    if side == Names.prefixes['right']:
        follow_chain = [ '%s%s_%s'%(Names.prefixes['right'], jnt, Names.suffixes['follow']) for jnt in Names.joints_arm]
        fk_chain = [ '%s%s_%s'%(Names.prefixes['right'], jnt, Names.suffixes['fk']) for jnt in Names.joints_arm]
        ik_chain = [ '%s%s_%s'%(Names.prefixes['right'], jnt, Names.suffixes['ik']) for jnt in Names.joints_arm]
        fkControls = Names.controls_rightArmFk
        ikControls = Names.controls_rightArmIk

    # Build functions
    topOffsetNode = _makeFkControls(fkControls=fkControls, side  = side) # topOffsetNode
    _cleanUp( topOffsetNode )
    #_makeIkControls(ikControls=ikControls)
    #_makeJoints(side=side, fkChain=fk_chain, ikChain=ik_chain)
    #_makeFkRig(side=side, fkChain=fk_chain)
    #_makeIkRig(side=side, ikChain=ik_chain)
    #_bindFollowChain(followChain=follow_chain, fkChain=fk_chain, ikChain=ik_chain) 
    pymelLogger.debug('End: build()...')

def _getSideColor(side=None):
    
    if side == Names.prefixes['left']: crv_color='red'
    elif side == Names.prefixes['right']: crv_color='midBlue'
    else: crv_color='white'
    return crv_color

def _makeFkControls(fkControls=None, side=None):
    pymelLogger.debug('Starting: _makeControls()...')

    topNodeList = []
    for ctrl in fkControls:
        parent = ctrl.replace('_'+Names.suffixes['fk']+'_'+Names.suffixes['control'],'')
        topNode = Control.create( name=ctrl, offsets=3, shape='circle_01', 
                                  size=1.5, color=_getSideColor(side), 
                                  pos=None, parent=parent, typ='body' )
        pm.parent(topNode, world=1)
        topNodeList.append(topNode)
        
        # getting ctrl and contrainting it directly to the jnt
        childs = topNode.listRelatives(ad=1)
        if 'Shape' in str(childs[0]):
            cc = childs[1]  
        else: cc = childs[0]
        pm.parentConstraint(cc,parent, mo=1)
        
    # parent each offset to the previous ctrl
    topNodeList.reverse()
    last = ''
    for element in topNodeList:
        if last:
            last.setParent(element.listRelatives(ad=1)[1]) # getting transform node not shape
        last = element 
   
    topOffsetNode = last
    return topOffsetNode   

    pymelLogger.debug('End: _makeControls()...')

def _cleanUp( topOffsetNode ):
    
    # parent legs to legs group
    if not pm.objExists( Names.arms_module ):
        arms_module = pm.group(em=1, name=Names.arms_module)
        # contraint to spine2_ctrl # hard coded we should get it from  the character node
        pm.parentConstraint('Spine2_ctrl', arms_module, mo=1)
        arms_module.setParent( Names.modules_grp )
    else: arms_module = pm.ls( Names.arms_module )

    topOffsetNode.setParent( arms_module )
    
    
    
def _makeIkControls(ikControls=None):
    pymelLogger.debug('Starting: _makeIkControls()...')
    
    for ctrl in ikControls:
        if 'IK' in ctrl:
            if Names.prefixes['left'] in ctrl:
                parent = '%s%s'%(Names.prefixes['left'],Names.joints_arm[-1])
            if Names.prefixes['right'] in ctrl:
                parent = '%s%s'%(Names.prefixes['right'],Names.joints_arm[-1])
            topNode = Control.create( name=ctrl, offsets=3, shape='circle_01', 
                                      size=None, color=None, 
                                      pos=None, parent=parent, typ='body' )   
            pm.parent(topNode, 'controls')
        if 'PV' in ctrl:
            pass
        
    pymelLogger.debug('End: _makeIkControls()...')
    
def _positionPV(joints=None):
    pymelLogger.debug('Starting: _positionPV()...') 
    pymelLogger.debug('End: _positionPV()...')    
    
def _makeJoints(side=None, fkChain=None, ikChain=None):
    pymelLogger.debug('Starting: _makeJoints()...') 
    pymelLogger.debug('End: _makeJoints()...')
    
def _makeFkRig(side=None, fkChain=None):
    pymelLogger.debug('Starting: _makeFkRig()...') 
    pymelLogger.debug('End: _makeFkRig()...')
    
def _makeIkRig(side=None, ikChain=None):
    pymelLogger.debug('Starting: _makeIkRig()...') 
    pymelLogger.debug('End: _makeIkRig()...')
    
def _bindFollowChain(followChain=None, fkChain=None, ikChain=None):
    pymelLogger.debug('Starting: _bindFollowChain()...') 
    pymelLogger.debug('End: _bindFollowChain()...')

def _constrainSHToControls(side=None):
    pymelLogger.debug('Starting: _constrainSHToControls()...') 

    pymelLogger.debug('End: _constrainSHToControls()...')

