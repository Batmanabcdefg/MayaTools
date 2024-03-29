from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *

"""
Copyright (c) 2010 Mauricio Santos-Hoyos
Name: createRigJoints.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 10 Nov 2010

$Revision: 140 $
$LastChangedDate: 2011-09-13 00:36:32 -0700 (Tue, 13 Sep 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/createRigJoints.py $
$Id: createRigJoints.py 140 2011-09-13 07:36:32Z mauricio $

Description: 
    -Create bind joints using naming defined in standardNames.py
    -Relies on locators defined in placeLocators.py


@todo    

Additional Notes:

Development Notes:

   
Example call:

"""

import standardNames

reload( standardNames )

class createRigJoints():
    """
    - Create bind joints using naming defined in standardNames.py
    - Relies on locators named and created in placeLocators.py
    """
    def __init__(self,**keywords):
        """
        Build the bind skeleton
        """
        # Store command line data
        self.orientation = keywords['orientation'] # String, i.e. 'xyz'
        self.side = keywords['side']
        self.numToes = keywords['numToes']
        
        # Create standard names object
        self.sNames = standardNames.standardNames()
        
        # Store names of created joints
        self.rigJoints = []
        
        self.createJoints()
        
    def createJoints(self,*args):
        """
        Create joints at locator positions.
        """
        if self.side == 1:
            #--- Get positions from locators
            # Head joints
            head_pos = xform('head_loc',query=True, ws=True,t=True)
            neck2_pos = xform('neck_loc',query=True, ws=True,t=True)
            neck1_pos = xform('back_end_loc',query=True, ws=True,t=True)
            l_eye_pos = xform('l_eye_loc',query=True, ws=True,t=True)
            r_eye_pos = xform('r_eye_loc',query=True, ws=True,t=True)
            jaw_pos = xform('jaw_loc',query=True, ws=True,t=True)
            l_ear_pos = xform('l_ear_loc',query=True, ws=True,t=True)
            r_ear_pos = xform('r_ear_loc',query=True, ws=True,t=True)
            tongue1_pos = xform('tongue_loc_1',query=True, ws=True,t=True)
            tongue2_pos = xform('tongue_loc_2',query=True, ws=True,t=True)
            tongue3_pos = xform('tongue_loc_3',query=True, ws=True,t=True) 
    
            # Back/torso
            root_pos = xform('root_loc',query=True, ws=True,t=True)
            hip_pos = xform('root_loc',query=True, ws=True,t=True)
            backStart_pos = xform('root_loc',query=True, ws=True,t=True)
            back1_pos = xform('back_loc_1',query=True, ws=True,t=True)
            back2_pos = xform('back_loc_2',query=True, ws=True,t=True)
            back3_pos = xform('back_loc_3',query=True, ws=True,t=True)
            back4_pos = xform('back_loc_4',query=True, ws=True,t=True)
            back5_pos = xform('back_loc_5',query=True, ws=True,t=True)
            backEnd_pos = xform('back_end_loc',query=True, ws=True,t=True)
            
            # Left arm
            l_clav_pos = xform('l_clav_loc',query=True, ws=True,t=True)
            l_shoulder_pos = xform('l_shoulder_loc',query=True, ws=True,t=True)
            l_elbow_pos = xform('l_elbow_loc',query=True, ws=True,t=True)
            l_wrist_pos = xform('l_wrist_loc',query=True, ws=True,t=True)
            l_palm_pos = xform('l_palm_loc',query=True, ws=True,t=True)
            
            # Left hand
            l_pinky_base_pos = xform('l_pinky_base_loc',query=True, ws=True,t=True)
            l_pinky1_pos = xform('l_pinky_loc_1',query=True, ws=True,t=True)
            l_pinky2_pos = xform('l_pinky_loc_2',query=True, ws=True,t=True)
            l_pinky3_pos = xform('l_pinky_loc_3',query=True, ws=True,t=True)
            l_pinky4_pos = xform('l_pinky_loc_4',query=True, ws=True,t=True)
            
            l_ring1_pos = xform('l_ring_loc_1',query=True, ws=True,t=True)
            l_ring2_pos = xform('l_ring_loc_2',query=True, ws=True,t=True)
            l_ring3_pos = xform('l_ring_loc_3',query=True, ws=True,t=True)
            l_ring4_pos = xform('l_ring_loc_4',query=True, ws=True,t=True)
            
            l_middle1_pos = xform('l_middle_loc_1',query=True, ws=True,t=True)
            l_middle2_pos = xform('l_middle_loc_2',query=True, ws=True,t=True)
            l_middle3_pos = xform('l_middle_loc_3',query=True, ws=True,t=True)
            l_middle4_pos = xform('l_middle_loc_4',query=True, ws=True,t=True)
            
            l_index1_pos = xform('l_index_loc_1',query=True, ws=True,t=True)
            l_index2_pos = xform('l_index_loc_2',query=True, ws=True,t=True)
            l_index3_pos = xform('l_index_loc_3',query=True, ws=True,t=True)
            l_index4_pos = xform('l_index_loc_4',query=True, ws=True,t=True)
            
            l_thumb1_pos = xform('l_thumb_loc_1',query=True, ws=True,t=True)
            l_thumb2_pos = xform('l_thumb_loc_2',query=True, ws=True,t=True)
            l_thumb3_pos = xform('l_thumb_loc_3',query=True, ws=True,t=True)
            l_thumb4_pos = xform('l_thumb_loc_4',query=True, ws=True,t=True)
            
            # Left leg
            l_thigh_pos = xform('l_thigh_loc',query=True, ws=True,t=True)
            l_knee_pos = xform('l_knee_loc',query=True, ws=True,t=True)
            l_ankle_pos = xform('l_ankle_loc',query=True, ws=True,t=True)
            l_ball_pos = xform('l_ball_loc',query=True, ws=True,t=True)
            l_toe_pos = xform('l_toe_loc',query=True, ws=True,t=True)
            
            if self.numToes > 0:
                # Left foot
                l_pinkyToe1_pos = xform('l_pinkyToe_loc_1',query=True, ws=True,t=True)
                l_pinkyToe2_pos = xform('l_pinkyToe_loc_2',query=True, ws=True,t=True)
                l_pinkyToe3_pos = xform('l_pinkyToe_loc_3',query=True, ws=True,t=True)
                l_pinkyToe4_pos = xform('l_pinkyToe_loc_4',query=True, ws=True,t=True)
                
                l_ringToe1_pos = xform('l_ringToe_loc_1',query=True, ws=True,t=True)
                l_ringToe2_pos = xform('l_ringToe_loc_2',query=True, ws=True,t=True)
                l_ringToe3_pos = xform('l_ringToe_loc_3',query=True, ws=True,t=True)
                l_ringToe4_pos = xform('l_ringToe_loc_4',query=True, ws=True,t=True)
                
                l_middleToe1_pos = xform('l_middleToe_loc_1',query=True, ws=True,t=True)
                l_middleToe2_pos = xform('l_middleToe_loc_2',query=True, ws=True,t=True)
                l_middleToe3_pos = xform('l_middleToe_loc_3',query=True, ws=True,t=True)
                l_middleToe4_pos = xform('l_middleToe_loc_4',query=True, ws=True,t=True)
                
                l_indexToe1_pos = xform('l_indexToe_loc_1',query=True, ws=True,t=True)
                l_indexToe2_pos = xform('l_indexToe_loc_2',query=True, ws=True,t=True)
                l_indexToe3_pos = xform('l_indexToe_loc_3',query=True, ws=True,t=True)
                l_indexToe4_pos = xform('l_indexToe_loc_4',query=True, ws=True,t=True)
                
                l_thumbToe1_pos = xform('l_thumbToe_loc_1',query=True, ws=True,t=True)
                l_thumbToe2_pos = xform('l_thumbToe_loc_2',query=True, ws=True,t=True)
                l_thumbToe3_pos = xform('l_thumbToe_loc_3',query=True, ws=True,t=True)
                l_thumbToe4_pos = xform('l_thumbToe_loc_4',query=True, ws=True,t=True)    
            
            #--- Create the joints
            #@todo - Add tongue joints
            
            # Head joints
            select(clear=True)
            self.rigJoints.append( joint(p=neck1_pos,      n = self.sNames.headJoints['neck1']))
            #joint( self.sNames.headJoints['neck1'], edit=True, oj='none' )
            self.rigJoints.append( joint(p=neck2_pos,      n = self.sNames.headJoints['neck2'] ))
            #joint( self.sNames.headJoints['neck2'], edit=True, oj='none' )
            self.rigJoints.append( joint(p=head_pos,       n = self.sNames.headJoints['head'] ))
            #joint( self.sNames.headJoints['head'], edit=True, oj='none' )
            
            select(clear=True)
            self.rigJoints.append( joint(p=l_eye_pos,      n = self.sNames.headJoints['left_eye']))
            select(clear=True)
            self.rigJoints.append( joint(p=r_eye_pos,      n = self.sNames.headJoints['right_eye']))
            select(clear=True)
            self.rigJoints.append( joint(p=jaw_pos,        n = self.sNames.headJoints['jaw']))
            select(clear=True)
            self.rigJoints.append( joint(p=l_ear_pos,      n = self.sNames.headJoints['left_ear']))
            select(clear=True)
            self.rigJoints.append( joint(p=r_ear_pos,      n = self.sNames.headJoints['right_ear']))
            
            # Create the back/torso joints
            select(clear=True)
            self.rigJoints.append( joint(p=hip_pos,        n = self.sNames.hipJoint ))
            select(clear=True)
            self.rigJoints.append( joint(p=root_pos,       n = self.sNames.rootJoint ))
            self.rigJoints.append( joint(p=backStart_pos,  n = self.sNames.backJoints['start']))
            self.rigJoints.append( joint(p=back1_pos,      n = self.sNames.backJoints['back1']))
            self.rigJoints.append( joint(p=back2_pos,      n = self.sNames.backJoints['back2']))
            self.rigJoints.append( joint(p=back3_pos,      n = self.sNames.backJoints['back3']))
            self.rigJoints.append( joint(p=back4_pos,      n = self.sNames.backJoints['back4']))
            self.rigJoints.append( joint(p=back5_pos,      n = self.sNames.backJoints['back5']))
            self.rigJoints.append( joint(p=backEnd_pos,    n = self.sNames.backJoints['end']))
            
            #Create the left arm joints
            select(clear=True)
            self.rigJoints.append( joint(p=l_clav_pos,     n = self.sNames.armJoints['left_clav']))
            self.rigJoints.append( joint(p=l_shoulder_pos, n = self.sNames.armJoints['left_shoulder']))
            self.rigJoints.append( joint(p=l_elbow_pos,    n = self.sNames.armJoints['left_elbow']))
            self.rigJoints.append( joint(p=l_wrist_pos,    n = self.sNames.armJoints['left_wrist']))
            
            self.rigJoints.append( joint(p=l_palm_pos,    n = self.sNames.handJoints['left_palm']))
            self.rigJoints.append( joint(p=l_pinky_base_pos,    n = self.sNames.handJoints['left_pinky_base']))
            
            self.rigJoints.append( joint(p=l_pinky1_pos,   n = self.sNames.handJoints['left_pinky1']))
            self.rigJoints.append( joint(p=l_pinky2_pos,   n = self.sNames.handJoints['left_pinky2']))
            self.rigJoints.append( joint(p=l_pinky3_pos,   n = self.sNames.handJoints['left_pinky3']))
            self.rigJoints.append( joint(p=l_pinky4_pos,   n = self.sNames.handJoints['left_pinky4']))
            
            select(self.sNames.handJoints['left_palm'],r=True)
            self.rigJoints.append( joint(p=l_ring1_pos,   n = self.sNames.handJoints['left_ring1']))
            self.rigJoints.append( joint(p=l_ring2_pos,   n = self.sNames.handJoints['left_ring2']))
            self.rigJoints.append( joint(p=l_ring3_pos,   n = self.sNames.handJoints['left_ring3']))
            self.rigJoints.append( joint(p=l_ring4_pos,   n = self.sNames.handJoints['left_ring4']))
            
            select(self.sNames.handJoints['left_palm'],r=True)
            self.rigJoints.append( joint(p=l_middle1_pos,   n = self.sNames.handJoints['left_middle1']))
            self.rigJoints.append( joint(p=l_middle2_pos,   n = self.sNames.handJoints['left_middle2']))
            self.rigJoints.append( joint(p=l_middle3_pos,   n = self.sNames.handJoints['left_middle3']))
            self.rigJoints.append( joint(p=l_middle4_pos,   n = self.sNames.handJoints['left_middle4']))
            
            select(self.sNames.handJoints['left_palm'],r=True)
            self.rigJoints.append( joint(p=l_index1_pos,   n = self.sNames.handJoints['left_index1']))
            self.rigJoints.append( joint(p=l_index2_pos,   n = self.sNames.handJoints['left_index2']))
            self.rigJoints.append( joint(p=l_index3_pos,   n = self.sNames.handJoints['left_index3']))
            self.rigJoints.append( joint(p=l_index4_pos,   n = self.sNames.handJoints['left_index4']))
            
            select(self.sNames.armJoints['left_wrist'],r=True)
            self.rigJoints.append( joint(p=l_thumb1_pos,   n = self.sNames.handJoints['left_thumb1']))
            self.rigJoints.append( joint(p=l_thumb2_pos,   n = self.sNames.handJoints['left_thumb2']))
            self.rigJoints.append( joint(p=l_thumb3_pos,   n = self.sNames.handJoints['left_thumb3']))
            self.rigJoints.append( joint(p=l_thumb4_pos,   n = self.sNames.handJoints['left_thumb4']))
                  
            # Create the left legs
            select(clear=True)
            self.rigJoints.append( joint(p=l_thigh_pos,    n = self.sNames.legJoints['left_thigh']))
            self.rigJoints.append( joint(p=l_knee_pos,     n = self.sNames.legJoints['left_knee']))
            self.rigJoints.append( joint(p=l_ankle_pos,    n = self.sNames.legJoints['left_ankle']))
            self.rigJoints.append( joint(p=l_ball_pos,     n = self.sNames.feetJoints['left_footBall']))
            self.rigJoints.append( joint(p=l_toe_pos,      n = self.sNames.feetJoints['left_footToe']))
            
            if self.numToes > 0:
                select(self.sNames.feetJoints['left_footBall'],r=True)
                self.rigJoints.append( joint(p=l_pinkyToe1_pos,   n = self.sNames.feetJoints['left_pinkyToe1']))
                self.rigJoints.append( joint(p=l_pinkyToe2_pos,   n = self.sNames.feetJoints['left_pinkyToe2']))
                self.rigJoints.append( joint(p=l_pinkyToe3_pos,   n = self.sNames.feetJoints['left_pinkyToe3']))
                self.rigJoints.append( joint(p=l_pinkyToe4_pos,   n = self.sNames.feetJoints['left_pinkyToe4']))
                
                select(self.sNames.feetJoints['left_footBall'],r=True)
                self.rigJoints.append( joint(p=l_ringToe1_pos,   n = self.sNames.feetJoints['left_ringToe1']))
                self.rigJoints.append( joint(p=l_ringToe2_pos,   n = self.sNames.feetJoints['left_ringToe2']))
                self.rigJoints.append( joint(p=l_ringToe3_pos,   n = self.sNames.feetJoints['left_ringToe3']))
                self.rigJoints.append( joint(p=l_ringToe4_pos,   n = self.sNames.feetJoints['left_ringToe4']))
                
                select(self.sNames.feetJoints['left_footBall'],r=True)
                self.rigJoints.append( joint(p=l_middleToe1_pos,   n = self.sNames.feetJoints['left_middleToe1']))
                self.rigJoints.append( joint(p=l_middleToe2_pos,   n = self.sNames.feetJoints['left_middleToe2']))
                self.rigJoints.append( joint(p=l_middleToe3_pos,   n = self.sNames.feetJoints['left_middleToe3']))
                self.rigJoints.append( joint(p=l_middleToe4_pos,   n = self.sNames.feetJoints['left_middleToe4']))
                
                select(self.sNames.feetJoints['left_footBall'],r=True)
                self.rigJoints.append( joint(p=l_indexToe1_pos,   n = self.sNames.feetJoints['left_indexToe1']))
                self.rigJoints.append( joint(p=l_indexToe2_pos,   n = self.sNames.feetJoints['left_indexToe2']))
                self.rigJoints.append( joint(p=l_indexToe3_pos,   n = self.sNames.feetJoints['left_indexToe3']))
                self.rigJoints.append( joint(p=l_indexToe4_pos,   n = self.sNames.feetJoints['left_indexToe4']))
                
                select(self.sNames.feetJoints['left_footBall'],r=True)
                self.rigJoints.append( joint(p=l_thumbToe1_pos,   n = self.sNames.feetJoints['left_bigToe1']))
                self.rigJoints.append( joint(p=l_thumbToe2_pos,   n = self.sNames.feetJoints['left_bigToe2']))
                self.rigJoints.append( joint(p=l_thumbToe3_pos,   n = self.sNames.feetJoints['left_bigToe3']))
                self.rigJoints.append( joint(p=l_thumbToe4_pos,   n = self.sNames.feetJoints['left_bigToe4']))
            
            # Orient the joint chains
            joint(self.sNames.headJoints['neck1'],edit=True,oj=self.orientation,sao='yup',ch=True)
            joint(self.sNames.backJoints['start'],edit=True,oj=self.orientation,sao='yup',ch=True)
            joint(self.sNames.armJoints['left_clav'], edit=True, oj=self.orientation,sao='yup',ch=True)
            joint(self.sNames.legJoints['left_thigh'], edit=True, oj=self.orientation,sao='yup',ch=True)

        if self.side == 2:
            # Create the right arm joints
            select(clear=True)
            temp = mirrorJoint( self.sNames.armJoints['left_clav'], mirrorYZ=True, mirrorBehavior=True, searchReplace=('l_', 'r_') )
            for each in temp:
                self.rigJoints.append(each)
    
            # Create the right leg joints
            select(clear=True)
            temp = mirrorJoint( self.sNames.legJoints['left_thigh'], mirrorYZ=True, mirrorBehavior=True, searchReplace=('l_', 'r_') )
            
            # Fix: 'r_footBalr_jnt' back to 'r_footBall_jnt'
            rename('r_footBalr_jnt','r_footBall_jnt')
            
            for each in temp:
                if 'lr_' in each:
                    self.rigJoints.append('r_footBall_jnt')
                else:
                    self.rigJoints.append(each)

        select(clear=True)
        
        
        
        
        
        
        
        