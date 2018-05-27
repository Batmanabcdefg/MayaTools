from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *

"""
Copyright (c) 2010 Mauricio Santos
Name: createHeadRig.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created:   22 Oct 2010

$Revision: 140 $
$LastChangedDate: 2011-09-13 00:36:32 -0700 (Tue, 13 Sep 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/createHeadRig.py $
$Id: createHeadRig.py 140 2011-09-13 07:36:32Z mauricio $

Description: 
    Create rigs for eyes, mouth(teeth, tongue,jaw ),ears.
    Joint placement based on default names defined in placeLocators.py

Process:


    
    
Additional Notes: 

Example call:
    import createHeadRig
    createHeadRig.createHeadRig()
      
Attributes:
    createdNodes = list of created nodes.

Keywords:

             
Requires:


Development notes:

    @todo - Tounge

"""

import makeIkStretchy
import orientJoints
import connectJointChains
import spaceSwitch
import standardNames
import createFingersOrToesRig
import commonMayaLib

# During development
reload(  makeIkStretchy )
reload(  orientJoints )
reload(  connectJointChains )
reload(  spaceSwitch )
reload( createFingersOrToesRig )

class createHeadRig():
    """
    Create eyes, tongue, head, neck
    """
    def __init__(self,**keywords):
        # common library
        self.commonLib = commonMayaLib.commonMayaLib()
        
        # standard names object
        self.sNames = standardNames.standardNames()
        
        # Used to store names of all created nodes, 
        # to be returned when the tool is done.
        self.createdNodes = {} 
        
        self.commandlineCall(keywords)

            
    def commandlineCall(self,keywords):
        """
        Verify and Store the data passed via command line keywords dictionary.
        """    
        self.prefix = keywords['prefix']
        self.rotateOrder = keywords['rotateOrder']
        self.normal = keywords['normal']
        self.radius = keywords['radius']
        
        self.create()
        
    def create(self,*args):
        """
        Create rigs for eyes, mouth(teeth, tongue, jaw),ears
        """
        self.rigNeck()
        self.rigJaw()
        self.rigEyes()
        self.rigTongue()
        #@todo - self.rigEars()

    def rigNeck(self,*args):
        """
        Orient joints and create controllers. Build hierarchy.
        """            
        #--- Orient neck joints
        # Neck 1
        #Parent to back base jnt
        #neck1_parent = listRelatives(self.sNames.headJoints['neck1'],parent=True) 
#        parent(self.sNames.headJoints['neck1'], self.sNames.backJoints['start'])
#        joint(self.sNames.headJoints['neck1'], edit=True, oj='none' )
#        parent(self.sNames.headJoints['neck1'],w=True)
        
        # Neck 2
        #neck2_parent = listRelatives(self.sNames.headJoints['neck2'],parent=True) 
