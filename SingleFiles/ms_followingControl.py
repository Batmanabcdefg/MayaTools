from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *

import os as os
import sys


"""
Copyright (c) 2010, Mauricio Santos
Name: FollowingControl.py
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Version: 1.04
Description: 
			Create facial controls. Technique explained by Eric Miller in:
			"Hyper Realistic Creature Creation"
			-Modified: Ken N. helped work out a double transform issue.

To do: 
	-Test with scaling. Does it scale? How?
		
History:
	2010-???-?? : Fixed double transforms on cluster controller ---> Thankx Ken N!
	2010-Sep-30 : Refactored using PyMEL
				  Working on: Add frameCallbacks() to resize windows as user opens/closes frame
	2010-Oct-01 : Finished refactoring with PyMEL 
	

Procedure:    
		Variables:
        -verts:       Capture selection (Verts should be selected)
        -theCluster:  cluster deformer
        -rivet:       Rivet created by user
        -rivetLocation:  rivet WS location
        
        Process:
        -Delete aim constraint on rivet							
        -Orient constraint rivet to joint
        -Create Cluster(Relative option on, Inherits transformations off)
        -Snap Cluster rotate and scale pivot's to rivetLocation 
        -Snap controls pivots to rivetLocation as well
        -nameCluster: Group Cluster, name it:  name + "Cluster"				
        -Create a group:
        	-Freeze its transformations
        	-Rename it: name + "OR"	nameOR  (OR = Over ride)
        	-Parent nameOR to rivet
        -Zero out control with null node method	cntNull
        -Parent cntNull to nameOR
        -Group rivet and nameCluster together: nameClusterSetup
                        
        -Connect Translates, rotates, scale from control to clusterHandle
        
        -Create MD Node to cancel double transformations: nameOR = cnt.t(xyz) * - 1
        
        -Reorder deformers. Put skin cluster on top, cluster just below it.
                
        -Hide cluster
        
        Result: prefix_followCnt_grp <----- Can be placed anywhere in hierarchy. Scaling not tested yet.
"""
"""
Development notes:
	- Ran into issue with double transformations. Was stuck. Found two solutions:
	   -Negate one of the transformations by using a MD node set to -1
	   -Disable "Inherits transforms".
	   
	- Why make the cluster relative?
	   -Observations:
	     -With relative set: Expected behaviour
	     -Without: No difference observed.
	   -Conclusion:
	     -It really makes no difference.
"""


