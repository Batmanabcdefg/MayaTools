from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *

"""
Copyright (c) 2010 Mauricio Santos-Hoyos
Name: makeIkStretchy.py
Version: 1.0
Author: Mauricio Santos-Hoyos
Contact: mauricioptkvp@hotmail.com
Date Created:   9 Oct 2010

$Revision: 135 $
$LastChangedDate: 2011-08-28 07:06:08 -0700 (Sun, 28 Aug 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/makeIkStretchy.py $
$Id: makeIkStretchy.py 135 2011-08-28 14:06:08Z mauricio $

Description: 
    Given RP IK handle or splineIK curve, and a control, make the IK stretchy
    and add stretchy 'on/off' and 'volume' attributes.
    

Used by: createArmRig.py, createLegRig.py

Uses:

Process:
        
    
Additional Notes: 

Example call:
>>import makeIkStretchy as mis
>>makeIkStretchy.makeIkStretchy( prefix='%s_legRig'%self.prefix,
                             type=1,
                             axis=1,
                             control=self.ikControl,
                             ik=self.leg_ikHandle[0] )
      
Attributes:

Keywords:
    type: 1 = Spline IK, 2 = RP IK

    axis: 1=x, 2=y, 3=z : Axis to stretchy along.

    control:    Any controller you want the attributes on.
    
    ik: ikHandle
    
    ikControl: IK control object (curve)
             
Requires:


Development notes:
   
   @todo - On/off attribute : Got it working for RP stretch setup.
   
"""

import commonMayaLib as cml

class MakeIkStretchyError(Exception): pass

class SplineIkNotSelected(MakeIkStretchyError):
    def __repr__(self,*args):
        return 'Spline IK Handle not selected!'

class ikRpNotSelected(MakeIkStretchyError):
    def __repr__(self,*args):
        return 'IK RP Handle not selected!'

