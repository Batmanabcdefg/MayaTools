from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *
"""
Copyright (c) 2010,2011 Mauricio Santos
Name: createLegRig.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created:   22 Oct 2010

$Revision: 140 $
$LastChangedDate: 2011-09-13 00:36:32 -0700 (Tue, 13 Sep 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/createLegRig.py $
$Id: createLegRig.py 140 2011-09-13 07:36:32Z mauricio $

Description: 
    Creates a stretchy IK/FK leg rig with IK/FK matching.
    
    This script only concerns itself with thigh/knee/ankle joints.
    Foot joints( ball and toe ) are setup in createFootRig.py

Process:
    
    
Additional Notes: 

Example call:

        temp = createLegRig.createLegRig(    prefix = 'l_leg',
                                        side = 1,
                                        cog_cntrl = 'Cog_cnt',
                                        hips_cntrl = 'Hips_cnt',
                                        world_cntrl = 'Main_cnt',
                                        foot_cntrl = 'l_Foot_cnt',
                                        aim_axis = self.aimAxis,
                                        aim_polarity = self.aimPolarity,
                                        up_axis = self.upAxis,
                                        up_polarity = self.upPolarity,
                                        fkNormal_axis = self.fkNormal,
                                        fkRadius = self.fkRadius,
                                        rotateOrder = self.rotateOrder )
    
    self.leftArmNodes = temp.createdNodes
      
Attributes:
    createdNodes = list of created nodes.

Keywords:

             
Requires:


Development notes:

    @Todo - Ik/Fk Matching
    @todo - thigh / root 50% skin joint setup

"""
import commonMayaLib as cml
import orientJoints as oj
import createIkPoleVector as cipv
import connectJointChains as cjc
import makeIkStretchy as miks
import spaceSwitch as ss
import standardNames

# During development
reload( cml )
reload( oj )
reload( cipv )
reload( cjc )
reload( miks )
reload( ss )

