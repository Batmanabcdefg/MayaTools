from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *
"""
Copyright (c) 2010 Mauricio Santos
Name: createFootRig.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created:   22 Oct 2010


$Revision: 140 $
$LastChangedDate: 2011-09-13 00:36:32 -0700 (Tue, 13 Sep 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/createFootRig.py $
$Id: createFootRig.py 140 2011-09-13 07:36:32Z mauricio $

Description: 
    Creates a reverse foot rig with attributes on ik controller and
    an Fk rig. Attributes to control toes are on the foot ik/fk switch control.

Process:
    
Additional Notes: 

Example call:
    import createFootRig
    createFootRig.createFootRig( )
      
Attributes:
    createdNodes = list of created nodes.

Keywords:

             
Requires:


Development notes:


"""

import orientJoints
import createFingersOrToesRig
import standardNames
import commonMayaLib as cml

import connectJointChains as cjc

class createFootRig():
    """
    Creates a reverse foot rig with attributes on ik controller and
    an Fk rig. Attributes to control toes are on the foot ik/fk switch control.
    """
    def __init__(self,**keywords):
        # Standard names object
        self.sNames = standardNames.standardNames()
        
        # Common tools as a library
        self.lib = cml.commonMayaLib()
        
        # Used to store names of all created nodes, 
        # to be returned when the tool is done.
        self.createdNodes = {} 
        
        # Check if command line call
        self.commandlineCall(keywords)

            
    def commandlineCall(self,keywords):
        """
        Verify and Store the data passed via command line keywords dictionary.
        """    
        self.prefix = keywords['prefix']
                
        self.side = keywords['side']
        self.numToes = keywords['numToes']
        self.ballJnt = keywords['ballJnt']
        self.toeJnt = keywords['toeJnt']
        
        self.followAnkleJnt = keywords['followAnkleJnt']
        self.ikAnkleJnt = keywords['ikAnkleJnt']
        self.fkAnkleJnt = keywords['fkAnkleJnt']
        
        self.legIkHandle = keywords['legIkHandle']
        self.ikCnt = keywords['ikCnt']
        self.footCnt = keywords['footCnt']
    
        # Locators
        self.heelLoc = keywords['heelLoc']
        self.outterBankLoc = keywords['outterBankLoc']
        self.innerBankLoc = keywords['innerBankLoc']
        
        # Options
        self.upAxis = keywords['upAxis']
        self.aimAxis = keywords['aimAxis']
        
        self.fkNormal = keywords['fkNormal']
        self.fkRadius = keywords['fkRadius']
        
        self.outterBankVal = keywords['outterBankVal']
        self.innerBankVal = keywords['innerBankVal']
                
        #--- Defining initial data       
        #Store appropriate value based on self.upAxisBtnVal
        if self.upAxis == 1:
            self.upAxis = 1,0,0
            self.upAxisChar = 'X'
            
        if self.upAxis == 2:
            self.upAxis = 0,1,0
            self.upAxisChar = 'Y'
            
        if self.upAxis == 3:
            self.upAxis = 0,0,1
            self.upAxisChar = 'Z' 
 
        #Store appropriate value based on self.aimAxisBtnVal
        if self.aimAxis == 1:
            self.aimAxis = 1,0,0
            self.aimAxisChar = 'X'
            
        if self.aimAxis == 2:
            self.aimAxis = 0,1,0
            self.aimAxisChar = 'Y'
            
        if self.aimAxis == 3:
            self.aimAxis = 0,0,1
            self.aimAxisChar = 'Z'

        self.create()

    def create(self,*args):
        """
        Store data, setup scene for building rig
        and call general functions.
        """             
        #--- Call: buidChains() Create three joint chains
        self.buildChains()    
            
    def buildChains(self,*args):
        """
        Create follow,ik,fk joint chains rooted to their respective
        chains.
        """ 
        self.followChain = []
        self.ikChain = []
        self.fkChain = []
        
        # Follow chain
        self.followChain.append(self.followAnkleJnt)
        self.followChain.append(self.ballJnt) 
        self.followChain.append(self.toeJnt)
        
        #--- Create duplicate ik/fk joint chains
        # IK
        temp = []
        temp.append(self.ikAnkleJnt)
        t = duplicate(self.ballJnt,parentOnly=True)
        temp.append(t[0])
        t = duplicate(self.toeJnt,parentOnly=True)
        temp.append(t[0])
        
        parent(temp[2],temp[1])
        parent(temp[1],temp[0])
               
        x = 0
        for each in temp:
            if x == 0:
                # Skip the ankle
                self.ikChain.append(each)
                x += 1
                continue
            
            name = '%s_ik' % each[:-1] # Slice off number maya adds during duplication
            rename(each, name)
            self.ikChain.append(name)

            x += 1
        
        # FK
        # Ankle joint
        self.fkChain.append(self.fkAnkleJnt)
        
        # Ball joint
        temp = duplicate(self.followChain[1],parentOnly=True)
        
        if self.side == 1:
            name = self.sNames.controlNames['left_fkFootBall']
        if self.side == 2:
            name = self.sNames.controlNames['right_fkFootBall']
            
        rename(temp[0], name)
        self.fkChain.append(name)
        
        parent(self.fkChain[1],self.fkChain[0])
        
        # Toe joint
        temp = duplicate(self.followChain[2],parentOnly=True)
        
        if self.side == 1:
            name = self.sNames.controlNames['left_fkFootToe']
        if self.side == 2:
            name = self.sNames.controlNames['right_fkFootToe']

        rename(temp[0], name)
        self.fkChain.append(name)
        
        parent(self.fkChain[2],self.fkChain[1])
        
        

        #--- Call: createIkRi() Setting up the Ik rig
        self.createIkRig()
        
    def createIkRig(self,*args):
        """
        Creates a reverse foot rig with attributes on controller based
        on pivots specified by user.
        """        
        #--- Create the rig  
        
        #Now, we create the single chain IK for the feet     #Not using the self.prefix because A: it's not necessary, and 
        #ballIk = self.prefix+"ball"                    # B: This was leading to name clashing upon IK handle creation.
        temp = ikHandle(sj=self.ikChain[0],ee=self.ikChain[1],sol='ikSCsolver')
        ballIk = temp[0]
        rename(temp[0],ballIk)
        
        #toeIk = self.prefix+"toe"
        temp = ikHandle(sj=self.ikChain[1],ee=self.ikChain[2],sol='ikSCsolver')
        toeIk = temp[0]
        rename(temp[0],toeIk)
        
        #Here, we start grouping...
        peelGrp = self.prefix + "peel_"
        temp = group(self.legIkHandle,a=True)
        peelGrp = peelGrp + temp
        rename(temp,peelGrp)
        
        peelGrp2 = self.prefix + "peel2_"
        temp = group(peelGrp,a=True)
        peelGrp2 = peelGrp2 + temp
        rename(temp,peelGrp2)        
        
        toeTapGrp = self.prefix + "toeTap_"
        temp = group(ballIk,toeIk)
        toeTapGrp = toeTapGrp + temp
        rename(temp,toeTapGrp)
        
        ballTwistGrp = self.prefix + "ballTwist_"
        temp = group(toeTapGrp)
        ballTwistGrp = ballTwistGrp + temp
        rename(temp,ballTwistGrp)
        
        toePivotGrp = self.prefix + "toePivot_"
        temp = group(peelGrp2,toeTapGrp)
        toePivotGrp = toePivotGrp + temp
        rename(temp,toePivotGrp)
        
        heelPivotGrp = self.prefix + "heelPivot_"
        temp = group(ballTwistGrp)
        heelPivotGrp = heelPivotGrp + temp
        rename(temp,heelPivotGrp)
        
        bankOuterGrp = self.prefix + "bankOuterPivot_"
        temp = group(heelPivotGrp)
        bankOuterGrp = bankOuterGrp + temp
        rename(temp,bankOuterGrp)
        
        bankInnerGrp = self.prefix + "bankInnerPivot_"
        temp = group(bankOuterGrp)
        bankInnerGrp = bankInnerGrp + temp
        rename(temp,bankInnerGrp)
        
        parent(toePivotGrp,ballTwistGrp)

        #Snap pivots to their respective locations
        #PeelGrp
        tempPos = xform(self.ballJnt,query=True,ws=1,t=1)
        move(peelGrp + ".scalePivot",tempPos[0],tempPos[1],tempPos[2], peelGrp + ".rotatePivot",xyz=True,ws=True)
        
        #PeelGrp2
        tempPos = xform(self.ballJnt,query=True,ws=1,t=1)
        move(peelGrp2 + ".scalePivot",tempPos[0],tempPos[1],tempPos[2], peelGrp2 + ".rotatePivot",xyz=True,ws=True)        
        
        #toeTapGrp
        tempPos = xform(self.ballJnt,query=True,ws=1,t=1)
        move(toeTapGrp + ".scalePivot",tempPos[0],tempPos[1],tempPos[2], toeTapGrp + ".rotatePivot",xyz=True,ws=True)
        
        #toePivotGrp
        tempPos = xform(self.toeJnt,query=True,ws=1,t=1)
        move(toePivotGrp + ".scalePivot",tempPos[0],tempPos[1],tempPos[2], toePivotGrp + ".rotatePivot",xyz=True,ws=True)    
        
        #ballTwistGrp
        tempPos = xform(self.ballJnt,query=True,ws=1,t=1)
        move(ballTwistGrp + ".scalePivot",tempPos[0],tempPos[1],tempPos[2], ballTwistGrp + ".rotatePivot",xyz=True,ws=True)
        
        #heelPivotGrp
        tempPos = xform(self.heelLoc,query=True,ws=1,t=1)
        move(heelPivotGrp + ".scalePivot",tempPos[0],tempPos[1],tempPos[2], heelPivotGrp + ".rotatePivot",xyz=True,ws=True)
        
        #bankOutter
        tempPos = xform(self.outterBankLoc,query=True,ws=1,t=1)
        move(bankOuterGrp + ".scalePivot",tempPos[0],tempPos[1],tempPos[2], bankOuterGrp + ".rotatePivot",xyz=True,ws=True)
        
        #bankInner
        tempPos = xform(self.innerBankLoc,query=True,ws=1,t=1)
        move(bankInnerGrp + ".scalePivot",tempPos[0],tempPos[1],tempPos[2], bankInnerGrp + ".rotatePivot",xyz=True,ws=True)
        
        #Now, lets parent it all under the foot control
        parent(bankInnerGrp,self.ikCnt[0])        

        #
        # Create Attributes for SDKs
        #
        addAttr(self.ikCnt[0],at='float',ln="footControls",dv=0,min=0,max=1,keyable=True)
        setAttr(self.ikCnt[0] + ".footControls",lock=True)
        #addAttr(self.ikCnt[0],at='float',ln="footRoll",dv=0,min=-10,max=10,keyable=True)
        addAttr(self.ikCnt[0],at='float',ln="heelRoll",dv=0,min=-10,max=10,keyable=True)
        addAttr(self.ikCnt[0],at='float',ln="ballRoll",dv=0,min=-10,max=10,keyable=True)
        addAttr(self.ikCnt[0],at='float',ln="toeRoll",dv=0,min=-10,max=10,keyable=True)
        addAttr(self.ikCnt[0],at='float',ln="toeTap",dv=0,min=-10,max=10,keyable=True)
        
        addAttr(self.ikCnt[0],at='float',ln="heelTwist",dv=0,min=-10,max=10,keyable=True)
        addAttr(self.ikCnt[0],at='float',ln="ballTwist",dv=0,min=-10,max=10,keyable=True)
        addAttr(self.ikCnt[0],at='float',ln="toeTwist",dv=0,min=-10,max=10,keyable=True)
        
        addAttr(self.ikCnt[0],at='float',ln="Bank",dv=0,min=-10,max=10,keyable=True)
        
        ###SDK's
        ###Driver: self.ikCnt[0]
        #####-----------------Roll: Pivots: peelGrp, toePivotGrp
        
        setDrivenKeyframe( heelPivotGrp, cd=self.ikCnt[0] + ".heelRoll",  at= "rotate%s"%self.aimAxisChar, dv = 0,v = 0 )
        setDrivenKeyframe( heelPivotGrp, cd=self.ikCnt[0] + ".heelRoll",  at= "rotate%s"%self.aimAxisChar, dv = -10,v = 90 )
        setDrivenKeyframe( heelPivotGrp, cd=self.ikCnt[0] + ".heelRoll",  at= "rotate%s"%self.aimAxisChar, dv = 10,v = -90 )
        
        setDrivenKeyframe( peelGrp, cd=self.ikCnt[0] + ".ballRoll",  at= "rotate%s"%self.aimAxisChar, dv = 0,v = 0 )
        setDrivenKeyframe( peelGrp, cd=self.ikCnt[0] + ".ballRoll",  at= "rotate%s"%self.aimAxisChar, dv = -10,v = 90 )
        setDrivenKeyframe( peelGrp, cd=self.ikCnt[0] + ".ballRoll",  at= "rotate%s"%self.aimAxisChar, dv = 10,v = -90 )
        
        setDrivenKeyframe( toePivotGrp, cd=self.ikCnt[0] + ".toeRoll",  at= "rotate%s"%self.aimAxisChar, dv = 0,v = 0 )
        setDrivenKeyframe( toePivotGrp, cd=self.ikCnt[0] + ".toeRoll",  at= "rotate%s"%self.aimAxisChar, dv = -10,v = 90 )
        setDrivenKeyframe( toePivotGrp, cd=self.ikCnt[0] + ".toeRoll",  at= "rotate%s"%self.aimAxisChar, dv = 10,v = -90 )
        
        setDrivenKeyframe( toeTapGrp, cd=self.ikCnt[0] + ".toeTap",  at= "rotate%s"%self.aimAxisChar, dv = 0,v = 0 )
        setDrivenKeyframe( toeTapGrp, cd=self.ikCnt[0] + ".toeTap",  at= "rotate%s"%self.aimAxisChar, dv = -10,v = 90 )
        setDrivenKeyframe( toeTapGrp, cd=self.ikCnt[0] + ".toeTap",  at= "rotate%s"%self.aimAxisChar, dv = 10,v = -90 )
        
        setDrivenKeyframe( heelPivotGrp, cd=self.ikCnt[0] + ".heelTwist",  at= "rotate%s"%self.upAxisChar, dv = 0, v = 0)   
        setDrivenKeyframe( heelPivotGrp, cd=self.ikCnt[0] + ".heelTwist",  at= "rotate%s"%self.upAxisChar , dv = -10, v = 90) 
        setDrivenKeyframe( heelPivotGrp, cd=self.ikCnt[0] + ".heelTwist",  at= "rotate%s"%self.upAxisChar , dv = 10, v = -90)
               
        setDrivenKeyframe( ballTwistGrp, cd=self.ikCnt[0] + ".ballTwist",  at= "rotate%s"%self.upAxisChar, dv = 0, v = 0)   
        setDrivenKeyframe( ballTwistGrp, cd=self.ikCnt[0] + ".ballTwist",  at= "rotate%s"%self.upAxisChar , dv = -10, v = -90) 
        setDrivenKeyframe( ballTwistGrp, cd=self.ikCnt[0] + ".ballTwist",  at= "rotate%s"%self.upAxisChar , dv = 10, v = 90)
        
        setDrivenKeyframe( toePivotGrp, cd=self.ikCnt[0] + ".toeTwist",  at= "rotate%s"%self.upAxisChar, dv = 0, v = 0)   
        setDrivenKeyframe( toePivotGrp, cd=self.ikCnt[0] + ".toeTwist",  at= "rotate%s"%self.upAxisChar , dv = -10, v = -90) 
        setDrivenKeyframe( toePivotGrp, cd=self.ikCnt[0] + ".toeTwist",  at= "rotate%s"%self.upAxisChar , dv = 10, v = 90)

        # SDK for foot roll
