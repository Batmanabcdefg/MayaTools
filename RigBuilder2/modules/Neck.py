import logging
import os
import sys

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

def build():
    pymelLogger.debug('Starting: build()...') 
    
    _makeControls()
    _constrainSHToControls()
    _connectToBody()
    
    pymelLogger.debug('End: build()...')
    
def _makeControls():
    pymelLogger.debug('Starting: _makeControls()...') 
    
    # Neck
    parent = 'head_controls'
    ctrl= Names.controls_neck[0]
    pos = pm.xform('Neck',ws=1,q=1,rp=1)
    rot = pm.xform('Neck',ws=1,q=1,ro=1)
    s = [['head_body_attach_space','head_world_space'],['local','world'],'orient']
    Control.create( name=ctrl, offsets=3, shape='circle_01', 
                size=None, rot=rot, color=None, switch=s, 
                pos=pos, parent=parent, typ='head' )  
    
    # Neck1
    parent = Names.controls_neck[0]
    ctrl= Names.controls_neck[1]
    pos = pm.xform('Neck1',ws=1,q=1,rp=1)
    rot = pm.xform('Neck1',ws=1,q=1,ro=1)
    Control.create( name=ctrl, offsets=3, shape='circle_01', 
                size=None, rot=rot, color=None, 
                pos=pos, parent=parent, typ='head' )  
    
    pymelLogger.debug('End: _makeControls()...')
    
def _constrainSHToControls():
    pymelLogger.debug('Starting: _constrainSHToControls()...') 
    
    # Neck
    pm.parentConstraint(Names.controls_neck[0],'Neck',mo=1)
    
    # Neck1
    pm.parentConstraint(Names.controls_neck[1],'Neck1',mo=1) 
    
    pymelLogger.debug('End: _constrainSHToControls()...')
    
def _connectToBody():
    ''' 
    Connect if there is a BodyCharacterNode and
    it has a "Spine2_ctrl" registered.
    '''
    if pm.objExists('BodyCharacterNode'):
        ctrl = pm.listConnections('BodyCharacterNode.Spine2_ctrl')
        if ctrl:
            pm.parentConstraint(ctrl,'%s_offsetA'%(Names.controls_neck[0]),mo=1)
            pm.parentConstraint(ctrl,'head_body_attach_space',mo=1)

        