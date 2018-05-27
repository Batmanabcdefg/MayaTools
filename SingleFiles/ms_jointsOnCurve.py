"""
Copyright (c) 2009 Mauricio Santos
Name: ms_jointsOnCurve.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 10 November 2009
Last Modified: 10 November 2009
License: LGNU
Description: 
	Build joint chain along selected curve

To do: 

	
"""

import maya.cmds as mc

class ms_jointsOnCurve():
	"""
		Build joint chain along selected curve
	"""
	def __init__(self,*args):
		#Get curve
		sel = mc.ls(sl=True,fl=True)
		
		#Get number of spans + degree
		spans = mc.getAttr('%s.spans'%sel[0])
		degree = mc.getAttr('%s.degree'%sel[0])
		numJnts = spans + degree - 1
				
		#build joints along curve
		x = 0
		while(x<=numJnts):
			if x == 1: #Skip second CV
				x = x + 1
				continue
			if x == (numJnts-1): #Skip second to last CV
				x = x + 1
				continue

			pos = mc.getAttr( '%s.cv[%i]'%(sel[0],x) )
			mc.joint( p = (pos[0][0],pos[0][1],pos[0][2]) )
			
			x = x + 1
			