import logging

"""
Lists, dictionaries of names used in RigBuilder.py
"""

#--- Logging
from pymel.tools import loggingControl
loggingControl.initMenu()
from pymel.internal.plogging import pymelLogger
pymelLogger.setLevel(logging.DEBUG)

pymelLogger.debug('Importing: Names') 

# Prefixes
prefixes = {'left':'Left',
            'right':'Right',
            'center':'Center',
            'singleHierarchy':'SH',
            'driver':'drv'}
            
# Suffixes
suffixes = {'control':'ctrl',
            'offset':'off',
            'multiplyDivide':'md',
            'plusMinusAvg':'pma',
            'distance':'dist',
            'bind':'bind',
            'joint':'jnt',
            'influence':'inf',
            'ik':'ik',
            'fk':'fk',
            'follow':'follow',
            'ikhandle':'ikh',
            'start':'start',
            'end':'end',
            'frameCache':'fc',
            'expression':'exp',
            'switch':'switch',
            'attach':'attach',
            'group':'grp'
            }     

# Influence
influence = 'inf'

# switch ik fk
switchIkFk = 'switch_ik_fk'


#
#----------------------------------- Joint names
#

#Torso
joints_torso = ['Reference','Hips','Spine','Spine1','Spine2','Spine3','Spine4','Spine5','Neck1','Neck2','Head']

# ideally user will be able to pass the number of spines he wants
joints_torso_ww = ['Hips', 'Spine', 'Spine1', 'Spine2']

# Arms
joints_arm = ['Shoulder','Arm','ArmRoll','ArmRoll1','ArmRoll2','ForeArm','ForeArmRoll','ForeArmRoll1','ForeArmRoll2','Hand']
joints_leftArm = [ '%s%s'%(prefixes['left'], jnt) for jnt in joints_arm]
joints_rightArm = [ '%s%s'%(prefixes['right'], jnt) for jnt in joints_arm]

# Legs       
joints_leg = ['UpLeg','UpLegRoll','UpLegRoll2','UpLegRoll3','Leg','LegRoll','LegRoll1','LegRoll2','Foot','ToeBase']
joints_leftLeg = [ '%s%s'%(prefixes['left'], jnt) for jnt in joints_leg]
joints_rightLeg = [ '%s%s'%(prefixes['right'], jnt) for jnt in joints_leg]

joints_leftLegNoRoll=[]
joints_rightLegNoRoll=[]
for jnt in joints_leg:
    if 'Roll' in jnt: continue
    joints_leftLegNoRoll.append('%s%s' %(prefixes['left'],jnt))
    joints_rightLegNoRoll.append('%s%s' %(prefixes['right'],jnt))
# for ww we need to add the toe1 and toe2
joints_leftLegNoRoll.append('%s%s%s' %(prefixes['left'],joints_leg[-1],'1') )
joints_leftLegNoRoll.append('%s%s%s' %(prefixes['left'],joints_leg[-1],'2') )
joints_rightLegNoRoll.append('%s%s%s' %(prefixes['right'],joints_leg[-1],'1'))
joints_rightLegNoRoll.append('%s%s%s' %(prefixes['right'],joints_leg[-1],'2') )


# Hands
joints_endLimbSegments = ['1','2','3','4']
joints_hf = ['Hand', 'Foot']
joints_fingers = ['Thumb','Index','Middle','Ring','Pinky']

joints_leftToes = ['%s%s%s%s'%(prefixes['left'],joints_hf[1],t,s) for s,t in zip(joints_endLimbSegments,joints_fingers)]
#joints_leftFingers = ['%s%s%s%s'%(prefixes['left'],joints_hf[0],t,s) for s,t in zip(joints_endLimbSegments,joints_fingers)]
joints_rightToes = ['%s%s%s%s'%(prefixes['right'],joints_hf[1],t,s) for s,t in zip(joints_endLimbSegments,joints_fingers)]
#joints_rightFingers = ['%s%s%s%s'%(prefixes['right'],joints_hf[0],t,s) for s,t in zip(joints_endLimbSegments,joints_fingers)]

