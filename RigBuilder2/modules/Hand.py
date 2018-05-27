import pymel.core as pm
import logging
import os
import sys

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
import Finger
reload(Finger)

#--- Logging
from pymel.tools import loggingControl
loggingControl.initMenu()
from pymel.internal.plogging import pymelLogger
pymelLogger.setLevel(logging.DEBUG)

def build( side=None ):
    pymelLogger.debug('Starting: build()...') 
    
    if side == None: raise Exception('Make sure side: %s is valid '%side) 
    if side != Names.prefixes['left'] and side != Names.prefixes['right']:
        raise Exception('Make sure side: %s is valid '%side)
    
    # create hand jnt
    handJntList = _createHandJnt( side ) # [handJnt, handJntName]
    handJnt = handJntList[0]
    handJntSH = handJntList[1]
    
    # create hand switch
    ctrl = handJntSH + '_' + Names.suffixes['switch']
    hand_switch_offset = Control.create( name= ctrl  , offsets=1, shape='cube', 
                    size=[1,1,1], color=_getSideColor(side), 
                    pos=None, parent=handJnt, typ='body' )
    
    hand_switch_offset.setParent( world=1 )
    hand_switch = hand_switch_offset.getChildren()[0] # it will work only with one offset
    
    hideLockAttr(hand_switch, lockHideTRSV)
    
    # add switch attr
    pm.addAttr( hand_switch, longName= Names.switchIkFk, k=True, min=0, max=1 )
    
    # parentConstraint switch offset to sh handJnt !!!! Make sure it will work
    pm.parentConstraint(handJntSH, hand_switch_offset, mo=True)
    
    # build fingers
    Finger.build( side=side, label='Fingers', control=hand_switch, parentJnt = handJnt,
                  curl='Z',twist='X',spread='Y', fkNormal=(1.0, 0.0, 0.0), radius=0.3 )
    
    # group switch and hand
    hand_grp = pm.group(hand_switch_offset,handJnt,name = handJntSH + '_' + Names.suffixes['group'])
    _cleanUp( hand_grp )
    
    pymelLogger.debug('End: build()...')


   
def hideLockAttr(object, values=[]):
    for val in values:
        pm.setAttr(object + val, lock = True, keyable = False, channelBox = False)

# use this as constants
lockHideTRSV = ['.tx','.ty','.tz','.rx','.ry','.rz','.sx','.sy','.sz','.v']
lockHideTSV = ['.tx','.ty','.tz','.sx','.sy','.sz','.v']
lockHideSV = ['.sx','.sy','.sz','.v']
lockHideS = ['.sx','.sy','.sz']
lockHideXZ = ['.sx','.sz'] 


def _cleanUp( hand_grp ):
    
    pymelLogger.debug('Starting: _cleanUp()...') 
    # parent side+hand to hands group
    if not pm.objExists( Names.hands_module ):
        hands_module = pm.group( em=1, name=Names.hands_module )
        hands_module.setParent( Names.modules_grp )
    else: hands_module = pm.ls( Names.hands_module, r=1 )[0]
    
    hand_grp.setParent(hands_module)
    pymelLogger.debug('End: _cleanUp()...') 
   



def _getSideColor(side=None):
    
    pymelLogger.debug('Starting: _getSideColor()...') 
    if side == Names.prefixes['left']: crv_color='red'
    elif side == Names.prefixes['right']: crv_color='midBlue'
    else: crv_color='white'
    return crv_color
    pymelLogger.debug('End: _getSideColor()...') 


def _createHandJnt( side ):
    
    pymelLogger.debug('Starting: _createHandJnt()...') 
    handJntName = side + Names.joints_hf[0]
    handSHJnt = pm.ls(handJntName,r=1)[0]
    if not handSHJnt: raise 'Hand Jnt could not be found, make sure naming is correct and jnt exists' 
    handJnt = handSHJnt.duplicate(rr=True,po=True, name = handJntName + '_' + Names.suffixes['attach'])[0]
    handJnt.setParent(world=True)
    handJnt.setAttr('radius',1)
    rList = [handJnt, handSHJnt]
    return rList

    pymelLogger.debug('End: _createHandJnt()...') 
        