class makeIkStretchy():
    """
    Given RP IK handle or splineIK curve, and a control, make the IK stretchy
    and add stretchy 'on/off' and 'volume' attributes.
    """
    def __init__(self,**keywords):      
        # Create library instance
        self.lib = cml.commonMayaLib()
        
        # Used to store data to return to client
        self.createdNodes = {}
          
        # Command line call
        self.commandlineCall(keywords)

    def commandlineCall(self,keywords):
        """
        Verify and Store the data passed via command line keywords dictionary.
        """    
        self.prefix = keywords['prefix']
        self.side = keywords['side']
        self.type = keywords['type']
        self.axis = keywords['axis']
        self.control = keywords['control']
        self.ik = keywords['ik'] 
        
        self.makeStretchy()
        
    def makeStretchy(self,*args):
        """
        Call the appropriate function
        """
        if self.type == 1:
            self.makeRpStretchy()
        if self.type == 2:
            self.makeSplineStretchy()
            
    def makeRpStretchy(self,*args):
        """
        Make IK RP Handle Stretchy
        """
        # Get the shoulder and elbow
        try:
            self.joints = ikHandle(self.ik,query=True,jl=True)
        except:
            raise ikRpNotSelected
        
        # Get the stretch along axis
        if self.axis == 1:
            self.axisVal = 'X'
        if self.axis == 2:
            self.axisVal = 'Y'
        if self.axis == 3:
            self.axisVal = 'Z'
        
        # Get the wrist joint
        wrist = listRelatives(self.joints[1],children=True)
        self.joints.append( wrist[0] )
        
        #
        # Full length distance dimension node
        #
        
        #Get world space of ik_1 and ik_end joints, used to place distDimension node locators
        ikBaseJntPos = xform(self.joints[0],query=True,t=True,ws=True)
        ikEndJntPos = xform(self.joints[2],query=True,t=True,ws=True)
        
        # Create distanceDimensionShape. 
        # Create locators at locations that do not already have locators. 
        # If locations overlap, a new locator will not be created. The distance node 
        # will use the existing locator.
        fullLenDD = distanceDimension( sp=[1,0,0], ep=[0,1,0] )
        
        #Get created locators names
        temp = listConnections(fullLenDD)
        temp1 = temp[0]
        temp2 = temp[1]
        
        #Rename locators
        rename(temp1,('%s%s_fullLen_start'%(self.prefix,temp1) ) )
        rename(temp2,('%s%s_fullLen_end'%(self.prefix,temp2) ) )
        
        #Rename Distance Dimension node    
        temp = pickWalk(fullLenDD,direction='up')
        rename(temp[0],('%s%s_fullLen_DD'%(self.prefix,temp[0]) ) )
        
        #Store names
        fullLenLoc_start = '%s'%(temp1)
        fullLenLoc_end = '%s'%(temp2)
        fullLen_DD = '%s%s_fullLen_DD'%(self.prefix,temp[0])
        fullLen_DDShape = '%s%s_fullLen_DDShape'%(self.prefix,temp[0])
        
        #Now, snap the locators to the right position.
        move(fullLenLoc_start,ikBaseJntPos[0],ikBaseJntPos[1],ikBaseJntPos[2],moveXYZ=True)
        move(fullLenLoc_end,ikEndJntPos[0],ikEndJntPos[1],ikEndJntPos[2],moveXYZ=True)
        
        # Create the stretchy rig top node
        distGrp = self.prefix + '_distGrp'
        group(em=True,n=distGrp)
        parent(fullLenLoc_start,fullLenLoc_end,fullLen_DD,distGrp)
        setAttr(distGrp + '.visibility',0)
        
        # Store it so client can get the name
        self.createdNodes['distGrp'] = distGrp

        #point constraint locators
        fullLenDD_startLoc_PC = pointConstraint(self.joints[0], fullLenLoc_start,mo=False)
        fullLenDD_endLoc_PC = pointConstraint(self.ik, fullLenLoc_end,mo=False)

        #Get dimension value
        origLen = getAttr(fullLen_DDShape + '.distance')
        
        #
        # Now, lets create the stretchy setup
        #  
        topJntLength = getAttr('%s.translate%s'%(self.joints[1],self.axisVal) )
        btmJntLength = getAttr('%s.translate%s'%(self.joints[2],self.axisVal) )
        fullLength = topJntLength + btmJntLength
        
        fullLength = abs(fullLength)         # Absolute values because distance should never be negative
        topJntLength = abs(topJntLength)
        btmJntLength = abs(btmJntLength) 
        
        driver = fullLen_DDShape + '.distance'          
        
        # Create SDKs
        if self.side == 1:
            setDrivenKeyframe(self.joints[1],cd=driver,dv=fullLength,at=('translate%s'%self.axisVal),v=topJntLength,itt='linear',ott='linear')
            setDrivenKeyframe(self.joints[1],cd=driver,dv=(fullLength*5),at=('translate%s'%self.axisVal),v=(topJntLength*5),itt='linear',ott='linear' )
            
            setDrivenKeyframe(self.joints[2],cd=driver,dv=fullLength,at=('translate%s'%self.axisVal),v=btmJntLength,itt='linear',ott='linear')
            setDrivenKeyframe(self.joints[2],cd=driver,dv=(fullLength*5),at=('translate%s'%self.axisVal),v=(btmJntLength*5),itt='linear',ott='linear' )
                
            setDrivenKeyframe(self.joints[1],cd=driver,dv=0,at=('translate%s'%self.axisVal),v=topJntLength,itt='linear',ott='linear' )
            setDrivenKeyframe(self.joints[2],cd=driver,dv=0,at=('translate%s'%self.axisVal),v=btmJntLength,itt='linear',ott='linear' )
        
        if self.side == 2:
            setDrivenKeyframe(self.joints[1],cd=driver,dv=fullLength,at=('translate%s'%self.axisVal),v=-topJntLength,itt='linear',ott='linear')
            setDrivenKeyframe(self.joints[1],cd=driver,dv=(fullLength*5),at=('translate%s'%self.axisVal),v=(-topJntLength*5),itt='linear',ott='linear' )
            
            setDrivenKeyframe(self.joints[2],cd=driver,dv=fullLength,at=('translate%s'%self.axisVal),v=-btmJntLength,itt='linear',ott='linear')
            setDrivenKeyframe(self.joints[2],cd=driver,dv=(fullLength*5),at=('translate%s'%self.axisVal),v=(-btmJntLength*5),itt='linear',ott='linear' )
                
            setDrivenKeyframe(self.joints[1],cd=driver,dv=0,at=('translate%s'%self.axisVal),v=-topJntLength,itt='linear',ott='linear' )
            setDrivenKeyframe(self.joints[2],cd=driver,dv=0,at=('translate%s'%self.axisVal),v=-btmJntLength,itt='linear',ott='linear' )

        # Disable cycle check
        #mel.eval('cycleCheck -e off')
        
        # Create the on/off attributes
        node_attr = '%s.%sW0'%( fullLenDD_endLoc_PC, self.ik)
        self.createOnOffSwitch( 'rp', self.control[0], node_attr)
        
            
    def makeSplineStretchy(self,*args):
        """
        Make spline Ik stretchy
        """
        self.joints = ikHandle(self.ik,query=True,jl=True)
        
        if(self.axis == 1):
            self.axisVal = 'X'
        if(self.axis == 2):
            self.axisVal = 'Y'
        if(self.axis == 3):
            self.axisVal = 'Z'
        
        try:
            #Get the ik curve
            curve = ikHandle(self.ik,query=True,c=True)
            curve = curve.split("|")
            curve = curve[1]
        except:
            raise SplineIkNotSelected
        
        #CurveInfo node creation
        curveInfoNode = arclen(curve,ch=True)
        
        #create/setup MD node
        mdNode = createNode("multiplyDivide")
        setAttr(mdNode + ".operation",2)
        connectAttr(curveInfoNode + ".arcLength", mdNode + ".i1x")
        arcLen = getAttr(curveInfoNode + ".arcLength")
        setAttr(mdNode + ".i2x", arcLen)

