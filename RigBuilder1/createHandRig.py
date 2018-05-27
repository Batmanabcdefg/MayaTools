from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *

"""
Copyright (c) 2010 Mauricio Santos
Name: createHandRig.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created:   22 Oct 2010


$Revision: 136 $
$LastChangedDate: 2011-08-29 01:35:29 -0700 (Mon, 29 Aug 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/createHandRig.py $
$Id: createHandRig.py 136 2011-08-29 08:35:29Z mauricio $

Description: 
    Given:
        Uses finger joints defined by createRigJoints.py.
        Rigs the finger joints to have channel box attributes and
        fk controllers on the joints. They work independently of
        one another.
        
        It's advised to work with only one at a time. However, having the option
        is nice.
    
    How:
        Using joints created by createRigJoints.py, calls: 
        createFingersOrToesRig.createFingersOrToesRig()
        
Used by: createArmRig.py

Uses:

Process:
    
Additional Notes: 

Example call:
    import createHandRig
    createHandRig.createHandRig( label = 'l_hand',
                                       control = 'l_Hand_cnt',
                                       side = 1,
                                       curl = self.curl,
                                       twist = self.twist,
                                       spread = self.spread,
                                       fkNormal = self.fkNormal,
                                       radius = self.fkRadius/2.0  )
    
Attributes:
    createdNodes = list of created nodes.

Keywords:
        self.label = keywords['label']
        self.control = keywords['control']
        self.side = 1 or 2 / left or right
        self.wrsitJnt = keywords['wristJnt'] ( Wrist joint that follows Ik/Fk arms.)
        
        # Characters (X,Y,Z)
        self.curl = keywords['curl']    
        self.twist = keywords['twist']
        self.spread = keywords['up']
        
Requires:

Development notes:

    @Todo   - Thumb/Pinky/Palm cup 
            -  
    
"""
import createFingersOrToesRig
import standardNames
import orientSwitch    

# During development
reload( createFingersOrToesRig )

