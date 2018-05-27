"""
Copyright (c) 2009 Mauricio Santos
Name: ms_pistonMaker.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 30 Dec 2009
Last Modified: 30 Dec 2009
Description: 
	Given two locators, sets up a piston rig. Based on Art of Rigging Volume II method.

To do: 
	-Error checking
	
Additional Notes: 
	
Requires:
	
"""


import maya.mel as mel
import maya.cmds as mc

class ms_pistonMaker():
	"""
		Chain builder assistant.
	"""
	
	def __init__(self,*args):
		if(mc.window("msPistonMakerWin",exists=True)):
			mc.deleteUI("msPistonMakerWin",window=True)
		
		mc.window("msPistonMakerWin",title="Piston Rig Maker v1.0",rtf=1)
		mc.columnLayout()
		
		self.prefixFld = mc.textFieldGrp(l='Prefix:',text='l_leg_')
		
		mc.frameLayout(l="  Create Locator",fn='boldLabelFont',w=450)
		mc.columnLayout()
		mc.rowLayout(nc=2,cw2=(320,100))
		mc.text("    Create a locator at the pivot of the currently selected vertices.")
		mc.button(label='    Create Locator ',c=self.locAtSel,w=100)
		mc.setParent("..")
		mc.rowLayout(nc=2,cw2=(320,100))
		mc.text("    Create a locator at the pivot of selected object.")
		mc.button(label='    Create Locator ',c=self.locAtObj,w=100)
		mc.setParent("..")
		mc.setParent("..")	
		mc.setParent("..")
		
		
		mc.frameLayout(l="  Piston rig",fn='boldLabelFont',w=450)
		mc.columnLayout()
		
		self.casingFld = mc.textFieldButtonGrp(label='Piston Casing Locator',bc=self.loadCasing,bl='Load')
		self.rodFld = mc.textFieldButtonGrp(label='Piston Rod Locator',bc=self.loadRod,bl='Load')
		
		mc.rowLayout(nc=2)
		mc.text(" ")
		mc.button(label='Create Rig',c=self.createRig)
		mc.setParent("..")	
		mc.setParent("..")
		
		mc.setParent("..")	
		mc.setParent("..")
	
		mc.setParent("..")
		mc.setParent("..")

		mc.showWindow("msPistonMakerWin")

	def createRig(self,*args):
		"""
		  Create Piston rig.
		"""
		prefix = mc.textFieldGrp(self.prefixFld,query=True,text=True)
		casingLoc = mc.textFieldButtonGrp(self.casingFld,query=True,text=True)
		rodLoc = mc.textFieldButtonGrp(self.rodFld,query=True,text=True)
		
		aim1 = mc.aimConstraint(rodLoc, casingLoc, weight=1, aimVector=(1,0,0), upVector=(0,1,0), worldUpType='vector', worldUpVector=(0,1,0), mo=False)
		aim2 = mc.aimConstraint(casingLoc, rodLoc, weight=1, aimVector=(1,0,0), upVector=(0,1,0), worldUpType='vector', worldUpVector=(0,1,0), mo=False)
		
		casingGrp = mc.group(casingLoc,n=casingLoc+'_buffer')
		rodGrp = mc.group(rodLoc,n=rodLoc+'_buffer')
		
		mc.group(casingGrp,rodGrp,n=prefix+'_grp')
		
		
		
	def locAtObj(self,*args):
		"""
		  Create locator at selected object's pivot.
		"""
		prefix = mc.textFieldGrp(self.prefixFld,query=True,text=True)
		sel = mc.ls(sl=True,fl=True)
		pos = mc.xform(sel[0],query=True,ws=True,pivots=True)

		loc = mc.spaceLocator(p=(pos[0],pos[1],pos[2]),n=prefix+'_loc' )
		mc.xform(loc,cp=True)
		
	def locAtSel(self,*args):
		"""
			Additional tool:
			Create a locator at the pivot of the current selection.
		"""
		prefix = mc.textFieldGrp(self.prefixFld,query=True,text=True)
		sel = mc.ls(sl=True,fl=True)
		locations = []        # Locations (x,y,z) of selected objects/verts/etc...
		sumX = 0              # Sum of all locations
		sumY = 0
		sumZ = 0
		avgX  = 0             # The average of the location (The selection center)
		avgY  = 0
		avgZ  = 0
		
		#get selection pivot location
		for vert in sel:
			locations.append( mc.pointPosition(vert,w=True) )
		
		for each in locations:
			sumX = sumX + each[0]
			sumY = sumY + each[1]
			sumZ = sumZ + each[2]
			
		avgX = sumX / len(sel)
		avgY = sumY / len(sel)
		avgZ = sumZ / len(sel)
			
		#create locator
		loc = mc.spaceLocator(p=(avgX,avgY,avgZ),n=prefix+'_loc')
		mc.select(loc,r=True)
		mel.eval("CenterPivot;")
		
		mc.setAttr('%s.scaleX'%loc[0], .03)
		mc.setAttr('%s.scaleY'%loc[0], .03)
		mc.setAttr('%s.scaleZ'%loc[0], .03)
		
		mc.select(sel,r=True)
		
		mel.eval("changeSelectMode -component;")
	

	def loadCasing(self,*args): 
		sel = mc.ls(sl=True)
		mc.textFieldGrp(self.casingFld,edit=True,text=sel[0])
		
	def loadRod(self,*args): 
		sel = mc.ls(sl=True)
		mc.textFieldGrp(self.rodFld,edit=True,text=sel[0])