# plain list
joints_leftFingers=[]
for finger in joints_fingers:
    for num in joints_endLimbSegments:
        joints_leftFingers.append( prefixes['left']+joints_hf[0]+finger+num )

joints_rightFingers=[]
for finger in joints_fingers:
    for num in joints_endLimbSegments:
        joints_rightFingers.append( prefixes['right']+joints_hf[0]+finger+num )  
              
# list of lists       
joints_leftFingers_list = []
for finger in joints_fingers:
    fingers = ['%s%s%s%s'%(prefixes['left'],joints_hf[0],finger,num) for num in joints_endLimbSegments]
    joints_leftFingers_list.append(fingers)

joints_rightFingers_list = []
for finger in joints_fingers:
    fingers = ['%s%s%s%s'%(prefixes['right'],joints_hf[0],finger,num) for num in joints_endLimbSegments]
    joints_rightFingers_list.append(fingers)
    




#joints_leftHand = joints_leftFingers
#joints_rightHand = joints_rightFingers
#joints_leftHand = ['%s_palm_%s'%(prefixes['left'], suffixes['jnt'])]
#joints_leftHand.append( x for x in joints_leftFingers )
#joints_rightHand = ['%s_palm_%s'%(prefixes['right'], suffixes['jnt'])]
#joints_rightHand.append( x for x in joints_rightFingers )

# Feet
#joints_leftFoot = joints_leftToes
#joints_rightFoot = joints_rightToes
#joints_leftFoot = ['%s_ball_%s'%(prefixes['left'], suffixes['jnt'])]
#joints_leftFoot.append( x for x in joints_leftToes )
#joints_rightFoot = ['%s_ball_%s'%(prefixes['right'], suffixes['jnt'])]
#joints_rightFoot.append( x for x in joints_rightToes )

# Face
_faceCenter = ["chin_below","chin_tip","chin_upper","forehead","lip_lower","lip_upper",
                     "nose_bridge_upper","nose_bridge_wrinkle","nose_lower","nose_ridge","nose_tip","oris_lower"]
_face = ["brow_below_mid","brow_below_outter","brow_inner","brow_mid","brow_outter","depressor_01","depressor_02",
         "depressor_small","ear","eyeBall","frontalis_inner","frontalis_outter","levator_upper",
         "lid_inner","lid_low_below","lid_low_inner_pivot","lid_low_mid_pivot","lid_low_outter_pivot","lid_outter",
         "lid_up_inner_pivot","lid_up_mid_pivot","lid_up_outter_pivot",
         "lip_corner","lip_low_inner","lip_low_outter","lip_up_inner","lip_up_outter",
         "massater_lower","massater_upper",
         "nostril","nostril_lower","nostril_outter","nostril_upper",
         "oris_corner","oris_lower","oris_upper","risorius","temporal",
         "ziggy","zygo_low_back","zygo_low_front","zygo_up_back","zygo_up_front","zygo_up_mid"]
joints_faceCenter = ['%s_%s_%s'%(prefixes['center'],x,suffixes['joint']) for x in _faceCenter]
joints_faceLeft = ["%s_%s_%s"%(prefixes['left'],x,suffixes['joint']) for x in _face]
joints_faceRight = ["%s_%s_%s"%(prefixes['right'],x,suffixes['joint']) for x in _face]

#
#----------------------------------- Control names
#
# Head
controls_head = [ 'head_%s'%suffixes['control'] ]

# Face
controls_face = [ '%s_%s'%(x,suffixes['control']) for x in ['face','mouth','nose'] ] 
for each in ['eye','brow','cheek']:
    controls_face.append('%s_%s_%s'%(prefixes['left'],each,suffixes['control']))
    controls_face.append('%s_%s_%s'%(prefixes['right'],each,suffixes['control']))
    
