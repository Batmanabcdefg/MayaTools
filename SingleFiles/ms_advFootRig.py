"""
Copyright (c) 2009 Mauricio Santos
Name: ms_advFootRig.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 8 July 2008
Last Modified: 19 Dec 2009

Description: Creates a reverse foot rig with attributes on controller based
				on pivots specified by user.

Command Line Arguments: (Right now, order dependant, but can use dict{} so order
		is arbitrary. <-----Update)
		
		prefix, ankleJnt, ballJnt, toeJnt, ankleCnt, footCnt, upAxisBtnVal				
				
To do: 
		Use dict{} to handle cmd line self.arguments

Additional Notes:
		We call bankPivots first, with all self.arguments, and if there are self.arguments when bankPivots called,
		the "Continue" button call createFoot, passing the self.arguments, and thus we control the flow!

"""


import os as os
import sys
import maya.cmds as mc
import maya.mel as mel


class ms_advFootRig:
	#### Internal classes:
	
	"""
		Reverse Foot Setup Script
			
	"""
	def __init__(self,*args): #Main interface
		temp = len(args)
		
		#Test to see if called with self.arguments, if so, run script by passing self.arguments to it
		if(0): #Short cuircuited to always run GUI
			self.bankPivots(args) #Passing self.arguments to function, by-passing GUI
			
		else:
			### Initialize, definitions		
			if(mc.window("ms_footRigWin",exists=True)):
			    mc.deleteUI("ms_footRigWin",window=True)
			mc.window("ms_footRigWin",title="Reverse Foot v1.0",rtf=True)

			#main window
			mc.columnLayout()

			mc.text(" ")
			self.prefixField = mc.textFieldGrp( label="Prefix:",text="L_")
			
			mc.text(" ")
			mc.text("     Joints:",fn="boldLabelFont")
			self.ankleJntField = mc.textFieldButtonGrp( label="Ankle Joint", buttonLabel="Load", bc = self.loadAnkleJnt,text = "joint1")
			self.ballField = mc.textFieldButtonGrp( label="Ball Joint", buttonLabel="Load", bc = self.loadBall,text = "joint2")
			self.toeField = mc.textFieldButtonGrp( label="Toe Joint", buttonLabel="Load", bc = self.loadToe,text = "joint3" )
			mc.text(" ")
			
			mc.separator(w=500)
			mc.text(" ")
			mc.text("     Controls:",fn="boldLabelFont")
			self.ikCntField = mc.textFieldButtonGrp(label="Leg IK Handle",buttonLabel="Load", bc = self.loadIkCnt,text = "ikHandle1")
			self.footCntField = mc.textFieldButtonGrp(label="Foot Control", buttonLabel="Load", bc = self.loadFootCnt,text = "nurbsCircle2")

			mc.text(" ")
			mc.separator(w=500)
			mc.text("     Options:",fn="boldLabelFont")
			self.upAxisField = mc.radioButtonGrp(label="Up Axis",nrb=3,labelArray3=("x","y","z"),sl=2)
			self.aimAxisField = mc.radioButtonGrp(label="Aim Axis",nrb=3,labelArray3=("x","y","z"),sl=1)
			
			mc.text("        Bank Pivot Rotational Values")
			mc.rowLayout(nc=3)
			mc.text(" ")
			mc.text("Inner Bank Value:")
			self.bankInnerValField = mc.intField(v=40)
			mc.setParent("..")
			
			mc.rowLayout(nc=3)
			mc.text(" ")
			mc.text("Outer Bank Value:")
			self.bankOutterValField = mc.intField(v=-40)
			mc.setParent("..")

			mc.text(" ")
			mc.separator(w=500)
			mc.text(" ")

			mc.rowLayout(nc=3)
			mc.text(" ")
			mc.text(" ")
			mc.button(label=" 1: Place pivots",c=self.bankPivots,w=150)
			mc.setParent("..")

			mc.rowLayout(nc=3)
			mc.text(" ")
			mc.text(" ")
			mc.button(label=" 2: Create Reverse Foot",c=self.createFoot, w=150)
			mc.setParent("..")

			mc.showWindow("ms_footRigWin")



	def bankPivots(self,*args):
		#
		#  First, we have the user place locators where they want
		#	the pivot points to be:
		#
		#			Used for:
		#	Heel Pivot
		#	Bank Inner	Medial Bank
		#	Bank Outer	Lateral Bank
		#Minimize Main window
		mc.window("ms_footRigWin",edit=True,i=True)
			
		#Prompt User
		if(mc.window("ms_footRigWin2",exists=True)):
			mc.deleteUI("ms_footRigWin2",window=True)
		mc.window("ms_footRigWin2",title="Reverse Foot v1.0",rtf=True)
	    	
		mc.columnLayout()
		mc.text("     Place the three locators.\nClick 'Continue' when done.")
	    	
		if(1):#Shorted to read from GUI
			#Store prefix value
			prefix = mc.textFieldGrp(self.prefixField,query=True,text=True)
		if(0):
			#Store prefix value
			prefix = self.arguments[0]			

	    	
	    	#Create locators, center pivots after translation	    	
	    	temp = mc.spaceLocator(p=(0,0,0))
	    	self.heelLoc = prefix + "heelPivot" + temp[0]
	    	mc.rename(temp,self.heelLoc)
	    	mc.move(-1,self.heelLoc,z=True)
	    		    	    	
	    	temp = mc.spaceLocator(p=(0,0,0))
	    	self.bankInnerLoc = prefix + "bankInner" + temp[0]
	    	mc.rename(temp,self.bankInnerLoc)
	    	mc.move(-1,self.bankInnerLoc,x=True)
	    	
	    	temp = mc.spaceLocator(p=(0,0,0))
	    	self.bankOuterLoc = prefix + "bankOuter" + temp[0]
	    	mc.rename(temp,self.bankOuterLoc)
	    	mc.move(1,self.bankOuterLoc,x=True)
	    	
		if(0):
			mc.text(" ")
			mc.rowLayout(nc=2,cw=(1,50))
			mc.text(" ")
			mc.button(label = "Continue",c='mc.deleteUI("ms_footRigWin2",window=True),mc.window("ms_footRigWin",edit=True,i=False)')
			mc.setParent("..")

		if(1): # shorted to GUI call
			mc.text(" ")
			mc.rowLayout(nc=2,cw=(1,50))
			mc.text(" ")
			mc.button(label = "Continue",c=self.createFootCall)
			mc.setParent("..")
	    	
	    	mc.showWindow("ms_footRigWin2")
	
	#We use this to call createFoot and delete bankPivots window
	def createFootCall(self,*args):
		self.createFoot()
		if(mc.window("ms_footRigWin2",exists=True)):
			mc.deleteUI("ms_footRigWin2",window=True)
		
		

	def createFoot(self,*args):
		
		#First, as always, we store all the names. The bank globals are already storing the locator names.
		#But not before testing to see if this was called with self.arguments.
		
		#temp = len(self.arguments)
		if(0): #Short-Circuited for now to default to GUI call
			#Storing names from GUI
				
			prefix = self.arguments[0]
			ankleJnt = self.arguments[1]
			ballJnt = self.arguments[2]
			toeJnt = self.arguments[3]
			ikCnt = self.arguments[4]
			footCnt = self.arguments[5]
			upAxisBtnVal = self.arguments[6]
			aimAxisBtnVal = self.arguments[7]
			bankInnerVal = self.arguments[8]
			bankOuterVal = self.arguments[9]
			
			#self.bankPivots(prefix) # call  bankPivots
		else:
			#Store prefix value
			prefix = mc.textFieldGrp(self.prefixField,query=True,text=True)

			#Joint names	
			ankleJnt = mc.textFieldButtonGrp(self.ankleJntField,query=True,text=True)
			ballJnt = mc.textFieldButtonGrp(self.ballField,query=True,text=True)
			toeJnt = mc.textFieldButtonGrp(self.toeField,query=True,text=True)

			#Control Name
			ikCnt = mc.textFieldButtonGrp(self.ikCntField,query=True,text=True)
			footCnt = mc.textFieldButtonGrp(self.footCntField,query=True,text=True)	
			
			bankInnerVal = mc.intField(self.bankInnerValField,q=True,v=True)
			bankOutterVal = mc.intField(self.bankOutterValField,q=True,v=True)

			#Up Axis
			upAxisBtnVal = mc.radioButtonGrp(self.upAxisField,query=True,sl=True) 
			
			#Aim Axis	
	    	aimAxisBtnVal = mc.radioButtonGrp(self.aimAxisField,query=True,sl=True)
	    	
	 	#Store appropriate value based on upAxisBtnVal
	 	upAxis = 0
	 	if(upAxisBtnVal == 1):
	 		upAxis = 1,0,0
	 		uAxis = 'X'
	 		
	 	if(upAxisBtnVal == 2):
	 		upAxis = 0,1,0
	 		uAxis = 'Y'
	 		
	 	if(upAxisBtnVal == 3):
	 		upAxis = 0,0,1
	 		uAxis = 'Z'
 		
 
	 	#Store appropriate value based on aimAxisBtnVal
	 	aimAxis = 0
	 	if(aimAxisBtnVal == 1):
	 		aimAxis = 1,0,0
	 		aAxis = 'X'
	 	if(aimAxisBtnVal == 2):
	 		aimAxis = 0,1,0
	 		aAxis = 'Y'
	 	if(aimAxisBtnVal == 3):
	 		aimAxis = 0,0,1
	 		aAxis = 'Z'
	 		
		#Now, we create the single chain IK for the feet     #Not using the prefix because A: it's not necessary, and 
		#ballIk = prefix+"ball"					# B: This was leading to name clashing upon IK handle creation.
		temp = mc.ikHandle(sj=ankleJnt,ee=ballJnt,sol='ikSCsolver')
		ballIk = temp[0]
		mc.rename(temp[0],ballIk)
		
		#toeIk = prefix+"toe"
		temp = mc.ikHandle(sj=ballJnt,ee=toeJnt,sol='ikSCsolver')
		toeIk = temp[0]
		mc.rename(temp[0],toeIk)
		
		#Here, we start grouping...
		peelGrp = prefix + "peel_"
		temp = mc.group(ikCnt,a=True)
		peelGrp = peelGrp + temp
		mc.rename(temp,peelGrp)
		
		peelGrp2 = prefix + "peel2_"
		temp = mc.group(peelGrp,a=True)
		peelGrp2 = peelGrp2 + temp
		mc.rename(temp,peelGrp2)		
		
		toeTapGrp = prefix + "toeTap_"
		temp = mc.group(ballIk,toeIk)
		toeTapGrp = toeTapGrp + temp
		mc.rename(temp,toeTapGrp)
		
		ballTwistGrp = prefix + "ballTwist_"
		temp = mc.group(toeTapGrp)
		ballTwistGrp = ballTwistGrp + temp
		mc.rename(temp,ballTwistGrp)
		
		toePivotGrp = prefix + "toePivot_"
		temp = mc.group(peelGrp2,toeTapGrp)
		toePivotGrp = toePivotGrp + temp
		mc.rename(temp,toePivotGrp)
		
		heelPivotGrp = prefix + "heelPivot_"
		temp = mc.group(ballTwistGrp)
		heelPivotGrp = heelPivotGrp + temp
		mc.rename(temp,heelPivotGrp)
		
		bankOuterGrp = prefix + "bankOuterPivot_"
		temp = mc.group(heelPivotGrp)
		bankOuterGrp = bankOuterGrp + temp
		mc.rename(temp,bankOuterGrp)
		
		bankInnerGrp = prefix + "bankInnerPivot_"
		temp = mc.group(bankOuterGrp)
		bankInnerGrp = bankInnerGrp + temp
		mc.rename(temp,bankInnerGrp)
		
		mc.parent(toePivotGrp,ballTwistGrp)
		

		
		#Snap pivots to their respective locations
		#PeelGrp
		tempPos = mc.xform(ballJnt,query=True,ws=1,t=1)
		mc.move(tempPos[0],tempPos[1],tempPos[2],peelGrp + ".scalePivot", peelGrp + ".rotatePivot",xyz=True,ws=True)
		
		#PeelGrp2
		tempPos = mc.xform(ballJnt,query=True,ws=1,t=1)
		mc.move(tempPos[0],tempPos[1],tempPos[2],peelGrp2 + ".scalePivot", peelGrp2 + ".rotatePivot",xyz=True,ws=True)		
		
		#toeTapGrp
		tempPos = mc.xform(ballJnt,query=True,ws=1,t=1)
		mc.move(tempPos[0],tempPos[1],tempPos[2],toeTapGrp + ".scalePivot", toeTapGrp + ".rotatePivot",xyz=True,ws=True)
		
		#toePivotGrp
		tempPos = mc.xform(toeJnt,query=True,ws=1,t=1)
		mc.move(tempPos[0],tempPos[1],tempPos[2],toePivotGrp + ".scalePivot", toePivotGrp + ".rotatePivot",xyz=True,ws=True)	
		
		#ballTwistGrp
		tempPos = mc.xform(ballJnt,query=True,ws=1,t=1)
		mc.move(tempPos[0],tempPos[1],tempPos[2],ballTwistGrp + ".scalePivot", ballTwistGrp + ".rotatePivot",xyz=True,ws=True)
		
		#heelPivotGrp
		tempPos = mc.xform(self.heelLoc,query=True,ws=1,t=1)
		mc.move(tempPos[0],tempPos[1],tempPos[2],heelPivotGrp + ".scalePivot", heelPivotGrp + ".rotatePivot",xyz=True,ws=True)
		
		#bankOutter
		tempPos = mc.xform(self.bankOuterLoc,query=True,ws=1,t=1)
		mc.move(tempPos[0],tempPos[1],tempPos[2],bankOuterGrp + ".scalePivot", bankOuterGrp + ".rotatePivot",xyz=True,ws=True)
		
		#bankInner
		tempPos = mc.xform(self.bankInnerLoc,query=True,ws=1,t=1)
		mc.move(tempPos[0],tempPos[1],tempPos[2],bankInnerGrp + ".scalePivot", bankInnerGrp + ".rotatePivot",xyz=True,ws=True)

		
		#Delete locators. They have served their purpose.
		mc.delete(self.heelLoc,self.bankInnerLoc,self.bankOuterLoc)
		
		#Now, lets parent it all under the foot control
		mc.parent(bankInnerGrp,footCnt)		

		#
		# Create Attributes for SDKs
		#
		mc.addAttr(footCnt,at='float',ln="footControls",dv=0,min=0,max=1,keyable=True)
		mc.setAttr(footCnt + ".footControls",lock=True)		
		mc.addAttr(footCnt,at='float',ln="heelRoll",dv=0,min=-10,max=10,keyable=True)
		mc.addAttr(footCnt,at='float',ln="ballRoll",dv=0,min=-10,max=10,keyable=True)
		mc.addAttr(footCnt,at='float',ln="toeRoll",dv=0,min=-10,max=10,keyable=True)
		mc.addAttr(footCnt,at='float',ln="toeTap",dv=0,min=-10,max=10,keyable=True)
		
		mc.addAttr(footCnt,at='float',ln="heelTwist",dv=0,min=-10,max=10,keyable=True)
		mc.addAttr(footCnt,at='float',ln="ballTwist",dv=0,min=-10,max=10,keyable=True)
		mc.addAttr(footCnt,at='float',ln="toeTwist",dv=0,min=-10,max=10,keyable=True)
		
		mc.addAttr(footCnt,at='float',ln="Bank",dv=0,min=-10,max=10,keyable=True)

	    
	    ###SDK's
	    ###Driver: footCnt
	    #####-----------------Roll: Pivots: peelGrp, toePivotGrp
	    
	    	mc.setDrivenKeyframe( heelPivotGrp, cd=footCnt + ".heelRoll",  at= "rotate%s"%aAxis, dv = 0,v = 0 )
		mc.setDrivenKeyframe( heelPivotGrp, cd=footCnt + ".heelRoll",  at= "rotate%s"%aAxis, dv = -10,v = 90 )
		mc.setDrivenKeyframe( heelPivotGrp, cd=footCnt + ".heelRoll",  at= "rotate%s"%aAxis, dv = 10,v = -90 )
		
		mc.setDrivenKeyframe( peelGrp, cd=footCnt + ".ballRoll",  at= "rotate%s"%aAxis, dv = 0,v = 0 )
		mc.setDrivenKeyframe( peelGrp, cd=footCnt + ".ballRoll",  at= "rotate%s"%aAxis, dv = -10,v = 90 )
		mc.setDrivenKeyframe( peelGrp, cd=footCnt + ".ballRoll",  at= "rotate%s"%aAxis, dv = 10,v = -90 )
		
		mc.setDrivenKeyframe( toePivotGrp, cd=footCnt + ".toeRoll",  at= "rotate%s"%aAxis, dv = 0,v = 0 )
		mc.setDrivenKeyframe( toePivotGrp, cd=footCnt + ".toeRoll",  at= "rotate%s"%aAxis, dv = -10,v = 90 )
		mc.setDrivenKeyframe( toePivotGrp, cd=footCnt + ".toeRoll",  at= "rotate%s"%aAxis, dv = 10,v = -90 )
		
		mc.setDrivenKeyframe( toeTapGrp, cd=footCnt + ".toeTap",  at= "rotate%s"%aAxis, dv = 0,v = 0 )
		mc.setDrivenKeyframe( toeTapGrp, cd=footCnt + ".toeTap",  at= "rotate%s"%aAxis, dv = -10,v = 90 )
		mc.setDrivenKeyframe( toeTapGrp, cd=footCnt + ".toeTap",  at= "rotate%s"%aAxis, dv = 10,v = -90 )
		
		mc.setDrivenKeyframe( heelPivotGrp, cd=footCnt + ".heelTwist",  at= "rotate%s"%uAxis, dv = 0, v = 0)   
		mc.setDrivenKeyframe( heelPivotGrp, cd=footCnt + ".heelTwist",  at= "rotate%s"%uAxis , dv = -10, v = 90) 
		mc.setDrivenKeyframe( heelPivotGrp, cd=footCnt + ".heelTwist",  at= "rotate%s"%uAxis , dv = 10, v = -90)
		   	
		mc.setDrivenKeyframe( ballTwistGrp, cd=footCnt + ".ballTwist",  at= "rotate%s"%uAxis, dv = 0, v = 0)   
		mc.setDrivenKeyframe( ballTwistGrp, cd=footCnt + ".ballTwist",  at= "rotate%s"%uAxis , dv = -10, v = -90) 
		mc.setDrivenKeyframe( ballTwistGrp, cd=footCnt + ".ballTwist",  at= "rotate%s"%uAxis , dv = 10, v = 90)
		
		mc.setDrivenKeyframe( toePivotGrp, cd=footCnt + ".toeTwist",  at= "rotate%s"%uAxis, dv = 0, v = 0)   
		mc.setDrivenKeyframe( toePivotGrp, cd=footCnt + ".toeTwist",  at= "rotate%s"%uAxis , dv = -10, v = -90) 
		mc.setDrivenKeyframe( toePivotGrp, cd=footCnt + ".toeTwist",  at= "rotate%s"%uAxis , dv = 10, v = 90)
		
		
	   	

		## Bank  	
		mc.setDrivenKeyframe( bankInnerGrp, cd=footCnt + ".Bank",  at= "rotateZ", dv = 0, v = 0)
		mc.setDrivenKeyframe( bankInnerGrp, cd=footCnt + ".Bank",  at= "rotateZ" , dv = 10, v = (bankInnerVal))
		   	
		## outerBank: 
		mc.setDrivenKeyframe( bankOuterGrp, cd=footCnt + ".Bank",  at= "rotateZ", dv = 0, v = 0)   
		mc.setDrivenKeyframe( bankOuterGrp, cd=footCnt + ".Bank",  at= "rotateZ" , dv = -10, v = (bankOutterVal))

	   	#Great, now lets zero the foot Control
	   	
		zeroNode = mc.group(em=True)

		pos = mc.xform( footCnt, q=1, ws=True, t=1)
		mc.xform( zeroNode, ws=True, t=[pos[0], pos[1], pos[2]]) 

		rot = mc.xform( footCnt, q=1, ws=True, ro=1)
		mc.xform( zeroNode, ws=True, ro=[rot[0], rot[1], rot[2]]) 

		mc.parent(footCnt, zeroNode, a=True)
		
		#The lock and hiding part! 
		#Foot Control
		mc.setAttr(footCnt + ".sx", lock=True,keyable=False)
		mc.setAttr(footCnt + ".sy", lock=True,keyable=False)
		mc.setAttr(footCnt + ".sz", lock=True,keyable=False)	
		mc.setAttr(footCnt + ".visibility",keyable=False)
		
		#Ik handles
		mc.setAttr(ballIk + ".visibility", 0)
		mc.setAttr(toeIk + ".visibility", 0)		

		mc.select(clear=True)
	   	
	   	
  


	
	### Load buttons	
	def loadAnkleJnt(self,*args):
		sel = mc.ls(sl=1)
		mc.textFieldButtonGrp(self.ankleJntField,edit=True,text=sel[0])
	    	
	def loadBall(self,*args):
		sel = mc.ls(sl=1)
		mc.textFieldButtonGrp(self.ballField,edit=True,text=sel[0])
		
	def loadToe(self,*args): 
		sel = mc.ls(sl=1)
		mc.textFieldButtonGrp(self.toeField,edit=True,text=sel[0])
		
	def loadIkCnt(self,*args):
		sel = mc.ls(sl=1)
		mc.textFieldButtonGrp(self.ikCntField,edit=True,text=sel[0])
		
	def loadFootCnt(self,*args): 
		sel = mc.ls(sl=1)
		mc.textFieldButtonGrp(self.footCntField,edit=True,text=sel[0])