class createHandRig():
    """
        Uses finger joints defined by createRigJoints.py.
        
        Rigs the finger joints to have channel box attributes and
        fk controllers on the joints. They work independently of
        one another.
        
        It's advised to work with only one at a time. However, having the option
        is nice.
        
        Notes:
            Perhaps, there is a way to have changes on the control curve rotation
            update the channel box attributes, and yet they can both be set by user?
            
            Maybe a script fires on control curve selection that says:
                -set channel box attribute to rotations of the curve
            
            And a change command on the channel box attribute the says:
                -when set, set rotations on control curve
                
            But for each finger? Sounds heavy in computations/script/expression calls.

    """
    def __init__(self,**keywords):
        # Standard names object
        self.sNames = standardNames.standardNames()
        
        # Used to store names of all created nodes, 
        # to be returned when the tool is done.
        self.createdNodes = [] 
        
        # Command line call
        self.commandlineCall(keywords)

            
    def commandlineCall(self,keywords):
        """
        Verify and Store the data passed via command line keywords dictionary.
        """        
        self.l_wristFollowJnt = keywords['l_wristFollowJnt']
        self.r_wristFollowJnt = keywords['r_wristFollowJnt']

        self.curl = keywords['curl']
        self.twist = keywords['twist']
        self.spread = keywords['spread']
        
        self.fkNormal = keywords['fkNormal']     
        self.radius = keywords['radius']
        
        self.create()


    def create(self,*args):
        """
        Given input, create the hand rig.
        """        
        # Names derived from keys in standard joint names dictionary.
        
        #--- Setup orient switch on hand controls
        self.orientConstraintOnHands()
        
        #--- Setup the palm cup / bend on the hand controls.
        self.palmSetup()
        
        # Left
        jntNames = self.sNames.handJoints.keys()
        
        temp = self.sNames.handJoints['left_pinky1'].split('_')
        leftAttName1 = temp[1]
        temp = self.sNames.handJoints['left_ring1'].split('_')
        leftAttName2 = temp[1]
        temp = self.sNames.handJoints['left_middle1'].split('_')
        leftAttName3 = temp[1]
        temp = self.sNames.handJoints['left_index1'].split('_')
        leftAttName4 = temp[1]
        temp = self.sNames.handJoints['left_thumb1'].split('_')
        leftAttName5 = temp[1]
        
        leftAttNames = [leftAttName1,
                           leftAttName2,
                           leftAttName3,
                           leftAttName4,
                           leftAttName5 ] 
        
        leftStartJoints = [self.sNames.handJoints['left_pinky1'],
                           self.sNames.handJoints['left_ring1'],
                           self.sNames.handJoints['left_middle1'],
                           self.sNames.handJoints['left_index1'],
                           self.sNames.handJoints['left_thumb1'] ] 
        
        leftEndJoints = [self.sNames.handJoints['left_pinky3'],
                           self.sNames.handJoints['left_ring3'],
                           self.sNames.handJoints['left_middle3'],
                           self.sNames.handJoints['left_index3'],
                           self.sNames.handJoints['left_thumb3'] ]
        
        # Right
        temp = self.sNames.handJoints['right_pinky1'].split('_')
        rightAttName1 = temp[1]
        temp = self.sNames.handJoints['right_ring1'].split('_')
        rightAttName2 = temp[1]
        temp = self.sNames.handJoints['right_middle1'].split('_')
        rightAttName3 = temp[1]
        temp = self.sNames.handJoints['right_index1'].split('_')
        rightAttName4 = temp[1]
        temp = self.sNames.handJoints['right_thumb1'].split('_')
        rightAttName5 = temp[1]
        
        rightAttNames = [rightAttName1,
                           rightAttName2,
                           rightAttName3,
                           rightAttName4,
                           rightAttName5 ] 
        
        rightStartJoints = [self.sNames.handJoints['right_pinky1'],
                           self.sNames.handJoints['right_ring1'],
                           self.sNames.handJoints['right_middle1'],
                           self.sNames.handJoints['right_index1'],
                           self.sNames.handJoints['right_thumb1'] ] 
        
        rightEndJoints = [self.sNames.handJoints['right_pinky3'],
                           self.sNames.handJoints['right_ring3'],
                           self.sNames.handJoints['right_middle3'],
                           self.sNames.handJoints['right_index3'],
                           self.sNames.handJoints['right_thumb3'] ]
        
        #--- Create the controllers and attributes
        # Left
        createFingersOrToesRig.createFingersOrToesRig( label = '%s_hand'%self.sNames.prefix['left'],  
                                                       control = self.sNames.controlNames['left_hand'],
                                                       attNames = leftAttNames,
                                                       startJnts = leftStartJoints,
                                                       endJnts = leftEndJoints,
                                                       curl = self.curl,
                                                       twist = self.twist,
                                                       spread = self.spread,
                                                       fkNormal = self.fkNormal,
                                                       radius = self.radius )
        
        # Right
        createFingersOrToesRig.createFingersOrToesRig( label = '%s_hand'%self.sNames.prefix['right'],  
                                                       control = self.sNames.controlNames['right_hand'],
                                                       attNames = rightAttNames,
                                                       startJnts = rightStartJoints,
                                                       endJnts = rightEndJoints,
                                                       curl = self.curl,
                                                       twist = self.twist,
                                                       spread = self.spread,
                                                       fkNormal = self.fkNormal,
                                                       radius = self.radius )
        
        #--- Setup All Spread SDK
        # Left side
        count = 0
        for jnt in leftStartJoints:
            if count == 0: # Pinky
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['left_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 0,
                                v = 0 )
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['left_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 10,
                                v = 50 )
            if count == 1: # Ring
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['left_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 0,
                                v = 0 )
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['left_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 10,
                                v = 30 )
            if count == 2: # middle
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['left_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 0,
                                v = 0 )
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['left_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 10,
                                v = -5 )
            if count == 3: # index
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['left_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 0,
                                v = 0 )
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['left_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 10,
                                v = -40 )
            if count == 4: # index
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['left_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 0,
                                v = 0 )
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['left_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 10,
                                v = -40 )
            count += 1

        # Right side
        count = 0
        for jnt in rightStartJoints:
            if count == 0: # Pinky
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['right_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 0,
                                v = 0 )
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['right_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 10,
                                v = 50 )
            if count == 1: # Ring
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['right_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 0,
                                v = 0 )
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['right_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 10,
                                v = 30 )
            if count == 2: # middle
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['right_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 0,
                                v = 0 )
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['right_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 10,
                                v = -5 )
            if count == 3: # index
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['right_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 0,
                                v = 0 )
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['right_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 10,
                                v = -40 )
            if count == 4: # index
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['right_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 0,
                                v = 0 )
                setDrivenKeyframe( jnt, 
                                cd=self.sNames.controlNames['right_hand'] + '.spread_all',
                                at= "rotate%s"%self.spread,
                                dv = 10,
                                v = -40 )
            count += 1

        
        #--- Setup left hand       
        # Lock the translations for the hand
        setAttr( '%s.translateX'%self.sNames.armJoints['left_wrist'], lock=True, keyable=False )
        setAttr( '%s.translateY'%self.sNames.armJoints['left_wrist'], lock=True, keyable=False )
        setAttr( '%s.translateZ'%self.sNames.armJoints['left_wrist'], lock=True, keyable=False )
        
        #--- Setup right hand    
        # Lock the translations for the hand
        setAttr('%s.translateX'%self.sNames.armJoints['right_wrist'], lock=True, keyable=False)
        setAttr('%s.translateY'%self.sNames.armJoints['right_wrist'], lock=True, keyable=False)
        setAttr('%s.translateZ'%self.sNames.armJoints['right_wrist'], lock=True, keyable=False)
        
        #--- Left / Right Hand Control Setup
        # Orient Constrain the follow joints to the Hand Controller
        orientConstraint(self.sNames.controlNames['right_hand'],self.r_wristFollowJnt,mo=True)
        orientConstraint(self.sNames.controlNames['left_hand'],self.l_wristFollowJnt,mo=True)

        # Point constrain Hand cnt buffer nodes to wrist follow joints
        pointConstraint( self.sNames.armJoints['left_wrist'],'%s_buffer' % self.sNames.controlNames['left_hand'], mo=True)
        pointConstraint( self.sNames.armJoints['right_wrist'],'%s_buffer' % self.sNames.controlNames['right_hand'], mo=True)
        
        # Parent buffer node to the main control
        parent('%s_buffer' % self.sNames.controlNames['left_hand'], self.sNames.controlNames['main'])
        parent('%s_buffer' % self.sNames.controlNames['right_hand'], self.sNames.controlNames['main'])
        
    def palmSetup(self):
        """ Setup the Cup / Bend on left/right Hand controls. """
        #--- Store the names.
        l_palm_jnt = self.sNames.handJoints['left_palm']
        l_pinky_base_jnt = self.sNames.handJoints['left_pinky_base']
        r_palm_jnt = self.sNames.handJoints['right_palm']
        r_pinky_base_jnt = self.sNames.handJoints['right_pinky_base']
        
        #--- orient the pinky base joint to match parent
        joint(self.sNames.handJoints['left_pinky_base'],edit=True,oj='none')
        joint(self.sNames.handJoints['right_pinky_base'],edit=True,oj='none')
        
        #--- Create attribute on controllers  
        # Left
        addAttr(self.sNames.controlNames['left_hand'],
            at='long',
            longName='palm',k=True)
        
        setAttr(self.sNames.controlNames['left_hand'] + '.palm',lock=True)
          
        addAttr(self.sNames.controlNames['left_hand'],
            at='long',
            longName='palm_cup',k=True,
            hasMaxValue=True, hasMinValue=True,
            maxValue=10,minValue=-10)
        
        addAttr(self.sNames.controlNames['left_hand'],
            at='long',
            longName='palm_bend',k=True)
        
        # Right
        addAttr(self.sNames.controlNames['right_hand'],
            at='long',
            longName='palm',k=True)
        
        setAttr(self.sNames.controlNames['right_hand'] + '.palm',lock=True)
          
        addAttr(self.sNames.controlNames['right_hand'],
            at='long',
            longName='palm_cup',k=True,
            hasMaxValue=True, hasMinValue=True,
            maxValue=10,minValue=-10)
        
        addAttr(self.sNames.controlNames['right_hand'],
            at='long',
            longName='palm_bend',k=True)   
        
        #--- Cup SDKs
        # Left palm joint
        setDrivenKeyframe( l_palm_jnt, 
                           cd=self.sNames.controlNames['left_hand'] + '.palm_cup',  
                           at= "rotateX", 
                           dv = 0,
                           v = 0 )
        setDrivenKeyframe( l_palm_jnt, 
                           cd=self.sNames.controlNames['left_hand'] + '.palm_cup',  
                           at= "rotateX", 
                           dv = 10,
                           v = 45 )
        setDrivenKeyframe( l_palm_jnt, 
                           cd=self.sNames.controlNames['left_hand'] + '.palm_cup',  
                           at= "rotateX", 
                           dv = -10,
                           v = -15 )
        # Left pinky base joint
        setDrivenKeyframe( l_pinky_base_jnt, 
                           cd=self.sNames.controlNames['left_hand'] + '.palm_cup',  
                           at= "rotateX", 
                           dv = 0,
                           v = 0 )
        setDrivenKeyframe( l_pinky_base_jnt, 
                           cd=self.sNames.controlNames['left_hand'] + '.palm_cup',  
                           at= "rotateX", 
                           dv = 10,
                           v = -90 )
        setDrivenKeyframe( l_pinky_base_jnt, 
                           cd=self.sNames.controlNames['left_hand'] + '.palm_cup',  
                           at= "rotateX", 
                           dv = -10,
                           v = 30 )
        
        # Right palm joint
        setDrivenKeyframe( l_palm_jnt, 
                           cd=self.sNames.controlNames['right_hand'] + '.palm_cup',  
                           at= "rotateX", 
                           dv = 0,
                           v = 0 )
        setDrivenKeyframe( l_palm_jnt, 
                           cd=self.sNames.controlNames['right_hand'] + '.palm_cup',  
                           at= "rotateX", 
                           dv = 10,
                           v = 45 )
        setDrivenKeyframe( l_palm_jnt, 
                           cd=self.sNames.controlNames['right_hand'] + '.palm_cup',  
                           at= "rotateX", 
                           dv = -10,
                           v = -15 )
        # Right pinky base joint
        setDrivenKeyframe( l_pinky_base_jnt, 
                           cd=self.sNames.controlNames['right_hand'] + '.palm_cup',  
                           at= "rotateX", 
                           dv = 0,
                           v = 0 )
        setDrivenKeyframe( l_pinky_base_jnt, 
                           cd=self.sNames.controlNames['right_hand'] + '.palm_cup',  
                           at= "rotateX", 
                           dv = 10,
                           v = -90 )
        setDrivenKeyframe( l_pinky_base_jnt, 
                           cd=self.sNames.controlNames['right_hand'] + '.palm_cup',  
                           at= "rotateX", 
                           dv = -10,
                           v = 30 )
        
        #--- Bend direct connection
        connectAttr(self.sNames.controlNames['left_hand'] + '.palm_bend', l_palm_jnt + '.rotate' + self.curl, f=True)
        connectAttr(self.sNames.controlNames['right_hand'] + '.palm_bend', r_palm_jnt + '.rotate' + self.curl, f=True)
        
        
    def orientConstraintOnHands(self, *args):
        """
        Create an orient constrain on the hands controls to either follow the rig world
        orientations or those of the bind elbow (local).
        
        """
        #--- Left hand
        #--- Create locator with matching orientations as main and hand cntrl buffer
        loc = spaceLocator(n='leftHandOrient_loc')
        setAttr('%s.visibility'%loc,0)
        
        #--- Snap locator to elbow
        temp = pointConstraint(self.sNames.armJoints['left_elbow'],loc,mo=False)
        delete(temp)
        
        #--- Parent locator to the elbow
        parent(loc,self.sNames.armJoints['left_elbow'])
        
        temp = pickWalk(self.sNames.controlNames['left_hand'],direction='up')
        constObj = pickWalk(temp,direction='up')
        
        orientSwitch.orientSwitch(   constObj=constObj,
                            control=self.sNames.controlNames['left_hand'],
                            attName='orientation',
                            op1Name='local',
                            op2Name='world',
                            op3Name='',
                            op4Name='',
                            op5Name='',
                            op6Name='',
                            op7Name='',
                            op8Name='',
                            object1=loc,
                            object2=self.sNames.controlNames['main'],
                            object3='',
                            object4='',
                            object5='',
                            object6='',
                            object7='',
                            object8='')

        #--- Right hand
        #--- Create locator with matching orientations as main and hand cntrl buffer
        loc = spaceLocator(n='rightHandOrient_loc')
        setAttr('%s.visibility'%loc,0)
        
        #--- Snap locator to elbow
        temp = pointConstraint(self.sNames.armJoints['right_elbow'],loc,mo=False)
        delete(temp)
        
        #--- Parent locator to the elbow
        parent(loc,self.sNames.armJoints['right_elbow'])
        
        temp = pickWalk( self.sNames.controlNames['right_hand'], direction='up' )
        constObj = pickWalk( temp, direction='up' )
        
        orientSwitch.orientSwitch(   constObj=constObj,
                            control=self.sNames.controlNames['right_hand'],
                            attName='orientation',
                            op1Name='local',
                            op2Name='world',
                            op3Name='',
                            op4Name='',
                            op5Name='',
                            op6Name='',
                            op7Name='',
                            op8Name='',
                            object1=loc,
                            object2=self.sNames.controlNames['main'],
                            object3='',
                            object4='',
                            object5='',
                            object6='',
                            object7='',
                            object8=''  )
        
        #--- Set attributtes to world
        setAttr( '%s.world'%self.sNames.controlNames['left_hand'],1)
        setAttr( '%s.world'%self.sNames.controlNames['right_hand'],1)  
        