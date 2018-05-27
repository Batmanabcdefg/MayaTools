from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *

"""
Copyright (c) 2010 Mauricio Santos-Hoyos
Script name: orientJoints.py
Created on: 8 Oct 2010
Last modified: 8 Oct 2010
Version: 1.0
Author(s): Mauricio Santos-Hoyos

$Revision: 132 $
$LastChangedDate: 2011-08-06 19:27:15 -0700 (Sat, 06 Aug 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/orientJoints.py $
$Id: orientJoints.py 132 2011-08-07 02:27:15Z mauricio $

Description:
    Problem: 
        When you move a joint, it un-aligns the axis that 
        should be pointing to the next joint down the chain. 

    Solution:
        Quickly re-orient either the selected joint, or its hierarchy via GUI or command line.
        Joint chain should have no branches below selected joint.

Used by:
    createArmRig.py
    

Uses:
    

Inputs (keywords) :
                joint = name of joint
                hierarchy = 1/2 (1=True,2=False)
                aim_axis = 1,2 or 3 (x,y,z)
                aim_polarity = 1,2 (+/-)
                up_axis = 1,2 or 3 (x,y,z)
                up_polarity = 1,2 (+/-)
    


Returns:

Example call:
>> import orientJoints
>> orientJoints(joint='joint1',
                hierarchy=1,
                aim_axis=1,
                aim_polarity=1,
                up_axis=2,
                up_polarity=1)


Development notes:
    2010-10-08 : Initial creation
    2010-10-13 : Handle transform in chain
"""

class orientJointsError():
    def __repr__(self,*args):
        return 'No joint selected!'