#        parent(self.sNames.headJoints['neck2'], self.sNames.backJoints['start'])
#        joint(self.sNames.headJoints['neck2'], edit=True, oj='none' )
        #parent(self.sNames.headJoints['neck2'],neck2_parent)
        
        #--- Create Fk controllers for the two neck joints.
        # Neck 1
        temp = circle(nr=self.normal, r=(self.radius*1.5))
        #Parent transform under fk joint
        parent(temp, self.sNames.headJoints['neck1']) 
        #Zero it so it snaps to FK position/orientation
        move(temp,0, 0, 0 ) 
        #Get shape node for the parent command
        shape = pickWalk(temp, direction='down') 
        #Parent shape to joints transform
        parent(shape, self.sNames.headJoints['neck1'], s=True, r=True) 
        #Delete empty transform
        delete(temp)  
        
        #Create buffer group
        neck1Buffer = self.commonLib.zero(self.sNames.headJoints['neck1']) 
    
        # Neck 2
        temp = circle(nr=self.normal, r=(self.radius*1.5))
        #Parent transform under fk joint
        parent(temp, self.sNames.headJoints['neck2']) 
        #Zero it so it snaps to FK position/orientation
        move(temp,0, 0, 0 ) 
        #Get shape node for the parent command
        shape = pickWalk(temp, direction='down') 
        #Parent shape to joints transform
        parent(shape, self.sNames.headJoints['neck2'], s=True, r=True) 
        #Delete empty transform
        delete(temp)     
        
        #Create buffer group
        neck2Buffer = self.commonLib.zero(self.sNames.headJoints['neck2']) 
        
        # Parent ears/jaw to head
        parent(self.sNames.headJoints['left_ear'], self.sNames.headJoints['head'])
        parent(self.sNames.headJoints['right_ear'], self.sNames.headJoints['head'])
        parent(self.sNames.headJoints['jaw'], self.sNames.headJoints['head'])
        
        #--- Set orientations for the head control
        # Snap the head control buffer to the head joint
        self.commonLib.snapping(self.sNames.controlNames['head']+'_buffer', self.sNames.headJoints['head'])        
        
        # Parent controller to the neck1_jnt.
        parent(self.sNames.controlNames['head']+'_buffer',self.sNames.headJoints['neck2'] ) 
        
        # Freeze transformations
        select(self.sNames.controlNames['head']+'_buffer',r=True)
        mel.eval('FreezeTransformations;')
               
        # Get buffer grp
        head_buffer_grp = self.sNames.controlNames['head'] + '_buffer' #group(self.sNames.controlNames['head'],n=self.sNames.controlNames['head'] + '_buffer_grp')

        # Add translation values to buffer node translation values ( zero control translates )
        orig_val = getAttr( self.sNames.controlNames['head']+'_buffer.translate' )
        new_val = getAttr( self.sNames.controlNames['head']+'.translate' )
        setAttr( head_buffer_grp+'.translate', (orig_val + new_val ))
        orig_val = getAttr( self.sNames.controlNames['head']+'_buffer.rotate' )
        new_val = getAttr( self.sNames.controlNames['head']+'.rotate' )
        setAttr( head_buffer_grp+'.rotate', (orig_val + new_val ))
        
        # Parent the head joint to the head_cnt
        parent( self.sNames.headJoints['head'], self.sNames.controlNames['head'] )

        
        # Parent neck1Buffer to shoulder ik control
        parent(neck1Buffer, self.sNames.controlNames['shoulder']+'_ik')
        
        #--- Clean up neck rig
        # Disable scale, and visibility
        setAttr('%s.scaleX' % self.sNames.headJoints['neck1'], lock=True, keyable=False)
        setAttr('%s.scaleY' % self.sNames.headJoints['neck1'], lock=True, keyable=False)
        setAttr('%s.scaleZ' % self.sNames.headJoints['neck1'], lock=True, keyable=False)
        setAttr('%s.visibility' % self.sNames.headJoints['neck1'], lock=True, keyable=False)
        setAttr('%s.radius' % self.sNames.headJoints['neck1'], lock=True, keyable=False, channelBox=False) 
        
        setAttr('%s.scaleX' % self.sNames.headJoints['neck2'], lock=True, keyable=False)
        setAttr('%s.scaleY' % self.sNames.headJoints['neck2'], lock=True, keyable=False)
        setAttr('%s.scaleZ' % self.sNames.headJoints['neck2'], lock=True, keyable=False)
        setAttr('%s.visibility' % self.sNames.headJoints['neck2'], lock=True, keyable=False)
        setAttr('%s.radius' % self.sNames.headJoints['neck2'], lock=True, keyable=False, channelBox=False)
        
        # Head control scale
        setAttr('%s.scaleX' % self.sNames.controlNames['head'], lock=True, keyable=False)
        setAttr('%s.scaleY' % self.sNames.controlNames['head'], lock=True, keyable=False)
        setAttr('%s.scaleZ' % self.sNames.controlNames['head'], lock=True, keyable=False)
        
        # Disable buffer nodes
        setAttr(head_buffer_grp + '.translateX' , lock=True, keyable=False)
        setAttr(head_buffer_grp + '.translateY' , lock=True, keyable=False)
        setAttr(head_buffer_grp + '.translateZ' , lock=True, keyable=False)
