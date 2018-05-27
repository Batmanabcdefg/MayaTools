from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *
"""
Copyright (c) 2010,2011 Mauricio Santos-Hoyos
Name: connectJointChains.py
Version: 1.0
Author: Mauricio Santos-Hoyos
Contact: mauricioptkvp@hotmail.com
Date Created:   9 Oct 2010
Last Modified:  21 Mar 2011

$Revision: 140 $
$LastChangedDate: 2011-09-13 00:36:32 -0700 (Tue, 13 Sep 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/createIkPoleVector.py $
$Id: createIkPoleVector.py 140 2011-09-13 07:36:32Z mauricio $

Description: 
    Given RP IK handle, IK_Controller curve, create PV_Control and twist, visibility attributes.
    

Used by: createArmRig.py, createLegRig.py

Uses:

Process:
            Create the pole vector control curve.
            Create plane with points on shoulder, elbow and wrist.
            Translate elbow point of plane along the normal,
            then snap the control curve to the point.
            Zero controller
            Setup elbow twist attribute on ikControl
            Setup PV visibility attribute on ikControl
            Delete the plane
    
Additional Notes: 

Example call:
>>import createIkPoleVector as cpv
>>cpv.createIkPoleVector(    prefix='test',
                             side = 1, 
                             type = 'arm', 
                             ikHandle='test_l_arm_ikRpHandle',
                             ikControl='test_l_armIk_cntrl',
                             worldcontrol = 'Main_cnt'    )
      
Attributes:

Keywords:
    prefix: Prefix for nodes created during setup

    Side:    1 == Left/+X  and  2 == Right/-X
    
    type: 'arm' = move PV back. 'leg' = move PV forward
    
    ikHandle: RPIK Handle
    
    ikControl: IK control object (curve)
             
Requires:


Development notes:
@Todo    
- Create 'Follow' attribute on pv_cnt: Switch between: ik_arm,cog,world.
- support up and aim axis input. Used to draw controller curve.
         
   
"""

import commonMayaLib as cml
import spaceSwitch as ss
import standardNames

reload( cml )
reload( ss )
reload( standardNames )

