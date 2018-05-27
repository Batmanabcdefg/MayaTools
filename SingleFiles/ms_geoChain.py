"""
Copyright (c) 2009 Mauricio Santos
Name: ms_pistonMaker.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 30 Dec 2009
Last Modified: 30 Dec 2009
License: LGNU
Description: 
	Given two locators, sets up a piston rig. Based on Art of Rigging Volume II method.

To do: 
	-Error checking
	
Additional Notes: 
	
Requires:
	
"""


import maya.mel as mel
import maya.cmds as mc

class ms_geoChain():
	"""
		Chain builder assistant.
	"""
	
	def __init__(self,*args):
		if(mc.window("msGeoChainWin",exists=True)):
			mc.deleteUI("msGeoChainWin",window=True)
		
		mc.window("msGeoChainWin",title="Geometry Chain Setup v1.0",rtf=1)
		mc.columnLayout()
		
		self.prefixFld = mc.textFieldGrp(l='Prefix:',text='chain1_')
		
		mc.frameLayout(l="Create Locator",fn='boldLabelFont',cll=True,cl=False,w=450)
		mc.columnLayout()
		mc.rowLayout(nc=2,cw2=(320,100))
		mc.text("    Create a locator at the pivot of the currently selected vertices.")
		mc.button(label='    Create Locator ',c=self.locAtSel,w=100)
		mc.setParent("..")
		mc.setParent("..")	
		mc.setParent("..")
		
		
		mc.frameLayout(l="Create Curve",fn='boldLabelFont',cll=True,cl=False,w=450)
		mc.columnLayout()
		mc.text("\n    Create a curve along selected locators. Rotations is the \n   number of times to draw the curve over the same locators.\n")
		self.rotFld = mc.intFieldGrp(l='Number of rotations: (1-10)',v1=5)
		mc.rowLayout(nc=2,cw2=(200,100))
		mc.text(" ")
		mc.button(label='    Create Curve ',c=self.createCurve,w=100)
		mc.setParent("..")
		mc.setParent("..")	
		mc.setParent("..")	
		
		
		mc.frameLayout(l="Create Spline IK",fn='boldLabelFont',cll=True,cl=False,w=450)
		mc.columnLayout()
		mc.text("    Create spline IK and attributes on controller based on selected locators.")
		self.cntFld = mc.textFieldButtonGrp(l="Controller:",bl="Load",bc=self.loadCnt,text='chain_cnt')
		self.crvFld = mc.textFieldButtonGrp(l="Curve:",bl="Load",bc=self.loadCrv,text='')
		mc.rowLayout(nc=2,cw2=(200,100))
		mc.text(" ")
		mc.button(label='    Create SplineIK ',c=self.createSplineIK,w=100)
		mc.setParent("..")	
		mc.setParent("..")	
		mc.setParent("..")
	
		mc.setParent("..")
		mc.setParent("..")

		mc.showWindow("msGeoChainWin")

	def createCurve(self,*args):
		"""
		  Create curve on locators
		"""
		prefix = mc.textFieldGrp(self.prefixFld,query=True,text=True)
		locators = mc.ls(sl=True,fl=True)
		rotations = mc.intFieldGrp(self.rotFld,query=True,v1=True)
		
		#Error checking here: Are locators selected?
		if len(locators) == 0:
			print '\nSelection is empty. Please select locators.\n'
			
		#create splineIK curve
		curve = " "
		x = 0
		while x < rotations:
			for each in locators:
				try:        #Try to append to existing curve
					x_loc = mc.getAttr('%s.localPositionX'%each)
					y_loc = mc.getAttr('%s.localPositionY'%each)
					z_loc = mc.getAttr('%s.localPositionZ'%each)
					mc.curve(curve,a=True,p=(x_loc,y_loc,z_loc) )
					
				except:     #If appending fails, means a new curve needs to be created
					x_loc = mc.getAttr('%s.localPositionX'%each)
					y_loc = mc.getAttr('%s.localPositionY'%each)
					z_loc = mc.getAttr('%s.localPositionZ'%each)
					curve = mc.curve( p=(x_loc,y_loc,z_loc), n='%s_ikCurve'%prefix ) 
			x = x + 1

		
	def createSplineIK(self,*args):
		"""
		  Create the rig
		"""
		prefix = mc.textFieldGrp(self.prefixFld,query=True,text=True)
		cntObj = mc.textFieldButtonGrp( self.cntFld,query=True,text=True )
		crv = mc.textFieldButtonGrp( self.crvFld,query=True,text=True )
		locators = mc.ls(sl=True,fl=True)
		
		#Error checking here: Are locators selected?
		if len(locators) == 0:
			print '\nSelection is empty. Please select locators. See "Directions"\n'
			
		#Create joint chain
		mc.select(clear=True)
		
		jntChain = []
		x = 0
		for each in locators:
			if((x%2)==0):
				x_loc = mc.getAttr('%s.localPositionX'%each)
				y_loc = mc.getAttr('%s.localPositionY'%each)
				z_loc = mc.getAttr('%s.localPositionZ'%each)
				jntChain.append( mc.joint(p=(x_loc,y_loc,z_loc),n='%s_%s'%(prefix,x)) )
			x = x + 1
		
		mc.select(clear=True)
			
		#Create splineIK
		temp = len(jntChain)
		startJnt = jntChain[0]
		endJnt = jntChain[temp-1]
		
		handle = mc.ikHandle( sj=startJnt, ee=endJnt, c=crv, sol='ikSplineSolver', n=('%s_ikHandle'%prefix), ccv=False )
		
		#Create attribute to drive the offset/roll/twist
		mc.addAttr(cntObj, ln='%s_offset'%prefix,at='float',k=True)
		mc.addAttr(cntObj, ln='%s_roll'%prefix,at='float',k=True)
		mc.addAttr(cntObj, ln='%s_twist'%prefix,at='float',k=True)
		
		#Connect the attribute
		mc.connectAttr('%s.%s_offset'%(cntObj,prefix), '%s.offset'%handle[0], f=True)
		mc.connectAttr('%s.%s_roll'%(cntObj,prefix), '%s.roll'%handle[0], f=True)
		mc.connectAttr('%s.%s_twist'%(cntObj,prefix), '%s.twist'%handle[0], f=True)	
		
		
	
	def locAtSel(self,*args):
		"""
			Additional tool:
			Create a locator at the pivot of the current selection.
		"""
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
		loc = mc.spaceLocator(p=(avgX,avgY,avgZ))
		mc.select(loc,r=True)
		mel.eval("CenterPivot;")
		
		mc.setAttr('%s.scaleX'%loc[0], .03)
		mc.setAttr('%s.scaleY'%loc[0], .03)
		mc.setAttr('%s.scaleZ'%loc[0], .03)
		
		mc.select(sel,r=True)
		
		mel.eval("changeSelectMode -component;")
	

	def loadCnt(self,*args): 
		cntName = mc.ls(sl=True)
		mc.textFieldGrp(self.cntFld,edit=True,text=cntName[0])
		
	def loadCrv(self,*args): 
		crvName = mc.ls(sl=True)
		mc.textFieldGrp(self.crvFld,edit=True,text=crvName[0])

	def loadGeo(self,*args): 
		geoName = mc.ls(sl=True)
		mc.textFieldGrp(self.geoFld,edit=True,text=geoName[0])
