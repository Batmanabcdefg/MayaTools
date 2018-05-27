"""
Copyright (c) 2010,2011 Mauricio Santos-Hoyos
Name: standardNames.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 8 Nov 2010

$Revision: 140 $
$LastChangedDate: 2011-09-13 00:36:32 -0700 (Tue, 13 Sep 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/standardNames.py $
$Id: standardNames.py 140 2011-09-13 07:36:32Z mauricio $

Description:
    - Defines standard names as attributes in a class.
    - All other tools should use this object to name their nodes.


@ todo - To String: Print list of defined names and their variable

Additional Notes:

Development Notes:

   
Example call:
    import standardNames as sNames
    names = standardNames.createFullRig()
    
    # Create a bind joint with a standard name
    joint( p=(0,0,0), n = '%s_%s'%(sNames.rootJoint,sNames.self.suffix['bind'] )
"""

class standardNames():
    """
    -Defines standard names as attributes in a class.
    -All other tools should use this object to name their nodes.
    """
    def __init__(self,**keywords):
        #--- Prefixes
        self.prefix = {}
        self.prefix['name'] = '' # Name used as unique self.prefix 
        self.prefix['left'] = 'l'
        self.prefix['right'] = 'r'
        
        #--- Suffixes
        self.suffix = {}
        self.suffix['joint'] = 'jnt'
        self.suffix['group'] = 'grp'
        self.suffix['control'] = 'cnt'
        self.suffix['bind'] = 'bind'
        self.suffix['ik'] = 'ik'
        self.suffix['fk'] = 'fk'
        self.suffix['follow'] = 'follow'
        
        #--- Control names 
        self.controlNames = {}
        self.controlNames['main'] = 'main_cnt'
        self.controlNames['geo_vis'] = 'geo_vis'
        self.controlNames['cnt_vis'] = 'control_vis'
        
        self.controlNames['head'] = 'head_cnt'
        self.controlNames['jaw'] = 'jaw_cnt'
        self.controlNames['shoulder'] = 'shoulder_cnt'
        self.controlNames['top_teeth'] = 'top_teeth_cnt'
        self.controlNames['btm_teeth'] = 'btm_teeth_cnt'
        self.controlNames['left_ear'] = self.prefix['left'] + '_ear_cnt'
        self.controlNames['right_ear'] = self.prefix['right'] + '_ear_cnt'
        
        #--- Left side
        # Arms
        self.controlNames['left_clav'] = '%s_clav_cnt'%self.prefix['left']
        self.controlNames['left_fkShoulder'] = '%s_fkShldr_cnt'%self.prefix['left']
        self.controlNames['left_fkElbow'] = '%s_fkElbow_cnt'%self.prefix['left']
        self.controlNames['left_fkWrist'] = '%s_fkWrist_cnt'%self.prefix['left']
        
        self.controlNames['left_hand'] = '%s_hand_cnt'%self.prefix['left']
        self.controlNames['left_armIk'] = '%s_armIK_cnt'%self.prefix['left']
        
        # Legs
        self.controlNames['left_fkThigh'] = '%s_fkThigh_cnt'%self.prefix['left']
        self.controlNames['left_fkKnee'] = '%s_fkKnee_cnt'%self.prefix['left']
        self.controlNames['left_fkAnkle'] = '%s_fkAnkle_cnt'%self.prefix['left']
        self.controlNames['left_fkFootBall'] = '%s_fkFootBall_cnt'%self.prefix['left']
        self.controlNames['left_fkFootToe'] = '%s_fkFootToe_cnt'%self.prefix['left']
        
        self.controlNames['left_foot'] = '%s_foot_cnt'%self.prefix['left']
        self.controlNames['left_footIk'] = '%s_legIk_cnt'%self.prefix['left']
        self.controlNames['left_toe'] = '%s_toe_cnt_crv'%self.prefix['left']
        
        #--- Right side
        # Arms
        self.controlNames['right_clav'] = '%s_clav_cnt'%self.prefix['right']
        self.controlNames['right_fkShoulder'] = '%s_fkShldr_cnt'%self.prefix['right']
        self.controlNames['right_fkElbow'] = '%s_fkElbow_cnt'%self.prefix['right']
        self.controlNames['right_fkWrist'] = '%s_fkWrist_cnt'%self.prefix['right']
        
        self.controlNames['right_hand'] = '%s_hand_cnt'%self.prefix['right']
        self.controlNames['right_armIk'] = '%s_armIK_cnt'%self.prefix['right']
        
        # Legs
        self.controlNames['right_fkThigh'] = '%s_fkThigh_cnt'%self.prefix['right']
        self.controlNames['right_fkKnee'] = '%s_fkKnee_cnt'%self.prefix['right']
        self.controlNames['right_fkAnkle'] = '%s_fkAnkle_cnt'%self.prefix['right']
        self.controlNames['right_fkFootBall'] = '%s_fkFootBall_cnt'%self.prefix['right']
        self.controlNames['right_fkFootToe'] = '%s_fkFootToe_cnt'%self.prefix['right']
        
        self.controlNames['right_foot'] = '%s_Foot_cnt'%self.prefix['right']
        self.controlNames['right_footIk'] = '%s_legIk_cnt'%self.prefix['right']
        self.controlNames['right_toe'] = '%s_toe_cnt_crv'%self.prefix['right']
        
        # Hand/Foot controls and Arm/Leg Ik controls
        self.controlNames['cog'] = 'cog_cnt'
        self.controlNames['hip'] = 'hips_cnt'
        self.controlNames['head'] = 'head_cnt'
        
        self.controlNames['eyes_follow'] = 'eyes_follow_cnt'
        self.controlNames['left_eye_aim'] = '%s_eye_follow_cnt'%self.prefix['left']
        self.controlNames['right_eye_aim'] = '%s_eye_follow_cnt'%self.prefix['right']
        self.controlNames['left_eye_fk'] = '%s_eye_cnt'%self.prefix['left']
        self.controlNames['right_eye_fk'] = '%s_eye_cnt'%self.prefix['right']
        
        #--- Joint names
        # Single joints defined as strings
        self.rootJoint = 'root_%s'%self.suffix['joint']
        self.hipJoint = 'hips_%s'%self.suffix['joint']
        
        #--- Head joints
        self.headJoints = {}
        self.headJoints['head'] = 'head_%s'%self.suffix['joint']
        self.headJoints['jaw'] = 'jaw_%s'%self.suffix['joint']
        self.headJoints['left_eye'] = '%s_eye_%s'%(self.prefix['left'],self.suffix['joint'])
        self.headJoints['right_eye'] = '%s_eye_%s'%(self.prefix['right'],self.suffix['joint'])
        self.headJoints['left_ear'] = '%s_ear_%s'%(self.prefix['left'],self.suffix['joint'])
        self.headJoints['right_ear'] = '%s_ear_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.headJoints['neck1'] = 'neck1_%s'%(self.suffix['joint'])  
        self.headJoints['neck2'] = 'neck2_%s'%(self.suffix['joint'])         
        
        #--- Arm joints
        self.armJoints = {}
        self.armJoints['left_clav'] = '%s_clav_%s'%(self.prefix['left'],self.suffix['joint'])
        self.armJoints['left_shoulder'] = '%s_shldr_%s'%(self.prefix['left'],self.suffix['joint'])
        self.armJoints['left_elbow'] = '%s_elbow_%s'%(self.prefix['left'],self.suffix['joint'])
        self.armJoints['left_wrist'] = '%s_wrist_%s'%(self.prefix['left'],self.suffix['joint'])
        
        self.armJoints['right_clav'] = '%s_clav_%s'%(self.prefix['right'],self.suffix['joint'])
        self.armJoints['right_shoulder'] = '%s_shldr_%s'%(self.prefix['right'],self.suffix['joint'])
        self.armJoints['right_elbow'] = '%s_elbow_%s'%(self.prefix['right'],self.suffix['joint'])
        self.armJoints['right_wrist'] = '%s_wrist_%s'%(self.prefix['right'],self.suffix['joint'])
        
        #--- Leg joints
        self.legJoints = {}
        self.legJoints['left_thigh'] = '%s_thigh_%s'%(self.prefix['left'],self.suffix['joint'])
        self.legJoints['left_knee'] = '%s_knee_%s'%(self.prefix['left'],self.suffix['joint'])
        self.legJoints['left_ankle'] = '%s_ankle_%s'%(self.prefix['left'],self.suffix['joint'])
        
        self.legJoints['right_thigh'] = '%s_thigh_%s'%(self.prefix['right'],self.suffix['joint'])
        self.legJoints['right_knee'] = '%s_knee_%s'%(self.prefix['right'],self.suffix['joint'])
        self.legJoints['right_ankle'] = '%s_ankle_%s'%(self.prefix['right'],self.suffix['joint'])
        
        #--- Hand joints
        self.handJoints = {}
        
        # Left hand
        self.handJoints['left_palm'] = '%s_palm_%s'%(self.prefix['left'],self.suffix['joint'])
        
        self.handJoints['left_pinky_base'] = '%s_pinky_base_%s'%(self.prefix['left'],self.suffix['joint'])
        self.handJoints['left_pinky1'] = '%s_pinky1_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.handJoints['left_pinky2'] = '%s_pinky2_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.handJoints['left_pinky3'] = '%s_pinky3_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.handJoints['left_pinky4'] = '%s_pinky4_%s'%(self.prefix['left'],self.suffix['joint']) 
        
        self.handJoints['left_ring1'] = '%s_ring1_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.handJoints['left_ring2'] = '%s_ring2_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.handJoints['left_ring3'] = '%s_ring3_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.handJoints['left_ring4'] = '%s_ring4_%s'%(self.prefix['left'],self.suffix['joint'])
        
        self.handJoints['left_middle1'] = '%s_middle1_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.handJoints['left_middle2'] = '%s_middle2_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.handJoints['left_middle3'] = '%s_middle3_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.handJoints['left_middle4'] = '%s_middle4_%s'%(self.prefix['left'],self.suffix['joint'])
        
        self.handJoints['left_index1'] = '%s_index1_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.handJoints['left_index2'] = '%s_index2_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.handJoints['left_index3'] = '%s_index3_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.handJoints['left_index4'] = '%s_index4_%s'%(self.prefix['left'],self.suffix['joint'])
        
        self.handJoints['left_thumb1'] = '%s_thumb1_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.handJoints['left_thumb2'] = '%s_thumb2_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.handJoints['left_thumb3'] = '%s_thumb3_%s'%(self.prefix['left'],self.suffix['joint'])
        self.handJoints['left_thumb4'] = '%s_thumb4_%s'%(self.prefix['left'],self.suffix['joint'])
        self.handJoints['left_thumb5'] = '%s_thumb5_%s'%(self.prefix['left'],self.suffix['joint'])
        
        # Right hand
        self.handJoints['right_palm'] = '%s_palm_%s'%(self.prefix['right'],self.suffix['joint']) 
        
        self.handJoints['right_pinky_base'] = '%s_pinky_base_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.handJoints['right_pinky1'] = '%s_pinky1_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.handJoints['right_pinky2'] = '%s_pinky2_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.handJoints['right_pinky3'] = '%s_pinky3_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.handJoints['right_pinky4'] = '%s_pinky4_%s'%(self.prefix['right'],self.suffix['joint']) 
        
        self.handJoints['right_ring1'] = '%s_ring1_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.handJoints['right_ring2'] = '%s_ring2_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.handJoints['right_ring3'] = '%s_ring3_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.handJoints['right_ring4'] = '%s_ring4_%s'%(self.prefix['right'],self.suffix['joint'])
        
        self.handJoints['right_middle1'] = '%s_middle1_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.handJoints['right_middle2'] = '%s_middle2_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.handJoints['right_middle3'] = '%s_middle3_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.handJoints['right_middle4'] = '%s_middle4_%s'%(self.prefix['right'],self.suffix['joint'])
        
        self.handJoints['right_index1'] = '%s_index1_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.handJoints['right_index2'] = '%s_index2_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.handJoints['right_index3'] = '%s_index3_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.handJoints['right_index4'] = '%s_index4_%s'%(self.prefix['right'],self.suffix['joint'])
        
        self.handJoints['right_thumb1'] = '%s_thumb1_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.handJoints['right_thumb2'] = '%s_thumb2_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.handJoints['right_thumb3'] = '%s_thumb3_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.handJoints['right_thumb4'] = '%s_thumb4_%s'%(self.prefix['right'],self.suffix['joint'])
        self.handJoints['right_thumb5'] = '%s_thumb5_%s'%(self.prefix['right'],self.suffix['joint'])
        
        #--- Foot joints
        self.feetJoints = {}
        
        # Left foot
        self.feetJoints['left_footBall'] = '%s_footBall_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.feetJoints['left_footToe'] = '%s_footToe_%s'%(self.prefix['left'],self.suffix['joint']) 
        
        self.feetJoints['left_pinkyToe1'] = '%s_pinkyToe1_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.feetJoints['left_pinkyToe2'] = '%s_pinkyToe2_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.feetJoints['left_pinkyToe3'] = '%s_pinkyToe3_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.feetJoints['left_pinkyToe4'] = '%s_pinkyToe4_%s'%(self.prefix['left'],self.suffix['joint']) 
        
        self.feetJoints['left_ringToe1'] = '%s_ringToe1_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.feetJoints['left_ringToe2'] = '%s_ringToe2_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.feetJoints['left_ringToe3'] = '%s_ringToe3_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.feetJoints['left_ringToe4'] = '%s_ringToe4_%s'%(self.prefix['left'],self.suffix['joint'])
        
        self.feetJoints['left_middleToe1'] = '%s_middleToe1_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.feetJoints['left_middleToe2'] = '%s_middleToe2_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.feetJoints['left_middleToe3'] = '%s_middleToe3_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.feetJoints['left_middleToe4'] = '%s_middleToe4_%s'%(self.prefix['left'],self.suffix['joint'])
        
        self.feetJoints['left_indexToe1'] = '%s_indexToe1_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.feetJoints['left_indexToe2'] = '%s_indexToe2_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.feetJoints['left_indexToe3'] = '%s_indexToe3_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.feetJoints['left_indexToe4'] = '%s_indexToe4_%s'%(self.prefix['left'],self.suffix['joint'])
        
        self.feetJoints['left_bigToe1'] = '%s_bigToe1_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.feetJoints['left_bigToe2'] = '%s_bigToe2_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.feetJoints['left_bigToe3'] = '%s_bigToe3_%s'%(self.prefix['left'],self.suffix['joint']) 
        self.feetJoints['left_bigToe4'] = '%s_bigToe4_%s'%(self.prefix['left'],self.suffix['joint'])
        self.feetJoints['left_bigToe5'] = '%s_bigToe5_%s'%(self.prefix['left'],self.suffix['joint'])
        
        # Right feet
        self.feetJoints['right_footBall'] = '%s_footBall_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.feetJoints['right_footToe'] = '%s_footToe_%s'%(self.prefix['right'],self.suffix['joint']) 
        
        self.feetJoints['right_pinkyToe1'] = '%s_pinkyToe1_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.feetJoints['right_pinkyToe2'] = '%s_pinkyToe2_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.feetJoints['right_pinkyToe3'] = '%s_pinkyToe3_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.feetJoints['right_pinkyToe4'] = '%s_pinkyToe4_%s'%(self.prefix['right'],self.suffix['joint']) 
        
        self.feetJoints['right_ringToe1'] = '%s_ringToe1_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.feetJoints['right_ringToe2'] = '%s_ringToe2_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.feetJoints['right_ringToe3'] = '%s_ringToe3_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.feetJoints['right_ringToe4'] = '%s_ringToe4_%s'%(self.prefix['right'],self.suffix['joint'])
        
        self.feetJoints['right_middleToe1'] = '%s_middleToe1_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.feetJoints['right_middleToe2'] = '%s_middleToe2_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.feetJoints['right_middleToe3'] = '%s_middleToe3_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.feetJoints['right_middleToe4'] = '%s_middleToe4_%s'%(self.prefix['right'],self.suffix['joint'])
        
        self.feetJoints['right_indexToe1'] = '%s_indexToe1_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.feetJoints['right_indexToe2'] = '%s_indexToe2_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.feetJoints['right_indexToe3'] = '%s_indexToe3_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.feetJoints['right_indexToe4'] = '%s_indexToe4_%s'%(self.prefix['right'],self.suffix['joint'])
        
        self.feetJoints['right_bigToe1'] = '%s_bigToe1_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.feetJoints['right_bigToe2'] = '%s_bigToe2_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.feetJoints['right_bigToe3'] = '%s_bigToe3_%s'%(self.prefix['right'],self.suffix['joint']) 
        self.feetJoints['right_bigToe4'] = '%s_bigToe4_%s'%(self.prefix['right'],self.suffix['joint'])
        self.feetJoints['right_bigToe5'] = '%s_bigToe5_%s'%(self.prefix['right'],self.suffix['joint']) 
        
        # Back joints
        self.backJoints = {}
        self.backJoints['start'] = 'backStart_%s'%self.suffix['joint']    
        self.backJoints['end'] = 'backEnd_%s'%self.suffix['joint'] 
        self.backJoints['back1'] = 'back1_%s'%self.suffix['joint']
        self.backJoints['back2'] = 'back2_%s'%self.suffix['joint']    
        self.backJoints['back3'] = 'back3_%s'%self.suffix['joint']    
        self.backJoints['back4'] = 'back4_%s'%self.suffix['joint']    
        self.backJoints['back5'] = 'back5_%s'%self.suffix['joint']    
        self.backJoints['back6'] = 'back6_%s'%self.suffix['joint']    
        self.backJoints['back7'] = 'back7_%s'%self.suffix['joint']   
        self.backJoints['back8'] = 'back8_%s'%self.suffix['joint']
        self.backJoints['back9'] = 'back9_%s'%self.suffix['joint']
        self.backJoints['back10'] = 'back10_%s'%self.suffix['joint'] 
        
        
        
        
        
        
        
        
        
        
        