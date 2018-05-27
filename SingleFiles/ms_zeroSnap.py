"""
Copyright (c) 2009 Mauricio Santos
Name: ms_zeroSnap.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 28 August 2008
Last Modified: 9 June 2009
License: LGNU
Description: Zero's and snaps given object by creating null node above it. Retains orientation,
        but channels get zero'd.

To do: 

Additional Notes:
This code is based on a script I got during Tom Meade's rigging class at AAU.

"""

import maya.cmds as mc

class ms_zeroSnap():
	   #Creates a window with two buttons: "Zero" and "Snap"
	   #	Zero: Select object, press button. Creates null node, snaps to object, parents object to itself, flushing values
	   #			from objects channels into the zero (null) node, the new parent of object.
	   #	Snap: Select A and B. Press button .
	   #			Queries object B's location, rotation and sets object A to those values
	

	
	def __init__(self,*args):
		if(mc.window("zeroSnapWin",exists=True)):
			mc.deleteUI("zeroSnapWin",window=True)
		
		mc.window("zeroSnapWin",title="Zero, Snap v 1.0", rtf=True)
		mc.columnLayout()

		mc.button(l="Snap", c=self.msh_snapping,w=100)
		mc.button(l="Zero", c=self.msh_zeroing,w=100)

		mc.showWindow("zeroSnapWin")		


	def msh_snapping(self,*args):
		selObj = mc.ls(sl=True)
	
		pos = mc.xform( selObj[1], q=1, ws=True, t=1)
		mc.xform( selObj[0], ws=True, t=[pos[0], pos[1], pos[2]]) 
	
		rot = mc.xform( selObj[1], q=1, ws=True, ro=1)
		mc.xform( selObj[0], ws=True, ro=[rot[0], rot[1], rot[2]]) 
			
	def msh_zeroing(self,*args):
		selObj = mc.ls(sl=True)
		name = '%s_buffer'%selObj[0]
		zeroNode = mc.group(em=True,n=name)

		pos = mc.xform( selObj, q=1, ws=True, t=1)
		mc.xform( zeroNode, ws=True, t=[pos[0], pos[1], pos[2]]) 

		rot = mc.xform( selObj, q=1, ws=True, ro=1)
		mc.xform( zeroNode, ws=True, ro=[rot[0], rot[1], rot[2]]) 
		
		scale = mc.xform( selObj, q=1, r=True, s=1)
		mc.xform( zeroNode, ws=True, s=[scale[0], scale[1], scale[2]])

		mc.parent(selObj, zeroNode, a=True)



