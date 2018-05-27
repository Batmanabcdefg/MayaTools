from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *
"""
Copyright (c) 2010, 2011 Mauricio Santos
Name: createArmRig.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created:   6 Oct 2010

$Revision: 140 $
$LastChangedDate: 2011-09-13 00:36:32 -0700 (Tue, 13 Sep 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/createArmRig.py $
$Id: createArmRig.py 140 2011-09-13 07:36:32Z mauricio $

Description: 
	IK/FK stretchy arm rig.

Used by: CreateRig.py

Uses:

Process:
		Done - #--- Create joint chains (ik,fk,follow)
		Done - #--- Connect the chains Call: connectJointChains.py
		Done - #--- Create IK arm
		Done - #--- Setup FK controls
		Done - #--- Arm orientation setup
		Done - #--- Stretchy setup
		Debugging - #--- Print IKFK Script to file

Example call:
	
	temp = createArmRig.createArmRig(	prefix = self.name+'_l',
									side = 1,
									shoulder = 'Shoulder_cnt',
									cog = 'Cog_cnt',
									head = 'troll_v1_locators_main_control',
									world = 'Main_cnt',
									hips = 'Hips_cnt',
									hand = 'l_Hand_cnt',
									aim_axis = self.aimAxis,
									aim_polarity = self.aimPolarity,
									up_axis = self.upAxis,
									up_polarity = self.upPolarity,
									fkNormal_axis = self.fkNormal,
									fkRadius = self.fkRadius,
									rotateOrder = self.rotateOrder )
	
	self.leftArmNodes = temp.createdNodes

	
Additional Notes: 

@Todo	- IK/FK Matching
		- Elbow pin
		- FK Shoulder follow, make floats, not menu 
		- Forearm twisting system
		- Auto clavicle

"""
import commonMayaLib as cml
import orientJoints as oj
import createIkPoleVector as cipv
import connectJointChains as cjc
import makeIkStretchy as miks
import spaceSwitch as ss
import standardNames

import time