class createIkPoleVector():
    """
    Given RP IK handle, IK_Controller curve, create PV_Control and twist, visibility attributes.
    Assumes Y will always be up.
    """
    def __init__(self,**keywords):      
        # Create library instance
        self.lib = cml.commonMayaLib()
        
        # Create standard names instance
        self.sNames = standardNames.standardNames()
        
        # Used to return the name of created nodes
        self.createdNodes = []
          
        # Check if command line call
        if len(keywords):
            self.commandlineCall(keywords)
        else:
            self.buildGUI()
            
    def commandlineCall(self,keywords):
        """
        Verify and Store the data passed via command line keywords dictionary.
        """    
        self.prefix = keywords['prefix']
        self.side = keywords['side']
        self.type = keywords['type']
        self.ikHandle = keywords['ikHandle']
        self.ikControl = keywords['ikControl']
        self.worldControl = keywords['worldControl']
        
        self.createPoleVector()

    def buildGUI(self,*args):
        """
        Create GUI in Maya
        """
        if(window("msCreatePoleVectorWin",exists=True)):
                deleteUI("msCreatePoleVectorWin",window=True)
        
        with window("msCreatePoleVectorWin",title="Create Pole Vector Setup v1.0",rtf=True) as mainWin:
            with formLayout() as form:
                text('\t\tCreate a Pole Vector control and attributes for given IK handle/ Control.',font='boldLabelFont')
                
                separator(w=500)
                
                self.prefixFld = textFieldGrp(label='Prefix:',text='')
                self.sideFld = radioButtonGrp(label="Side:",labelArray2=['Left(+X)','Right(-X)'],nrb=2,sl = 1)
                self.typeFld = radioButtonGrp(label="Type:",labelArray2=['Arm','Leg'],nrb=2,sl = 1)
                
                separator(w=500)
                
                self.ikHandleFld = textFieldButtonGrp(label='IK RP Handle:',bc=self.loadIkHandle,bl='Load',text='')
                self.ikControlFld = textFieldButtonGrp(label='IK Control:',bc=self.loadIkControl,bl='Load',text='')
                self.worldControlFld = textFieldButtonGrp(label='World Control:',bc=self.loadWorldControl,bl='Load',text='')
                separator(w=500)
                
                with rowLayout(nc=2,cw2=(200,100)):
                    text(" ")
                    button(label="-=Create=-",c=self.guiCall,w=80)
                
                form.redistribute()
            mainWin.show()
            
    def guiCall(self,*args):
        """
        Verify and Store the data passed via GUI.
        """
        self.prefix = textFieldGrp(self.prefixFld,query=True,text=True)
        self.side = radioButtonGrp(self.sideFld,q=True,sl=True)
        self.type = textFieldGrp(self.typeFld,query=True,text=True)
        
        if self.type == 1:
            self.type = 'arm'
        if self.type == 2:
            self.type = 'leg'
        
        self.ikHandle = textFieldButtonGrp(self.ikHandleFld,q=True,text=True)
        self.ikControl = textFieldButtonGrp(self.ikControlFld,q=True,text=True)
        self.worldControl = textFieldButtonGrp(self.worldControlFld,q=True,text=True)
                
        self.createPoleVector()
        
    def createPoleVector(self,*args):
        """
        Given RP IK handle, IK_Controller curve, create PV_Control and twist, visibility attributes.
        """
        """
            Create the pole vector control curve.
            Create plane with points on shoulder, elbow and wrist.
            Translate elbow point of plane along the normal,
            then snap the control curve to the point.
            Zero controller
            Setup elbow twist attribute on ikControl
            Setup PV visibility attribute on ikControl
            Delete the plane
        """
        #  Get shoulder, elbow, wrist joints
        shoulderJoint = self.ikHandle.getStartJoint()
        effector = self.ikHandle.getEndEffector()
        temp = listRelatives(effector,parent=True)
        elbowJoint = temp[0]
        temp = listRelatives(elbowJoint,children=True)
        wristJoint = temp[0]
        
        self.pv_cnt = '%s_pv_cnt' % self.prefix
        
        # Store the name so client can access it
        self.createdNodes.append(self.pv_cnt)
        
        #Create the pole vector control curve
        self.createControl()
        
        #Get joint positions
        loc1Pos = xform(shoulderJoint,q=True,ws=True,t=True)
        loc2Pos = xform(elbowJoint,q=True,ws=True,t=True)
        loc3Pos = xform(wristJoint,q=True,ws=True,t=True)
        
        #Draw the plane used to get location for pole vector control
        temp = polyPlane(sx=1, sy=1, w=1, h=1)
        plane = temp[0]
        
        #Delete vertex 4
        delete('%s.vtx[3]' % plane)
        
        #Snap verts to positions
        move('%s.vtx[0]' % plane,loc1Pos[0], loc1Pos[1], loc1Pos[2],  moveXYZ=True)
        move('%s.vtx[1]' % plane,loc2Pos[0], loc2Pos[1], loc2Pos[2],  moveXYZ=True)
        move('%s.vtx[2]' % plane,loc3Pos[0], loc3Pos[1], loc3Pos[2], moveXYZ=True)
        
        #Move vertex 1 along it's normal by a magnitude of 10 units
        if self.type == 'arm': # -Z
            moveVertexAlongDirection('%s.vtx[1]' % plane,d=(0,0,-1),m=10)
        if self.type == 'leg': # +Z
            moveVertexAlongDirection('%s.vtx[1]' % plane,d=(0,0,1),m=10)
        
        #Snap self.pv_cnt to the vert
        self.lib.snapping(self.pv_cnt,'%s.vtx[1]'%plane)
        
        #Rotate PV_cnt 90 in Y
        setAttr('%s.rotateY'%self.pv_cnt,90)
        
        # zero self.pv_cnt
        self.bufferNode = self.lib.zero(self.pv_cnt)
        
        # Delete the plane
        delete(plane)
        
        # Parent bufferNode to ikControl 
        parent(self.bufferNode,self.ikControl)  
       
        # Create a follow attribute      
        #--- Setup space switch
        self.createSwitch()

        # Create the constraint
        poleVectorConstraint(self.pv_cnt, self.ikHandle)
        
        # Lock rotates of buffer node
        setAttr('%s.rotateX'%self.bufferNode,lock=True,keyable=False)
        setAttr('%s.rotateY'%self.bufferNode,lock=True,keyable=False)
        setAttr('%s.rotateZ'%self.bufferNode,lock=True,keyable=False)
        
        # PV elbow twist / PV_control vis switch
        addAttr(self.ikControl, ln='pv_vis__', k=True, at='short')
        setAttr('%s.pv_vis__'%self.ikControl,lock=True)
        addAttr(self.ikControl, ln='pv_vis', k=True, at='short',hasMinValue=True,hasMaxValue=True,min=0,max=1,dv=1)
        connectAttr('%s.pv_vis' % self.ikControl, '%s.visibility' % self.bufferNode, f=True)
        addAttr(self.ikControl, ln='elbow', k=True, at='float')
            
        if self.side == 1:
            connectAttr('%s.elbow' % self.ikControl, '%s.twist' % self.ikHandle, f=True)
            
            # Set the color to red
            setAttr('%s.ovc' % self.ikControl, 13)
            
        else: #Route through a reverse node so that behavior mirrors left.
            mdNode = createNode('multiplyDivide')
            setAttr('%s.input2X'%mdNode,1)
            name = self.prefix + '_' + mdNode
            rename(mdNode,name)
            mdNode = name
            
            connectAttr('%s.elbow' % self.ikControl, '%s.input1X' % mdNode, f=True)
            connectAttr('%s.outputX' % mdNode, '%s.twist' % self.ikHandle, f=True)     
            
            # Set the color to blue
            setAttr('%s.ovc' % self.ikControl, 6)      

    def createSwitch(self,*args):
        """
        Create space switch for PV controller.
        """
        # Add attributes to IK controller
        select(self.ikControl,r=True)
        addAttr(longName='pv_space_switch',k=True)
        setAttr(self.ikControl + '.pv_space_switch',lock=True)
        addAttr(longName='pv_world',k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        addAttr(longName='pv_arm',k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        addAttr(longName='pv_shoulder',k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        addAttr(longName='pv_cog',k=True,hasMinValue=True,hasMaxValue=True,minValue=0,maxValue=1.0)
        
        # Constrain IK controller buffer node
        pConst = parentConstraint( self.worldControl,
                                   self.ikControl,
                                   self.sNames.controlNames['shoulder'],
                                   self.sNames.controlNames['cog'],
                                   self.bufferNode,mo=True )

        # Make direct connections
        connectAttr( '%s.pv_world'%self.ikControl, 
                     pConst + '.' + str(self.worldControl) + 'W0' )
        connectAttr( '%s.pv_arm'%self.ikControl, 
                     pConst + '.' + str(self.ikControl) + 'W1' )
        connectAttr( '%s.pv_shoulder'%self.ikControl, 
                     pConst + '.' + str(self.sNames.controlNames['shoulder']) + 'W2' )
        connectAttr( '%s.pv_cog'%self.ikControl, 
                     pConst + '.' + str(self.sNames.controlNames['cog']) + 'W3' )      

    def createControl(self,*args):
        """
        Create the pole vector controller curve.
        """
        if 'l_' in self.prefix:
            color_val = 13
        else:
            color_val = 6
        
        melString = 'createNode transform -n "%s";' %self.pv_cnt 
        melString = melString + 'setAttr ".ove" yes;'
        melString = melString + 'setAttr ".ovc" %s;'%color_val
        melString = melString + 'createNode nurbsCurve -n "%sShape1" -p "%s";' % (self.pv_cnt,self.pv_cnt)
        melString = melString + 'setAttr -k off ".v";'
        melString = melString + 'setAttr ".cc" -type "nurbsCurve"'
        melString = melString + '    1 7 0 no 3'
        melString = melString + '    8 0 1 2 3 4 5 6 7'
        melString = melString + '    8'
        melString = melString + '    -2 0 0'
        melString = melString + '    1 0 1'
        melString = melString + '    1 0 -1'
        melString = melString + '    -2 0 0'
        melString = melString + '    1 1 0'
        melString = melString + '    1 0 0'
        melString = melString + '    1 -1 0'
        melString = melString + '    -2 0 0'

        mel.eval( melString )
        
    def loadIkHandle(self,*args):
        sel = ls(sl=True,fl=True)
        textFieldButtonGrp(self.ikHandleFld,e=True,text=sel[0])  
        
    def loadIkControl(self,*args):
        sel = ls(sl=True,fl=True)
        textFieldButtonGrp(self.ikControlFld,e=True,text=sel[0]) 
        
    def loadWorldControl(self,*args):
        sel = ls(sl=True,fl=True)
        textFieldButtonGrp(self.worldControlFld,e=True,text=sel[0]) 
        