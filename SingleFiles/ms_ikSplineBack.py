"""
Copyright (c) 2009 Mauricio Santos
Name: ms_ikSplineBack.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 19 June 2009
Last Modified: 25 June 2009
License: LGNU
Description: 
		Jason Schleifer IK/FK 2006 Master Class Method (Stretchy IK Spline on FK joints, Shoulders, hips controls. No mid back.)
		Called by GUI: ms_backRig.py
To do: 

		
Additional Notes:


Development Notes:
    

"""
import maya.cmds as mc

class ms_ikSplineBack():
	def __init__(self,*args,**kwargs):
		"""
		  IK stretchy spline as explained by Jason Schleifer.
		  Initialize variables, then call tasks. 
		"""
		#Initialize variables (Storing names)
		self.prefix = kwargs['prefix']
		
		self.shldrCnt = kwargs['shldrCnt']
		self.hipsCnt = kwargs['hipsCnt']
		self.bodyCnt = kwargs['bodyCnt']
		self.scaleCnt = kwargs['scaleCnt']
		
		self.baseJnt = kwargs['baseJnt']
		self.endJnt = kwargs['endJnt']
		
		self.numSpans = kwargs['numSpans']
		
		self.worldUpType = kwargs['worldUpType']
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
		self.ikSplineSetup()
		
	
	
	
	def ikSplineSetup(self,*args):
		"""
		 Build IK Spline 
		"""
		#Store ikChain
		mc.select(self.baseJnt,hi=True,r=True)
		ikChain = mc.ls(sl=True,fl=True)
		
		
		# Create hip and shldr jnts
		mc.select(clear=True)
		self.hipJnt = mc.joint( n = self.prefix + 'hipJnt' ) 
		mc.select(clear=True)
		self.shldrJnt = mc.joint( n = self.prefix + 'shldrJnt' ) 
        
		# Snap created joints to base + end joints
		temp = mc.pointConstraint( self.baseJnt, self.hipJnt, mo=False )
		mc.delete( temp )
		temp = mc.pointConstraint( self.endJnt, self.shldrJnt, mo=False )
		mc.delete( temp )
		
		#Match orientations by parenting the jnts, then orienting with none value, then unparenting
		mc.parent(self.hipJnt, self.baseJnt)
		mc.parent(self.shldrJnt, self.endJnt)
		mc.joint(self.hipJnt,e=True, oj='none',zso=True,ch=True)
		mc.joint(self.shldrJnt,e=True, oj='none',zso=True,ch=True)
		mc.parent( self.hipJnt, w=True )
		mc.parent( self.shldrJnt, w=True )
		
		#Set rotation orders based on rotate order of body control
		mc.setAttr(self.hipJnt + ".rotateOrder", (self.rotateOrder))
		mc.setAttr(self.shldrJnt + ".rotateOrder", (self.rotateOrder))
		
		#Value used in spline ik command
		self.numSpans = self.numSpans + 1
		
		#SplineIK for back: Create and store name
		backIkHandle = self.prefix + "back_"
		temp = mc.ikHandle(sj=self.baseJnt,ee=self.endJnt,sol="ikSplineSolver",pcv=False,ns=self.numSpans) 
		backIkHandle = backIkHandle + temp[0]
		mc.rename(temp[0],backIkHandle)
		
		#Get back ik curve name
		temp = mc.listConnections(backIkHandle,s=True)
		for each in temp:
			if "curve" in each:
				backCurve = each #Storing the back ik curve name
		#Name back curve
		temp = self.prefix + '_backIkCrv'		
		mc.rename(backCurve, temp)
		backCurve=temp
				
		#Skin hip/shldr jnt's to back curve
		mc.skinCluster(self.hipJnt,self.shldrJnt,backCurve,dr=4)
		
		#Parent hipsJnt/shldrJnt to controllers
		mc.parent(self.hipJnt,self.hipsCnt)
		mc.parent(self.shldrJnt,self.shldrCnt)
		
		#Turn off inherit transforms on backCurve
		mc.setAttr(backCurve +".inheritsTransform", 0)
		
		#
		#---Set up stretchy
		#
		
		#0Select and store the joints to link in the back expression
		mc.select(self.baseJnt,hi=True,r=True)
		backJoints = mc.ls(sl=1,fl=1,type='joint')
			
		jntNum = len(backJoints)
		

		stretch = '.scale' + self.stretchyAxis  #i.e. 'scaleX'

		#Now,Create curveInfo node 
		curveInfo = mc.arclen(backCurve,ch=1)
		#Rename curve info node
		temp = self.prefix + 'backCrvInfo'
		mc.rename(curveInfo, temp)
		curveInfo = temp
		
		#Create backScaleMD and connect arclength to input1X
		backScaleMD = mc.createNode('multiplyDivide',n=self.prefix + 'backMD')		
		mc.connectAttr(curveInfo + ".arcLength",backScaleMD + ".i1x")	

		#Get ArcLength value, set backScaleMD node to divide by it
		arcLen = mc.getAttr(curveInfo+".arcLength")
		mc.setAttr(backScaleMD+".i2x",arcLen)
		mc.setAttr(backScaleMD+".operation",2) #Divide

		#
		#---Advance Twist setup
		# Make these values variables in the interface...
		mc.setAttr( backIkHandle + ".dTwistControlEnable", 1)	#Enable advanced twist
		mc.setAttr( backIkHandle + ".dWorldUpType", self.worldUpType-1) 	
		mc.setAttr( backIkHandle + ".dWorldUpAxis", self.upAxis-1) 			
		mc.setAttr( backIkHandle + ".dWorldUpVectorX", self.upVecX)		     
		mc.setAttr( backIkHandle + ".dWorldUpVectorY", self.upVecY)		    
		mc.setAttr( backIkHandle + ".dWorldUpVectorZ", self.upVecZ)		    
		mc.setAttr( backIkHandle + ".dWorldUpVectorEndX", self.upVec2X)	    
		mc.setAttr( backIkHandle + ".dWorldUpVectorEndY", self.upVec2Y) 	
		mc.setAttr( backIkHandle + ".dWorldUpVectorEndZ", self.upVec2Z) 	
		
		mc.connectAttr(self.hipsCnt + '.worldMatrix', backIkHandle+'.dWorldUpMatrix', f=True)
		mc.connectAttr(self.shldrCnt + '.worldMatrix', backIkHandle+'.dWorldUpMatrixEnd', f=True)
				
		#
		#---Make volume preservation expression
		#
		
		#Create attributes for each joint so the user can set the 
		# scaling factor per joint via the hipControl
		mc.addAttr(self.hipsCnt,ln='BackVolumeScaleFactor',k=True,dv=0)
		mc.setAttr(self.hipsCnt + '.BackVolumeScaleFactor',lock=True)
		
		x = 0
		for each in backJoints:
				#Not the backBaseJnt
				if(each == self.baseJnt):
					x = x + 1
					continue
				#Skipping the last one
				if( x == (jntNum-1) ):
					x = x + 1
					break
				mc.addAttr(self.hipsCnt,ln=each,dv=1,k=True)
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
				if(jnt == self.baseJnt):
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
				if(jnt == self.baseJnt):
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
				if(jnt == self.baseJnt):
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
				
		mc.expression( s=backExpString,n=self.prefix+'backVolumeExp' )
		
		#Connect scaleY to X + Z for a global scale effect.
		mc.connectAttr(self.scaleCnt + '.scaleY',self.scaleCnt+'.scaleX',f=True)
		mc.connectAttr(self.scaleCnt + '.scaleY',self.scaleCnt+'.scaleZ',f=True)
			
		#
		#--- Moveable pivot
		#--- Work in progress: Moving on for now, revisit should necessity arrive.			
		"""
		#Create pivot control locator ad snap to body/COG
		pivLoc = mc.spaceLocator()
		temp = mc.parentConstraint(self.hipsCnt,pivLoc,mo=False)
		mc.delete(temp)
		
		#Rename locator
		temp = self.prefix + 'hipsPivot_Ctrl'
		mc.rename(pivLoc,temp)
		pivLoc=temp

		#Attach locator to hipCnt pivot
		mc.connectAttr(pivLoc + '.translate', self.hipsCnt + '.rotatePivot',f=True)	

		#Parent the locator to hipsCnt
		mc.parent(pivLoc,self.hipsCnt)
		#Freeze transform now, so it inherits the orientation of it's parent
		mc.makeIdentity(pivLoc, apply=True )
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
			mc.select(clear=True)
			#Get rotate order from hips control
			rotateOrder = mc.getAttr(self.hipsCnt+'.rotateOrder')
			fkJnts = []
			x = 0
			while x < (self.numFkJnts[0] + 1):
				pos = mc.xform(ikChain[x], query=True,ws=True,t=True)
				#point = mc.xform(fkCrv + '.cv['+str(x)+']', query=True,ws=True,t=True)
				if x == 0: #If first joint
					fkJnts.append( mc.joint( p = (pos) ,n=self.prefix+'fbBackBase' )  )
					#Set rotate order	
					mc.setAttr(fkJnts[x] + '.rotateOrder', rotateOrder)
					x = x + 1
					continue
				if x == ( self.numFkJnts[0] ): #If last joint
					fkJnts.append( mc.joint( p = (pos) ,n=self.prefix+'fkBackEnd' )  )
					break
				else:
					fkJnts.append( mc.joint( p = (pos) ,n=self.prefix+'fkBack_'+str(x) )  )
				#Set rotate order	
				mc.setAttr(fkJnts[x] + '.rotateOrder', rotateOrder)
				
				x = x + 1
			#mc.delete(fkCrv)
			
			""" May not be needed: when building along ik, it will orient to the next joint
				automatically.
			"""
			x = 0	
			for jnt in fkJnts:
				#Parent to baseJnt, makeIdentity to match orientation
				mc.parent( jnt, self.baseJnt )
				mc.makeIdentity(jnt, apply=True, jo=True )
				temp = mc.group( jnt )
				mc.ungroup( temp, w=True )
				#It will always fail with an index out of range error for the fist one.
				try:
					#This puts it back into the fk hierarchy
					mc.parent( jnt, fkJnts[x-1] )
				except:
					pass
				
				x = x + 1
			
			#Create fk controller curves
			x = 0
			for jnt in fkJnts:
				    				
				#Skip the last one
				if x == (len(fkJnts)+1): 
					break
				
				if self.stretchyAxis == 'X':
					tempCnt = mc.circle( nr = (1,0,0),r=self.radius[0] )
				if self.stretchyAxis == 'Y':
					tempCnt = mc.circle( nr = (0,1,0),r=self.radius[0] )
				if self.stretchyAxis == 'Z':
					tempCnt = mc.circle( nr = (0,0,1),r=self.radius[0] )
				
				#Select the shape
				tempShp = mc.pickWalk(tempCnt,direction='down')
				mc.parent(tempShp,jnt,r=True,s=True)
				
				#Delete empty transform
				mc.delete(tempCnt)
				
				x = x + 1
				
			#Parent fkBase joint to body/COG
			mc.parent(fkJnts[0],self.bodyCnt)
			
			#Parent hipCnt to body/COG
			mc.select(self.hipsCnt,r=True)
			bufferGrp = mc.pickWalk(direction='up')
			#bufferGrp = mc.ls(sl=True,fl=True) 
			mc.parent(bufferGrp[0], self.bodyCnt)
			
			#Parent shldrCnt to fkJnts[last one]
			mc.select(self.shldrCnt,r=True)
			bufferGrp = mc.pickWalk(direction='up')
			#bufferGrp = mc.ls(sl=True,fl=True) 
			mc.parent(bufferGrp[0], fkJnts[-1:])
			
			#Grp ikCurve, ikHandle into doNotTouch group
			if mc.objExists(self.prefix + '_NoTouchy'):
				mc.parent(backCurve, backIkHandle, self.prefix + '_NoTouchy')
			else:
				noTouchGrp = mc.group( backCurve, backIkHandle, n = self.prefix + '_NoTouchy') 
            
			#Group + parent joints to world control (ScaleCnt)
			jntsGrp = mc.group( self.baseJnt , n=self.prefix+'_backJntsGrp')
			mc.parent( jntsGrp, self.scaleCnt )
            
			#Get body/COG control buffer, parent it to scaleCnt 
			mc.select(self.bodyCnt,r=True)
			mc.pickWalk(direction='up')
			buffer = mc.ls(sl=True,fl=True)
			mc.parent(buffer,self.scaleCnt)
