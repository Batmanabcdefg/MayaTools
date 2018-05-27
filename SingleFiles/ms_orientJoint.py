"""
Copyright (c) 2008, 2009 Mauricio Santos
Name: ms_orientJoint.py
Version: 1.1
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 31 July 2008
Last Modified: 9 June 2009
License: LGNU
Description: 
		Orient jointA to jointB along: 
		$aimAxis, and $upVector, 
		up type = object, up object = $locator

To do: 

Additional Notes:
		
Updates:
			1.1: Changed flow of execution. Operates on selected object, no fields to input values, just select joints and hit orient.
				Deleted "Orient  & Close" button. 

"""


import os as os
import sys
import maya.cmds as mc
import maya.mel as mel

class ms_orientJoint:
	

	#### Internal classes:
	
	"""
		Orient Joint Tool:
		
		Select A, B(Child of A)
		Unparent B from A
		Zero Orients + Rotations on A
		Create Locator
		Snap to A
		Translate 1 in UpAxis
		Aim A at B
		Delete AimConstraint/Locator
		Copy Joint Rotations 
		Paste to Joint Orients
		Set joint Rotations to 0,0,0
		Parent B to A
		
	"""
	def __init__(self): 
		### Initialize, definitions		
	    	if(mc.window("ms_orientJoint",exists=True)):
            	    mc.deleteUI("ms_orientJoint",window=True)
	    	mc.window("ms_orientJoint",title="Orient Joint v1.0",rtf=True)
	    	mc.columnLayout()
	    	
	    	mc.rowLayout(nc=2)
	    	mc.text(" ")
	    	mc.text("Orient joint A to joint B")
	    	mc.setParent("..")
	    	
	    	mc.separator(w=500)

		self.aimAxisField = mc.radioButtonGrp(label="Aim Axis",labelArray3=['x','y','z'],nrb=3,sl = 1)
		self.aimAxisPolField = mc.radioButtonGrp(label="Aim Axis Polarity",labelArray2=['+','-'],nrb=2,sl = 1)
		self.upAxisField = mc.radioButtonGrp(label="Up Axis",labelArray3=['x','y','z'],nrb=3,sl  = 2)
		self.upPolarityField = mc.radioButtonGrp(label="Up Axis Polarity",labelArray2=['+','-'],nrb=2,sl=1)
		
		mc.separator(w=500)
		
		mc.rowLayout(nc=3)
		mc.text(" ")
		mc.button(label="-=Orient=-",c=self.orient)
		mc.button(label="-=None Orient=-",c=self.noneOrient)
		
		mc.setParent("..")

	    	mc.showWindow("ms_orientJoint")
	    	
	###Internal methods    	
	    	
	def orient(self, *args):
		aimPol = mc.radioButtonGrp(self.aimAxisPolField,query=True,sl=True)
		
		sel = mc.ls(sl=True,fl=True)
		
		if(not(len(sel))):
			mc.promptDialog(title="Error!",m="No objects selected. Select two joints. (A and B)")
			return 0
		
		srcName = sel[0]
		tgtName = sel[1]
		
		#Create a list of values according to user entry for the upAxis
		upVal = mc.radioButtonGrp(self.upAxisField,query=True,sl=True)
		upAxis = []
		
		if(upVal == 1):
			upAxis = (1,0,0)
		if(upVal == 2):
			upAxis = (0,1,0)			
		if(upVal == 3):
			upAxis = (0,0,1)

		
		#Create a list of values according to user entry for the aimAxis
		aimVal = mc.radioButtonGrp(self.aimAxisField,query=True,sl=True)
		aimAxis = []
		
		if(aimPol == 1):
			if(aimVal == 1):
				aimAxis = (1,0,0)
			if(aimVal == 2):
				aimAxis = (0,1,0)			
			if(aimVal == 3):
				aimAxis = (0,0,1)
		else:
			if(aimVal == 1):
				aimAxis = (-1,0,0)
			if(aimVal == 2):
				aimAxis = (0,-1,0)			
			if(aimVal == 3):
				aimAxis = (0,0,-1)
			
		upPolVal = mc.radioButtonGrp(self.upPolarityField,query=True,sl=True)
		upPol = []
		
		if(upPolVal == 1):
			upPol = 1
		if(upPolVal == 2):
			upPol = -1			

			
		#Unparent B(Tgt) from A(Src)
		parentJnt = mc.listRelatives(tgtName,parent=True)
		if(parentJnt): #If it has a parent, unparent it.
			mc.parent(tgtName,w=True)
	
		#Zero Orients and Rotations on A(Src)
		mc.setAttr(srcName + ".rotate",0,0,0)
		mc.setAttr(srcName + ".jointOrient",0,0,0)
		
		#Locator stuff (Snapping, moving 1 in upAxis)
		loc = mc.spaceLocator()
		self.snapping(loc,srcName)
		temp = mc.orientConstraint(srcName,loc)
		mc.delete(temp)
		
		#Move locator 1 in upAxis
		if(upVal == 1):
			mc.move(upPol,loc,x=1,r=1)
		if(upVal == 2):
			mc.move(upPol,loc,y=1,r=1)			
		if(upVal == 3):
			mc.move(upPol,loc,z=1,r=1)			
		
		#The Aim constriant
		temp = mc.aimConstraint(tgtName,srcName,aimVector=aimAxis,upVector=upAxis,worldUpType="object",worldUpObject=loc[0])
		mc.delete(temp)
		mc.delete(loc[0])
		
		#Copy Joint Rotations and Paste to Joint Orients
		#and then Set joint Rotations to 0,0,0
		
		tempRotations = mc.getAttr(srcName + ".rotate")
		mc.setAttr(srcName + ".rotate",0,0,0)
		mc.setAttr(srcName + ".jointOrient",tempRotations[0][0],tempRotations[0][1],tempRotations[0][2])
		
		#print tempRotations
		#print mc.getAttr(srcName + ".jointOrient")

		#Parent B to A
		if(parentJnt): #Only if it had a parent in the first place.
			mc.parent(tgtName,srcName)
			
	def noneOrient(self,*args):
		#Create a list of values according to user entry for the upAxis
		upVal = mc.radioButtonGrp(self.upAxisField,query=True,sl=True)
		upAxis = []
		
		sel = mc.ls(sl=True,type="joint",fl=True)
		
		if(upVal == 1): 
			upAxis = "xup"
		if(upVal == 2):
			upAxis = "yup"			
		if(upVal == 3):
			upAxis = "zup"
			
		mc.joint(sel[0],e=True, oj='none',secondaryAxisOrient=upAxis,zso=True,ch=True)
		
		
	
	def snapping(self,loc,srcName,*args):

		pos = mc.xform( srcName, q=1, ws=True, t=1)
		mc.xform( loc, ws=True, t=[pos[0], pos[1], pos[2]]) 

		rot = mc.xform( srcName, q=1, ws=True, ro=1)
		mc.xform( loc, ws=True, ro=[rot[0], rot[1], rot[2]])	