#        setDrivenKeyframe( self.ikCnt[0], cd=self.ikCnt[0] + ".footRoll",  at= "heelRoll", dv = 0, v = 0)
#        setDrivenKeyframe( self.ikCnt[0], cd=self.ikCnt[0] + ".footRoll",  at= "ballRoll", dv = 0, v = 0)
#        setDrivenKeyframe( self.ikCnt[0], cd=self.ikCnt[0] + ".footRoll",  at= "toeRoll", dv = 0, v = 0)
#           
#        setDrivenKeyframe( self.ikCnt[0], cd=self.ikCnt[0] + ".footRoll",  at= "heelRoll" , dv = -10, v = 10) 
#        setDrivenKeyframe( self.ikCnt[0], cd=self.ikCnt[0] + ".footRoll",  at= "ballRoll" , dv = 5, v = -3)
#        setDrivenKeyframe( self.ikCnt[0], cd=self.ikCnt[0] + ".footRoll",  at= "ballRoll" , dv = 10, v = -3)
#        setDrivenKeyframe( self.ikCnt[0], cd=self.ikCnt[0] + ".footRoll",  at= "toeRoll" , dv = 5, v = 0)
#        setDrivenKeyframe( self.ikCnt[0], cd=self.ikCnt[0] + ".footRoll",  at= "toeRoll" , dv = 10, v = -4)
        
        if self.side == 1: 
            ## Bank  
            setDrivenKeyframe( bankInnerGrp, cd=self.ikCnt[0] + ".Bank",  at= "rotateZ", dv = 0, v = 0)
            setDrivenKeyframe( bankInnerGrp, cd=self.ikCnt[0] + ".Bank",  at= "rotateZ" , dv = 10, v = (self.innerBankVal))
                   
            ## outerBank: 
            setDrivenKeyframe( bankOuterGrp, cd=self.ikCnt[0] + ".Bank",  at= "rotateZ", dv = 0, v = 0)   
            setDrivenKeyframe( bankOuterGrp, cd=self.ikCnt[0] + ".Bank",  at= "rotateZ" , dv = -10, v = (self.outterBankVal))
            
        if self.side == 2: 
            ## Bank  
            setDrivenKeyframe( bankInnerGrp, cd=self.ikCnt[0] + ".Bank",  at= "rotateZ", dv = 0, v = 0)
            setDrivenKeyframe( bankInnerGrp, cd=self.ikCnt[0] + ".Bank",  at= "rotateZ" , dv = 10, v = (self.innerBankVal))
                   
            ## outerBank: 
            setDrivenKeyframe( bankOuterGrp, cd=self.ikCnt[0] + ".Bank",  at= "rotateZ", dv = 0, v = 0)   
            setDrivenKeyframe( bankOuterGrp, cd=self.ikCnt[0] + ".Bank",  at= "rotateZ" , dv = -10, v = (self.outterBankVal))  
        
        #The lock and hiding part! 
        #Foot Control
        setAttr(self.ikCnt[0] + ".sx", lock=True,keyable=False)
        setAttr(self.ikCnt[0] + ".sy", lock=True,keyable=False)
        setAttr(self.ikCnt[0] + ".sz", lock=True,keyable=False)    
        setAttr(self.ikCnt[0] + ".visibility",keyable=False)
        
        #SDK'd roll attributes
