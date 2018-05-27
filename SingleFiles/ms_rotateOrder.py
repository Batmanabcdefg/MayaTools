"""
Copyright (c) 2008,2009 Mauricio Santos
Name: ms_rotateOrder.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 1 Aug 2008
Last Modified: 9 June 2009
License: LGNU
Description: Set rotate order for selected joints.

To do: 

Additional Notes:

"""


import os as os
import sys
import maya.cmds as mc
import maya.mel as mel

class ms_rotateOrder:
	#### Internal classes:
	
	"""
		Set rotate order for selected joints.
		
	"""
	def __init__(self):
		global optionValue
		global selectionField
	
		
	    	### Initialize, definitions		
	    	if(mc.window("ms_rotateOrder",exists=True)):
            	    mc.deleteUI("ms_rotateOrder",window=True)
	    	mc.window("ms_rotateOrder",title="Set Rotate Order v1.0",rtf=True)
	    	mc.columnLayout()
	    	
	    	mc.text(" ")

	    	mc.rowLayout(nc=2)
	    	mc.text(" ")
	    	selectionField = mc.radioButtonGrp(nrb=2,labelArray2=("Selected","Hierarchy"),sl=1)
		mc.setParent("..")

		
		#This will load objects currently selected into name fields upon GUI creation
		objects = mc.ls(sl=1)
		try:
			mc.textFieldButtonGrp(jntField,edit=True,text=objects[0])
		except:
			pass
		
		mc.separator(w=300)
		
		mc.rowLayout(nc=2)
		mc.text(" ")
		optionValue = mc.optionMenu(label="Rotate Order:   ")
		mc.menuItem(label="xyz")
		mc.menuItem(label="yzx")
		mc.menuItem(label="zxy")
            	mc.menuItem(label="xzy")
            	mc.menuItem(label="yxz")
            	mc.menuItem(label="zyx")
            	mc.setParent("..")
            	
            	mc.text(" ")
            	mc.separator(w=300)

            	
            	
            	mc.rowLayout(nc=2)
            	mc.text(" ")
            	mc.button(label="Set Rotation Order",c=self.setRotations)            
            	mc.setParent("..")
		mc.text(" ")

	    	mc.showWindow("ms_rotateOrder")

	
	def setRotations(self,*args):
		global optionValue
		global selectionField
		
		setType = mc.radioButtonGrp(selectionField,query=True,sl=True)
		rotateOrder = mc.optionMenu(optionValue,query=True,sl=True)
		
		allJnts = mc.ls(sl=True)
		rootName = allJnts[0]
		
		if(setType == 1): #Only orient the selected joints
			allJnts = mc.ls(sl=True)
			
			for each in allJnts:
				mc.setAttr(each + ".rotateOrder", (rotateOrder - 1))
			
			mc.select(allJnts,r=True)
			return
		
		#Otherwise, set children as well as selected
		
		mc.select(rootName,hi=True)
		allJnts = mc.ls(sl=True)
		
		for each in allJnts:
			try:
				mc.setAttr(each + ".rotateOrder", (rotateOrder - 1))	
			except:
				pass
		
		mc.select(clear=True)
			
		
		

	