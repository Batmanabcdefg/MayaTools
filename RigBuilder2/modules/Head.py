import logging
import os
import sys
import pdb

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
    ''' Make Head and Face controls, parented to Neck '''
    pymelLogger.debug('Starting: build()...') 
    
    _makeControls()
    _constrainLocsToControls()
    _addFacePoseAttrs()
    _constrainSpaces()
    
    pymelLogger.debug('End: build()...')

def _makeControls():
    ''' Make Head and Face controls, parented to Neck '''
    pymelLogger.debug('Starting: _makeControls()...') 
    
    # Head
    parent = Names.controls_neck[1]
    ctrl= Names.controls_head[0]
    pos = pm.xform('Head',ws=1,q=1,rp=1)
    rot = pm.xform('Head',ws=1,q=1,ro=1)
    s = [['head_head_ctrl_space','head_world_space'],['local','world'],'orient']
    Control.create( name=ctrl, offsets=3, shape='circle_01', 
                size=None, color=None, switch=s, 
                pos=pos, rot=rot, parent=parent, typ='head' )  
    
    # Face controls
    parent = 'head_controls'
    ctrl= Names.controls_face[0]
    pos = pm.xform('Head',ws=1,q=1,rp=1)
    pos[0] += 3
    Control.create( name=ctrl, offsets=3, shape='circle_01', 
                size=None, color=None, 
                pos=pos, parent=parent, typ='head' )  
    
    pos[0] += 1
    for ctrl in Names.controls_face:
        if ctrl == Names.controls_face[0]: 
            continue
        
        pos[1] += 1
        parent = Names.controls_face[0]
        ctrl= ctrl
        Control.create( name=ctrl, offsets=3, shape='circle_01', 
                    size=None, color=None, 
                    pos=pos, parent=parent, typ='head' )        
    
    pymelLogger.debug('End: _makeControls()...')

def _constrainLocsToControls():
    pymelLogger.debug('Starting: _constrainLocsToControls()...') 
    # Head
    pm.parentConstraint(Names.controls_head[0],'Head_ctrl_bind_grp',mo=1)
    # Neck1
    pm.parentConstraint(Names.controls_neck[1],'Neck1_grp',mo=1)    
    # Neck
    pm.parentConstraint(Names.controls_neck[0],'Neck_grp',mo=1)    
    pymelLogger.debug('End: _constrainLocsToControls()...')
    
def _constrainSpaces():
    pymelLogger.debug('Starting: _constrainSpaces()...') 
    # Head
    pm.parentConstraint(Names.controls_neck[1],'head_head_ctrl_space',mo=1)
    pymelLogger.debug('End: _constrainSpaces()...')
    
def _addFacePoseAttrs():
    pymelLogger.debug('Starting: _addFacePoseAttrs()...') 
    
    # Eyes
    pm.select( Names.controls_face[3], r=True )
    for attr in Names.controls_face_eye_poses:
        pm.addAttr( longName=attr, k=True, min=0, max=10 )
    pm.select( Names.controls_face[4], r=True )
    for attr in Names.controls_face_eye_poses:
        pm.addAttr( longName=attr, k=True, min=0, max=10 )
        
    # Brows
    pm.select( Names.controls_face[5], r=True )
    for attr in Names.controls_face_brow_poses:
        pm.addAttr( longName=attr, k=True, min=0, max=10 )
    pm.select( Names.controls_face[6], r=True )
    for attr in Names.controls_face_brow_poses:
        pm.addAttr( longName=attr, k=True, min=0, max=10 )
        
    # Cheeks
    pm.select( Names.controls_face[7], r=True )
    for attr in Names.controls_face_cheek_poses:
        pm.addAttr( longName=attr, k=True, min=-10, max=10 )
    pm.select( Names.controls_face[8], r=True )
    for attr in Names.controls_face_cheek_poses:
        pm.addAttr( longName=attr, k=True, min=-10, max=10 )
        
    # Mouth
    pm.select( Names.controls_face[1], r=True )
    for attr in Names.controls_werewolf_mouth_poses:
        pm.addAttr( longName=attr, k=True, min=0, max=10 )
        
    # Nose
    pm.select( Names.controls_face[2], r=True )
    for attr in Names.controls_face_nose_poses:
        pm.addAttr( longName=attr, k=True, min=0, max=10 )
        
    # Face
    pm.select( Names.controls_face[0], r=True )
    for attr in Names.controls_werewolf_poses:
        pm.addAttr( longName=attr, k=True, min=-10, max=10 )
    
    pymelLogger.debug('End: _addFacePoseAttrs()...')
    
