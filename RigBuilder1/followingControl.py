from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *

import os as os
import sys
"""
Copyright (c) 2010, Mauricio Santos
Name: followingControl.py
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Version: 1.0
Date Created:   29 Dec 2010
Last Modified:  28 Dec 2010

Description: 
			Create facial controls. Technique explained by Eric Miller in:
			"Hyper Realistic Creature Creation"
			-Modified: Ken N. helped work out a double transform issue.

To do: 

	-Test with scaling. Does it scale? How? Low priority.
		
	

Procedure:    
		Variables:
        -verts:       Capture selection (Verts should be selected)
        -theCluster:  cluster deformer 
        -rivet:       Rivet created by user
        -rivetLocation:  rivet WS location
        
        Process:
        -User selects two edges
        -Create rivet
        -Delete aim constraint on rivet							
        -Orient constraint rivet to joint
        -Create Cluster(Relative option on, Inherits transformations off)
        -Snap Cluster rotate and scale pivot's to rivetLocation 
        -Create control
        -Snap controls pivots to rivetLocation as well
        -nameCluster: Group Cluster, name it:  name + "Cluster"				
        -Create a group:
        	-Freeze its transformations
        	-Rename it: name + "OR"	nameOR  (OR = Over ride)
        	-Parent nameOR to rivet
        -Zero out control with null node method: cntNull
        -Parent cntNull to nameOR
        -Group rivet and nameCluster together: nameClusterSetup
                        
        -Connect Translates, rotates, scale from control to clusterHandle
        
        -Create MD Node to cancel double transformations: nameOR = cnt.t(xyz) * - 1
        
        -Reorder deformers. Put mesh deformer (skinCluster/cMuscle)on top, cluster just below it.
                
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
	     -With relative set: Expected behavior
	     -Without: No difference observed.
	   -Conclusion:
	     -It really makes no difference.(?)
"""