# Neck
controls_neck = [ '%s_%s'%(x,suffixes['control']) for x in ['neck1','neck2'] ]
    
# Torso
controls_torso = [ x + '_%s' %suffixes['control'] for x in joints_torso ]
controls_torso.append('Cog_%s' %suffixes['control'])

controls_torso_cog = 'Cog_%s' %suffixes['control']

# Arms
controls_leftArmFk = []
controls_rightArmFk = []
for jnt in joints_arm:
    if 'Roll' in jnt: continue  
    controls_leftArmFk.append('%s%s_%s_%s' %(prefixes['left'],jnt,suffixes['fk'],suffixes['control']))
    controls_rightArmFk.append('%s%s_%s_%s' %(prefixes['right'],jnt,suffixes['fk'],suffixes['control']))
    
controls_leftArmIk = []
controls_rightArmIk = []
controls_leftArmIk.append( '%s_armIK_%s'%(prefixes['left'], suffixes['control']) )
controls_leftArmIk.append( '%s_armPV_%s'%(prefixes['left'], suffixes['control']) )
controls_rightArmIk.append( '%s_armIK_%s'%(prefixes['right'], suffixes['control']) )
controls_rightArmIk.append( '%s_armPV_%s'%(prefixes['right'], suffixes['control']) )

# Hands
#controls_leftHand = ['%sHand_%s' %(prefixes['left'], suffixes['control'])]
#controls_rightHand = ['%sHand_%s' %(prefixes['right'], suffixes['control'])]
controls_leftHand = ['%sHand_%s' %(prefixes['left'], suffixes['switch'])]
for jnt in joints_leftFingers:
    controls_leftHand.append( jnt+'_'+suffixes['control'] )

controls_rightHand = ['%sHand_%s' %(prefixes['right'], suffixes['switch'])]
for jnt in joints_rightFingers:
    controls_rightHand.append( jnt+'_'+suffixes['control'] )


# Legs
controls_leftLeg = [ x + '_%s' %suffixes['control'] for x in joints_leftLeg ]
controls_leftLeg.append( '%s_LegIK_%s'%(prefixes['left'], suffixes['control']) )
controls_leftLeg.append( '%s_LegPV_%s'%(prefixes['left'], suffixes['control']) )

controls_rightLeg = [ x + '_%s' %suffixes['control'] for x in joints_rightLeg ]
controls_rightLeg.append( '%s_LegIK_%s'%(prefixes['right'], suffixes['control']) )
controls_rightLeg.append( '%s_LegPV_%s'%(prefixes['right'], suffixes['control']) )

controls_leftLegIK =  '%s_LegIK_%s'%(prefixes['left'], suffixes['control'])
controls_leftLegIKPV = '%s_LegPV_%s'%(prefixes['left'], suffixes['control'])
controls_rightLegIK =  '%s_LegIK_%s'%(prefixes['right'], suffixes['control'])
controls_rightLegIKPV = '%s_LegPV_%s'%(prefixes['right'], suffixes['control'])

# Feet
controls_leftFoot = [ x + '_%s' %suffixes['control'] for x in joints_leftToes ]
#controls_leftFoot.append( '%s_FootIK_%s'%(prefixes['left'], suffixes['control']) )
#controls_leftFoot.append( '%s_FootPV_%s'%(prefixes['left'], suffixes['control']) )

controls_rightFoot = [ x + '_%s' %suffixes['control'] for x in joints_rightToes ]
#controls_rightFoot.append( '%s_FootIK_%s'%(prefixes['right'], suffixes['control']) )
#controls_rightFoot.append( '%s_FootPV_%s'%(prefixes['right'], suffixes['control']) )

# Body All Ctrls
controls_body = controls_torso + \
                controls_leftHand +\
                controls_rightHand +\
                controls_leftArmFk + \
                controls_rightArmFk + \
                controls_leftArmIk + \
                controls_rightArmIk + \
                controls_leftLeg + \
                controls_rightLeg + \
                controls_leftFoot + \
                controls_rightFoot     

