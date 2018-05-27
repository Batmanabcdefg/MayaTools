from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *
"""
Copyright (c) 2010 Mauricio Santos
Name: createBackRig.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created:   22 Oct 2010

$Revision: 140 $
$LastChangedDate: 2011-09-13 00:36:32 -0700 (Tue, 13 Sep 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/createBackRig.py $
$Id: createBackRig.py 140 2011-09-13 07:36:32Z mauricio $

Description: 
	Creates a stretchy Ik/Fk back rig with volume attributes.

Process:
	
Additional Notes: 

Example call:
	import createBackRig
	createBackRig.createBackRig( )
	  
Attributes:
	createdNodes = list of created nodes.

Keywords:

			 
Requires:


Development notes:

	@todo - 
		- Moveable pivot on cog?
"""

import makeIkStretchy
import orientJoints
import connectJointChains
import standardNames

class createBackRig():
	"""
	Creates a stretchy Ik/Fk back rig with volume attributes.
	Requires joints created by createRigJoints.py
	"""
	def __init__(self,**keywords):
		
		# Standard names object
		self.sNames = standardNames.standardNames()
		
		# Used to store names of all created nodes, 
		# to be returned when the tool is done.
		self.createdNodes = {} 
		
		self.commandlineCall(keywords)

	def commandlineCall(self,kwargs):
		"""
		Verify and Store the data passed via command line keywords dictionary.
		"""	
		#Initialize variables (Storing names)
		self.prefix = kwargs['prefix']
		
		self.shldrCnt = kwargs['shldrCnt']+'_ik'
		self.hipsCnt = kwargs['hipsCnt']
		self.bodyCnt = kwargs['bodyCnt']
		self.scaleCnt = kwargs['scaleCnt']
		
		self.numSpans = kwargs['numSpans']
		
		self.worldUpType = kwargs['worldUpType']
		
		self.aim = kwargs['aim']
		self.aimPolarity = kwargs['aimPolarity']
		self.up = kwargs['up']
		self.upPolarity = kwargs['upPolarity']
		
		self.upAxis = kwargs['upAxis']
		
		self.upVecX = kwargs['upVecX']
		self.upVecY = kwargs['upVecY']
		self.upVecZ = kwargs['upVecZ']
		
		self.upVec2X = kwargs['upVec2X']
		self.upVec2Y = kwargs['upVec2Y']
		self.upVec2Z = kwargs['upVec2Z']
					  
		self.stretchyAxis = kwargs['stretchyAxis']

		self.squashAxisX = kwargs['squashAxisX']
		self.squashAxisY = kwargs['squashAxisY']
		self.squashAxisZ = kwargs['squashAxisZ']
		
		self.fkOnOff = kwargs['fkOnOff']
		self.numFkJnts = kwargs['numFkJnts']
		self.fkNormal = kwargs['fkNormal']
		self.radius = kwargs['radius']
		
		self.mvPivOnOff = kwargs['mvPivOnOff']
		
		self.rotateOrder = kwargs['rotateOrder']

		if(self.stretchyAxis == 1):
			self.stretchyAxis = "X"
		if(self.stretchyAxis == 2):
			self.stretchyAxis = "Y"
		if(self.stretchyAxis == 3):
			self.stretchyAxis = "Z"
		
		#Call function to build rig
		self.createBackJoints()

	def createBackJoints(self,*args):
		"""
		Create joints for the back. 
		"""
		# Set rotate order variables
		if self.rotateOrder == 1: 
			self.rotateOrder = 'xyz'
			self.rotateOrderInt = 0
		if self.rotateOrder == 2: 
			self.rotateOrder = 'yzx'
			self.rotateOrderInt = 1
		if self.rotateOrder == 3: 
			self.rotateOrder = 'zxy'
			self.rotateOrderInt = 2
		if self.rotateOrder == 4: 
			self.rotateOrder = 'xzy'
			self.rotateOrderInt = 3
		if self.rotateOrder == 5: 
			self.rotateOrder = 'yxz'
			self.rotateOrderInt = 4
		if self.rotateOrder == 6: 
			self.rotateOrder = 'zyx'   
			self.rotateOrderInt = 5  
		
		# Store joint names
		select(clear=True)
		self.backJoints = []
		self.backJoints.append( self.sNames.backJoints['start'] )
		self.backJoints.append( self.sNames.backJoints['back1'] )
		self.backJoints.append( self.sNames.backJoints['back2'] )
		self.backJoints.append( self.sNames.backJoints['back3'] )
		self.backJoints.append( self.sNames.backJoints['back4'] )
		self.backJoints.append( self.sNames.backJoints['back5'] )
		self.backJoints.append( self.sNames.backJoints['end'] )
		
		# Store ikChain
		select(self.backJoints[0],hi=True,r=True)
		ikChain = ls(sl=True,fl=True)
		
		# Store hip jnt and create shldr jnt
		select(clear=True)
		self.hipJnt = self.sNames.hipJoint
		select(clear=True)
		self.shldrJnt = joint( n = self.prefix + '_shldrJnt' ) 
		
		# Snap created joints to base + end joints
		temp = pointConstraint( self.backJoints[0], self.hipJnt, mo=False )
		delete( temp )
		temp = pointConstraint( self.backJoints[5], self.shldrJnt, mo=False )
		delete( temp )
		
		#Match orientations by parenting the jnts, then orienting with none value, then unparenting
		#parent(self.hipJnt, self.backJoints[0])
		parent(self.shldrJnt, self.backJoints[6])
		joint(self.hipJnt,e=True, oj='none',zso=True,ch=True)
		joint(self.shldrJnt,e=True, oj='none',zso=True,ch=True)
		#parent( self.hipJnt, w=True )
		parent( self.shldrJnt, w=True )
		
		#Set rotation orders
		setAttr(self.hipJnt + ".rotateOrder", self.rotateOrderInt)
		setAttr(self.shldrJnt + ".rotateOrder", self.rotateOrderInt)
		
		#Value used in spline ik command
		self.numSpans = self.numSpans + 1
		
		#SplineIK for back: Create and store name
		backIkHandle = self.prefix + "_back_"
		temp = ikHandle(sj=self.backJoints[0],ee=self.backJoints[6],sol="ikSplineSolver",pcv=False,ns=self.numSpans) 
		backIkHandle = backIkHandle + temp[0]
		rename(temp[0],backIkHandle)
		
		# Hide the handle
		setAttr('%s.visibility'%backIkHandle,0)
		
		#Get back ik curve name
		temp = listConnections(backIkHandle,s=True)
		
		#Storing the back ik curve name
		backCurve = ikHandle(backIkHandle,query=True,c=True)
				
		#Name back curve
		temp = self.prefix + '_backIkCrv'	   
		
		temp2 = backCurve.split('|')	
		 
		rename(temp2[1] , temp)
		backCurve=temp
				
		#Skin hip/shldr jnt's to back curve
		skinCluster(self.hipJnt,self.shldrJnt,backCurve,dr=4)
		
		#Parent hipsJnt/shldrJnt to controllers
		parent(self.hipJnt,self.hipsCnt)
		parent(self.shldrJnt,self.shldrCnt)
		
		#Turn off inherit transforms on backCurve
		setAttr(backCurve +".inheritsTransform", 0)
		
		#
		#---Set up stretchy
		#
		
		#0Select and store the joints to link in the back expression
		select(self.backJoints[0],hi=True,r=True)
		backJoints = ls(sl=1,fl=1,type='joint')
			
		jntNum = len(backJoints)
		
		stretch = '.scale' + self.stretchyAxis  #i.e. 'scaleX'

		#Now,Create curveInfo node 
		curveInfo = arclen(backCurve,ch=1)
		
		#Rename curve info node
		temp = self.prefix + 'backCrvInfo'
		rename(curveInfo, temp)
		curveInfo = temp
		
		#Create backScaleMD and connect arclength to input1X
		backScaleMD = createNode('multiplyDivide',n=self.prefix + 'backMD')		
		connectAttr(curveInfo + ".arcLength",backScaleMD + ".i1x")	

		#Get ArcLength value, set backScaleMD node to divide by it
		arcLen = getAttr(curveInfo+".arcLength")
		setAttr(backScaleMD+".i2x",arcLen)
		setAttr(backScaleMD+".operation",2) #Divide

		#
		#---Advance Twist setup
		# Make these values variables in the interface...
		setAttr( backIkHandle + ".dTwistControlEnable", 1)	#Enable advanced twist
		setAttr( backIkHandle + ".dWorldUpType", self.worldUpType-1)	 
		setAttr( backIkHandle + ".dWorldUpAxis", self.upAxis-1)			 
		setAttr( backIkHandle + ".dWorldUpVectorX", self.upVecX)			 
		setAttr( backIkHandle + ".dWorldUpVectorY", self.upVecY)			
		setAttr( backIkHandle + ".dWorldUpVectorZ", self.upVecZ)			
		setAttr( backIkHandle + ".dWorldUpVectorEndX", self.upVec2X)		
		setAttr( backIkHandle + ".dWorldUpVectorEndY", self.upVec2Y)	 
		setAttr( backIkHandle + ".dWorldUpVectorEndZ", self.upVec2Z)	 
		
		connectAttr(self.hipsCnt + '.worldMatrix', backIkHandle+'.dWorldUpMatrix', f=True)
		connectAttr(self.shldrCnt+'.worldMatrix', backIkHandle+'.dWorldUpMatrixEnd', f=True)
				
		#
		#---Make volume preservation expression
		#
		
		#Create attributes for each joint so the user can set the 
		# scaling factor per joint via the hipControl
		addAttr(self.hipsCnt,ln='BackVolumeScaleFactor',k=True,dv=0)
		setAttr(self.hipsCnt + '.BackVolumeScaleFactor',lock=True)
		
		x = 0
		for each in backJoints:
				#Not the backBaseJnt
				if(each == self.backJoints[0]):
					x = x + 1
					continue
				#Skipping the last one
				if( x == (jntNum-1) ):
					x = x + 1
					break
				addAttr(self.hipsCnt,ln=each,dv=1,k=True)
				x = x + 1
		
		backExpString = '//Back volume preservation expression\n'\
						  '$scale = %s.ox/%s.scaleY;\n'\
						  '$invScale = 1 / sqrt($scale);\n'\
						  '//Apply scale values to back.\n' % (backScaleMD,self.scaleCnt)
		
								   
		#Enter lines in expression string per joint 
		#connecting their scales to the inverse scale with the pow scale factor
		x = 0
		if self.stretchyAxis == 'X':
			for jnt in backJoints:
				#Not the backBaseJnt
				if(jnt == self.backJoints[0]):
					x = x + 1
					continue
				#Skipping the last one
				if( x == (jntNum-1) ):
					x = x + 1
					break
				temp = '%s.scaleX = $scale;\n' % (jnt) 
				backExpString =  backExpString + temp 
				temp = '%s.scaleY = pow($invScale,%s.%s);\n' % (jnt, self.hipsCnt, jnt) 
				backExpString =  backExpString + temp 
				temp = '%s.scaleZ = pow($invScale,%s.%s);\n' % (jnt, self.hipsCnt, jnt)  
				backExpString =  backExpString + temp
				x = x + 1
				
		if self.stretchyAxis == 'Y':
			for jnt in backJoints:
				#Not the backBaseJnt
				if(jnt == self.backJoints[0]):
					x = x + 1
					continue
				#Skipping the last one
				if( x == (jntNum-1) ):
					x = x + 1
					break
				temp = '%s.scaleX = pow($invScale,%s.%s);\n' % (jnt, self.hipsCnt, jnt) 
				backExpString =  backExpString + temp 
				temp = '%s.scaleZ = pow($invScale,%s.%s);\n' % (jnt, self.hipsCnt, jnt) 
				backExpString =  backExpString + temp
				x = x + 1
				
		if self.stretchyAxis == 'Z':
			for jnt in backJoints:
				#Not the backBaseJnt
				if(jnt == self.backJoints[0]):
					x = x + 1
					continue
				#Skipping the last one
				if( x == (jntNum-1) ):
					x = x + 1
					break
				temp = '%s.scaleX = pow($invScale,%s.%s);\n' % (jnt, self.hipsCnt, jnt) 
				backExpString =  backExpString + temp 
				temp = '%s.scaleY = pow($invScale,%s.%s);\n' % (jnt, self.hipsCnt, jnt) 
				backExpString =  backExpString + temp
				x = x + 1
				
		expression( s=backExpString,n=self.prefix+'backVolumeExp' )
		
		#Connect scaleY to X + Z for a global scale effect.
		connectAttr(self.scaleCnt + '.scaleY',self.scaleCnt+'.scaleX',f=True)
		connectAttr(self.scaleCnt + '.scaleY',self.scaleCnt+'.scaleZ',f=True)
			
		#
		#--- Moveable pivot
		#--- Work in progress: Moving on for now, revisit should necessity arrive.			
		"""
		#Create pivot control locator ad snap to body/COG
		pivLoc = spaceLocator()
		temp = parentConstraint(self.hipsCnt,pivLoc,mo=False)
		delete(temp)
		
		#Rename locator
		temp = self.prefix + 'hipsPivot_Ctrl'
		rename(pivLoc,temp)
		pivLoc=temp

		#Attach locator to hipCnt pivot
		connectAttr(pivLoc + '.translate', self.hipsCnt + '.rotatePivot',f=True)	

		#Parent the locator to hipsCnt
		parent(pivLoc,self.hipsCnt)
		#Freeze transform now, so it inherits the orientation of it's parent
		makeIdentity(pivLoc, apply=True )
		"""
		
		#Create the user space locator, the one they interface with.
		#Need to integrate the update pivot functionality to this script.
		# Methods might be a script node/script job that happens when a set attribute changes state, or something...
		#-------< Not finished
		
		#
		#--- FK setup
		#
		if self.fkOnOff == 1: #On
			#build fkChain On ikchain joints
			select(clear=True)
			#Get rotate order from hips control
			rotateOrder = self.rotateOrderInt
			fkJnts = []
			x = 0
			while x < (self.numFkJnts[0] + 1):
				pos = xform(ikChain[x], query=True,ws=True,t=True)
				if x == 0: #If first joint
					fkJnts.append( joint( p = (pos) ,n=self.backJoints[0]+'_cnt' )  )
					#Set rotate order	
					setAttr(fkJnts[x] + '.rotateOrder', rotateOrder)
					x = x + 1
					continue
				if x == ( self.numFkJnts[0] ): #If last joint
					fkJnts.append( joint( p = (pos) , n = self.sNames.controlNames['shoulder']) )
					break
				else:
					fkJnts.append( joint( p = (pos) ,n='back_'+str(x) )  )
				#Set rotate order	
				setAttr(fkJnts[x] + '.rotateOrder', rotateOrder)
				
				x = x + 1
				
			#Store fk joint names for client
			self.createdNodes['fkJoints'] = fkJnts
			
			""" May not be needed: when building along ik, it will orient to the next joint
				automatically.
			"""
			x = 0	
			for jnt in fkJnts:
				#Parent to baseJnt, makeIdentity to match orientation
				parent( jnt, self.backJoints[0] )
				makeIdentity(jnt, apply=True, jo=True )
				temp = group( jnt )
				ungroup( temp, w=True )
				#It will always fail with an index out of range error for the fist one.
				try:
					#This puts it back into the fk hierarchy
					parent( jnt, fkJnts[x-1] )
				except:
					pass
				
				x = x + 1
			
			#Create fk controller curves
			if self.fkNormal == 1:
				normal = (1,0,0)
			if self.fkNormal == 2:
				normal = (0,1,0)
			if self.fkNormal == 3:
				normal = (0,0,1)
			
			
			x = 0
			for jnt in fkJnts:
									
				#Skip the last one 
				if x == (len(fkJnts)+1): 
					break
				
				tempCnt = circle( nr = normal,r=self.radius[0] )
				
				#Select the shape node
				tempShp = pickWalk(tempCnt,direction='down')
				parent(tempShp,jnt,r=True,s=True)
				
				#Delete empty transform
				delete(tempCnt)
				
				# Zero FK controls, and enable translation.
				tmp_grp = group(jnt,n=str(jnt)+'_offset_grp')
				
				#Center their pivots
				select( str(jnt), r=True )
				mel.eval('CenterPivot;')
				select( str(tmp_grp), r=True )
				mel.eval('CenterPivot;')
				
				#Copy values from controller/jnt to the offset tmp_grp.
				copyAttr(str(jnt),str(tmp_grp),inConnections=True,values=True)
				
				#Zero the translations of the control/jnt
				setAttr('%s.translateX'%str(jnt),0)
				setAttr('%s.translateY'%str(jnt),0)
				setAttr('%s.translateZ'%str(jnt),0)
				
								
				x = x + 1
				
			#Parent fkBase joint buffer to body/COG
			fkparent = listRelatives(fkJnts[0],parent=True)
			parent(fkparent,self.bodyCnt)
			
			#Parent hipCnt to body/COG
			select(self.hipsCnt,r=True)
			bufferGrp = pickWalk(direction='up')
			#bufferGrp = ls(sl=True,fl=True) 
			parent(bufferGrp[0], self.bodyCnt)
			
			#Parent shldrCnt to fkJnts[last one]
			select(self.shldrCnt,r=True)
			bufferGrp = pickWalk(direction='up')
			#bufferGrp = ls(sl=True,fl=True) 
			parent(bufferGrp[0], fkJnts[-1:])
			
			#Hide the shoulder control
			setAttr('%sShape.visibility'%self.shldrCnt,0)
			
			#Grp ikCurve, ikHandle into doNotTouch group
			if objExists(self.prefix + '_doNotTranslate'):
				parent(backCurve, backIkHandle, self.prefix + '_doNotTranslate')
			else:
				noTouchGrp = group( backCurve, backIkHandle, n = self.prefix + '_doNotTranslate') 

			#Group + parent joints to world control (ScaleCnt)
			jntsGrp = group( self.backJoints[0] , n=self.prefix+'_backJntsGrp')
			parent( jntsGrp, self.scaleCnt )
			
			#Get body/COG control buffer, parent it to scaleCnt 
			select(self.bodyCnt,r=True)
			pickWalk(direction='up')
			buffer = ls(sl=True,fl=True)
			parent(buffer,self.scaleCnt)
			
			# Return nodes: hips joint
			self.createdNodes['hip_joint'] = self.hipJnt
			self.createdNodes['noTouchGrp'] = self.prefix + '_doNotTranslate'
			
			# Disable Translations/Scale/Visibility
			for jnt in fkJnts:
				#Disable translations