class followingControl:
	"""
		Create cluster/rivet face controls. Method described by Eric Miller in Maya Techniques - Hyper Real Face Setup class.
	"""	
	def __init__(self):
		if __name__ == 'followingControl': # Top module: 'fileName'.py)
			self.buildGUI()
		
	def buildGUI(self,*args):
		if(window("followCntWin",exists=True)):
			deleteUI("followCntWin",window=True)
			
		with window("followCntWin",title="Follow Control Setup v1.04",rtf=True,menuBar=True) as mainWin:
			with menu(label="Help",helpMenu=True) as m:		
			    menuItem( m, label='Directions',command=self.helpWin )	
			
			with formLayout(w=500) as form:
				with frameLayout(l='Step 1: Set up rivet and control',cl=False,cll=False,w=500):
					with columnLayout():
						 
						self.nameField = textFieldButtonGrp(label="Name:",bl="Load",bc=self.loadName,text="lowLip_01")
						text("\n                                                                Select two edges.\n")
						with rowLayout(nc=2,cw2=(200,110)):
							text(" ")
							button(label="Setup",c=self.createRivet)
							
				with frameLayout(l='Step 2: Finalize Control',cl=False,cll=False,w=500):
					with columnLayout():
						
						self.controlField = textFieldButtonGrp(label="Control:",bl="Load",bc=self.loadControl,text="")
						self.rivetField = textFieldButtonGrp(label="Rivet:",bl="Load",bc=self.loadRivet,text="")
						self.jointField = textFieldButtonGrp(label="Constrain to:",bl="Load",bc=self.loadJoint,text="")
			
						text("\n                  Make sure to select the vertices to influence.       \n",font='boldLabelFont') 
						
						with rowLayout(nc=2,cw2=(200,110)):
							text(" ")
							button(label="Finish",c=self.setupControl)
		
				form.redistribute()
			mainWin.show()	
			
	def createRivet(self,*args):
		"""
		With two edges selected by user, create the rivet and control.
		"""
		cnt = textFieldButtonGrp(self.nameField,q=True,text=True)
		edges = ls(sl=True)
		
		# Ensure name is unique
		if objExists(cnt):
			#@todo - Send to error output
			print 'Name is not unique!'
			return
		
		# Create rivet
		try:
			rivet = mel.eval('rivet')
			#Rename the rivet
			rename(rivet,cnt+'_rivet')
			rivet = cnt+'_rivet'
		except:
			#@todo - Send to error output
			print 'Two edges where not selected!'
			
		# Create controller
		try:
			self.createController(cnt)
		except:
			#@todo - Send to error output
			print 'Failed to create controller: %s'%cnt
			
		# Load part 2 GUI fields with created objects
		textFieldButtonGrp(self.controlField,e=True,text=cnt)
		textFieldButtonGrp(self.rivetField,e=True,text=rivet)
		
		# Snap controller to rivet and zero/orient to world
		temp = pointConstraint(rivet,cnt,mo=False)
		delete(temp)
		makeIdentity(cnt,apply=True,t=True,r=True,s=True,n=True)
		
		# Hide rivet shape visibility
		setAttr('%sShape.visibility'%rivet,0)
		
	def setupControl(self,*args):
		#Load variables
		name = textFieldButtonGrp(self.nameField,q=True,text=True)
		control = textFieldButtonGrp(self.controlField,q=True,text=True)
		rivet = textFieldButtonGrp(self.rivetField,q=True,text=True)
		constObj = textFieldButtonGrp(self.jointField,q=True,text=True)
		
		
		#Load selection
		verts = ls(sl=True,fl=True)
		
		#Create Cluster. Relative off so when the rivet is orient constrained to constraint object,
		#and the constraint object is rotated, cluster will move in a local space, vs world.
		theCluster = cluster(rel=True,n=name+'_clstr')
		
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
		setAttr(control+'.scalePivot',rivetLocation)
		setAttr(control+'.rotatePivot',rivetLocation)

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
#		temp = pointConstraint(control,zeroNode,mo=False)
#		delete(temp)
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
		
		#Get meshDeformer
		history = listHistory(mesh)             
		for each in history:
			#print " History: " + each
			if("skinCluster" in str(each)):
				#Possible match for meshDeformer
				if("Group" not in str(each)):
					meshDeformer = each
			if("cMuscleSystem" in str(each)):
				if("Group" not in str(each)):
					meshDeformer = each
					
		#Reorder deformer nodes
		#Move cluster + meshDeformer to top of deformer stack
		reorderDeformers(clusterHandle,meshDeformer,mesh)
		
		#Move meshDeformer to top of deformer stack
		reorderDeformers(meshDeformer,clusterHandle,mesh)
		
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
		
	def createController(self,name):
		"""
		Creates controller curve at origin.
		"""
		cnt = mel.eval('createNode transform -n "%s";\n'%name+\
			'setAttr ".ove" yes;\n'+\
			'setAttr ".ovc" 15;\n'+\
			'createNode nurbsCurve -n "%sShape" -p "%s";\n'%(name,name)+\
			'setAttr -k off ".v";\n'+\
			'setAttr ".cc" -type "nurbsCurve" \n'+\
			'1 52 0 no 3 \n'+\
			'53 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 \n'+\
			' 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 \n'+\
			'53 \n'+\
			'0 0.074400512458903195 0 \n'+\
			'0 0.068737145450531487 0.028471811309310452 \n'+\
			'0 0.052609123163277663 0.052609123163277663 \n'+\
			'0 0.028471811309310452 0.068737145450531487 \n'+\
			'0 0 0.074400512458903195 \n'+\
			'0 -0.028471811309310452 0.068737145450531487 \n'+\
			'0 -0.052609123163277663 0.052609123163277663 \n'+\
			'0 -0.068737145450531487 0.028471811309310452 \n'+\
			'0 -0.074400512458903195 0 \n'+\
			'0 -0.068737145450531487 -0.028471811309310452 \n'+\
			'0 -0.052609123163277663 -0.052609123163277663 \n'+\
			'0 -0.028471811309310452 -0.068737145450531487 \n'+\
			'0 0 -0.074400512458903195 \n'+\
			'0 0.028471811309310452 -0.068737145450531487 \n'+\
			'0 0.052609123163277663 -0.052609123163277663 \n'+\
			'0 0.068737145450531487 -0.028471811309310452 \n'+\
			'0 0.074400512458903195 0 \n'+\
			'0.028471811309310452 0.068737145450531487 0 \n'+\
			'0.052609123163277663 0.052609123163277663 0 \n'+\
			'0.068737145450531487 0.028471811309310452 0 \n'+\
			'0.074400512458903195 0 0 \n'+\
			'0.068737145450531487 -0.028471811309310452 0 \n'+\
			'0.052609123163277663 -0.052609123163277663 0 \n'+\
			'0.028471811309310452 -0.068737145450531487 0 \n'+\
			'0 -0.074400512458903195 0 \n'+\
			'-0.028471811309310452 -0.068737145450531487 0 \n'+\
			'-0.052609123163277663 -0.052609123163277663 0 \n'+\
			'-0.068737145450531487 -0.028471811309310452 0 \n'+\
			'-0.074400512458903195 0 0 \n'+\
			'-0.068737145450531487 0.028471811309310452 0 \n'+\
			'-0.052609123163277663 0.052609123163277663 0 \n'+\
			'-0.028471811309310452 0.068737145450531487 0 \n'+\
			'0 0.074400512458903195 0 \n'+\
			'0 0.068737145450531487 -0.028471811309310452 \n'+\
			'0 0.052609123163277663 -0.052609123163277663 \n'+\
			'0 0.028471811309310452 -0.068737145450531487 \n'+\
			'0 0 -0.074400512458903195 \n'+\
			'-0.028471811309310452 0 -0.068737145450531487 \n'+\
			'-0.052609123163277663 0 -0.052609123163277663 \n'+\
			'-0.068737145450531487 0 -0.028471811309310452 \n'+\
			'-0.074400512458903195 0 0 \n'+\
			'-0.068737145450531487 0 0.028471811309310452 \n'+\
			'-0.052609123163277663 0 0.052609123163277663 \n'+\
			'-0.028471811309310452 0 0.068737145450531487 \n'+\
			'0 0 0.074400512458903195 \n'+\
			'0.028471811309310452 0 0.068737145450531487 \n'+\
			'0.052609123163277663 0 0.052609123163277663 \n'+\
			'0.068737145450531487 0 0.028471811309310452 \n'+\
			'0.074400512458903195 0 0 \n'+\
			'0.068737145450531487 0 -0.028471811309310452 \n'+\
			'0.052609123163277663 0 -0.052609123163277663 \n'+\
			'0.028471811309310452 0 -0.068737145450531487 \n'+\
			'0 0 -0.074400512458903195 \n'+\
			';')
		
	def helpWin(self,*args):
		"""
		window to show when "directions" pressed in help menu.
		"""
		if(window('msfcHelpWin',exists=True)):
			deleteUI('msfcHelpWin',window=True)
			
		with window('msfcHelpWin',title="Following Control Help",rtf=True) as helpWin:
			with formLayout():
				with columnLayout():
					text("   What it does:\n")
					text("   ---------------\n")
					text("      Creates a cluster based control that deforms the\n")
					text("      mesh and follows other deformations on the mesh,\n")	
					text("      like blendShapes.\n")	
					text("   Pre-conditions:\n")
					text("   ---------------\n")
					text("      pymel should be available.\n")
					text("      rivet.mel should be available.\n")
					text("      Polygonal mesh should be skinned (skinCluster/cMuscleDeformer).\n")
					text("   Definitions:\n")
					text("   ------------\n")
					text("      Prefix:  All nodes will have this prefix.")
					text("      Control: Controller Curve/Object.")
					text("      Rivet:   Rivet created using rivet script.")
					text("      Constraint to object: Joint / Node to orient constrain control rig to.")
					text("\n")
					text("  Directions:\n")
					text("  -----------\n")
					text("  -Setup rivet and control:\n")
					text("		Select two edges on the mesh, Click \"Setup\".\n")
					text("  -Finalize control setup:\n")
					text("		Load constrain to object into field, (Jaw joint for a lower lip control)\n")
					text("		select vertices to be influenced by the controller, then click \"Finish\".\n")
					text("\n  Creates/Returns: prefix_cnt_grp\n")  
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