#--- Main class
class createArmRig():
	"""
		Stretchy IK/FK arm rig. Pending: elbow pin and IK/FK matching
	"""
	def __init__(self,**keywords):
		
		# Set version number
		self.version = 0.9
		
		# Create library instance
		self.lib = cml.commonMayaLib()
		
		# Standard names object
		self.sNames = standardNames.standardNames()
		
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

		self.shoulder = keywords['shoulder']
		self.cog = keywords['cog']
		self.head = keywords['head']
		self.world = keywords['world']
		self.hips = keywords['hips']
		self.hand = keywords['hand'] # Hand control
		
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
		
		# Create the arm rig.
		self.createArm()

	def createArm(self, *args):
		"""
		  Main process: Sets up variables and calls sub-routines
		"""
		#--- De-select everything
		select(clear=True)
		
		#--- Create joint chains (follow,ik,fk)
		self.buildChains()
		

	def buildChains(self, *args):
		"""
		Build joint chains based on joint positions.
		"""
		self.followChain = [] # Shoulder,elbow,wrist
		self.ikChain = []
		self.fkChain = []
		
		if self.side == 1:
			self.clavJnt = self.sNames.armJoints['left_clav']
			self.followChain.append( self.sNames.armJoints['left_shoulder'] )
			self.followChain.append( self.sNames.armJoints['left_elbow'] )
			self.followChain.append( self.sNames.armJoints['left_wrist'] )
			
		if self.side == 2:
			self.clavJnt = self.sNames.armJoints['right_clav']
			self.followChain.append( self.sNames.armJoints['right_shoulder'] )
			self.followChain.append( self.sNames.armJoints['right_elbow'] )
			self.followChain.append( self.sNames.armJoints['right_wrist'] )
		
		# Store the follow wrist and clav to return it to client
		self.createdNodes['followWrist'] = self.followChain[2]
		self.createdNodes['clavJnt'] = self.clavJnt
		
		parent(self.followChain[0],w=True)
		
		#--- Parent to clav and orient whole chain, then unparent again
		parent(self.followChain[0],self.clavJnt)
					
		#--- Unparent the followChain
		parent(self.followChain[0],w=True)

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
		# @Todo - Get ride of side 1/2 checking during for loop. Just use left_ikChain/right_ikChain, etc...
		temp = duplicate(self.followChain,rc=True)
		x = 0
		for each in temp:
			name = ''

			if x == 0:
				if self.side == 1:
					name = self.sNames.controlNames['left_fkShoulder']
				if self.side == 2:
					name = self.sNames.controlNames['right_fkShoulder']
			if x == 1:
				if self.side == 1:
					name = self.sNames.controlNames['left_fkElbow']
				if self.side == 2:
					name = self.sNames.controlNames['right_fkElbow']
			if x == 2:
				if self.side == 1:
					name = self.sNames.controlNames['left_fkWrist']
				if self.side == 2:
					name = self.sNames.controlNames['right_fkWrist']
			x = x + 1

			rename(each, name)
			self.fkChain.append(name)
		
		# Store data for caller	
		if self.side == 1:
			self.createdNodes['left_ikChain'] = self.ikChain
			self.createdNodes['left_fkChain'] = self.fkChain
			self.createdNodes['left_followChain'] = self.followChain
			
		if self.side == 2:
			self.createdNodes['right_ikChain'] = self.ikChain
			self.createdNodes['right_fkChain'] = self.fkChain
			self.createdNodes['right_followChain'] = self.followChain
		
		# Delete children joints of the duplicates below the wrist
		temp = listRelatives(self.ikChain[2],children=True)
		delete(temp)
		temp = listRelatives(self.fkChain[2],children=True)
		delete(temp)
			
		#--- Connect the chains
		self.connectChains()		
					
	def connectChains(self,*args):
		"""
		Create blend color nodes and connect ik/fk/bind joint chains.
		"""
		temp = cjc.connectJointChains(	prefix=self.prefix,
								   followJoint=self.followChain[0],
								   leadAJoint=self.ikChain[0],
								   leadBJoint=self.fkChain[0],
								   type=2,
								   translations=1,
								   rotations=1 )
		
		# Store nodes created
		self.switchNodes = temp.createdNodes	
		
		# continue with rig building
		self.finalizeArmRig()
		
	def finalizeArmRig(self,*args):
		"""
		Once the user has verified the joint orientations,
		finalize the rig setup.
		
		called by: buildChains2()
		"""		
		# Progress window
		amount = 0
		self.pWin = progressWindow(  title='Creating %s Arm rig'%self.prefix,
									progress=amount,
									status='Creating...: 0%',
									isInterruptable=True )
		
		# Define clav control
		if self.side == 1:
			self.clav = self.sNames.controlNames['left_clav']
		if self.side == 2:
			self.clav = self.sNames.controlNames['right_clav']
			
		#--- Build IK
		self.buildIK()
		progressWindow(self.pWin, edit=True, progress=20, status=('creating...: 20%' ) )
		
		#--- Setup FK controls
		self.buildFK()
		progressWindow(self.pWin, edit=True, progress=40, status=('creating...: 40%' ) )
		
		#--- Arm orientation setup
		self.fkArmOrientSetup()
		progressWindow(self.pWin, edit=True, progress=60, status=('creating...: 60%' ) )
		
		#--- Stretchy setup
		self.stretchySetup()
		progressWindow(self.pWin, edit=True, progress=80, status=('creating...: 80%' ) )
				
		#--- Setup hand IK/FK switch attribute on control
		self.handControlSetup()
		progressWindow(self.pWin, edit=True, progress=95, status=('creating...: 90%' ) )
		
		#--- Setup clavicles
		self.clavSetup()
		progressWindow(self.pWin, edit=True, progress=95, status=('creating...: 95%' ) )
		
		#--- clean up
		self.cleanUp()
		progressWindow(self.pWin, edit=True, progress=100, status=('creating...: 100%' ) )
		
		progressWindow(self.pWin,endProgress=1)

	def buildIK(self, *args):
		"""
			Build the IK arm
		"""
		#Setup variables
		#@todo - Is this actually working?
		self.normal = (1,0,0)
		if self.normalAxis == 2:
			self.normal = (0, 1, 0)
		if self.normalAxis == 3:
			self.normal = (0, 0, 1)   

		#Create IK control
		if self.prefix == 'l_arm':
			self.ikControl = circle(nr=self.normal, r=self.radius,n=self.sNames.controlNames['left_armIk'])
			# Set the color
			setAttr('%s.overrideEnabled'%self.ikControl[0], 1)
			setAttr('%s.ovc'%self.ikControl[0], 13)
		
		if self.prefix == 'r_arm':
			self.ikControl = circle(nr=self.normal, r=self.radius,n=self.sNames.controlNames['right_armIk'])
			# Set the color
			setAttr('%s.overrideEnabled'%self.ikControl[0], 1)
			setAttr('%s.ovc'%self.ikControl[0], 6)
		
		select(self.ikControl[0],r=True)
		
		mel.eval("DeleteHistory;")

		# Set rotate orders
		setAttr('%s.rotateOrder'%self.ikControl[0], self.rotateOrderInt) #ZXY

		#Parent circle under wrist joint
		parent(self.ikControl[0], self.ikChain[2])  
		  
		#Zero it so it snaps to joint position/orientation   
		move(self.ikControl[0], 0, 0, 0,os=True)			 
		parent(self.ikControl[0],w=True)
		
		#Zero it's values and create the buffer node
		ikBuffer01 = self.lib.zero(self.ikControl[0])			 
			 
		#Create RP IK

		self.arm_ikHandle = ikHandle(sj=self.ikChain[0], ee=self.ikChain[2], solver='ikRPsolver', name=(self.prefix + '_armIkHandle'))
		setAttr(self.arm_ikHandle[0] + '.visibility', 0)
		
		#Parent IK Handle to the ikWrist_cnt
		parent(self.arm_ikHandle[0], self.ikControl[0])

		# Creates: self.pv_cnt
		self.createPoleVector(self.arm_ikHandle[0],self.ikControl[0],self.world)
		
		# Setup space switch
		# first, re-zero ik control to have an other node above it.
		ikBuffer02 = self.lib.zero(ikBuffer01)  
		ss.spaceSwitch(   constObj=ikBuffer02,
							control=self.ikControl[0],
							attName='space_switches',
							op1Name='world_space',
							op2Name='cog_space',
							op3Name='hips_space',
							op4Name='shoulders_space',
							op5Name='head_space',
							op6Name='',
							op7Name='',
							op8Name='',
							object1=self.world,
							object2=self.cog,
							object3=self.hips,
							object4=self.shoulder,
							object5=self.head,
							object6='',
							object7='',
							object8=''  )
		
		#@todo - Works at orienting ik control to hand, but causes propagation issues
		#			when a value is directly enter for the ik controller, the follow chain
		#			blendColor nodes do not update. Weird but verified.
		# Constrain IK control to hand control
		#orientConstraint(self.hand,self.ikControl[0],mo=True)
		
		# Add the top buffer node to return it to client
		self.createdNodes['ikCntBuffer'] = ikBuffer02
		
	def createPoleVector(self,ikHandle,ikControl, worldControl):
		"""
		Call: createIkPoleVector()
		"""
		#--- Create the pole vector
		temp = cipv.createIkPoleVector( prefix = self.prefix,
								 side = self.side,
								 type='arm',
								 ikHandle = ikHandle,
								 ikControl = ikControl,
								 worldControl = worldControl)
		temp2 = temp.createdNodes[0]	
		
		self.pv_cnt = temp2					
		
	def buildFK(self, *args):
		"""
			Create FK controllers
		"""
		#shoulder
		temp = circle(nr=self.normal, r=self.radius)
		parent(temp, self.fkChain[0]) #Parent transform under fk joint
		move(temp,0, 0, 0 ) #Zero it so it snaps to FK position/orientation
		shape = pickWalk(temp, direction='down') #Get shape node for the parent command
		parent(shape, self.fkChain[0], s=True, r=True) #Parent shape to joints transform
		delete(temp)   #Delete empty transform

		#elbow1
		temp = circle(nr=self.normal, r=self.radius)
		parent(temp, self.fkChain[1]) #Parent transform under fk joint
		move(temp,0, 0, 0 ) #Zero it so it snaps to FK position/orientation
		shape = pickWalk(temp, direction='down') #Get shape node for the parent command
		parent(shape, self.fkChain[1], s=True, r=True) #Parent shape to joints transform
		delete(temp)   #Delete empty transform

		#wrist
		temp = circle(nr=self.normal, r=self.radius)
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
		setDrivenKeyframe(self.fkChain[1], cd='%s.length' % self.fkChain[0], at='translate%s' % aim, dv=0, v=0)		 #Set min
		setDrivenKeyframe(self.fkChain[1], cd='%s.length' % self.fkChain[0], at='translate%s' % aim, dv=2, v=(val1 * 5)) #Set max

		setDrivenKeyframe(self.fkChain[2], cd='%s.length' % self.fkChain[1], at='translate%s' % aim, dv=1) #Set default with current value in .tx
		setDrivenKeyframe(self.fkChain[2], cd='%s.length' % self.fkChain[1], at='translate%s' % aim, dv=0, v=0)		 #Set min
		setDrivenKeyframe(self.fkChain[2], cd='%s.length' % self.fkChain[1], at='translate%s' % aim, dv=2, v=(val2 * 5))#Set max

	def fkArmOrientSetup(self, *args):
		"""
		 Setup following rotations linked to : world, cog, shoulders
		"""
		#This is the locator that switches between the other two.The entire FK/IK/Follow arms parent'd to this guy.
		shldr_loc = '%s_shldrLoc' % self.prefix 
		spaceLocator(n=shldr_loc)
		
		# Follows shoulders
		shldr_torso_orient_loc = '%s_torsoLoc' % self.prefix 
		spaceLocator(n=shldr_torso_orient_loc)
		
		# Follows body
		shldr_cog_orient_loc = '%s_cogLoc' % self.prefix 
		spaceLocator(n=shldr_cog_orient_loc)	
		
		# Hide the locators
		setAttr('%sShape.visibility'%shldr_loc,0)
		setAttr('%sShape.visibility'%shldr_torso_orient_loc,0)
		setAttr('%sShape.visibility'%shldr_cog_orient_loc,0)	

		#Scale down the locators. Can't hide them. Hides the child nodes (Arm controls/joints)
		setAttr('%s.scaleX' % shldr_loc, .05)
		setAttr('%s.scaleY' % shldr_loc, .05)
		setAttr('%s.scaleZ' % shldr_loc, .05)

		setAttr('%s.scaleX' % shldr_torso_orient_loc, .05)
		setAttr('%s.scaleY' % shldr_torso_orient_loc, .05)
		setAttr('%s.scaleZ' % shldr_torso_orient_loc, .05)

		setAttr('%s.scaleX' % shldr_cog_orient_loc, .05)
		setAttr('%s.scaleY' % shldr_cog_orient_loc, .05)
		setAttr('%s.scaleZ' % shldr_cog_orient_loc, .05)

		# Snap locators into position
		temp = pointConstraint(self.fkChain[0], shldr_loc, mo=False)
		delete(temp)
		temp = pointConstraint(self.fkChain[0], shldr_torso_orient_loc, mo=False)
		delete(temp)
		temp = pointConstraint(self.cog, shldr_cog_orient_loc, mo=False)
		delete(temp)
		
		# Place locators in the hierarchy
		parent(shldr_loc, self.clavJnt) 
		parent(shldr_torso_orient_loc, self.clavJnt) #Parent to the same joint that shldr_loc is parent'd to.
		parent(shldr_cog_orient_loc, self.cog) #Parent to cog that will move the arm with the torso	  
		
		parent(self.fkChain[0], shldr_loc)
		parent(self.ikChain[0], shldr_loc) #So the IK arm follows along
		parent(self.followChain[0], shldr_loc) #So this guy plays too
		
		# Create the constraint that will switch determine the arm orientation behavior.
		rotConst = orientConstraint(shldr_torso_orient_loc, shldr_cog_orient_loc, self.world, shldr_loc, mo=True)

		#Create switching attribute
		addAttr(self.fkChain[0], ln='Follow', at='float',k=True)
		setAttr('%s.Follow'%self.fkChain[0], lock=True)
		addAttr(self.fkChain[0], ln='Shoulder', at='float', min=0.0,max=1.0,k=True)
		addAttr(self.fkChain[0], ln='COG', at='float', min=0.0,max=1.0,k=True)
		addAttr(self.fkChain[0], ln='World', at='float', min=0.0,max=1.0,k=True)
		
