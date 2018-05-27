import logging
import os
import sys
import pymel.core as pm

#--- Add cwd and lib
cwd = os.path.dirname(os.path.abspath(__file__))
lib = cwd+'/library'
modules = cwd+'/modules'
if modules not in sys.path:
    sys.path.append(modules)
if lib not in sys.path:
    sys.path.append(lib)
    
import Names
reload( Names )

import Neck
reload( Neck )
import Head
reload( Head )
import Arm
reload( Arm)
import Torso
reload(Torso)
import CanidaeLeg
reload(CanidaeLeg)
import Control
reload(Control)
import Finger
reload(Finger)
import Hand
reload(Hand)

#--- Logging
from pymel.tools import loggingControl
loggingControl.initMenu()
from pymel.internal.plogging import pymelLogger
pymelLogger.setLevel(logging.DEBUG)

def build_head():
    pymelLogger.debug('Starting: build_head()...') 
    
    Neck.build()
    Head.build()
    
    pymelLogger.debug('End: build_head()...')
    
def build_body():
    pymelLogger.debug('Starting: build_body()...') 
    
    
    Torso.build()
    
    # legs
    CanidaeLeg.build(side = Names.prefixes['left'])
    CanidaeLeg.build(side = Names.prefixes['right'])
    # arms
    Arm.build(side = Names.prefixes['left'])
    Arm.build(side = Names.prefixes['right'])
    
   

    # Hands and fingers
    Hand.build( side = Names.prefixes['left'] )
    Hand.build( side = Names.prefixes['right'] )
    
    
    # main ctrl
    main_cnt_name =  Names.joints_torso[0] + '_' + Names.suffixes['control']
    main_cnt = Control.create( name=main_cnt_name, offsets=0, shape='circle_4_arrow', 
                size=1, color='yellow', 
                pos=None, parent=None, typ='body' )
    pm.parent(main_cnt, 'controls')
    ######################
    ######################
    # hard coded! fix!
    consGrp = [Names.torso_module, Names.legs_module]
    for grp in consGrp:
        try: pm.parentConstraint( main_cnt, grp, mo=1 )
        except: print 'Could not constraint: ' + main_cnt + ' to ' + grp
    # constraint main to reference_jnt
    pm.parentConstraint(main_cnt, Names.joints_torso[0], mo=1)
    ######################
    ######################
   
    
    
  
    pymelLogger.debug('End: build_body()...')
    
def import_head_rig():
    pymelLogger.debug('Starting: connect_head_body()...') 
    Head.attachToBody()
    pymelLogger.debug('End: connect_head_body()...')