def attachToBody():
    '''
    Connect a head to a body. Run inside the body rig.
    
    Example:
        import sys
        path = '/Users/3mo/Documents/repos/artpipeline/maya/RigBuilder/modules'
        if path not in sys.path:
            sys.path.insert(0, path)
        
        import Head as head
        reload( head )
        
        head.attachToBody()
    '''
    # Get head rig file from user, Import file
    try:
        pm.importFile( pm.fileDialog(t='Select Head Rig file') )
    except Exception,e:
        raise Exception(e)
    
    # Place in main rig group
    pm.group('HeadRig','BodyRig','BodyCharacterNode',n='TopNode')

    # Place SH joints
    pm.parent('Neck','Spine2')
    
    # Constrain spaces
    pm.parentConstraint('Reference_ctrl','head_world_space',mo=1)
    pm.parentConstraint('Cog_ctrl','head_main_ctrl_space',mo=1)
    pm.parentConstraint('Spine2_ctrl','head_chest_space',mo=1)
    pm.parentConstraint('Hips_ctrl','head_hip_ctrl_Space',mo=1)
    pm.parentConstraint('Spine2_ctrl','head_body_attach_space',mo=1)
    
    # Constrain controls
    pm.parentConstraint('Spine2_ctrl','head_controls',mo=1)
    
    # Per geo:
    geometry = [
        "custom|body",
        "custom|eyeR",
        "custom|eyeL",
        "custom|tongue",
        "custom|gums",
        "custom|upperTeeth",
        "custom|lowerTeeth",
        ]
    
    # Add neck/head/face joints as influences to referenced model in rig
    for geo in geometry:
        headSc = pm.mel.eval('findRelatedSkinCluster("%s");'%geo)
        bodySc = pm.mel.eval('findRelatedSkinCluster("%s%s");'%('Male_Werewolf_01_model:',geo.split('|')[-1]))
        if headSc:
            infs = pm.skinCluster(headSc,q=True,inf=True)
        pm.select(clear=True)
        #pdb.set_trace()
        if infs:
            if not bodySc:
                pm.skinCluster(infs,'Male_Werewolf_01_model:%s'%geo.split('|')[-1])
                bodySc = pm.mel.eval('findRelatedSkinCluster("%s");'%('Male_Werewolf_01_model:'+geo.split('|')[-1]))
            else:
                for each in infs:
                    pm.skinCluster(bodySc,edit=True,ai=each)
    
    # Copy weights to referenced geo in rig for head
    # Body
    faces = ['Male_Werewolf_01_model:body.f[1461:1497]',
             'Male_Werewolf_01_model:body.f[1520:1525]',
             'Male_Werewolf_01_model:body.f[1527]',
             'Male_Werewolf_01_model:body.f[1544:1555]',
             'Male_Werewolf_01_model:body.f[1762:1788]',
             'Male_Werewolf_01_model:body.f[1817:1827]',
             'Male_Werewolf_01_model:body.f[1833]',
             'Male_Werewolf_01_model:body.f[1888:1905]',
             'Male_Werewolf_01_model:body.f[1907]',
             'Male_Werewolf_01_model:body.f[2067:2069]',
             'Male_Werewolf_01_model:body.f[2071:2072]',
             'Male_Werewolf_01_model:body.f[2074:2093]',
             'Male_Werewolf_01_model:body.f[2101:2626]',
             'Male_Werewolf_01_model:body.f[2635]',
             'Male_Werewolf_01_model:body.f[2640:2676]',
             'Male_Werewolf_01_model:body.f[2686:2799]',
             'Male_Werewolf_01_model:body.f[2840:2841]',
             'Male_Werewolf_01_model:body.f[4126:4131]',
             'Male_Werewolf_01_model:body.f[4150:4257]',
             'Male_Werewolf_01_model:body.f[4262:4400]',
             'Male_Werewolf_01_model:body.f[5862:5898]',
             'Male_Werewolf_01_model:body.f[5921:5926]',
             'Male_Werewolf_01_model:body.f[5928]',
             'Male_Werewolf_01_model:body.f[5945:5956]',
             'Male_Werewolf_01_model:body.f[6163:6189]',
             'Male_Werewolf_01_model:body.f[6218:6228]',
             'Male_Werewolf_01_model:body.f[6234]',
             'Male_Werewolf_01_model:body.f[6289:6306]',
             'Male_Werewolf_01_model:body.f[6308]',
             'Male_Werewolf_01_model:body.f[6468:6470]',
             'Male_Werewolf_01_model:body.f[6472:6473]',
             'Male_Werewolf_01_model:body.f[6475:6494]',
             'Male_Werewolf_01_model:body.f[6502:7027]',
             'Male_Werewolf_01_model:body.f[7036]',
             'Male_Werewolf_01_model:body.f[7041:7077]',
             'Male_Werewolf_01_model:body.f[7087:7200]',
             'Male_Werewolf_01_model:body.f[7241:7242]',
             'Male_Werewolf_01_model:body.f[8527:8532]',
             'Male_Werewolf_01_model:body.f[8551:8658]',
             'Male_Werewolf_01_model:body.f[8663:8801]']
    
    pm.select(geometry[0],replace=1)
    pm.select(faces,add=1)
    pm.mel.eval('CopySkinWeights;')
    
    
    # Eyes, Tongue, Teeth, Gums are full copy
    for geo in geometry:
        if 'body' in geo: continue
        headSc = pm.mel.eval('findRelatedSkinCluster("%s");'%geo)
        bodySc = pm.mel.eval('findRelatedSkinCluster("%s%s");'%('Male_Werewolf_01_model:',geo.split('|')[-1]))
        pm.select(bodySc, headSc, replace=1)
        pm.mel.eval('CopySkinWeights;')
    
    # Delete head rig geo
    pm.delete('HeadRig|custom')