# Control Colors
controls_color = { 'lightGrey': 0, 'black':1, 
                    'midGrey': 2, 'redPink':4,
                    'darkBlue':5, 'midBlue':6,
                    'darkGreen':7, 'purple':8,
                    'pink': 9, 'red':13,
                    'lightGreen':14, 'lightBlue':15,
                    'white':16, 'yellow':17,
                    'cyan':18, 'blueGreen': 19                  
                   }

# offset grp names
offsetGrp = 'offset'
offset_suffix = ['A','B','C','D','E','F','G', 'H','I','J','K','L','M','N','O']
offset_names=[ offsetGrp + x for x in offset_suffix]

# Hierarchy Group names
modules_grp = 'modules'
torso_module = 'torso_module'
legs_grp = 'legs_grp'
legs_ikgrp = 'legs_ikgrp'
legs_module = 'legs_module'
arms_module = 'arms_module'
hands_module = 'hands_module'

# torso grps names
torso_anim_controls = 'grp_cc_body_anim'
torso_notouch = 'torso_noTouchGrp'
torso_hips_grp = 'grp_cc_hip'
torso_shoulders_grp = 'grp_cc_shoulder'


# Character Nodes
body_character_node = ['BodyCharacterNode']
head_character_node = ['HeadCharacterNode']
character_nodes = []
character_nodes.append(body_character_node)
character_nodes.append(head_character_node)

#---- Face pose names
controls_face_brow_poses = [
"BrowLower",
"BrowInnerRaise",
"BrowOutterRaise"
]

controls_face_eye_poses =  [
"UpperLidOpenClose",
"LowerLidOpenClose",
"LowerLidSquint",
"Squint",
"EyeBallUpDown",
"EyeBallLeftRight",
"PupilDialate"
]

controls_face_nose_poses =  [
"L_sneerA",
"R_sneerA",
"L_sneerB",
"R_sneerB",
"L_Nostril_Dialate",
"R_Nostril_Dialate"
]

controls_face_cheek_poses = [
"CheekRaise",
"CheekPuff",
]

controls_face_mouth_poses =  [
"JawOpenClose",
"JawLeftRight",
"LipPart",
"L_UpperLipRaise",
"R_UpperLipRaise",
"L_LipCornerDown",
"R_LipCornerDown",
"L_LipStretch",
"R_LipStretch",
"L_LowerLipDrop",
"R_LowerLipDrop",
"L_LipCornerPull",
"R_LipCornerPull",
"L_LipPucker",
"R_LipPucker",
"L_LipFunneler",
"R_LipFunneler",
"L_LipUpperPressor",
"L_LipLowerPressor",
"R_LipUpperPressor",
"R_LipLowerPressor",
"L_LipUpperSuckIn",
"L_LipLowerSuckIn",
"R_LipUpperSuckIn",
"R_LipLowerSuckIn",
"L_ChinRaiser",
"R_ChinRaiser"
]

controls_face_poses = [
"Neutral",
"L_Ear_Up_Down",
"L_Ear_Back",
"R_Ear_Up_Down",
"R_Ear_Back"
]


#---- Werewolf pose names
controls_werewolf_mouth_poses =  [
"JawOpenClose",
"JawLeftRight",
"JawTwist",
"L_LipStretch",
"R_LipStretch",
"L_narrow",
"R_narrow",
"L_LowerLipDown",
"R_LowerLipDown"
]

controls_werewolf_poses = [
"L_Ear_Up_Down",
"R_Ear_Up_Down",
"R_Ear_Back",
"L_Ear_Back",
"L_Ear_Twist",
"R_Ear_Twist"
]

spaces = ['head_world_space',
          'head_main_ctrl_space',
          'head_chest_space',
          'head_hip_ctrl_Space',
          'head_body_attach_space']

pymelLogger.debug('Imported: Names')

        