#        setAttr(self.ikCnt[0] + ".heelRoll", lock=True,keyable=False)
#        setAttr(self.ikCnt[0] + ".ballRoll", lock=True,keyable=False)
#        setAttr(self.ikCnt[0] + ".toeRoll", lock=True,keyable=False)
        
        #Ik handles
        setAttr(ballIk + ".visibility", 0)
        setAttr(toeIk + ".visibility", 0)        

        select(clear=True)    
        
        #--- Call: createFkRig() Setting up the Fk rig
        self.createFkRig()
            
    def createFkRig(self,*args):
        """
        Disabled due to toe_cnt
        Create an fk controller on the ball joint
        """
        # Ball joint
        temp = circle(nr=self.fkNormal, r=self.fkRadius)
        parent(temp, self.fkChain[1]) #Parent transform under fk joint
        move(temp,0, 0, 0 ) #Zero it so it snaps to FK position/orientation
        shape = pickWalk(temp, direction='down') #Get shape node for the parent command
        parent(shape, self.fkChain[1], s=True, r=True) #Parent shape to joints transform
        delete(temp)   #Delete empty transform  
        
        # Hide tis controller as it is replaced by the new: toe_cnt
        setAttr('%s.visibility'%shape[0],0)
        
        # Lock / Hide attributes
        setAttr('%s.translateX' % self.fkChain[1], lock=True, keyable=False)
        setAttr('%s.translateY' % self.fkChain[1], lock=True, keyable=False)
        setAttr('%s.translateZ' % self.fkChain[1], lock=True, keyable=False)
        setAttr('%s.scaleX' % self.fkChain[1], lock=True, keyable=False)
        setAttr('%s.scaleY' % self.fkChain[1], lock=True, keyable=False)
        setAttr('%s.scaleZ' % self.fkChain[1], lock=True, keyable=False)
        setAttr('%s.visibility' % self.fkChain[1], keyable=False)
        
        #---Call: connectChains() Connect the three joint chains
        self.connectChains() 
        
    def connectChains(self,*args):
        """
        Connect the follow chain to the IK/FK chains.
        """            
        #Ball blendColors creation/linking
        self.createdNodes['switchNodes'] = []
        self.setupBlendNode(name = 'footBall_rotations',
                                    type = 1,
                                    src1 = self.ikChain[1],
                                    src2 = self.fkChain[1],
                                    tgt = self.followChain[1])
    
        self.setupBlendNode(name = 'footBall_translations',
                                    type = 2,
                                    src1 = self.ikChain[1],
                                    src2 = self.fkChain[1],
                                    tgt = self.followChain[1])
        
        #--- Call: setupSwitch()
        self.setupSwitch()
        
    def setupBlendNode(self,name,type,src1,src2,tgt):
        """
        Create and connect three objects via blendColor node
        """
        # Rotations
        if type == 1: 
            type = 'rotate'
        else:
            type = 'translate'
            
        temp = createNode( 'blendColors' )
        blendNode = '%s_%s'%(self.prefix,name)
        rename( temp,blendNode )

        #blendNode attributes to connect
        nodeColor1 = (blendNode + ".color1")
        nodeColor2 = (blendNode + ".color2")
        nodeOutput = (blendNode + ".output")

        source1 = '%s.%s'%(src1,type)
        source2 = '%s.%s'%(src2,type)
        target = '%s.%s'%(tgt,type)

        connectAttr(source1, nodeColor1)
        connectAttr(source2, nodeColor2)
        connectAttr(nodeOutput, target)
        
        # Store name of created node to return to caller.
        self.createdNodes['switchNodes'].append(blendNode)

    def setupSwitch(self,*args):
        """
         Connect to attributes on foot_cnt:
        """
        #addAttr(self.foot_cnt,ln='FK_IK',at='float',dv=0,min=0,max=1,k=True)

        # Connect IK/FK attr to the blend color nodes
        for each in self.createdNodes['switchNodes']:
            connectAttr( '%s.FK_IK'%self.footCnt, '%s.blender'%each )

        #IK=0=Off / FK=1=Off controls vis switch
        connectAttr( '%s.FK_IK'%self.footCnt, '%s.visibility'%self.ikChain[0] )
        
        # FK=1=Off SDK
        setDrivenKeyframe(self.fkChain[0], cd='%s.FK_IK' % self.footCnt, at='visibility', dv=1, v=0)
        setDrivenKeyframe(self.fkChain[0], cd='%s.FK_IK' % self.footCnt, at='visibility', dv=0, v=1)

        if self.numToes > 0:
            #--- Call: Create toes rig
            self.createToesRig()           
    
    def createToesRig(self,*args):
        """
        Create fk attributes/controls on toe joints 
        on foot control.
        """
        if self.side == 1:
            # Left
            jntNames = self.sNames.feetJoints.keys()
            
            temp = self.sNames.feetJoints['left_pinkyToe1'].split('_')
            leftAttName1 = temp[1]
            temp = self.sNames.feetJoints['left_ringToe1'].split('_')
            leftAttName2 = temp[1]
            temp = self.sNames.feetJoints['left_middleToe1'].split('_')
            leftAttName3 = temp[1]
            temp = self.sNames.feetJoints['left_indexToe1'].split('_')
            leftAttName4 = temp[1]
            temp = self.sNames.feetJoints['left_bigToe1'].split('_')
            leftAttName5 = temp[1]
            
            leftAttNames = [leftAttName1,
                               leftAttName2,
                               leftAttName3,
                               leftAttName4,
                               leftAttName5 ] 
            
            leftStartJoints = [self.sNames.feetJoints['left_pinkyToe1'],
                               self.sNames.feetJoints['left_ringToe1'],
                               self.sNames.feetJoints['left_middleToe1'],
                               self.sNames.feetJoints['left_indexToe1'],
                               self.sNames.feetJoints['left_bigToe1'] ] 
            
            leftEndJoints = [self.sNames.feetJoints['left_pinkyToe3'],
                               self.sNames.feetJoints['left_ringToe3'],
                               self.sNames.feetJoints['left_middleToe3'],
                               self.sNames.feetJoints['left_indexToe3'],
                               self.sNames.feetJoints['left_bigToe3'] ]
            
            # Create the controllers @ todo - setup inputs/variables for curl, twist & spread vs constants
            createFingersOrToesRig.createFingersOrToesRig( label = '%s_foot'%self.sNames.prefix['left'],  
                                                           control = self.sNames.controlNames['left_foot'],
                                                           attNames = leftAttNames,
                                                           startJnts = leftStartJoints,
                                                           endJnts = leftEndJoints,
                                                           curl = 'Z',
                                                           twist = 'X',
                                                           spread = 'Y',
                                                           fkNormal = self.fkNormal,
                                                           radius = self.fkRadius/2.0 )
        
        if self.side == 2:
            # Right
            temp = self.sNames.feetJoints['right_pinkyToe1'].split('_')
            rightAttName1 = temp[1]
            temp = self.sNames.feetJoints['right_ringToe1'].split('_')
            rightAttName2 = temp[1]
            temp = self.sNames.feetJoints['right_middleToe1'].split('_')
            rightAttName3 = temp[1]
            temp = self.sNames.feetJoints['right_indexToe1'].split('_')
            rightAttName4 = temp[1]
            temp = self.sNames.feetJoints['right_bigToe1'].split('_')
            rightAttName5 = temp[1]
            
            rightAttNames = [rightAttName1,
                               rightAttName2,
                               rightAttName3,
                               rightAttName4,
                               rightAttName5 ] 
            
            rightStartJoints = [self.sNames.feetJoints['right_pinkyToe1'],
                               self.sNames.feetJoints['right_ringToe1'],
                               self.sNames.feetJoints['right_middleToe1'],
                               self.sNames.feetJoints['right_indexToe1'],
                               self.sNames.feetJoints['right_bigToe1'] ] 
            
            rightEndJoints = [self.sNames.feetJoints['right_pinkyToe3'],
                               self.sNames.feetJoints['right_ringToe3'],
                               self.sNames.feetJoints['right_middleToe3'],
                               self.sNames.feetJoints['right_indexToe3'],
                               self.sNames.feetJoints['right_bigToe3'] ]

            createFingersOrToesRig.createFingersOrToesRig( label = '%s_foot'%self.sNames.prefix['right'],  
                                                           control = self.sNames.controlNames['right_foot'],
                                                           attNames = rightAttNames,
                                                           startJnts = rightStartJoints,
                                                           endJnts = rightEndJoints,
                                                           curl = 'Z',
                                                           twist = 'X',
                                                           spread = 'Y',
                                                           fkNormal = self.fkNormal,
                                                           radius = self.fkRadius/2.0 )
        #--- Call: self.toeCntSetup()
        self.toeCntSetup()
    
    def toeCntSetup(self,*args):
            """
            Create toe control that follows IK / FK chains. Cnt curve at end of foot.
            """
            if self.side == 1:
                side = 'l_'
                toe_cnt_jnt = duplicate(self.sNames.feetJoints['left_footBall'], n=side + 'toe_cnt_jnt')
                temp = listRelatives(toe_cnt_jnt, children=True)
                delete(temp)
                
                # snap controller curve to joint
                self.lib.snapping(self.sNames.controlNames['left_toe'],toe_cnt_jnt)
                
                # Parent joint to control curve
                parent(  toe_cnt_jnt, self.sNames.controlNames['left_toe'] )
                
                # Parent control to footBall_jnt
                parent( self.sNames.controlNames['left_toe']+'_buffer', self.sNames.feetJoints['left_footBall'] )
                
                # Parent toes to toe_cnt_jnt
                parent( self.sNames.feetJoints['left_pinkyToe1'] +'_all_jnt', toe_cnt_jnt )
                parent( self.sNames.feetJoints['left_ringToe1'] +'_all_jnt', toe_cnt_jnt )
                parent( self.sNames.feetJoints['left_middleToe1'] +'_all_jnt', toe_cnt_jnt )
                parent( self.sNames.feetJoints['left_indexToe1'] +'_all_jnt', toe_cnt_jnt )
                parent( self.sNames.feetJoints['left_bigToe1'] +'_all_jnt', toe_cnt_jnt )
                
                # Move values from controller transform to its' buffer
                orig_val = getAttr( self.sNames.controlNames['left_toe']+'_buffer.translate' )
                new_val = getAttr( self.sNames.controlNames['left_toe']+'.translate' )
                setAttr( self.sNames.controlNames['left_toe']+'_buffer.translate', (orig_val + new_val ))
                setAttr( self.sNames.controlNames['left_toe']+'.translate', 0,0,0)
                
                orig_val = getAttr( self.sNames.controlNames['left_toe']+'_buffer.rotate' )
                new_val = getAttr( self.sNames.controlNames['left_toe']+'.rotate' )
                setAttr( self.sNames.controlNames['left_toe']+'_buffer.rotate', (orig_val + new_val ))
                setAttr( self.sNames.controlNames['left_toe']+'.rotate', 0,0,0)
                
            if self.side == 2:
                side = 'r_'
                toe_cnt_jnt = duplicate(self.sNames.feetJoints['right_footBall'], n=side + 'toe_cnt_jnt')
                temp = listRelatives(toe_cnt_jnt, children=True)
                delete(temp)
                                
                # snap controller curve to joint
                self.lib.snapping(self.sNames.controlNames['right_toe'],toe_cnt_jnt)
                
                # Parent joint to control curve
                parent(  toe_cnt_jnt, self.sNames.controlNames['right_toe'] )
                
                # Parent control to footBall_jnt
                parent( self.sNames.controlNames['right_toe']+'_buffer', self.sNames.feetJoints['right_footBall'] )
                
                # Parent toes to toe_cnt_jnt
                parent( self.sNames.feetJoints['right_pinkyToe1'] +'_all_jnt', toe_cnt_jnt )
                parent( self.sNames.feetJoints['right_ringToe1'] +'_all_jnt', toe_cnt_jnt )
                parent( self.sNames.feetJoints['right_middleToe1'] +'_all_jnt', toe_cnt_jnt )
                parent( self.sNames.feetJoints['right_indexToe1'] +'_all_jnt', toe_cnt_jnt )
                parent( self.sNames.feetJoints['right_bigToe1'] +'_all_jnt', toe_cnt_jnt )
 
                # For some reason, right control buffer and control need to be 0,0,0. If values creep onto controller, start investigating here!
                # Move values from controller transform to its' buffer
#                orig_val = getAttr( self.sNames.controlNames['right_toe']+'_buffer.translate' )
#                new_val = getAttr( self.sNames.controlNames['right_toe']+'.translate' )
                setAttr( self.sNames.controlNames['right_toe']+'_buffer.translate', 0,0,0)
                setAttr( self.sNames.controlNames['right_toe']+'.translate', 0,0,0)
                
#                orig_val = getAttr( self.sNames.controlNames['right_toe']+'_buffer.rotate' )
#                new_val = getAttr( self.sNames.controlNames['right_toe']+'.rotate' )
                setAttr( self.sNames.controlNames['right_toe']+'_buffer.rotate',0,0,0)
                setAttr( self.sNames.controlNames['right_toe']+'.rotate', 0,0,0)