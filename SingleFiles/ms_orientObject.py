"""
Copyright (c) 2008, 2009 Mauricio Santos
Name: ms_orientObject.py
Version: 1.1
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 15 Sep 2009
Last Modified: 15 Sep 2009
License: LGNU
Description: 
		Orient Object A to Object B

To do: 

Additional Notes:
		
Updates:


"""


import os as os
import sys
import maya.cmds as mc
import maya.mel as mel

class ms_orientObject:
	###Internal methods
	"""
		Orient Object Tool:
		
		Select A, B(Child of A)
		Unparent B from A
		Zero Orients + Rotations on A
		Create Locator
		Snap to A
		Translate 1 in UpAxis
		Aim A at B
		Delete AimConstraint/Locator
		Copy Object Rotations 
		Paste to Object Orients
		Set joint Rotations to 0,0,0
		Parent B to A
		
	"""
	def __init__(self): #(Initialization)

		### Initialize, definitions		
		if(mc.window("ms_orientObject",exists=True)):
			mc.deleteUI("ms_orientObject",window=True)
		mc.window("ms_orientObject",title="Orient Object v1.0",rtf=True)
		mc.columnLayout()

		mc.text(" ")
		mc.rowLayout(nc=4,cw4=(25,130,150,200) )
		mc.text(" ")
		mc.text("Orient object A to object B.")
		mc.text("Unparents during operation, so ")
		mc.text("constraints should not be applied yet.")
		mc.setParent("..")
		mc.text(" ")

		mc.separator(w=500)
		self.aObjFld = mc.textFieldButtonGrp( label='Object A:',bl='Load',bc=self.loadAObj,text='pCube1')
		self.bObjFld = mc.textFieldButtonGrp( label='Object B:',bl='Load',bc=self.loadBObj,text='inside_cube_small')
		mc.separator(w=500)
		
		mc.rowLayout(nc=2,cw2=(200,300))
		mc.text(" ")
		mc.button(label="-=Match Orientation=-",c=self.orient)
		mc.setParent("..")

		mc.showWindow("ms_orientObject")
	    	
	    	
	    	
	def orient(self, *args):
		### Orient A (Src) pointing or matching orientation of B (Tgt)
	
		aObj = mc.textFieldGrp(self.aObjFld,query=True,text=True)
		bObj = mc.textFieldGrp(self.bObjFld,query=True,text=True)
		
		
		#Orient Constraint
		temp = mc.orientConstraint(bObj,aObj,mo=False)
		mc.delete(temp)
		
		#Re-Parent A to it's original parent
		try:
			temp = len(aPrnt)
		except:
			temp = 0
			
		#If object has a parent	
		if temp: 
			mc.parent(aObj,aPrnt)
		else:
			mc.parent(aObj,world=True)	
		
			

	def loadAObj(self,*args):
		sel = mc.ls(sl=True,fl=True)
		mc.textFieldButtonGrp(self.aObjFld,edit=True,text=sel[0])
		
	def loadBObj(self,*args):
		sel = mc.ls(sl=True,fl=True)
		mc.textFieldButtonGrp(self.bObjFld,edit=True,text=sel[0])	