class orientJoints():
    """
    Quickly re-orient either the selected joint, or its hierarchy.
    Joint chain should have no branches below selected joint.
    """
    def __init__(self,**keywords):
        # Check if command line call
        if len(keywords):
            self.commandlineCall(keywords)
        else:
            self.buildGUI()
            
    def commandlineCall(self,keywords):
        """
        Verify and Store the data passed via command line keywords dictionary.
        """    
        # Used to track if called by GUI or command line
        self.gui = 0
                
        # Initialize variables based on user input
        jnt = keywords['joint']
        self.hierarchyOption = keywords['hierarchy']
        self.aim = keywords['aim_axis']
        self.aimPolarity = keywords['aim_polarity']
        self.up = keywords['up_axis']
        self.upPolarity = keywords['up_polarity']
        
        self.aimAxis = []
        self.upAxis = []

        if self.aimPolarity == 1:
            if self.aim == 1:
                self.aim = 'X' #Used in the fk control setup
                self.aimAxis = (1,0,0)
            if self.aim == 2:
                self.aim = 'Y'
                self.aimAxis = (0,1,0)
            if self.aim == 3:
                self.aim = 'Z'
                self.aimAxis = (0,0,1)
        else:
            if self.aim == 1:
                self.aim = 'X'
                self.aimAxis = (-1,0,0)
            if self.aim == 2:
                self.aim = 'Y'
                self.aimAxis = (0,-1,0)
            if self.aim == 3:
                self.aim = 'Z'
                self.aimAxis = (0,0,-1)

        if self.up == 1:
            self.upAxis = (1,0,0)
        if self.up == 2:
            self.upAxis = (0,1,0)
        if self.up == 3:
            self.upAxis = (0,0,1)

        if self.upPolarity == 1:
            self.upPolarity = 1
        if self.upPolarity == 2:
            self.upPolarity = -1
            
        self.orient(jnt)

    def buildGUI(self,*args):
        """
        Create GUI in Maya
        """
        if(window("msOrientJoint",exists=True)):
                deleteUI("msOrientJoint",window=True)
        
        with window("msOrientJoint",title="Orient Joint v1.0",rtf=True) as mainWin:
            with columnLayout():
        
                with rowLayout(nc=2):
                    text("\n\n")
                    text("\t\t\t\tOrient selected joint to it's child.",font='boldLabelFont')
                
                separator(w=500)
                
                text('\t\tJoint chain should not have branches if hierarchy is used.')
                self.hiFld = radioButtonGrp(label="Orient hierarchy?",labelArray2=['Yes','No'],nrb=2,sl=2)
                self.aimAxisFld = radioButtonGrp(label="Aim Axis",labelArray3=['x','y','z'],nrb=3,sl = 1)
                self.aimAxisPolFld = radioButtonGrp(label="Aim Axis Polarity",labelArray2=['+','-'],nrb=2,sl = 1)
                self.upAxisFld = radioButtonGrp(label="Up Axis",labelArray3=['x','y','z'],nrb=3,sl  = 2)
                self.upAxisPolFld = radioButtonGrp(label="Up Axis Polarity",labelArray2=['+','-'],nrb=2,sl=1)
                
                separator(w=500)
                text('\n\t\t\tSelect joint, then click a button below.')
                with rowLayout(nc=3,cw3=(150,100,100)):
                    text(" ")
                    button(label="-=Orient=-",c=self.guiCall,w=80)
                    button(label="-=None Orient=-",c=self.noneOrient,w=80)

            mainWin.show()
            
    def guiCall(self,*args):
        """
        Verify and Store the data passed via GUI.
        """
        jnt = ls(sl=True,type='joint')
        
        # If no joint selected
        if not len(jnt):
            raise orientJointsError
            return
         
        self.hierarchyOption = radioButtonGrp(self.hiFld,q=True,sl=True)
        self.aim = radioButtonGrp(self.aimAxisFld,q=True,sl=True)
        self.aimPolarity = radioButtonGrp(self.aimAxisPolFld,q=True,sl=True)
        self.up = radioButtonGrp(self.upAxisFld,q=True,sl=True)
        self.upPolarity = radioButtonGrp(self.upAxisPolFld,q=True,sl=True)
        
        self.aimAxis = []
        self.upAxis = []

        if self.aimPolarity == 1:
            if self.aim == 1:
                self.aim = 'X' 
                self.aimAxis = (1,0,0)
            if self.aim == 2:
                self.aim = 'Y'
                self.aimAxis = (0,1,0)
            if self.aim == 3:
                self.aim = 'Z'
                self.aimAxis = (0,0,1)
        else:
            if self.aim == 1:
                self.aim = 'X'
                self.aimAxis = (-1,0,0)
            if self.aim == 2:
                self.aim = 'Y'
                self.aimAxis = (0,-1,0)
            if self.aim == 3:
                self.aim = 'Z'
                self.aimAxis = (0,0,-1)

        if self.up == 1:
            self.upAxis = (1,0,0)
        if self.up == 2:
            self.upAxis = (0,1,0)
        if self.up == 3:
            self.upAxis = (0,0,1)

        if self.upPolarity == 1:
            self.upPolarity = 1
        if self.upPolarity == 2:
            self.upPolarity = -1
            
        self.orient(jnt[0])
        
    def orient(self,jnt):
        """
        Orient the selected joint, or it's entire hierarchy.
        """
        # If a none joint passed in, check it for a child joint
        select(jnt,replace=True)
        temp_jnt = ls(sl=True,type='joint')
        
        # Initial assignment of self.jnt
        # If it's a joint
        if len(temp_jnt):
            self.jnt = jnt
            
        # If it's not
        else:
            # Get the child
            child = listRelatives(jnt,c=True)
            
            # Check if it's a joint 
            select(child[0],replace=True)
            temp = ls(sl=True,type='joint')
            
            # Orient it.
            if len(temp):
                self.jnt = temp[0]
                
            # Terminate
            else:
                return
            
        if self.hierarchyOption == 2: # False
            # Get the child node
            childJnt = listRelatives(self.jnt,c=True)     
            
            if not len(childJnt): # No children = None orient
                select(self.jnt,replace=True)
                self.noneOrient()  
                   
            else:                     
                #Unparent child (aim target) so it retains its position during the reorientation of it's parent
                parent(childJnt[0],w=True)
    
                #Zero Orients and Rotations on joint
                setAttr(self.jnt + ".rotate",0,0,0)
                setAttr(self.jnt + ".jointOrient",0,0,0)
    
                #Create locator, snap to joint
                loc = spaceLocator()
                self.snapping(loc,self.jnt)
                
                #Match locator orientations to joint
                temp = orientConstraint(self.jnt,loc,mo=False)
                delete(temp)
    
                #Move locator 1 in up direction
                if self.up == 1:
                    move(loc,self.upPolarity,x=1,r=1)
                if self.up == 2:
                    move(loc,self.upPolarity,y=1,r=1)
                if self.up == 3:
                    move(loc,self.upPolarity,z=1,r=1)
    
                #The Aim constriant: joint aimed at it's child.
                temp = aimConstraint(childJnt[0],self.jnt,aimVector=self.aimAxis,upVector=self.upAxis,worldUpType="object",worldUpObject=loc)
                delete(temp)
                delete(loc)
    
                #Copy joint Rotations and Paste to joint Orients.
                #Then Set joint Rotations to 0,0,0
                tempRotations = getAttr(self.jnt + ".rotate")
                setAttr(self.jnt + ".jointOrient",tempRotations[0],tempRotations[1],tempRotations[2])
                setAttr(self.jnt + ".rotate",0,0,0)
    
                # Reparent the child
                parent(childJnt[0],self.jnt)
                select(childJnt[0],replace=True)
                
        else:
            # Get the child node
            childJnt = listRelatives(self.jnt,c=True)
            
            # No children = Last joint = None orient
            if not len(childJnt):
                select(self.jnt,replace=True)
                self.noneOrient()
                
            # Not a joint?
            
            else:
                #Unparent child (aim target) so it retains its position during the reorientation of it's parent
                parent(childJnt[0],w=True)
    
                #Zero Orients and Rotations on joint
                setAttr(self.jnt + ".rotate",0,0,0)
                setAttr(self.jnt + ".jointOrient",0,0,0)
    
                #Create locator, snap to self.jnt
                loc = spaceLocator()
                self.snapping(loc,self.jnt)
                
                #Match locator orientations to self.jnt
                temp = orientConstraint(self.jnt,loc,mo=False)
                delete(temp)
    
                #Move locator 1 in up direction
                if self.up == 1:
                    move(loc,self.upPolarity,x=1,r=1)
                if self.up == 2:
                    move(loc,self.upPolarity,y=1,r=1)
                if self.up == 3:
                    move(loc,self.upPolarity,z=1,r=1)
    
                #The Aim constriant: self.jnt aimed at it's child.
                temp = aimConstraint(childJnt[0],self.jnt,aimVector=self.aimAxis,upVector=self.upAxis,worldUpType="object",worldUpObject=loc)
                delete(temp)
                delete(loc)
    
                #Copy self.jnt Rotations and Paste to self.jnt Orients.
                #Then Set self.jnt Rotations to 0,0,0
                tempRotations = getAttr(self.jnt + ".rotate")
                setAttr(self.jnt + ".jointOrient",tempRotations[0],tempRotations[1],tempRotations[2])
                setAttr(self.jnt + ".rotate",0,0,0)
    
                # Reparent the child
                parent(childJnt[0],self.jnt)
                select(childJnt[0],replace=True)
                
                # Select the child joint and call orient function again (recursive call) 
                # Base case: selected joint has no children. end recursive calling.
                self.orient(childJnt[0])
                    
    def noneOrient(self,*args):
        """
        Perform a none-orient on the selected joint.
        """
        jnt  = ls(sl=True,type='joint')
        if(self.up == 1): 
            upAxis = "xup"
        if(self.up == 2):
            upAxis = "yup"            
        if(self.up == 3):
            upAxis = "zup"
            
        joint(jnt[0],e=True, oj='none',secondaryAxisOrient=upAxis,zso=True,ch=True)
    
    def snapping(self,loc,srcName,*args):
        """
        Snap loc to sourceName.
        """
        pos = xform( srcName, q=1, ws=True, t=1)
        xform( loc, ws=True, t=[pos[0], pos[1], pos[2]]) 

        rot = xform( srcName, q=1, ws=True, ro=1)
        xform( loc, ws=True, ro=[rot[0], rot[1], rot[2]])    
        
        
            