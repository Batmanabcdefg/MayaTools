"""
Copyright (c) 2008, 2009 Mauricio Santos
Name: ms_makeStretchy.py
Version: 
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 15 Aug 2008
Last Modified: 15 October 2009
License: LGNU
Description: Makes selected Ik stretchy

To do: 
	-Create GUI interface for build along value.

Additional Notes:

"""

"""
			_________________________________
			|	Make Stretchy:		|
			|				|
			| Solver: RP    or   Spline  	|
			| Stretch: Translation, Scale	|
			| Along what axis: X,Y,Z	|
			| Clusters?: Yes/No		|	
			|				|
			|IK Handle:_____________ Load	|
			|				|
			|				|
			| 	Make Stretchy!		|
			|_______________________________|
""" 


import os as os
import sys
import maya.cmds as mc
import maya.mel as mel



class ms_makeStretchy:
	"""
	 Make stretchy setup
	"""

	def __init__(self,*args,**kwargs):
		temp = kwargs
		
		if len(temp) > 1:
			cl = 1
			self.solverVal = kwargs['solverType']
			self.stretchVal = kwargs['stretchVal']
			self.axisVal = kwargs['aimAxis']
			self.ikHandle = kwargs['ikHandle']
			self.clusterVal = kwargs['clusters']
			self.prefix = kwargs['prefix']
			self.jointChain = kwargs['jointChain']
			self.kneeNum = kwargs['kneeNum']
			self.bAlong = kwargs['build']
			self.makeStretchyRun(cl)
			
		else: 
			### Initialize, definitions		
			if(mc.window("ms_makeStretchyWin",exists=True)):
				mc.deleteUI("ms_makeStretchyWin",window=True)
			mc.window("ms_makeStretchyWin",title="Make Stretchy v1.0",rtf=True)

			mc.columnLayout()

			self.solverField = mc.radioButtonGrp(l="Solver Type",labelArray2=("RP","Spline"),nrb=2,sl=2)
			self.stretchField = mc.radioButtonGrp(l="Stretch:",labelArray2=("Translate","Scale"),nrb=2,sl=1)
			self.axisField = mc.radioButtonGrp(l="Along what axis?",labelArray3=("x","y","z"),nrb=3,sl=1)
			self.clustersField = mc.radioButtonGrp(l="Create Clusters?",labelArray2=("Yes","No"),nrb=2,sl=1)
			

			mc.text(" ")
			self.ikHandleField = mc.textFieldButtonGrp( label="IK Handle:",buttonLabel="Load", bc = self.setHandle)

			mc.rowLayout(nc=3)
			mc.text(" ")
			mc.text(" ")
			mc.button(label="Make Stretchy!",c=self.makeStretchyRun)

			mc.showWindow("ms_makeStretchyWin")


	def makeStretchyRun(self,*args):
		#Store Values
		cl = args[0] #Will be set to 1 if called from the command line
		
		if cl == 1:
			pass
		
		else: #If not called by command line, get values from GUI
			self.solverVal = mc.radioButtonGrp(self.solverField,query=True,sl=True)
			self.stretchVal = mc.radioButtonGrp(self.stretchField,query=True,sl=True)
			self.axisVal = mc.radioButtonGrp(self.axisField,query=True,sl=True)
			self.ikHandle = mc.textFieldButtonGrp(self.ikHandleField,query=True,text=True)
			self.clusterVal = mc.radioButtonGrp(self.clustersField,query=True,sl=True)
		
		self.joints = mc.ikHandle(self.ikHandle,query=True,jl=True)
		
		if(self.axisVal == 1):
			self.axis = 'X'
		if(self.axisVal == 2):
			self.axis = 'Y'
		if(self.axisVal == 3):
			self.axis = 'Z'
		
		try:
			temp = mc.ikHandle(self.ikHandle,query=True,c=True)
			temp = temp.split('|')
			curve = temp[1]
		except:
			pass
		
		#Create clusters along curve
		if(self.clusterVal == 1):
			#Get Shape node
			temp = mc.listRelatives(curve,s=True)

			#These values added together tell us the number of CVs on the curve
			backSpans = mc.getAttr(temp[0]+".spans")
			backDegree = mc.getAttr(temp[0]+".degree")

			numClusters = backSpans + backDegree
			clusterNames = []
			x = 0
			while(x<numClusters):
				clusterNames.append( mc.cluster(curve+".cv["+str(x)+"]") )
				x = x + 1
		
		if(self.solverVal == 1): #RP solver
			self.rpStretchy()
		
		if(self.solverVal == 2): #Spline
			#Get the curve
			curve = mc.ikHandle(self.ikHandle,query=True,c=True)
			curve = curve.split("|")
			
			for each in curve:
				if("Shape" in each):
					continue
				if(each == " "):
					continue
				curve = each
			
			#CurveInfo node creation
			curveInfoNode = mc.arclen(curve,ch=True)
			
			#create MD node
			mdNode = mc.createNode("multiplyDivide")
			mc.setAttr(mdNode + ".operation",2)
			mc.connectAttr(curveInfoNode + ".arcLength", mdNode + ".i1x")
			arcLen = mc.getAttr(curveInfoNode + ".arcLength")
			mc.setAttr(mdNode + ".i2x", arcLen)

			if(self.stretchVal == 1):
				#Get existing translation values
				translateValues = []
				for each in self.joints:
					   translateValues.append(mc.getAttr(each + ".translate" + self.axis))
				
	  			#now lets hook up the MD nodes for each joint, except the base.
	  			x = 0
	  			for each in self.joints:		
	  				#Skip for base joint.
	  				#if(each == joints[0]):
	  				#	    continue 
					#create second MD node and set it up, connect it.   
					transMD = mc.createNode("multiplyDivide")
					mc.setAttr(transMD + ".i2x",translateValues[x])  
					mc.connectAttr(mdNode + ".outputX",transMD + ".i1x")
					mc.connectAttr(transMD + ".outputX",each + ".translate" + self.axis)
					x = x + 1   
				
				#mc.connectAttr(mdNode + ".outputX",each + ".translate" + self.axis)			
			
			if(self.stretchVal == 2):
				for each in self.joints:
					mc.connectAttr(mdNode + ".outputX",each + ".scale" + self.axis)
					
	def rpStretchy(self,*args):
		#
		# Full length distance dimension node
		#
		#Get world space of ik_1 and ik_end joints, used to place distDimension node locators
		ikBaseJntPos = mc.xform(self.joints[0],query=True,t=True,ws=True)
		ikEndJntPos = mc.xform(self.joints[1],query=True,t=True,ws=True)
		
		#Create distanceDimensionShape node. Create locators at locations that do not have locators.
		fullLen_DDNodeShape = mc.distanceDimension( sp=[1,0,0], ep=[0,1,0] )
		
		
		#Get created locators names
		temp = mc.listConnections(fullLen_DDNodeShape)
		temp1 = temp[0]
		temp2 = temp[1]
		
		#Rename locators
		mc.rename(temp1,('%s%sfullLen_start'%(self.prefix,temp1) ) )
		mc.rename(temp2,('%s%sfullLen_end'%(self.prefix,temp2) ) )
		
		#Rename Distance Dimension node    
		temp = mc.pickWalk(fullLen_DDNodeShape,direction='up')
		mc.rename(temp[0],('%s%sfullLen_DDnode'%(self.prefix,temp[0]) ) )
		
		#Store names
		fullLenLoc_start = '%s%sfullLen_start'%(self.prefix,temp1)
		fullLenLoc_end = '%s%sfullLen_end'%(self.prefix,temp2)
		fullLen_DDNode = '%s%sfullLen_DDnode'%(self.prefix,temp[0])
		fullLen_DDNodeShape = '%s%sfullLen_DDnodeShape'%(self.prefix,temp[0])
		
		#Now, snap the locators to the right position.
		mc.move(ikBaseJntPos[0],ikBaseJntPos[1],ikBaseJntPos[2],fullLenLoc_start,moveXYZ=True)
		mc.move(ikEndJntPos[0],ikEndJntPos[1],ikEndJntPos[2],fullLenLoc_end,moveXYZ=True)
		
		distGrp = self.prefix + '_distGrp'
		mc.group(em=True,n=distGrp)
		mc.parent(fullLenLoc_start,fullLenLoc_end,fullLen_DDNode,distGrp)
		mc.setAttr(distGrp + '.visibility',0)
		
		#point constraint locators
		fullLenDD_startLoc_PC = mc.pointConstraint(self.joints[0], fullLenLoc_start,mo=False)
		fullLenDD_endLoc_PC = mc.pointConstraint(self.ikHandle, fullLenLoc_end,mo=False)

		#Get dimension value
		origLen = mc.getAttr(fullLen_DDNodeShape + '.distance')
		
		#
		# Now, lets create the stretchy expression for one knee scenario
		#
		if self.kneeNum == 1:
			
			topJntLength = mc.getAttr('%s.translate%s'%(self.jointChain[1],self.axisVal) )
			btmJntLength = mc.getAttr('%s.translate%s'%(self.jointChain[2],self.axisVal) )
			fullLength = topJntLength + btmJntLength
			
			fullLength = abs(fullLength)         # Absolute values because distance should never be negative
			topJntLength = abs(topJntLength)
			btmJntLength = abs(btmJntLength) 
			
			driver = fullLen_DDNodeShape + '.distance'
			
			#Create SDKs
			if self.bAlong == 'positive':
				mc.setDrivenKeyframe(self.jointChain[1],cd=driver,dv=fullLength,at=('translate%s'%self.axisVal),v=topJntLength)
				mc.setDrivenKeyframe(self.jointChain[1],cd=driver,dv=(fullLength*5),at=('translate%s'%self.axisVal),v=(topJntLength*5) )
				
				mc.setDrivenKeyframe(self.jointChain[2],cd=driver,dv=fullLength,at=('translate%s'%self.axisVal),v=btmJntLength)
				mc.setDrivenKeyframe(self.jointChain[2],cd=driver,dv=(fullLength*5),at=('translate%s'%self.axisVal),v=(btmJntLength*5) )
				
			if self.bAlong == 'negative':
				mc.setDrivenKeyframe(self.jointChain[1],cd=driver,dv=-fullLength,at=('translate%s'%self.axisVal),v=topJntLength)
				mc.setDrivenKeyframe(self.jointChain[1],cd=driver,dv=-(fullLength*5),at=('translate%s'%self.axisVal),v=(topJntLength*5) )
				
				mc.setDrivenKeyframe(self.jointChain[2],cd=driver,dv=-fullLength,at=('translate%s'%self.axisVal),v=btmJntLength)
				mc.setDrivenKeyframe(self.jointChain[2],cd=driver,dv=-(fullLength*5),at=('translate%s'%self.axisVal),v=(btmJntLength*5) )
			
			mc.setDrivenKeyframe(self.jointChain[1],cd=driver,dv=0,at=('translate%s'%self.axisVal),v=topJntLength )
			mc.setDrivenKeyframe(self.jointChain[2],cd=driver,dv=0,at=('translate%s'%self.axisVal),v=btmJntLength )
			
			print "Don't forget to make the SDK curves linear and infinite."
			
		#
		# Now, lets create the stretchy expression for two knee scenario
		#
		if self.kneeNum == 2:
			
			topJntLength = mc.getAttr('%s.translate%s'%(self.jointChain[1],self.axisVal) )
			midJntLength = mc.getAttr('%s.translate%s'%(self.jointChain[2],self.axisVal) )
			btmJntLength = mc.getAttr('%s.translate%s'%(self.jointChain[3],self.axisVal) )
			fullLength = topJntLength + midJntLength + btmJntLength
			
			driver = fullLen_DDNodeShape + '.distance'
			
			#Create SDKs
			if self.bAlong == 'positive':
				mc.setDrivenKeyframe(self.jointChain[1],cd=driver,dv=fullLength,at=('translate%s'%self.axisVal),v=topJntLength)
				mc.setDrivenKeyframe(self.jointChain[1],cd=driver,dv=(fullLength*5),at=('translate%s'%self.axisVal),v=(topJntLength*5) )
				
				mc.setDrivenKeyframe(self.jointChain[3],cd=driver,dv=fullLength,at=('translate%s'%self.axisVal),v=btmJntLength)
				mc.setDrivenKeyframe(self.jointChain[3],cd=driver,dv=(fullLength*5),at=('translate%s'%self.axisVal),v=(btmJntLength*5) )
			if self.bAlong == 'negative':
				mc.setDrivenKeyframe(self.jointChain[1],cd=driver,dv=-fullLength,at=('translate%s'%self.axisVal),v=topJntLength)
				mc.setDrivenKeyframe(self.jointChain[1],cd=driver,dv=-(fullLength*5),at=('translate%s'%self.axisVal),v=(topJntLength*5) )
				
				mc.setDrivenKeyframe(self.jointChain[3],cd=driver,dv=-fullLength,at=('translate%s'%self.axisVal),v=btmJntLength)
				mc.setDrivenKeyframe(self.jointChain[3],cd=driver,dv=-(fullLength*5),at=('translate%s'%self.axisVal),v=(btmJntLength*5) )
			
			mc.setDrivenKeyframe(self.jointChain[1],cd=driver,dv=0,at=('translate%s'%self.axisVal),v=topJntLength )
			mc.setDrivenKeyframe(self.jointChain[3],cd=driver,dv=0,at=('translate%s'%self.axisVal),v=btmJntLength )
			
			print "Don't forget to make the SDK curves linear and infinite."
			
			

	def setHandle(self,*args):
		temp = mc.ls(sl=1)
		mc.textFieldGrp(self.ikHandleField,edit=True,text=temp[0])

