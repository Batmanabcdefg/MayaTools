"""
Copyright (c) 2009 Mauricio Santos
Name: ms_legRig.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 26 June 2009
Last Modified: 9 Dec 2009
License: LGNU
Description: 
	Given required input, create a stretchy FK/IK leg with no-flip knee option

To do: 
	Verify stretchy IK works with new changes.
	
Additional Notes: 
	Streamlined it. Abandoned matching and foot rig code. Better as separate scripts (Matching / Foot_Rig).
	
Requires:
	ms_makeStretchy.py
	
"""


import maya.mel as mel
import maya.cmds as mc
import math
import ms_makeStretchy as mks

class ms_legRig():
	"""
		Create FK/IK leg with no-flip knee.
	"""
	
	def __init__(self,*args):
		if(mc.window("msLegRigWin",exists=True)):
			mc.deleteUI("msLegRigWin",window=True)
		
		mc.window("msLegRigWin",title="Leg Rig v1.0",rtf=1)
		mc.columnLayout()
		mc.frameLayout(label='Directions',fn='boldLabelFont',w=500,cl=True,cll=True)
		mc.columnLayout()
		mc.text(' Joint Hierarchy:')
		mc.text('            leg_top')
		mc.text('               |_ knee1')
		mc.text('                     |_ knee2 (Optional)')
		mc.text('                           |_ ankle')
		mc.text(' ')
		mc.text('   Prerequisites/Assumptions:')
		mc.text('    - Initial joints are placed and oriented')
		mc.text("    - Leg is not in a hierarchy. It's parent is world")
		mc.text(' ')
		mc.text('   Return:')
		mc.text('    -StateNode is created to switch between FK/IK')
		mc.text('    -Matching script is output to script editor panel in Maya.')
		mc.text('     Copy and paste this for ik/fk matching button. (Needs work v1.0)')
		mc.text('    -You must also set Stretchy SDK curves to linear and infinite')
		mc.setParent('..')
		mc.setParent('..')
		
		self.prefixFld = mc.textFieldGrp(l='Prefix:',text='r_leg_')
		self.jointFld = mc.textFieldButtonGrp(l="Select leg_top joint:",bl="Load",bc=self.loadText,text='R_up_leg')
		self.kneesFld = mc.radioButtonGrp(l="How many knee joints?",nrb=2,labelArray2=('1','2'),sl=1 )
		self.stretchyFld = mc.radioButtonGrp(l="Stretchy?",nrb=2,labelArray2=('Yes','No'),sl=2 )
		self.aimFld = mc.radioButtonGrp(l="Chain Aim Axis:",nrb=3,labelArray3=('X','Y','Z'),sl=1 )
		mc.text('   Controls:  ',fn='boldLabelFont')
		self.ikCntFld = mc.textFieldButtonGrp(l="IK Foot Control:",bl="Load",bc=self.loadIKCnt)
		self.nrFld = mc.radioButtonGrp(l="FK Controllers Normal Axis:",nrb=3,labelArray3=('X','Y','Z'),sl=1 )
		self.rFld = mc.floatFieldGrp(l="FK Controls radius:",numberOfFields=1,v1=.3)
		self.buildFld = mc.radioButtonGrp(l='Build Type:',nrb=2,labelArray2=('Positive','Negative'),sl=2)
		
		mc.rowLayout(nc=3)
		mc.text(" ")
		mc.text(' ')
		mc.button(label="      Build Rig",c=self.createLeg,w=100)
		mc.setParent("..")

		mc.showWindow("msLegRigWin")

	def createLeg(self,*args):
		"""
		  Create the rig
		"""
		prefix = mc.textFieldGrp(self.prefixFld,query=True,text=True)
		fkRootJnt = mc.textFieldButtonGrp( self.jointFld,query=True,text=True )
		stretchy = mc.radioButtonGrp( self.stretchyFld,query=True,sl=True )
		kneeNum = mc.radioButtonGrp( self.kneesFld,query=True,sl=True )
		aim = mc.radioButtonGrp( self.aimFld,query=True,sl=True )
		foot_cnt = mc.textFieldGrp(self.ikCntFld,query=True,text=True)
		normal = mc.radioButtonGrp( self.nrFld,query=True,sl=True )
		radius = mc.floatFieldGrp(self.rFld,query=True,value1=True)
		build = mc.radioButtonGrp( self.buildFld,query=True,sl=True )
		
		if aim == 1:
			aim = 'X'
		if aim == 2:
			aim = 'Y'
		if aim == 3:
			aim = 'Z'
			
		if normal == 1:
			normal = (1,0,0)
		if normal == 2:
			normal = (0,1,0)
		if normal == 3:
			normal = (0,0,1)
			
		if build == 1:
			build = 'positive'
		if build == 2:
			build = 'negative'
		
		
		#	
		#--- Creating duplicate joint chains
		#
		# First, we duplicate and store the original joint chain 
		# for building the IK leg later on down the line.
		#
		ikChain = []
		temp = mc.duplicate(fkRootJnt,rc=True)
		for each in temp:
			name = '%sik_%s' % (prefix,each)
			mc.rename  (each, name)
			ikChain.append(name)
		
		#
		# Now, the bind leg joint chain
		#
		bindChain = []
		temp = mc.duplicate(fkRootJnt,rc=True)
		for each in temp:
			name = '%sbind_%s' % (prefix,each)
			mc.rename  (each, name)
			bindChain.append(name)
		
		#
		# Now, the FK leg joint chain
		#
		fkChain = []
		mc.select(fkRootJnt,hi=True)
		temp = mc.ls(sl=True,fl=True)
		for each in temp:
			name = '%sfk_%s' % (prefix,each)
			mc.rename  (each, name)
			fkChain.append(name)
			
		#
		# Creating two separate chains for: no flip-knee and pole vector
		#
		noFlipChain= []
		temp = mc.duplicate(ikChain[0],rc=True)
		mc.select(temp[0],hi=True)
		temp = mc.ls(sl=True,fl=True)
		for each in temp: #Search and replace: _ik_ with _noFlip_
			if 'effector' in each:
				mc.delete(each)
				continue
			newName = each.replace('_ik_','_noFlip_')
			mc.rename(each, newName) 
			noFlipChain.append( newName )
		
		#		
		# PV chain
		#
		pvChain= []
		temp = mc.duplicate(ikChain[0],rc=True)
		mc.select(temp[0],hi=True)
		temp = mc.ls(sl=True,fl=True)
		for each in temp: #Search and replace: _ik_ with _pv_
			if 'effector' in each:
				mc.delete(each)
				continue
			newName = each.replace('_ik_','_pv_')
			mc.rename(each, newName) 
			pvChain.append( newName )
			
		
		#
		#--- IK Control
		#
		#Hiding atts
		mc.setAttr(foot_cnt+'.visibility',channelBox=False)
		mc.setAttr(foot_cnt+'.scaleX',channelBox=False)
		mc.setAttr(foot_cnt+'.scaleY',channelBox=False)
		mc.setAttr(foot_cnt+'.scaleZ',channelBox=False)
		
		#Knee controls
		mc.addAttr(foot_cnt,ln='knee_controls',at='float',k=True)
		mc.setAttr(foot_cnt+'.knee_controls',lock=True)
		mc.addAttr(foot_cnt, ln='Type',at='enum',enumName='Pv:NoFlip',k=True)
		mc.setAttr(foot_cnt + '.Type',1)
		
				
		# 
		# Create state node for this leg rig and add attribute to it.
		#
		self.stateNode = mc.createNode('transform',n=('%s_stateNode'%prefix ) )
		mc.addAttr(self.stateNode, ln='FK_IK',min=0,max=1,at='float',k=True)
		
		#Hide all unneeded atts
		mc.setAttr(self.stateNode + '.translateX',keyable=False,channelBox=False)
		mc.setAttr(self.stateNode + '.translateY',keyable=False,channelBox=False)
		mc.setAttr(self.stateNode + '.translateZ',keyable=False,channelBox=False)
		mc.setAttr(self.stateNode + '.rotateX',keyable=False,channelBox=False)
		mc.setAttr(self.stateNode + '.rotateY',keyable=False,channelBox=False)
		mc.setAttr(self.stateNode + '.rotateZ',keyable=False,channelBox=False)
		mc.setAttr(self.stateNode + '.scaleX',keyable=False,channelBox=False)
		mc.setAttr(self.stateNode + '.scaleY',keyable=False,channelBox=False)
		mc.setAttr(self.stateNode + '.scaleZ',keyable=False,channelBox=False)
		mc.setAttr(self.stateNode + '.visibility',keyable=False,channelBox=False)
		
		#
		#--- Connect IK/FK to Bind via 'blendColors' nodes 
		#
		
		#
		# leg_top blendColors node creation/connections
		# Connecting rotates, translates not needed
		
		#leg_top blendColors creation/linking
		temp = mc.createNode( 'blendColors' )
		legTop_node1 = '%s_topLegRotate'%prefix
		mc.rename( temp, legTop_node1 )
		
		#legTop_node1 attributes to connect
		nodeColor1 = (legTop_node1 + ".color1")
		nodeColor2 = (legTop_node1 + ".color2")
		nodeOutput = (legTop_node1 + ".output")
		
		src1 = '%s.rotate'%fkChain[0]
		src2 = '%s.rotate'%ikChain[0]
		tgt = '%s.rotate'%bindChain[0]
		
		mc.connectAttr(src2, nodeColor1) 
		mc.connectAttr(src1, nodeColor2)
		mc.connectAttr(nodeOutput, tgt)
		
		#Connect each node to the self.stateNode so it's all driven by 1 att
		mc.connectAttr( '%s.FK_IK'%self.stateNode, '%s.blender'%legTop_node1 )
		
		#
		# knee1 blendColors nodes creation/connections
		# Connecting rotates and translates
		
		#knee1 blendColors creation/linking
		temp = mc.createNode( 'blendColors' )
		knee1_node1 = '%s_knee1Rotate'%prefix
		mc.rename( temp, knee1_node1 )
		
		temp = mc.createNode( 'blendColors' )
		knee1_node2 = '%s_knee1Translate'%prefix
		mc.rename( temp, knee1_node2 )
		
		#legTop_node1 attributes to connect
		nodeColor1 = (knee1_node1 + ".color1")
		nodeColor2 = (knee1_node1 + ".color2")
		nodeOutput = (knee1_node1 + ".output")
		
		src1 = '%s.rotate'%fkChain[1]
		src2 = '%s.rotate'%ikChain[1]
		tgt = '%s.rotate'%bindChain[1]
		
		mc.connectAttr(src2, nodeColor1) 
		mc.connectAttr(src1, nodeColor2)
		mc.connectAttr(nodeOutput, tgt)
	
		#legTop_node2 attributes to connect
		nodeColor1 = (knee1_node2 + ".color1")
		nodeColor2 = (knee1_node2 + ".color2")
		nodeOutput = (knee1_node2 + ".output")
		
		src1 = '%s.translate'%fkChain[1]
		src2 = '%s.translate'%ikChain[1]
		tgt = '%s.translate'%bindChain[1]
		
		mc.connectAttr(src2, nodeColor1) 
		mc.connectAttr(src1, nodeColor2)
		mc.connectAttr(nodeOutput, tgt)
		
		#Connect each node to the self.stateNode so it's all driven by 1 att
		mc.connectAttr( '%s.FK_IK'%self.stateNode, '%s.blender'%knee1_node1 )
		mc.connectAttr( '%s.FK_IK'%self.stateNode, '%s.blender'%knee1_node2 )
		
		if kneeNum == 2:
			#
			# knee2 blendColors nodes creation/connections
			# Connecting rotates and translates
			
			#knee2 blendColors creation/linking
			temp = mc.createNode( 'blendColors' )
			knee2_node1 = '%s_knee2Rotate'%prefix
			mc.rename( temp, knee2_node1 )
			
			temp = mc.createNode( 'blendColors' )
			knee2_node2 = '%s_knee2Translate'%prefix
			mc.rename( temp, knee2_node2 )
			
			#legTop_node1 attributes to connect
			nodeColor1 = (knee2_node1 + ".color1")
			nodeColor2 = (knee2_node1 + ".color2")
			nodeOutput = (knee2_node1 + ".output")
			
			src1 = '%s.rotate'%fkChain[2]
			src2 = '%s.rotate'%ikChain[2]
			tgt = '%s.rotate'%bindChain[2]
			
			mc.connectAttr(src2, nodeColor1) 
			mc.connectAttr(src1, nodeColor2)
			mc.connectAttr(nodeOutput, tgt)
		
			#legTop_node2 attributes to connect
			nodeColor1 = (knee2_node2 + ".color1")
			nodeColor2 = (knee2_node2 + ".color2")
			nodeOutput = (knee2_node2 + ".output")
			
			src1 = '%s.translate'%fkChain[2]
			src2 = '%s.translate'%ikChain[2]
			tgt = '%s.translate'%bindChain[2]
			
			mc.connectAttr(src2, nodeColor1) 
			mc.connectAttr(src1, nodeColor2)
			mc.connectAttr(nodeOutput, tgt)
			
			#Connect each node to the self.stateNode so it's all driven by 1 att
			mc.connectAttr( '%s.FK_IK'%self.stateNode, '%s.blender'%knee2_node1 )
			mc.connectAttr( '%s.FK_IK'%self.stateNode, '%s.blender'%knee2_node2 )
			
		#
		# ankle blendColors nodes creation/connections
		# 
		
		#ankle blendColors creation/linking
		temp = mc.createNode( 'blendColors' )
		ankle_node1 = '%s_ankleRotate'%prefix
		mc.rename( temp, ankle_node1 )
		
		temp = mc.createNode( 'blendColors' )
		ankle_node2 = '%s_ankleTranslate'%prefix
		mc.rename( temp, ankle_node2 )
		
		#legTop_node1 attributes to connect
		nodeColor1 = (ankle_node1 + ".color1")
		nodeColor2 = (ankle_node1 + ".color2")
		nodeOutput = (ankle_node1 + ".output")
		
		if kneeNum == 1: #One knee
			src1 = '%s.rotate'%fkChain[2]
			src2 = '%s.rotate'%ikChain[2]
			tgt = '%s.rotate'%bindChain[2]
			
		if kneeNum == 2: #Two knees
			src1 = '%s.rotate'%fkChain[3]
			src2 = '%s.rotate'%ikChain[3]
			tgt = '%s.rotate'%bindChain[3]
		
		mc.connectAttr(src2, nodeColor1) 
		mc.connectAttr(src1, nodeColor2)
		mc.connectAttr(nodeOutput, tgt)
	
		#legTop_node2 attributes to connect
		nodeColor1 = (ankle_node2 + ".color1")
		nodeColor2 = (ankle_node2 + ".color2")
		nodeOutput = (ankle_node2 + ".output")
		
		if kneeNum == 1: #One knee
			src1 = '%s.translate'%fkChain[2]
			src2 = '%s.translate'%ikChain[2]
			tgt = '%s.translate'%bindChain[2]
			
		if kneeNum == 2: #Two knees
			src1 = '%s.translate'%fkChain[3]
			src2 = '%s.translate'%ikChain[3]
			tgt = '%s.translate'%bindChain[3]
		
		mc.connectAttr(src2, nodeColor1) 
		mc.connectAttr(src1, nodeColor2)
		mc.connectAttr(nodeOutput, tgt)
		
		#Connect each node to the self.stateNode so it's all driven by 1 att
		mc.connectAttr( '%s.FK_IK'%self.stateNode, '%s.blender'%ankle_node1 )
		mc.connectAttr( '%s.FK_IK'%self.stateNode, '%s.blender'%ankle_node2 )
			
		#
		#--- Create FK controllers
		# 

		#leg_top
		temp = mc.circle(nr=normal,r=radius)
		mc.parent(temp,fkChain[0]) #Parent transform under fk joint
		mc.move(0,0,0, temp ) #Zero it so it snaps to FK position/orientation
		shape = mc.pickWalk( temp,direction='down') #Get shape node for the parent command
		mc.parent(shape,fkChain[0],s=True,r=True) #Parent shape to joints transform
		mc.delete(temp)   #Delete empty transform
		
		if kneeNum == 1:
			#knee1
			temp = mc.circle(nr=normal,r=radius)
			mc.parent(temp,fkChain[1]) #Parent transform under fk joint
			mc.move(0,0,0, temp ) #Zero it so it snaps to FK position/orientation
			shape = mc.pickWalk( temp,direction='down') #Get shape node for the parent command
			mc.parent(shape,fkChain[1],s=True,r=True) #Parent shape to joints transform
			mc.delete(temp)   #Delete empty transform
			
			#ankle
			temp = mc.circle(nr=normal,r=radius)
			mc.parent(temp,fkChain[2]) #Parent transform under fk joint
			mc.move(0,0,0, temp ) #Zero it so it snaps to FK position/orientation
			shape = mc.pickWalk( temp,direction='down') #Get shape node for the parent command
			mc.parent(shape,fkChain[2],s=True,r=True) #Parent shape to joints transform
			mc.delete(temp)   #Delete empty transform
			
		if kneeNum == 2:
			#knee1
			temp = mc.circle(nr=normal,r=radius)
			mc.parent(temp,fkChain[1]) #Parent transform under fk joint
			mc.move(0,0,0, temp ) #Zero it so it snaps to FK position/orientation
			shape = mc.pickWalk( temp,direction='down') #Get shape node for the parent command
			mc.parent(shape,fkChain[1],s=True,r=True) #Parent shape to joints transform
			mc.delete(temp)   #Delete empty transform
			
			#knee2: Connect second knee rotations to first knee. this way, we only need one control.
			mc.connectAttr('%s.rotate'%fkChain[2],'%s.rotate'%fkChain[1],f=True)
			
			#ankle
			temp = mc.circle(nr=normal,r=radius)
			mc.parent(temp,fkChain[3]) #Parent transform under fk joint
			mc.move(0,0,0, temp ) #Zero it so it snaps to FK position/orientation
			shape = mc.pickWalk( temp,direction='down') #Get shape node for the parent command
			mc.parent(shape,fkChain[3],s=True,r=True) #Parent shape to joints transform
			mc.delete(temp)   #Delete empty transform
			
			
		#
		# FK Length attributes setup/ Done using the translates of the child to avoid skewing that
		# occurs with scaling in a non-uniform manner, i.e. (1,2,1) vs. (1,1,1)
		#
		mc.addAttr(fkChain[0],ln='length',min=0,dv=1,max=5, k=True)
		mc.addAttr(fkChain[1],ln='length',min=0,dv=1,max=5, k=True)
		
		#Get current translate%s % aim value to set the max SDK as 5 times the default length
		val1 = mc.getAttr('%s.translate%s' %(fkChain[1],aim) )
		if kneeNum == 2:
			val2 = mc.getAttr('%s.translate%s' %(fkChain[3],aim) )
		else:
			val2 = mc.getAttr('%s.translate%s' %(fkChain[2],aim) )
		
		#SDK to connect them
		mc.setDrivenKeyframe( fkChain[1],cd='%s.length'%fkChain[0],at='translate%s'%aim,dv=1) #Set default with current value in .tx
		mc.setDrivenKeyframe( fkChain[1],cd='%s.length'%fkChain[0],at='translate%s'%aim,dv=0,v=0)         #Set min
		mc.setDrivenKeyframe( fkChain[1],cd='%s.length'%fkChain[0],at='translate%s'%aim,dv=5,v=(val1 * 5) ) #Set max
		
		if kneeNum == 1:					  
			mc.setDrivenKeyframe( fkChain[2],cd='%s.length'%fkChain[1],at='translate%s'%aim,dv=1) #Set default with current value in .tx
			mc.setDrivenKeyframe( fkChain[2],cd='%s.length'%fkChain[1],at='translate%s'%aim,dv=0,v=0)         #Set min
			mc.setDrivenKeyframe( fkChain[2],cd='%s.length'%fkChain[1],at='translate%s'%aim,dv=5,v=(val2 * 5) )#Set max
								  
		if kneeNum == 2:					  
			mc.setDrivenKeyframe( fkChain[3],cd='%s.length'%fkChain[1],at='translate%s'%aim,dv=1) #Set default with current value in .tx
			mc.setDrivenKeyframe( fkChain[3],cd='%s.length'%fkChain[1],at='translate%s'%aim,dv=0,v=0)         #Set min
			mc.setDrivenKeyframe( fkChain[3],cd='%s.length'%fkChain[1],at='translate%s'%aim,dv=5,v=(val2 * 5) )#Set max
			
		#
		# Lock and hide fk attributes as needed
		#
		mc.setAttr('%s.translateX' % fkChain[0], lock=True, keyable=False)
		mc.setAttr('%s.translateY' % fkChain[0], lock=True, keyable=False)
		mc.setAttr('%s.translateZ' % fkChain[0], lock=True, keyable=False)
		
		mc.setAttr('%s.translateX' % fkChain[1], keyable=False) #This channel connected to length
		mc.setAttr('%s.translateY' % fkChain[1], lock=True, keyable=False)
		mc.setAttr('%s.translateZ' % fkChain[1], lock=True, keyable=False)
		
		if kneeNum == 1:
			mc.setAttr('%s.translateX' % fkChain[2], keyable=False) #This channel connected to length
			mc.setAttr('%s.translateY' % fkChain[2], lock=True, keyable=False)
			mc.setAttr('%s.translateZ' % fkChain[2], lock=True, keyable=False)
			
		if kneeNum == 2:
			mc.setAttr('%s.translateX' % fkChain[2], lock=True,keyable=False) 
			mc.setAttr('%s.translateY' % fkChain[2], lock=True, keyable=False)
			mc.setAttr('%s.translateZ' % fkChain[2], lock=True, keyable=False)
			
			mc.setAttr('%s.translateX' % fkChain[3], keyable=False)#This channel connected to length
			mc.setAttr('%s.translateY' % fkChain[3], lock=True, keyable=False)
			mc.setAttr('%s.translateZ' % fkChain[3], lock=True, keyable=False)
			
		#
		#--- IK leg time!
		#

				
		#
		#--- Combining noFlip & pv via blendColors
		#
		# ik leg_top blendColors node creation/connections
		
		#
		#leg_top blendColors creation/linking
		#
		temp = mc.createNode( 'blendColors' )
		iklegTop_node1 = '%s_iktopLegRotate'%prefix
		mc.rename( temp, iklegTop_node1 )
		
		#legTop_node1 attributes to connect
		nodeColor1 = (iklegTop_node1 + ".color1")
		nodeColor2 = (iklegTop_node1 + ".color2")
		nodeOutput = (iklegTop_node1 + ".output")
		
		src1 = '%s.rotate'%pvChain[0]
		src2 = '%s.rotate'%noFlipChain[0]
		tgt = '%s.rotate'%ikChain[0]
		
		mc.connectAttr(src2, nodeColor1) 
		mc.connectAttr(src1, nodeColor2)
		mc.connectAttr(nodeOutput, tgt)
		
		#Connect each node to the self.foot_cnt so it's all switched by 1 att
		mc.connectAttr( '%s.Type'%foot_cnt, '%s.blender'%iklegTop_node1 ) #Defaults to: noFlip / 0 / node input 2
		
		#
		# ik leg_knee1, knee2, and ankle blendColors node creation/connections
		#
		if kneeNum == 1:
			#
			#iklegKnee1_node1 rotate blendColors creation/linking
			#
			temp = mc.createNode( 'blendColors' )
			iklegKnee1_node1 = '%s_ikknee1Rotate'%prefix
			mc.rename( temp, iklegKnee1_node1 )
			
			#iklegKnee1_node1 attributes to connect
			nodeColor1 = (iklegKnee1_node1 + ".color1")
			nodeColor2 = (iklegKnee1_node1 + ".color2")
			nodeOutput = (iklegKnee1_node1 + ".output")
			
			src1 = '%s.rotate'%pvChain[1]
			src2 = '%s.rotate'%noFlipChain[1]
			tgt = '%s.rotate'%ikChain[1]
			
			mc.connectAttr(src2, nodeColor1) 
			mc.connectAttr(src1, nodeColor2)
			mc.connectAttr(nodeOutput, tgt)
			
			#Connect each node to the foot_cnt so it's all driven by 1 att
			mc.connectAttr( '%s.Type'%foot_cnt, '%s.blender'%iklegKnee1_node1 ) 
			
			#iklegKnee1_node2 translate blendColors creation/linking
			temp = mc.createNode( 'blendColors' )
			iklegKnee1_node2 = '%s_ikKnee1Translate'%prefix
			mc.rename( temp, iklegKnee1_node2 )
			
			#iklegKnee1_node2 attributes to connect
			nodeColor1 = (iklegKnee1_node2 + ".color1")
			nodeColor2 = (iklegKnee1_node2 + ".color2")
			nodeOutput = (iklegKnee1_node2 + ".output")
			
			src1 = '%s.translate'%pvChain[1]
			src2 = '%s.translate'%noFlipChain[1]
			tgt = '%s.translate'%ikChain[1]
			
			mc.connectAttr(src2, nodeColor1) 
			mc.connectAttr(src1, nodeColor2)
			mc.connectAttr(nodeOutput, tgt)
			
			#Connect each node to the foot_cnt so it's all driven by 1 att
			mc.connectAttr( '%s.Type'%foot_cnt, '%s.blender'%iklegKnee1_node2 )
			
			#
			#ankle blendColors creation/linking
			#
			temp = mc.createNode( 'blendColors' )
			iklegAnkle_node = '%s_ikAnkleRotate'%prefix
			mc.rename( temp, iklegAnkle_node )
			
			#iklegAnkle_node attributes to connect
			nodeColor1 = (iklegAnkle_node + ".color1")
			nodeColor2 = (iklegAnkle_node + ".color2")
			nodeOutput = (iklegAnkle_node + ".output")
			
			src1 = '%s.rotate'%pvChain[2]
			src2 = '%s.rotate'%noFlipChain[2]
			tgt = '%s.rotate'%ikChain[2]
			
			mc.connectAttr(src2, nodeColor1) 
			mc.connectAttr(src1, nodeColor2)
			mc.connectAttr(nodeOutput, tgt)
			
			#Connect each node to the foot_cnt so it's all driven by 1 att
			mc.connectAttr( '%s.Type'%foot_cnt, '%s.blender'%iklegAnkle_node ) 
			
			#iklegAnkle_node2 translate blendColors creation/linking
			temp = mc.createNode( 'blendColors' )
			iklegAnkle_node2 = '%s_ikankleTranslate'%prefix
			mc.rename( temp, iklegAnkle_node2 )
			
			#iklegAnkle_node2 attributes to connect
			nodeColor1 = (iklegAnkle_node2 + ".color1")
			nodeColor2 = (iklegAnkle_node2 + ".color2")
			nodeOutput = (iklegAnkle_node2 + ".output")
			
			src1 = '%s.translate'%pvChain[2]
			src2 = '%s.translate'%noFlipChain[2]
			tgt = '%s.translate'%ikChain[2]
			
			mc.connectAttr(src2, nodeColor1) 
			mc.connectAttr(src1, nodeColor2)
			mc.connectAttr(nodeOutput, tgt)
			
			#Connect each node to the foot_cnt so it's all driven by 1 att
			mc.connectAttr( '%s.Type'%foot_cnt, '%s.blender'%iklegAnkle_node2 )
			
		if kneeNum == 2:
			#iklegKnee1_node1 blendColors creation/linking
			temp = mc.createNode( 'blendColors' )
			iklegKnee1_node1 = '%s_ikKnee1Rotate'%prefix
			mc.rename( temp, iklegKnee1_node1 )
			
			#iklegKnee1_node1 attributes to connect
			nodeColor1 = (iklegKnee1_node1 + ".color1")
			nodeColor2 = (iklegKnee1_node1 + ".color2")
			nodeOutput = (iklegKnee1_node1 + ".output")
			
			src1 = '%s.rotate'%pvChain[1]
			src2 = '%s.rotate'%noFlipChain[1]
			tgt = '%s.rotate'%ikChain[1]
			
			mc.connectAttr(src2, nodeColor1) 
			mc.connectAttr(src1, nodeColor2)
			mc.connectAttr(nodeOutput, tgt)
			
			#Connect each node to the foot_cnt so it's all driven by 1 att
			mc.connectAttr( '%s.Type'%foot_cnt, '%s.blender'%iklegKnee1_node1 ) 
			
			#iklegKnee1_node2 translate blendColors creation/linking
			temp = mc.createNode( 'blendColors' )
			iklegKnee1_node2 = '%s_ikknee1Translate'%prefix
			mc.rename( temp, iklegKnee1_node2 )
			
			#iklegKnee1_node2 attributes to connect
			nodeColor1 = (iklegKnee1_node2 + ".color1")
			nodeColor2 = (iklegKnee1_node2 + ".color2")
			nodeOutput = (iklegKnee1_node2 + ".output")
			
			src1 = '%s.translate'%pvChain[1]
			src2 = '%s.translate'%noFlipChain[1]
			tgt = '%s.translate'%ikChain[1]
			
			mc.connectAttr(src2, nodeColor1) 
			mc.connectAttr(src1, nodeColor2)
			mc.connectAttr(nodeOutput, tgt)
			
			#Connect each node to the foot_cnt so it's all driven by 1 att
			mc.connectAttr( '%s.Type'%foot_cnt, '%s.blender'%iklegKnee1_node2 )
			
			#iklegKnee2_node1 blendColors creation/linking
			temp = mc.createNode( 'blendColors' )
			iklegKnee2_node1 = '%s_ikKnee2Rotate'%prefix
			mc.rename( temp, iklegKnee2_node1 )
			
			#iklegKnee2_node1 attributes to connect
			nodeColor1 = (iklegKnee2_node1 + ".color1")
			nodeColor2 = (iklegKnee2_node1 + ".color2")
			nodeOutput = (iklegKnee2_node1 + ".output")
			
			src1 = '%s.rotate'%pvChain[2]
			src2 = '%s.rotate'%noFlipChain[2]
			tgt = '%s.rotate'%ikChain[2]
			
			mc.connectAttr(src2, nodeColor1) 
			mc.connectAttr(src1, nodeColor2)
			mc.connectAttr(nodeOutput, tgt)
			
			#Connect each node to the foot_cnt so it's all driven by 1 att
			mc.connectAttr( '%s.Type'%foot_cnt, '%s.blender'%iklegKnee2_node1 ) 
			
			#iklegKnee2_node2 translate blendColors creation/linking
			temp = mc.createNode( 'blendColors' )
			iklegKnee2_node2 = '%s_ikKnee2Translate'%prefix
			mc.rename( temp, iklegKnee2_node2 )
			
			#iklegKnee2_node2 attributes to connect
			nodeColor1 = (iklegKnee2_node2 + ".color1")
			nodeColor2 = (iklegKnee2_node2 + ".color2")
			nodeOutput = (iklegKnee2_node2 + ".output")
			
			src1 = '%s.translate'%pvChain[2]
			src2 = '%s.translate'%noFlipChain[2]
			tgt = '%s.translate'%ikChain[2]
			
			mc.connectAttr(src2, nodeColor1) 
			mc.connectAttr(src1, nodeColor2)
			mc.connectAttr(nodeOutput, tgt)
			
			#Connect each node to the foot_cnt so it's all driven by 1 att
			mc.connectAttr( '%s.Type'%foot_cnt, '%s.blender'%iklegKnee2_node2 )
			
			#iklegAnkle_node blendColors creation/linking
			temp = mc.createNode( 'blendColors' )
			iklegAnkle_node = '%s_ikAnkleRotate'%prefix
			mc.rename( temp, iklegAnkle_node )
			
			#iklegAnkle_node attributes to connect
			nodeColor1 = (iklegAnkle_node + ".color1")
			nodeColor2 = (iklegAnkle_node + ".color2")
			nodeOutput = (iklegAnkle_node + ".output")
			
			src1 = '%s.rotate'%pvChain[3]
			src2 = '%s.rotate'%noFlipChain[3]
			tgt = '%s.rotate'%ikChain[3]
			
			mc.connectAttr(src2, nodeColor1) 
			mc.connectAttr(src1, nodeColor2)
			mc.connectAttr(nodeOutput, tgt)
			
			#Connect each node to the foot_cnt so it's all driven by 1 att
			mc.connectAttr( '%s.Type'%foot_cnt, '%s.blender'%iklegAnkle_node )
			
			#iklegAnkle_node2 translate blendColors creation/linking
			temp = mc.createNode( 'blendColors' )
			iklegAnkle_node2 = '%s_ikankleTranslate'%prefix
			mc.rename( temp, iklegAnkle_node2 )
			
			#iklegAnkle_node2 attributes to connect
			nodeColor1 = (iklegAnkle_node2 + ".color1")
			nodeColor2 = (iklegAnkle_node2 + ".color2")
			nodeOutput = (iklegAnkle_node2 + ".output")
			
			src1 = '%s.translate'%pvChain[3]
			src2 = '%s.translate'%noFlipChain[3]
			tgt = '%s.translate'%ikChain[3]
			
			mc.connectAttr(src2, nodeColor1) 
			mc.connectAttr(src1, nodeColor2)
			mc.connectAttr(nodeOutput, tgt)
			
			#Connect each node to the foot_cnt so it's all driven by 1 att
			mc.connectAttr( '%s.Type'%foot_cnt, '%s.blender'%iklegAnkle_node2 )
			
		#Create RP IK on pv and no-flip chains
		if kneeNum == 1:
			noFlip_ikHandle = mc.ikHandle(sj=noFlipChain[0], ee=noFlipChain[2], solver = 'ikRPsolver', name = (prefix + '_noFlipIkHandle'))
			pv_ikHandle = mc.ikHandle(sj=pvChain[0], ee=pvChain[2], solver = 'ikRPsolver', name = (prefix + '_pvIkHandle'))
		if kneeNum == 2:	
			noFlip_ikHandle = mc.ikHandle(sj=noFlipChain[0], ee=noFlipChain[3], solver = 'ikRPsolver', name = (prefix + '_noFlipIkHandle'))
			pv_ikHandle = mc.ikHandle(sj=pvChain[0], ee=pvChain[3], solver = 'ikRPsolver', name = (prefix + '_pvIkHandle'))
		
		#Parent IK Handles to foot_cnt
		mc.parent(pv_ikHandle[0], noFlip_ikHandle[0], foot_cnt)
		
		#
		#---Set up no-Flip IK
		#
		noFlipPV_loc = mc.spaceLocator(n=('%s_noflipPV_loc'%prefix) )
		#Move it forward and out to the side
		mc.move(5,noFlipPV_loc,moveX=True) 
		#Make pv constraint
		mc.poleVectorConstraint( noFlipPV_loc, noFlip_ikHandle[0] )
		#Set twist to re-align with offset.
		mc.setAttr('%s.twist'%noFlip_ikHandle[0],90)
		#Group noFlipPV and connect the groups rotate Y to the 'noFlipKnee' attr on the foot_cnt 
		mc.select(clear=True)
		noFlipKneeGrp = mc.group( n=('%s_noFlipKneeGrp'%prefix),em=True )
		mc.parent( noFlipPV_loc, noFlipKneeGrp )
		mc.parent(noFlipKneeGrp, self.stateNode)
		mc.pointConstraint(foot_cnt,noFlipKneeGrp,mo=True)
		#Set up attribute to twist the knee
		
		mc.addAttr(foot_cnt,ln='noFlipKnee',at='float',k=True)
		mc.connectAttr('%s.noFlipKnee'%foot_cnt,'%s.rotateY'%noFlipKneeGrp, f=True)
		mc.setAttr(noFlipPV_loc[0]+'.visibility',0)
		
		#
		#---Set up pv IK
		#
		pv_loc = mc.spaceLocator( n=('%s_pv_loc'%prefix) )
		#Snap it to the knee and move it forward (Z) 5 units
		temp = mc.pointConstraint(ikChain[1],pv_loc,mo=False)
		mc.delete(temp) 
		if build == 'positive':
			mc.move(-5,pv_loc,moveZ=True)
		if build == 'negative':	
			mc.move(5,pv_loc,moveZ=True)
		mc.makeIdentity(pv_loc,apply=True)
		#Create the constraint
		mc.poleVectorConstraint(pv_loc, pv_ikHandle[0])
		#Zero pv
		pv_grp = mc.group(em=True,name='%s_pvBuffer'%prefix)
		if kneeNum == 1:
			temp = mc.pointConstraint(bindChain[2],pv_grp,mo=False)
		if kneeNum == 2:
			temp = mc.pointConstraint(bindChain[3],pv_grp,mo=False)
		mc.delete(temp)
		mc.parent(pv_grp,self.stateNode)
		mc.pointConstraint(foot_cnt,pv_grp,mo=True)
		mc.parent(pv_loc,pv_grp)
		#PV knee twist
		mc.addAttr(foot_cnt,ln='pv_knee',k=True,at='float')
		mc.connectAttr('%s.pv_knee'%foot_cnt,'%s.rotateY'%pv_grp,f=True)
		
		if stretchy == 1:	
			#
			#--- Call ms_makeStretchy for noFlip ik setup
			#
			##Create dictionary to pass with apply()
			arguments = { 'ikHandle':noFlip_ikHandle[0],
						  'solverType':1,
						  'aimAxis':aim,
						  'clusters':2,
						  'stretchVal':1,
						  'prefix':('nf'+prefix),
						  'jointChain':noFlipChain,
						  'kneeNum':self.kneeNum,
						  'build':build
						  }
			pargs=(1,2)	#No purpose besides satisfying the required list argument for the apply call.
					  
			#Call script, passing dictionary as an argument using apply()
			apply(mks.ms_makeStretchy,pargs,arguments)
			
			#
			#--- Call ms_makeStretchy for PV ik setup
			#
			##Create dictionary to pass with apply()
			arguments = { 'ikHandle':pv_ikHandle[0],
						  'solverType':1,
						  'aimAxis':aim,
						  'clusters':2,
						  'stretchVal':1,
						  'prefix':('pv'+prefix),
						  'jointChain':pvChain,
						  'kneeNum':self.kneeNum,
						  'build':build
						  }
			pargs=(1,2)	#No purpose besides satisfying the required list argument for the apply call.
					  
			#Call script, passing dictionary as an argument using apply()
			apply(mks.ms_makeStretchy,pargs,arguments)
		
		#
		#---Create vis switching stuff
		#
		mc.connectAttr('%s.FK_IK'%self.stateNode,'%s.visibility'%foot_cnt,f=True)
		mc.addAttr(foot_cnt,ln='pv_vis',at='float',k=True,min=0,max=1,dv=0)
		mc.connectAttr('%s.pv_vis'%foot_cnt,'%s.visibility'%pv_grp,f=True)	
		#Reverse node for the FK
		rvNode = '%s_rvNode'%prefix
		mc.createNode('reverse',n=rvNode)
		mc.connectAttr(self.stateNode+'.FK_IK',rvNode+'.inputX',f=True)
		mc.connectAttr(rvNode+'.outputX',fkChain[0]+'.visibility',f=True)
		
		#Now, we group and hide stuff
		jointsGrp = '%s_jointsGrp'%prefix
		mc.group(em=True,n=jointsGrp)
		mc.parent(bindChain[0],pvChain[0],noFlipChain[0],fkChain[0],ikChain[0],jointsGrp)
		mc.setAttr(ikChain[0]+'.visibility',0)
		mc.setAttr(pvChain[0]+'.visibility',0)
		mc.setAttr(noFlipChain[0]+'.visibility',0)
		
		#foot_cnt
		mc.setAttr(foot_cnt+'.visibility',lock=True,channelBox=False,keyable=False)
		mc.setAttr(foot_cnt+'.scaleX',lock=True,channelBox=False,keyable=False)
		mc.setAttr(foot_cnt+'.scaleY',lock=True,channelBox=False,keyable=False)
		mc.setAttr(foot_cnt+'.scaleZ',lock=True,channelBox=False,keyable=False)
		
		
		#fk controls
		for jnt in fkChain:
			mc.setAttr(jnt+'.scaleX',lock=True,channelBox=False,keyable=False)
			mc.setAttr(jnt+'.scaleY',lock=True,channelBox=False,keyable=False)
			mc.setAttr(jnt+'.scaleZ',lock=True,channelBox=False,keyable=False)
			mc.setAttr(jnt+'.visibility',lock=True,channelBox=False,keyable=False)
			mc.setAttr(jnt+'.radius',lock=True,channelBox=False,keyable=False)
		
			
	def loadText(self,*args): #Called by first window
		jntName = mc.ls(sl=True)
		mc.textFieldGrp(self.jointFld,edit=True,text=jntName[0])
		
	def loadIKCnt(self,*args): #Called by first window
		cntName = mc.ls(sl=True)
		mc.textFieldGrp(self.ikCntFld,edit=True,text=cntName[0])