class createLegRig():
    """
        Stretchy IK/FK leg rig ( Pending: with elbow pin and IK/FK matching )
        This script only concerns itself with thigh/knee/ankle joints.
        Foot joints( ball and toe ) are setup in createFootRig.py
            
    """
    def __init__(self,**keywords):
        # standard names object
        self.sNames = standardNames.standardNames()
        
        # Create library instance
        self.lib = cml.commonMayaLib()
        
        # Store the final node names to be returned to client
        self.createdNodes = {}
        
        # Command line call
        self.commandlineCall(keywords)
            
    def commandlineCall(self,keywords):
        """
        Verify and Store the data passed via command line keywords dictionary.
        """
        # Create variables and store values.
        self.prefix = keywords['prefix']
        self.side = keywords['side']

        self.cog = keywords['cog_cntrl']
        self.hips = keywords['hips_cntrl']
        self.world = keywords['world_cntrl']
        self.foot_cnt = keywords['foot_cntrl']
        
        self.joint_aim = keywords['aim_axis']
        self.joint_aimPolarity = keywords['aim_polarity']
        self.joint_up = keywords['up_axis']
        self.joint_upPolarity = keywords['up_polarity']

        self.normalAxis = keywords['fkNormal_axis']
        self.radius = keywords['fkRadius']
        self.rotateOrder = keywords['rotateOrder']
        
        if self.rotateOrder == 'xyz':
            self.rotateOrderInt = 0
        if self.rotateOrder == 'yzx':
            self.rotateOrderInt = 1
        if self.rotateOrder == 'zxy':
            self.rotateOrderInt = 2
        if self.rotateOrder == 'xzy':
            self.rotateOrderInt = 3
        if self.rotateOrder == 'yxz':
            self.rotateOrderInt = 4
        if self.rotateOrder == 'zyx':  
            self.rotateOrderInt = 5 
        
        # Create the leg rig.
        self.createLeg()

    def createLeg(self, *args):
        """
          Main process: Sets up variables and calls sub-routines
        """
        #--- De-select everything
        select(clear=True)
        
        #--- Create joint chains (follow,ik,fk)
        self.buildChains()
        
    def buildChains(self, *args):
        """
        Use joints created by createRigJoints.py to build
        Ik/Fk chains.
        """
        self.followChain = [] # Thigh, knee, ankle
        self.ikChain = []
        self.fkChain = []
        
        if self.side == 1:
            thigh = self.sNames.legJoints['left_thigh']
            knee = self.sNames.legJoints['left_knee']
            ankle = self.sNames.legJoints['left_ankle']
        if self.side == 2:
            thigh = self.sNames.legJoints['right_thigh']
            knee = self.sNames.legJoints['right_knee']
            ankle = self.sNames.legJoints['right_ankle']
                
        self.followChain.append( thigh )
        self.followChain.append( knee )
        self.followChain.append( ankle )
        
        # Store the names of the root joints so they can be parented to the hips.
        self.createdNodes['thigh'] = self.followChain[0]

        #--- Create duplicate ik/fk joint chains
        # IK
        temp = duplicate(self.followChain,rc=True)
                
        x = 0
        for each in temp:
            name = '%s_ik' % each[:-1] # Slice off number maya adds during duplication
            rename  (each, name)
            self.ikChain.append(name)

            x = x + 1
        
        # FK
        # @ todo - Get ride of side 1/2 checking during for loop. Just use left_ikChain/right_ikChain, etc...
        temp = duplicate(self.followChain,rc=True)
        
        x = 0
        for each in temp:
            name = ''

            if x == 0:
                if self.side == 1:
                    name = self.sNames.controlNames['left_fkThigh']
                if self.side == 2:
                    name = self.sNames.controlNames['right_fkThigh']
            if x == 1:
                if self.side == 1:
                    name = self.sNames.controlNames['left_fkKnee']
                if self.side == 2:
                    name = self.sNames.controlNames['right_fkKnee']
            if x == 2:
                if self.side == 1:
                    name = self.sNames.controlNames['left_fkAnkle']
                if self.side == 2:
                    name = self.sNames.controlNames['right_fkAnkle']
            x = x + 1

            rename(each, name)
            self.fkChain.append(name)
        

        
        # Delete children joints of the duplicates below the wrist
        temp = listRelatives(self.ikChain[2],children=True)
        delete(temp)
        temp = listRelatives(self.fkChain[2],children=True)
        delete(temp)
        
        #--- Build IK
        self.buildIK()
                
        #--- Stretchy setup
        self.stretchySetup()
        
        #--- Build FK
        self.buildFK()
        
        #--- Connect joint chains
        self.connectChains()
        
        #--- Setup switch on foot control
        self.setupSwitch()
                
        #--- clean up
        self.cleanUp()
        
    def buildIK(self, *args):
        """
            Build the IK leg
        """
        #Setup variables
        #@Todo - Is this actually working?
        self.normal = (1,0,0)
        if self.normalAxis == 1:
            self.normal = (1, 0, 0)
        if self.normalAxis == 2:
            self.normal = (0, 1, 0)
        if self.normalAxis == 3:
            self.normal = (0, 0, 1)   

        #Create IK control
        name = ''
        if self.side == 1:
            name = self.sNames.controlNames['left_footIk']
        if self.side == 2:
            name = self.sNames.controlNames['right_footIk']
            
        self.ikControl = circle(nr=self.normal, r=self.radius,n=name)
        select(self.ikControl[0],r=True)
        mel.eval("DeleteHistory;")
        
        if self.side == 1:
            # Set the color
            setAttr('%s.overrideEnabled'%self.ikControl[0], 1)
            setAttr('%s.ovc'%self.ikControl[0], 13)
            
        else:
            # Set the color
            setAttr('%s.overrideEnabled'%self.ikControl[0], 1)
            setAttr('%s.ovc'%self.ikControl[0], 6)

        # Set rotate orders
        setAttr('%s.rotateOrder'%self.ikControl[0], self.rotateOrderInt) # ZXY

        #Parent circle under third joint
        parent(self.ikControl[0], self.ikChain[2])  
          
        #Zero it so it snaps to joint position/orientation   
        move(self.ikControl[0], 0, 0, 0,os=True)             
        parent(self.ikControl[0],w=True)
        
        #Zero it's values and create the buffer node
        ikBuffer01 = self.lib.zero(self.ikControl[0])             
             
        #Create RP IK
        self.leg_ikHandle = ikHandle(sj=self.ikChain[0], ee=self.ikChain[2], solver='ikRPsolver', name=(self.prefix + '_legIkHandle'))
        setAttr(self.leg_ikHandle[0] + '.visibility', 0)
        
        #Parent IK Handle to the ikHandle_cnt
        parent(self.leg_ikHandle[0], self.ikControl[0])
        self.createdNodes['ik_handle'] = self.leg_ikHandle[0]

        # Creates: self.pv_cnt
        self.createPoleVector(self.leg_ikHandle[0], self.ikControl, self.sNames.controlNames['main'])
        
        # Setup space switch for ik control
        # first, re-zero ik control to have an other node above it.
        ikBuffer02 = self.lib.zero(ikBuffer01)  
        self.createdNodes['buffer'] = ikBuffer02
        ss.spaceSwitch(   constObj=ikBuffer02,
                            control=self.ikControl[0],
                            attName='space_switches',
                            op1Name='world_space',
                            op2Name='cog_space',
                            op3Name='hips_space',
                            op4Name='',
                            op5Name='',
                            op6Name='',
                            op7Name='',
                            op8Name='',
                            object1=self.world,
                            object2=self.cog,
                            object3=self.hips,
                            object4='',
                            object5='',
                            object6='',
                            object7='',
                            object8=''  )
        
    def createPoleVector(self,ikHandle,ikControl,worldControl):
        """
        Call: createIkPoleVector()
        """
        temp = cipv.createIkPoleVector( prefix = self.prefix,
                                 side = self.side,
                                 type='leg',
                                 ikHandle = ikHandle,
                                 ikControl = ikControl[0],
                                 worldControl = worldControl )
        temp2 = temp.createdNodes[0]    
        
        self.pv_cnt = temp2                             
        
    def stretchySetup(self, *args):
        """
        Call: makeIkStretchy
        """
        temp = miks.makeIkStretchy( prefix='%s_legRig'%self.prefix,
                             side = self.side,
                             type=1,
                             axis=1,
                             control=self.ikControl,
                             ik=self.leg_ikHandle[0] )
        
        # Store the distance grp    
        self.createdNodes['distGrp'] = temp.createdNodes['distGrp']       
        
    

    def buildFK(self,*args):
        """
        Set up FK controllers on leg FK joints
        """
        # Set the joint color
        setAttr('%s.overrideEnabled'%self.fkChain[0],1)
        if self.side == 1:
            setAttr('%s.ovc'%self.fkChain[0],13)
        if self.side == 2:
            setAttr('%s.ovc'%self.fkChain[0],6)
        
        #Thigh
        temp = circle(nr=self.normalAxis, r=self.radius)
        parent(temp, self.fkChain[0]) #Parent transform under fk joint
        move(temp,0, 0, 0 ) #Zero it so it snaps to FK position/orientation
        shape = pickWalk(temp, direction='down') #Get shape node for the parent command
        parent(shape, self.fkChain[0], s=True, r=True) #Parent shape to joints transform
        delete(temp)   #Delete empty transform

        #Knee
        temp = circle(nr=self.normalAxis, r=self.radius)
        parent(temp, self.fkChain[1]) #Parent transform under fk joint
        move(temp,0, 0, 0 ) #Zero it so it snaps to FK position/orientation
        shape = pickWalk(temp, direction='down') #Get shape node for the parent command
        parent(shape, self.fkChain[1], s=True, r=True) #Parent shape to joints transform
        delete(temp)   #Delete empty transform

        #Ankle
        temp = circle(nr=self.normalAxis, r=self.radius)
        parent(temp, self.fkChain[2]) #Parent transform under fk joint
        move(temp,0, 0, 0 ) #Zero it so it snaps to FK position/orientation
        shape = pickWalk(temp, direction='down') #Get shape node for the parent command
        parent(shape, self.fkChain[2], s=True, r=True) #Parent shape to joints transform
        delete(temp)   #Delete empty transform

        #
        # FK Length attributes setup/ Done using the translates of the child to avoid skewing that
        # occurs with scaling in a non-uniform manner (1,2,1)
        #
        addAttr(self.fkChain[0], ln='length', min=0, dv=1, k=True)
        addAttr(self.fkChain[1], ln='length', min=0, dv=1, k=True)

        #Get current translate%s % aim value to set the max SDK as twice the default length
        if self.joint_aim == 1:
            aim = 'X'
        if self.joint_aim == 2:
            aim = 'Y'
        if self.joint_aim == 3:
            aim = 'Z'     
        
        val1 = getAttr('%s.translate%s' % (self.fkChain[1], aim))
        val2 = getAttr('%s.translate%s' % (self.fkChain[2], aim))

        #SDK to connect them
        setDrivenKeyframe(self.fkChain[1], cd='%s.length' % self.fkChain[0], at='translate%s' % aim, dv=1) #Set default with current value in .tx
        setDrivenKeyframe(self.fkChain[1], cd='%s.length' % self.fkChain[0], at='translate%s' % aim, dv=0, v=0)         #Set min
        setDrivenKeyframe(self.fkChain[1], cd='%s.length' % self.fkChain[0], at='translate%s' % aim, dv=2, v=(val1 * 5)) #Set max

        setDrivenKeyframe(self.fkChain[2], cd='%s.length' % self.fkChain[1], at='translate%s' % aim, dv=1) #Set default with current value in .tx
        setDrivenKeyframe(self.fkChain[2], cd='%s.length' % self.fkChain[1], at='translate%s' % aim, dv=0, v=0)         #Set min
        setDrivenKeyframe(self.fkChain[2], cd='%s.length' % self.fkChain[1], at='translate%s' % aim, dv=2, v=(val2 * 5))#Set max

    
    def connectChains(self,*args):
        """
        Connect the follow chain to the IK/FK chains.
        """
        temp = cjc.connectJointChains(    prefix=self.prefix,
                                   followJoint=self.followChain[0],
                                   leadAJoint=self.ikChain[0],
                                   leadBJoint=self.fkChain[0],
                                   type=2,
                                   translations=1,
                                   rotations=1 )
        
        # Store nodes created
        self.createdNodes['switchNodes'] = temp.createdNodes

    def setupSwitch(self,*args):
        """
         Create attributes on foot_cnt: 
             FK_IK 
        """
        addAttr(self.foot_cnt,ln='FK_IK',at='float',dv=0,min=0,max=1,k=True)

        # Connect IK/FK attr to the blend color nodes
        for each in self.createdNodes['switchNodes']:
            connectAttr( '%s.FK_IK'%self.foot_cnt, '%s.blender'%each )

        #IK=0=Off / FK=1=Off controls vis switch
        connectAttr( '%s.FK_IK'%self.foot_cnt, '%s.visibility'%self.ikChain[0] )
        connectAttr( '%s.FK_IK'%self.foot_cnt, '%s.visibility'%self.ikControl[0] )
        
        # FK=1=Off SDK
        setDrivenKeyframe(self.fkChain[0], cd='%s.FK_IK' % self.foot_cnt, at='visibility', dv=1, v=0)
        setDrivenKeyframe(self.fkChain[0], cd='%s.FK_IK' % self.foot_cnt, at='visibility', dv=0, v=1)

    def cleanUp(self,*args):
        """
            Lock and hide attributes as needed and delete setup locators
        """
        #IK control
        setAttr('%s.scaleX' % self.ikControl[0], lock=True, keyable=False)
        setAttr('%s.scaleY' % self.ikControl[0], lock=True, keyable=False)
        setAttr('%s.scaleZ' % self.ikControl[0], lock=True, keyable=False)
        setAttr('%s.visibility' % self.ikControl[0], keyable=False)
        
        #FK controls
        for each in self.fkChain:
            setAttr('%s.translateX' % each, lock=True, keyable=False)
            setAttr('%s.translateY' % each, lock=True, keyable=False)
            setAttr('%s.translateZ' % each, lock=True, keyable=False)
            setAttr('%s.scaleX' % each, lock=True, keyable=False)
            setAttr('%s.scaleY' % each, lock=True, keyable=False)
            setAttr('%s.scaleZ' % each, lock=True, keyable=False)
            setAttr('%s.visibility' % each, keyable=False)
        
        #pv_cnt
        setAttr('%s.rotateX' % self.pv_cnt, lock=True, keyable=False)
        setAttr('%s.rotateY' % self.pv_cnt, lock=True, keyable=False)
        setAttr('%s.rotateZ' % self.pv_cnt, lock=True, keyable=False)        
        
        setAttr('%s.scaleX' % self.pv_cnt, lock=True, keyable=False)
        setAttr('%s.scaleY' % self.pv_cnt, lock=True, keyable=False)
        setAttr('%s.scaleZ' % self.pv_cnt, lock=True, keyable=False)
        setAttr('%s.visibility' % self.pv_cnt, keyable=False)

        #Lock IK / FK knee axes
        if self.joint_up == 1:
            setAttr('%s.rotateX'%self.ikChain[1],lock=True,k=False) 
            setAttr('%s.rotateZ'%self.ikChain[1],lock=True,k=False) 
            setAttr('%s.rotateX'%self.fkChain[1],lock=True,k=False) 
            setAttr('%s.rotateZ'%self.fkChain[1],lock=True,k=False)
        if self.joint_up == 2:
            setAttr('%s.rotateY'%self.ikChain[1],lock=True,k=False) 
            setAttr('%s.rotateX'%self.ikChain[1],lock=True,k=False)  
            setAttr('%s.rotateY'%self.fkChain[1],lock=True,k=False) 
            setAttr('%s.rotateX'%self.fkChain[1],lock=True,k=False)
        if self.joint_up == 3:
            setAttr('%s.rotateZ'%self.ikChain[1],lock=True,k=False) 
            setAttr('%s.rotateY'%self.ikChain[1],lock=True,k=False)
            setAttr('%s.rotateZ'%self.fkChain[1],lock=True,k=False) 
            setAttr('%s.rotateY'%self.fkChain[1],lock=True,k=False) 
                    
        # Set ik to world space by default
        setAttr(self.ikControl[0] + '.world_space',1)
        setAttr(self.ikControl[0] + '.world_space',1)  
            
        # get foot_cnt buffer node
        footBuffer= pickWalk(self.foot_cnt,direction='up')
        
        # Parent foot_cnt to follow ankle
        parent(self.foot_cnt,self.followChain[2])
        
        # Delete foot_cnt buffer node
        delete(footBuffer)
        
        # Lock and hide it's attributes
        setAttr('%s.translateX' % self.foot_cnt, lock=True, keyable=False)
        setAttr('%s.translateY' % self.foot_cnt, lock=True, keyable=False)
        setAttr('%s.translateZ' % self.foot_cnt, lock=True, keyable=False)
        setAttr('%s.rotateX' % self.foot_cnt, lock=True, keyable=False)
        setAttr('%s.rotateY' % self.foot_cnt, lock=True, keyable=False)
        setAttr('%s.rotateZ' % self.foot_cnt, lock=True, keyable=False)
        setAttr('%s.scaleX' % self.foot_cnt, lock=True, keyable=False)
        setAttr('%s.scaleY' % self.foot_cnt, lock=True, keyable=False)
        setAttr('%s.scaleZ' % self.foot_cnt, lock=True, keyable=False)
        setAttr('%s.visibility' % self.foot_cnt, keyable=False)
            
        # Define returned dictionary. Used by createFootRig.py
        self.createdNodes['followAnkleJnt'] = self.followChain[2] 
        self.createdNodes['ikAnkleJnt'] = self.ikChain[2] 
        self.createdNodes['fkAnkleJnt'] = self.fkChain[2]
        self.createdNodes['legIkHandle'] = self.leg_ikHandle[0]
        self.createdNodes['ikCnt'] = self.ikControl
        self.createdNodes['footCnt'] = self.foot_cnt
           
        if self.side == 1:
            self.createdNodes['left_ikChain'] = self.ikChain
            self.createdNodes['left_fkChain'] = self.fkChain
            self.createdNodes['left_followChain'] = self.followChain
            
        if self.side == 2:
            self.createdNodes['right_ikChain'] = self.ikChain
            self.createdNodes['right_fkChain'] = self.fkChain
            self.createdNodes['right_followChain'] = self.followChain        
    
    
        