#        setAttr(head_buffer_grp + '.rotateX' , lock=True, keyable=False)
#        setAttr(head_buffer_grp + '.rotateY' , lock=True, keyable=False)
#        setAttr(head_buffer_grp + '.rotateZ' , lock=True, keyable=False)
        setAttr(head_buffer_grp + '.scaleX' , lock=True, keyable=False)
        setAttr(head_buffer_grp + '.scaleY' , lock=True, keyable=False)
        setAttr(head_buffer_grp + '.scaleZ' , lock=True, keyable=False)
        setAttr(head_buffer_grp + '.visibility' , lock=True, keyable=False)           

        setAttr('%s.translateX' % neck1Buffer, lock=True, keyable=False)
        setAttr('%s.translateY' % neck1Buffer, lock=True, keyable=False)
        setAttr('%s.translateZ' % neck1Buffer, lock=True, keyable=False)
        setAttr('%s.rotateX' % neck1Buffer, lock=True, keyable=False)
        setAttr('%s.rotateY' % neck1Buffer, lock=True, keyable=False)
        setAttr('%s.rotateZ' % neck1Buffer, lock=True, keyable=False)
        setAttr('%s.scaleX' % neck1Buffer, lock=True, keyable=False)
        setAttr('%s.scaleY' % neck1Buffer, lock=True, keyable=False)
        setAttr('%s.scaleZ' % neck1Buffer, lock=True, keyable=False)
        setAttr('%s.visibility' % neck1Buffer, lock=True, keyable=False)         

        setAttr('%s.translateX' % neck2Buffer, lock=True, keyable=False)
        setAttr('%s.translateY' % neck2Buffer, lock=True, keyable=False)
        setAttr('%s.translateZ' % neck2Buffer, lock=True, keyable=False)
        setAttr('%s.rotateX' % neck2Buffer, lock=True, keyable=False)
        setAttr('%s.rotateY' % neck2Buffer, lock=True, keyable=False)
        setAttr('%s.rotateZ' % neck2Buffer, lock=True, keyable=False)
        setAttr('%s.scaleX' % neck2Buffer, lock=True, keyable=False)
        setAttr('%s.scaleY' % neck2Buffer, lock=True, keyable=False)
        setAttr('%s.scaleZ' % neck2Buffer, lock=True, keyable=False)
        setAttr('%s.visibility' % neck2Buffer, lock=True, keyable=False)                
        
    def rigJaw(self,*args):
        """
        Create controller curve and constrain joint to it.
        """
        # Parent jaw joint to controller
        parent(self.sNames.headJoints['jaw'],self.sNames.controlNames['jaw'])
        
        # Parent controller to the head
        parent('%s_buffer'%self.sNames.controlNames['jaw'],self.sNames.headJoints['head'])
        
    def rigEyes(self,*args):
        """
        Constrain joints to controls, so user can simply
        parent to the locators.
        """
        #--- Get eye positions
        l_pos = xform('l_eye_loc',q=True,ws=True,t=True)
        r_pos = xform('r_eye_loc',q=True,ws=True,t=True)
        
        #--- Create a follow and fk joint at each eye, all children of headjnt
        l_fkJoint = joint(p=l_pos,n='l_fkEye_jnt',a=True)
        r_fkJoint = joint(p=r_pos,n='r_fkEye_jnt',a=True)
        l_aimJoint = joint(p=l_pos,n='l_aimEye_jnt',a=True)
        r_aimJoint = joint(p=r_pos,n='r_aimEye_jnt',a=True)
        
        # Parent joints to fk control so it controls all position/scale
        parent(self.sNames.headJoints['left_eye'], self.sNames.controlNames['left_eye_fk'])
        parent(self.sNames.headJoints['right_eye'], self.sNames.controlNames['right_eye_fk'])
        parent(l_fkJoint, self.sNames.controlNames['left_eye_fk'])
        parent(r_fkJoint, self.sNames.controlNames['right_eye_fk'])
        parent(l_aimJoint, self.sNames.controlNames['left_eye_fk'])
        parent(r_aimJoint, self.sNames.controlNames['right_eye_fk'])
        
        # Parent the fk eye controllers to the head
        parent('%s_buffer'%self.sNames.controlNames['left_eye_fk'],self.sNames.headJoints['head'])
        parent('%s_buffer'%self.sNames.controlNames['right_eye_fk'],self.sNames.headJoints['head'])
        
        #--- Aim the follow joints to their respective controllers
        aimConstraint( self.sNames.controlNames['left_eye_aim'],l_aimJoint, offset = (0, 0, 0), weight = 1, aimVector = (1, 0, 0), 
                       upVector = (0, 1, 0), worldUpType = "vector", worldUpVector = (0, 1, 0),mo = True )
        aimConstraint( self.sNames.controlNames['right_eye_aim'], r_aimJoint, offset = (0, 0, 0), weight = 1, aimVector = (1, 0, 0), 
                       upVector = (0, 1, 0), worldUpType = "vector", worldUpVector = (0, 1, 0),mo = True )
        
        #--- Create eye switch attributes on head controller: Aim or fk 
        addAttr(self.sNames.controlNames['head'],ln='Eyes_Follow',at='float',k=True)
        setAttr('%s.Eyes_Follow'%self.sNames.controlNames['head'],lock=True)
        addAttr(self.sNames.controlNames['head'],ln='aim',at='float',dv=0,min=0,max=1,k=True)
        addAttr(self.sNames.controlNames['head'],ln='fk',at='float',dv=0,min=0,max=1,k=True)
        
        #--- Parent constraint eye joint to the follow and the fk joints. 
        l_pConst = parentConstraint(l_fkJoint,l_aimJoint,self.sNames.headJoints['left_eye'],mo=True)
        r_pConst = parentConstraint(r_fkJoint,r_aimJoint,self.sNames.headJoints['right_eye'],mo=True)
        
        #--- Connect constraint to head_cnt attributes
        connectAttr('%s.fk'%self.sNames.controlNames['head'],'%s.l_fkEye_jntW0'%l_pConst, f=True)
        connectAttr('%s.fk'%self.sNames.controlNames['head'],'%s.r_fkEye_jntW0'%r_pConst, f=True)
        
        connectAttr('%s.aim'%self.sNames.controlNames['head'],'%s.l_aimEye_jntW1'%l_pConst,f=True)
        connectAttr('%s.aim'%self.sNames.controlNames['head'],'%s.r_aimEye_jntW1'%r_pConst,f=True)
    
        #--- Create head/world switch on eye Follow control
        spaceSwitch.spaceSwitch(   constObj='%s_buffer'%self.sNames.controlNames['eyes_follow'],
                                    control=self.sNames.controlNames['eyes_follow'],
                                    attName='follow',
                                    op1Name='world',
                                    op2Name='head',
                                    op3Name='',
                                    op4Name='',
                                    op5Name='',
                                    op6Name='',
                                    op7Name='',
                                    op8Name='',
                                    object1=self.sNames.controlNames['main'],
                                    object2=self.sNames.controlNames['head'],
                                    object3='',
                                    object4='',
                                    object5='',
                                    object6='',
                                    object7='',
                                    object8=''  )
        
        # Parent to world
        parent('%s_buffer'%self.sNames.controlNames['eyes_follow'], self.sNames.controlNames['main'])
        
        setAttr('%s.world'%self.sNames.controlNames['eyes_follow'], 1)
        
        # lock and hide Eyes_Follow
        setAttr('%s.rotateX' % self.sNames.controlNames['eyes_follow'], lock=True, keyable=False)
        setAttr('%s.rotateY' % self.sNames.controlNames['eyes_follow'], lock=True, keyable=False)
        setAttr('%s.rotateZ' % self.sNames.controlNames['eyes_follow'], lock=True, keyable=False)
        setAttr('%s.scaleX' % self.sNames.controlNames['eyes_follow'], lock=True, keyable=False)
        setAttr('%s.scaleY' % self.sNames.controlNames['eyes_follow'], lock=True, keyable=False)
        setAttr('%s.scaleZ' % self.sNames.controlNames['eyes_follow'], lock=True, keyable=False) 

        setAttr('%s.rotateX' % self.sNames.controlNames['left_eye_aim'], lock=True, keyable=False)
        setAttr('%s.rotateY' % self.sNames.controlNames['left_eye_aim'], lock=True, keyable=False)
        setAttr('%s.rotateZ' % self.sNames.controlNames['left_eye_aim'], lock=True, keyable=False)
        setAttr('%s.scaleX' % self.sNames.controlNames['left_eye_aim'], lock=True, keyable=False)
        setAttr('%s.scaleY' % self.sNames.controlNames['left_eye_aim'], lock=True, keyable=False)
        setAttr('%s.scaleZ' % self.sNames.controlNames['left_eye_aim'], lock=True, keyable=False)
        setAttr('%s.visibility' % self.sNames.controlNames['left_eye_aim'], lock=True, keyable=False)   
        
        setAttr('%s.rotateX' % self.sNames.controlNames['right_eye_aim'], lock=True, keyable=False)
        setAttr('%s.rotateY' % self.sNames.controlNames['right_eye_aim'], lock=True, keyable=False)
        setAttr('%s.rotateZ' % self.sNames.controlNames['right_eye_aim'], lock=True, keyable=False)
        setAttr('%s.scaleX' % self.sNames.controlNames['right_eye_aim'], lock=True, keyable=False)
        setAttr('%s.scaleY' % self.sNames.controlNames['right_eye_aim'], lock=True, keyable=False)
        setAttr('%s.scaleZ' % self.sNames.controlNames['right_eye_aim'], lock=True, keyable=False)
        setAttr('%s.visibility' % self.sNames.controlNames['right_eye_aim'], lock=True, keyable=False)  

    def rigTongue(self,*args):
        """
        On hold.
        """
        # Draw ep curve along locators. 
        tng1 = xform('tongue_loc_1',q=True,ws=True,t=True)
        tng2 = xform('tongue_loc_2',q=True,ws=True,t=True)
        tng3 = xform('tongue_loc_3',q=True,ws=True,t=True)
        
        crv = curve( p=[tng1, tng2, tng3], d=2 )

        # Rebuild it with 8 cvs
        rebuildCurve( crv, s=8)
        
        # Draw joints on the curve
        #####Add joints to curves CV's
        x = 0 
        tngJoints = []
        while(x<11):
            cvPos = xform( 'curve1.cv[' + str(x) + ']', q=True, ws=True,t=True )
            tngJoints.append( joint( p = cvPos, radius =.2, 
                                     name = 'tongue_%s_%s'%(x,self.sNames.suffix['joint'] ) ))
            x = x + 1
        
        # Delete the curve
        delete(crv)
        
        # Duplicate and add to bind joints group        
        newJnts = duplicate(tngJoints[0])
        select(newJnts[0],replace=True,hi=True)
        newJnts = ls(sl=True)
        tngBindJoints = []
        for each in newJnts:
            newName = each + '_' + self.sNames.suffix['bind']
            rename(each,newName)
            tngBindJoints.append(newName)

        if objExists('bind_joints_grp'):
            parent(tngBindJoints[0],'bind_joints_grp')
        else:
            grp = group(em=True,n='bind_joints_grp')
            parent(tngBindJoints[0],'bind_joints_grp')
        
        # @todo - Add curl,twist,spread input
        # Create controllers on joints / attributes on jaw

        startJnt = []
        endJnt = []
        
        startJnt.append(tngJoints[0])
        endJnt.append(tngJoints[len(tngJoints)-1])
        
        createFingersOrToesRig.createFingersOrToesRig( label = 'Tongue',  
                                                       control = self.sNames.controlNames['jaw'],
                                                       attNames = '_',
                                                       startJnts = startJnt,
                                                       endJnts = endJnt,
                                                       curl = 'X',
                                                       twist = 'Z',
                                                       spread = 'Y',
                                                       fkNormal = (0,0,1),
                                                       radius = self.radius/3.0 )
                
        # Get parent of first joint, which is the new offset joint
        tmp = listRelatives(tngJoints[0],parent=True)
        tmp = listRelatives(tmp,parent=True)
        tmp = listRelatives(tmp,parent=True)
        prt = listRelatives(tmp,parent=True)
                
        # Parent tongue base to head
        parent(prt,self.sNames.headJoints['jaw'])
        
        # Enable translates on first controller
        setAttr('%s.translateX'%tngJoints[0],k=True,lock=False)
        setAttr('%s.translateY'%tngJoints[0],k=True,lock=False)
        setAttr('%s.translateZ'%tngJoints[0],k=True,lock=False)
        
        
        
        
        
        