#		#SDK's to set this constraint
		connectAttr('%s.Shoulder' % self.fkChain[0],'%s.%sW0'%(rotConst,shldr_torso_orient_loc), f=True )
		connectAttr('%s.COG' % self.fkChain[0],'%s.%sW1'%(rotConst,shldr_cog_orient_loc), f=True )
		connectAttr('%s.World' % self.fkChain[0],'%s.%sW2'%(rotConst,self.world), f=True )
		
		# Set shoulder to 1
		setAttr('%s.Shoulder' % self.fkChain[0],1)

	def handControlSetup(self, *args):
		"""
		 Create attributes on hand_cnt: 
		 	FK_IK 
		"""
		addAttr(self.hand,ln='FK_IK',at='float',dv=0,min=0,max=1,k=True)

		# Connect IK/FK attr to the blend color nodes
		for each in self.switchNodes:
		 connectAttr( '%s.FK_IK'%self.hand, '%s.blender'%each )

		#IK=0=Off / FK=1=Off controls vis switch
		connectAttr( '%s.FK_IK'%self.hand, '%s.visibility'%self.ikChain[0] )
		connectAttr( '%s.FK_IK'%self.hand, '%s.visibility'%self.ikControl[0] )
		
		# FK=1=Off SDK
		setDrivenKeyframe(self.fkChain[0], cd='%s.FK_IK' % self.hand, at='visibility', dv=1, v=0)
		setDrivenKeyframe(self.fkChain[0], cd='%s.FK_IK' % self.hand, at='visibility', dv=0, v=1)

		# Zero hand control
		self.lib.zero(self.hand)
		bufferNode = listRelatives(self.hand,parent=True)
		
		# Store the buffer grp so it is accessible to client
		self.createdNodes['handCntBuffer'] = bufferNode
	   
	def stretchySetup(self, *args):
		"""
		Call: makeIkStretchy
		"""
		temp = miks.makeIkStretchy( prefix=self.prefix,
							 side = self.side,
							 type=1,
							 axis=1,
							 control=self.ikControl,
							 ik=self.arm_ikHandle[0] )
		
		# Store the distance grp	
		self.createdNodes['distGrp'] = temp.createdNodes['distGrp']	
		
	def clavSetup(self,*args):
		"""
		Orient clav controls to joints, and parentConstraint joints to clav cntrols.
		"""	
		# Parent clavJnt to clav_cnt
		parentConstraint(self.clav,self.clavJnt,mo=True)
		
	def cleanUp(self,*args):
		"""
			Lock and hide attributes as needed and delete setup locators
		"""
		#FK Controls
		# Shoulder
		setAttr('%s.overrideEnabled' % self.fkChain[0], 1)
		if self.prefix == 'l_arm':
			setAttr('%s.overrideColor' % self.fkChain[0], 13)
		elif self.prefix == 'r_arm':
			setAttr('%s.overrideColor' % self.fkChain[0], 6)
			
		setAttr('%s.translateX' % self.fkChain[0], lock=True, keyable=False)
		setAttr('%s.translateY' % self.fkChain[0], lock=True, keyable=False)
		setAttr('%s.translateZ' % self.fkChain[0], lock=True, keyable=False)

		setAttr('%s.scaleX' % self.fkChain[0], lock=True, keyable=False)
		setAttr('%s.scaleY' % self.fkChain[0], lock=True, keyable=False)
		setAttr('%s.scaleZ' % self.fkChain[0], lock=True, keyable=False)
		setAttr('%s.visibility' % self.fkChain[0], keyable=False)
		setAttr('%s.radius' % self.fkChain[0], lock=True, cb=False)

		# Elbow
		setAttr('%s.translateX' % self.fkChain[1], keyable=False) #This channel connected to length
		setAttr('%s.translateY' % self.fkChain[1], lock=True, keyable=False)
		setAttr('%s.translateZ' % self.fkChain[1], lock=True, keyable=False)

		setAttr('%s.scaleX' % self.fkChain[1], keyable=False) 
		setAttr('%s.scaleY' % self.fkChain[1], lock=True, keyable=False)
		setAttr('%s.scaleZ' % self.fkChain[1], lock=True, keyable=False)
		setAttr('%s.visibility' % self.fkChain[1], lock=True, keyable=False)
		setAttr('%s.radius' % self.fkChain[1], lock=True, cb=False)

		# Wrist
		setAttr('%s.translateX' % self.fkChain[2], keyable=False) #This channel connected to length
		setAttr('%s.translateY' % self.fkChain[2], lock=True, keyable=False)
		setAttr('%s.translateZ' % self.fkChain[2], lock=True, keyable=False)

		setAttr('%s.scaleX' % self.fkChain[2], keyable=False) 
		setAttr('%s.scaleY' % self.fkChain[2], lock=True, keyable=False)
		setAttr('%s.scaleZ' % self.fkChain[2], lock=True, keyable=False)
		setAttr('%s.visibility' % self.fkChain[2],0)
		setAttr('%s.visibility' % self.fkChain[2], lock=True, keyable=False)
		setAttr('%s.radius' % self.fkChain[2], lock=True, cb=False)

		#Hand control
		setAttr('%s.scaleX' % self.hand, lock=True, keyable=False) 
		setAttr('%s.scaleY' % self.hand, lock=True, keyable=False)
		setAttr('%s.scaleZ' % self.hand, lock=True, keyable=False)

		#IK control
		setAttr('%s.rotateX' % self.ikControl[0], lock=True, keyable=False)
		setAttr('%s.rotateY' % self.ikControl[0], lock=True, keyable=False)
		setAttr('%s.rotateZ' % self.ikControl[0], lock=True, keyable=False)
		setAttr('%s.scaleX' % self.ikControl[0], lock=True, keyable=False)
		setAttr('%s.scaleY' % self.ikControl[0], lock=True, keyable=False)
		setAttr('%s.scaleZ' % self.ikControl[0], lock=True, keyable=False)
		setAttr('%s.visibility' % self.ikControl[0], keyable=False)
		
		#pv_cnt
		setAttr('%s.rotateX' % self.pv_cnt, lock=True, keyable=False)
		setAttr('%s.rotateY' % self.pv_cnt, lock=True, keyable=False)
		setAttr('%s.rotateZ' % self.pv_cnt, lock=True, keyable=False)		
		
		setAttr('%s.scaleX' % self.pv_cnt, lock=True, keyable=False)
		setAttr('%s.scaleY' % self.pv_cnt, lock=True, keyable=False)
		setAttr('%s.scaleZ' % self.pv_cnt, lock=True, keyable=False)
		setAttr('%s.visibility' % self.pv_cnt, keyable=False)

		#Lock elbow axis
		if self.joint_up == 1:
			setAttr('%s.rotateY'%self.fkChain[1],lock=True,k=False) 
			setAttr('%s.rotateZ'%self.fkChain[1],lock=True,k=False) 
			setAttr('%s.rotateY'%self.ikChain[1],lock=True,k=False) 
			setAttr('%s.rotateZ'%self.ikChain[1],lock=True,k=False) 
		if self.joint_up == 2:
			setAttr('%s.rotateX'%self.fkChain[1],lock=True,k=False) 
			setAttr('%s.rotateZ'%self.fkChain[1],lock=True,k=False) 
			setAttr('%s.rotateX'%self.ikChain[1],lock=True,k=False) 
			setAttr('%s.rotateZ'%self.ikChain[1],lock=True,k=False) 
		if self.joint_up == 3:
			setAttr('%s.rotateY'%self.fkChain[1],lock=True,k=False) 
			setAttr('%s.rotateX'%self.fkChain[1],lock=True,k=False) 
			setAttr('%s.rotateY'%self.ikChain[1],lock=True,k=False) 
			setAttr('%s.rotateX'%self.ikChain[1],lock=True,k=False) 
		
		# Set ik controller to world space by default
		setAttr('%s.world_space' % self.ikControl[0], 1)
		setAttr('%s.world_space' % self.ikControl[0], 1)
		
		# @todo - Find out why the warning is happening.
		# Disable cycle warning when using twist attribute...
		# mel.eval('cycleCheck -e off;')
 
	def loadClavLoc(self, *args): 
		locName = ls(sl=True)
		textFieldGrp(self.clavLocFld, edit=True, text=locName[0])

	def loadShldrLoc(self, *args): 
		locName = ls(sl=True)
		textFieldGrp(self.shldrLocFld, edit=True, text=locName[0])

	def loadElbowLoc(self, *args): 
		locName = ls(sl=True)
		textFieldGrp(self.elbowLocFld, edit=True, text=locName[0])

	def loadWristLoc(self, *args): 
		locName = ls(sl=True)
		textFieldGrp(self.wristLocFld, edit=True, text=locName[0])

	def loadHipsObj(self, *args): 
		objName = ls(sl=True)
		textFieldGrp(self.hipsFld, edit=True, text=objName[0])

	def loadShoulderObj(self, *args): 
		objName = ls(sl=True)
		textFieldGrp(self.shoulderFld, edit=True, text=objName[0])

	def loadCogObj(self, *args): 
		objName = ls(sl=True)
		textFieldGrp(self.cogFld, edit=True, text=objName[0])
		
	def loadHeadObj(self, *args): 
		objName = ls(sl=True)
		textFieldGrp(self.headFld, edit=True, text=objName[0])

	def loadWorldObj(self, *args):
		objName = ls(sl=True)
		textFieldGrp(self.worldFld, edit=True, text=objName[0])

	def loadHandObj(self, *args): 
		objName = ls(sl=True)
		textFieldGrp(self.handFld, edit=True, text=objName[0])			
			
			