class ms_followingControl:
	"""
		Create cluster/rivet face controls. Method described by Eric Miller in Maya Techniques - Hyper Real Face Setup class.
	"""	
	def __init__(self):
		if __name__ == 'ms_followingControl': # Top module: 'fileName'.py)
			self.buildGUI()
		
	def buildGUI(self,*args):
		if(window("followCntWin",exists=True)):
			deleteUI("followCntWin",window=True)
			
		with window("followCntWin",title="Follow Control Setup v1.04",rtf=True,menuBar=True) as mainWin:
			with menu(label="Help",helpMenu=True) as m:		
			    menuItem( m, label='Directions',command=self.helpWin )
			
			with formLayout(w=500,h=200) as form:
				self.nameField = textFieldButtonGrp(label="Prefix:",bl="Load",bc=self.loadName,text="test")
				self.controlField = textFieldButtonGrp(label="Control:",bl="Load",bc=self.loadControl,text="cntl_01")
				self.rivetField = textFieldButtonGrp(label="Rivet:",bl="Load",bc=self.loadRivet,text="rivet1")
				self.jointField = textFieldButtonGrp(label="Constrain to:",bl="Load",bc=self.loadJoint,text="main_cnt")
	
				text("\n            Make sure to select the vertices to influence.\n") 
				
				with rowLayout(nc=2,cw2=(200,110)):
					text(" ")
					button(label="Continue",c=self.createControl)
		
				form.redistribute()
			mainWin.show()
			
		return 'followCntWin'	
		
	def createControl(self,*args):
		#Load variables
		name = textFieldButtonGrp(self.nameField,q=True,text=True)
		control = textFieldButtonGrp(self.controlField,q=True,text=True)
		rivet = textFieldButtonGrp(self.rivetField,q=True,text=True)
		constObj = textFieldButtonGrp(self.jointField,q=True,text=True)
		
		
		#Load selection
		verts = ls(sl=True,fl=True)
		
		#Create Cluster. Relative off so when the rivet is orient constrained to constraint object,
		#and the constraint object is rotated, cluster will move in a local space, vs world.
		theCluster = cluster(rel=True)
		
		#Get the clusterHandle, object type: Transform
		clusterHandle = theCluster[1]
		
		#Get the transform name
		clusterName = theCluster[0]	

		#Delete Rivet's aim constraint because it causes flipping if the rivets lofted nurbs plane flips.
		#Add parent constraint to object.(constObj)
		try:
			temp = listConnections(rivet)
			delete(temp[1])
		except:
			# No constraint to delete on rivet
			pass
		
		#Rivet WS location
		rivetLocation = xform(rivet,q=True,ws=True,t=True)

		#Snap Cluster pivots to rivetLocation
		setAttr(clusterHandle+'.scalePivot',rivetLocation)
		setAttr(clusterHandle+'.rotatePivot',rivetLocation)
		
		#Snap Controls pivots to rivetLocation
		setAttr(constObj+'.scalePivot',rivetLocation)
		setAttr(constObj+'.rotatePivot',rivetLocation)

		#Group Cluster
		clusterGrp = group(clusterHandle)
		clusterGrp = rename(clusterGrp, name + 'Cluster_' + clusterHandle)
		
		#Create over ride group
		or_grp = group(em=True,name=name+"OR1") 
		or2_grp = group(em=True,name=name+"OR2") 
		
		#Parent override group to rivet
		parent(or_grp,or2_grp)  
		parent(or2_grp,rivet)   
		
		#Freeze transforms on override group
		makeIdentity(or_grp,apply=True,t=True,r=True,s=True,n=True)
		
		#Zero Control
		zeroNode = group(em=True,n=name + "nullGrp")

		pos = xform( control, q=1, ws=True, t=1)
		xform( zeroNode, ws=True, t=[pos[0], pos[1], pos[2]]) 

		rot = xform( control, q=1, ws=True, ro=1)
		xform( zeroNode, ws=True, ro=[rot[0], rot[1], rot[2]]) 
		
		scale = xform( control, q=1, r=1, s=1)
		xform( zeroNode, ws=True, s=[scale[0], scale[1], scale[2]])		
		
		#Snap zeroNode pivot to control
		controlLocation = xform(control,q=True,ws=True,rp=True)
		setAttr(zeroNode+'.scalePivot',controlLocation)
		setAttr(zeroNode+'.rotatePivot',controlLocation)
				
		#parent control to OverRide group
		parent(control, zeroNode, a=True)		
		parent(zeroNode,or_grp)
		
		#Connect control t,r,s to cluster, then hide the cluster and rivet group 
		connectAttr(control + ".translate", clusterHandle + ".translate")
		connectAttr(control + ".rotate", clusterHandle + ".rotate")
		connectAttr(control + ".scale", clusterHandle + ".scale")		
		
		#Create utility node and negate double transform
		#by reversing the transformation of or_grp <---- Cause of double transforms
		mdNode = createNode("multiplyDivide")
		nodeName = name + "_MD"
		rename(mdNode,nodeName)
		mdNode = nodeName
		
		#Unparent control
		parent(zeroNode,w=True)
		
		#Set up the MD node
		setAttr( "%s.input2X"%mdNode, -1)
		setAttr( "%s.input2Y"%mdNode, -1)
		setAttr( "%s.input2Z"%mdNode, -1)
		
		#Connect the nodes
		# control ---> mdNode
		connectAttr("%s.translateX"%control,"%s.input1X"%mdNode,f=True)
		connectAttr("%s.translateY"%control,"%s.input1Y"%mdNode,f=True)
		connectAttr("%s.translateZ"%control,"%s.input1Z"%mdNode,f=True)
		
		#mdNode ---> or_grp
		connectAttr("%s.outputX"%mdNode,"%s.translateX"%or_grp,f=True)
		connectAttr("%s.outputY"%mdNode,"%s.translateY"%or_grp,f=True)
		connectAttr("%s.outputZ"%mdNode,"%s.translateZ"%or_grp,f=True)
		
		#Reparent control
		parent(zeroNode,or_grp)

		#Get mesh name
		temp = verts[0].split('.') # ex. "meshName.vtx[35]"
		mesh = temp[0]
		
		#Get skinCluster
		history = listHistory(mesh)             
		for each in history:
			#print " History: " + each
			if("skinCluster" in str(each)):
				#print " Possible match for skinCluster: " + each
				if("Group" not in str(each)):
					#print ' skinCluster: ' + each
					skinCluster = each
					
		#Reorder deformer nodes
		#Move cluster + skinCluster to top of deformer stack
		reorderDeformers(clusterHandle,skinCluster,mesh)
		
		#Move skinCluster to top of deformer stack
		reorderDeformers(skinCluster,clusterHandle,mesh)
		
		#Create final group
		topGrp = group(em=True,name=name+"_followCnt_grp")
		parent(clusterGrp,rivet,topGrp)
		
		#Orient constrain rivet to constrain object
		orientConstraint(constObj,rivet,mo=True)
		
		#Hide cluster grp
		setAttr(clusterGrp + ".visibility",0) 
		
		#Hide the rivet
		rivetShape = listRelatives(rivet,shapes=True)
		setAttr(rivetShape[0] + ".visibility",0)
		
		#Clear selection
		select(clear=True)
		
	def helpWin(self,*args):
		"""
		window to show when "directions" pressed in help menu.
		"""
		if(window('msfcHelpWin',exists=True)):
			deleteUI('msfcHelpWin',window=True)
			
		with window('msfcHelpWin',title="Following Control Help",rtf=True) as helpWin:
			with formLayout():
				with columnLayout():		
					text("   Pre-conditions:\n")
					text("   ---------------\n")
					text("      pymel should be available.\n")
					text("      rivet.mel should be available.\n")
					text("      Polygonal mesh should be skinned (skinCluster).\n")
					text("      Controller and rivet should be setup.\n")
					text("      Control objects need to be zero'd, oriented to world.\n\n")
					text("   Definitions:\n")
					text("   ------------\n")
					text("      Prefix:  All nodes will have this prefix.")
					text("      Control: Controller Curve/Object.")
					text("      Rivet:   Rivet created using rivet script.")
					text("      Constraint to object: Joint / Node to constrain control rig to.")
					text("\n")
					text("  Directions:\n")
					text("  -----------\n")
					text("  -Load all fields")
					text("  -Select vertices to be driven by cluster setup. Click \"Continue\".\n\n")
					text("  Creates/Returns: prefix_cnt_grp")  
					text(" ")
			helpWin.show()
		
	def loadName(self,*args):
		sel = ls(sl=True)
		textFieldButtonGrp(self.nameField,e=True,text=sel[0])
		
	def loadControl(self,*args):
		sel = ls(sl=True)
		textFieldButtonGrp(self.controlField,e=True,text=sel[0])
		
	def loadRivet(self,*args):
		sel = ls(sl=True)
		textFieldButtonGrp(self.rivetField,e=True,text=sel[0])
		
	def loadJoint(self,*args):
		sel = ls(sl=True)
		textFieldButtonGrp(self.jointField,e=True,text=sel[0])		