# @todo - Stretch based on translating along axis.
#        if 0:
#            # Get existing translation values
#            translateValues = []
#            for each in self.joints:
#                translateValues.append(getAttr(each + ".translate" + self.axisVal))
#            
#            # Now lets hook up the MD nodes for each joint, except the base.
#            x = 0
#            for each in self.joints:        
#                #Skip for base joint.
#                #if(each == joints[0]):
#                #        continue 
#              # Create MD node for joint and set it up, connect it.   
#              transMD = createNode("multiplyDivide")
#              setAttr(transMD + ".i2x",translateValues[x])  
#              connectAttr(mdNode + ".outputX",transMD + ".i1x")
#              connectAttr(transMD + ".outputX",each + ".translate" + self.axisVal)
#              x = x + 1   
#            
#              connectAttr(mdNode + ".outputX",each + ".translate" + self.axisVal)            
        
        if 1:
            for each in self.joints:
                connectAttr(mdNode + ".outputX",each + ".scale" + self.axisVal)
        
                
    def createOnOffSwitch(self,type,control,node_attr,*args):
        """ 
        Create on / off attribute for hand control.
        type : Spline / RP
        control: Where to put the attributes.
        node_attr : 'nodeName.attribute' to connect stretchy switch to.
        """
        #--- Add attributes to controller
        try:
            addAttr(control,longName='Stretch_On_Off', min=0, dv=0, k=True)#,keyable=False,hidden=False )
            addAttr(control,longName='S_On_Off', min=0, dv=1, max=1, k=True )
            setAttr('%s.Stretch_On_Off'%control,lock=True)
        except Exception, e:
            print e
            
        #--- connect attributes to stretchy on / off attributes.
        if type == 'rp':
            connectAttr('%s.S_On_Off'%control,node_attr,f=True)
                    
    
    def loadIk(self,*args):
        sel = ls(sl=True)
        textFieldButtonGrp(self.ikFld,edit=True,text=sel[0])

    def loadControl(self,*args):
        sel = ls(sl=True)
        textFieldButtonGrp(self.controlFld,edit=True,text=sel[0])
    
    
    
    
    
    
    
    
    