"""
Copyright (c) 2008,2009 Mauricio Santos
Name: ms_fkController.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 20 Sep 2008
Last Modified: 9 June 2009
License: LGNU
Description: FK Control on a joint, or multiple joints

To do: Option: length + step

Additional Notes:

"""

import os as os
import sys
import maya.cmds as mc
import maya.mel as mel


class ms_fkController():
	"""
		Creates FK controller sharing transform nodes of joints in chain.
			
	"""
	def __init__(self,*args): #Main interface

		### Initialize, definitions		
		if(mc.window("ms_fkControlWin",exists=True)):
		    mc.deleteUI("ms_fkControlWin",window=True)
		mc.window("ms_fkControlWin",title="FK Control v1.0",rtf=True)

		#main window
		mc.columnLayout()

		mc.text(" ")
		self.prefixField = mc.textFieldGrp( label="Prefix:",text="L_")

		self.controlField = mc.textFieldButtonGrp( label="Control curve", buttonLabel="Load", bc = self.loadControl)
		self.jntField = mc.textFieldButtonGrp( label="Joint (Root)", buttonLabel="Load", bc = self.loadStartJnt)
		self.selectionField = mc.radioButtonGrp(label="Hierarchy:",nrb=2,labelArray2=('Yes','No'),sl=1)

		mc.text(" ")
		mc.separator(w=500)
		mc.text(" ")

		mc.rowLayout(nc=3)
		mc.text(" ")
		mc.text(" ")
		mc.button(label=" Create FK Control ",c=self.createControl, w=120)
		mc.setParent("..")

		mc.showWindow("ms_fkControlWin")

	def createControl(self,*args):
		""" Create FK control for selected joint, or it's hierarchy
		"""

		#Store values
		prefix = mc.textFieldGrp(self.prefixField,query=True,text=True)
		
		rootJnt = mc.textFieldButtonGrp(self.jntField,query=True,text=True)
		control = mc.textFieldButtonGrp(self.controlField,query=True,text=True)
		selection = mc.radioButtonGrp(self.selectionField,query=True,sl=True)
		
		#Main Chain
		if(selection == 1):
		    mc.select(rootJnt,r=True,hi=True)
		else:
			mc.select(rootJnt,r=True)
		
		sel = mc.ls(sl=True,fl=True)
		
		#Duplicate FK control, parent it to selected joints
		for each in sel:
			#Duplicate control
			tempCnt = mc.duplicate(control)
			#Select the shape
			tempShp = mc.pickWalk(tempCnt,direction='down')
			mc.parent(tempShp,each,r=True,s=True)
			
		
			
		
	### Load buttons	
	def loadControl(self,*args):
		sel = mc.ls(sl=1,fl=True)
		mc.textFieldButtonGrp(self.controlField,edit=True,text=sel[0])
	    	
	def loadStartJnt(self,*args):
		sel = mc.ls(sl=1,fl=True)
		mc.textFieldButtonGrp(self.jntField,edit=True,text=sel[0])
		
	
		