#				setAttr('%s.translateX'%jnt, lock=True, keyable=False)
#				setAttr('%s.translateY'%jnt, lock=True, keyable=False)
#				setAttr('%s.translateZ'%jnt, lock=True, keyable=False)
				
				#Disable Scale
				setAttr('%s.scaleX'%jnt, lock=True, keyable=False)
				setAttr('%s.scaleY'%jnt, lock=True, keyable=False)
				setAttr('%s.scaleZ'%jnt, lock=True, keyable=False)
				
				#Disable Visibility
				setAttr('%s.visibility'%jnt, lock=True, keyable=False)
				
				#Disable Radius
				try:
					setAttr('%s.radi'%jnt, lock=True, keyable=False)
				except:
					setAttr('%s.radius'%jnt, lock=True, keyable=False)
	
			 
	#--- GUI load functions
	def loadShldr(self,*args):
		sel = mc.ls(sl=True,fl=True)
		mc.textFieldButtonGrp(self.shldrsCtrFld,edit=True,text=sel[0])	
	def loadHips(self,*args):
		sel = mc.ls(sl=True,fl=True)
		mc.textFieldButtonGrp(self.hipsCtrFld,edit=True,text=sel[0])
	def loadBody(self,*args):
		sel = mc.ls(sl=True,fl=True)
		mc.textFieldButtonGrp(self.bodyCtrFld,edit=True,text=sel[0])
	def loadScale(self,*args):
		sel = mc.ls(sl=True,fl=True)
		mc.textFieldButtonGrp(self.scaleCtrFld,edit=True,text=sel[0])	
	def loadBack1(self,*args):
		sel = mc.ls(sl=True,fl=True)
		mc.textFieldButtonGrp(self.backLoc1Fld,edit=True,text=sel[0])
	def loadBack2(self,*args):
		sel = mc.ls(sl=True,fl=True)
		mc.textFieldButtonGrp(self.backLoc2Fld,edit=True,text=sel[0])
	def loadBack3(self,*args):
		sel = mc.ls(sl=True,fl=True)
		mc.textFieldButtonGrp(self.backLoc3Fld,edit=True,text=sel[0])
	def loadBack4(self,*args):
		sel = mc.ls(sl=True,fl=True)
		mc.textFieldButtonGrp(self.backLoc4Fld,edit=True,text=sel[0])
	def loadBack5(self,*args):
		sel = mc.ls(sl=True,fl=True)
		mc.textFieldButtonGrp(self.backLoc5Fld,edit=True,text=sel[0])
	def loadEndLoc(self,*args):
		sel = mc.ls(sl=True,fl=True)
		mc.textFieldButtonGrp(self.backEndFld,edit=True,text=sel[0])				
		