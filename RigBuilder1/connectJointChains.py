from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *
"""
Copyright (c) 2010,2011 Mauricio Santos
Name: connectJointChains.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created:   8 Oct 2010
Last Modified:  11 Jan 2011

$Revision: 132 $
$LastChangedDate: 2011-08-06 19:27:15 -0700 (Sat, 06 Aug 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/connectJointChains.py $
$Id: connectJointChains.py 132 2011-08-07 02:27:15Z mauricio $

Description: 
	Given 3 chains, blend them via blendColor nodes. Return created node names as list.
	

Used by: createRig.py, createArmRig.py,createLegRig.py

Uses:

Process:
	
	
Additional Notes: 

Example call:
	import connectJointChains as cjc
	cjc.connectJointChains(	prefix='test',
							   followJoint='test_shoulderJnt',
							   leadAJoint='test_shoulderJnt_ik',
							   leadBJoint='test_shoulderJnt_fk',
							   type=1,
							   translations=1,
							   rotations=1 )
	
	print temp.createdNodes = [nt.ParentConstraint(u'test_shoulderJnt_parentConstraint1'), nt.ParentConstraint(u'test_elbowJnt_parentConstraint1'), nt.ParentConstraint(u'test_wristJnt_parentConstraint1')]
	
Attributes:
	createdNodes = list of created nodes.

Keywords:
	prefix = Prefix to names of all created nodes

	followJoint = root joint of Follow chain
	
	leadAJoint = root joint of Lead A chain
	
	leadBJoint = root joint of Lead B chain # Not needed for type 1.
  
	type =  1 = Parent constraint 2 chains, 2 = BlendNodes connect 3 chains
			
	translate = 1 = On, 2 = Off
				
	rotate = 1 = On, 2 = Off
			 
Requires:


Development notes:

	@todo	- setup direct connections
	
"""
class connectJointChains():
	"""
	Given 3 chains, blend them via blendColor nodes. Return created node names as list.
	"""
	def __init__(self,**keywords):
		
		
		# Used to store names of all created nodes, 
		# to be returned when the tool is done.
		self.createdNodes = [] 
		
		# Command line call
		self.commandlineCall(keywords)
			
	def commandlineCall(self,keywords):
		"""
		Verify and Store the data passed via command line keywords dictionary.
		"""	
		self.prefix = keywords['prefix']
		
		self.followJoint = keywords['followJoint']
		self.leadAJoint = keywords['leadAJoint']
		try:
			self.leadBJoint = keywords['leadBJoint']
		except: #@todo - catch specific exception
			self.leadBJoint = ''
		
		self.type = keywords['type']
		self.translations = keywords['translations']
		self.rotations = keywords['rotations']
		
		self.connectChains()
		
	def connectChains(self,*args):
		"""
		Connect Follow chain to Lead A and/or Lead B chains.
		"""
		self.followChain = []
		self.leadAChain = []
		self.leadBChain = []
		   
		# Parent constraint connections:
		if self.type == 1:
			
			# handle two lists of joints and parent constrain them if their distance
			# apart is within tolerance
			for bindJnt in self.followJoint:
			   for rigJnt in self.leadAJoint:
				   self.getDistance(bindJnt,rigJnt)
				   print self.distVal
				   tolerance = .01
				   if self.distVal <= tolerance:
					   try: 
						   parentConstraint(rigJnt,bindJnt,mo=True)
					   except:
						   pass
							
		# Blend Color Node connections:
		if self.type == 2:
			
			# Get Follow chain
			select(self.followJoint,replace=True,hi=True)
			temp = ls(sl=True)
			for each in temp:
				self.followChain.append(each)
				
			# Get Lead A chain
			select(self.leadAJoint,replace=True,hi=True)
			temp = ls(sl=True)
			for each in temp:
				self.leadAChain.append(each)
				
			# Get Lead B chain
			if len(self.leadBJoint):
				select(self.leadBJoint,replace=True,hi=True)
				temp = ls(sl=True)
				for each in temp:
					self.leadBChain.append(each)
			
			#Shoulder blendColors creation/linking
			if self.rotations == 1:
				self.setupBlendNode(name = 'top_rotations',
											type = 1,
											src1 = self.leadAChain[0],
											src2 = self.leadBChain[0],
											tgt = self.followChain[0])
			if self.translations == 1:
				self.setupBlendNode(name = 'top_translations',
											type = 2,
											src1 = self.leadAChain[0],
											src2 = self.leadBChain[0],
											tgt = self.followChain[0])
			
			#Elbow blendColors creation/linking
			if self.rotations == 1:
				self.setupBlendNode(name = 'middle_rotations',
											type = 1,
											src1 = self.leadAChain[1],
											src2 = self.leadBChain[1],
											tgt = self.followChain[1])
			if self.translations == 1:
				self.setupBlendNode(name = 'middle_translations',
											type = 2,
											src1 = self.leadAChain[1],
											src2 = self.leadBChain[1],
											tgt = self.followChain[1])
			
			#Wrist blendColors creation/linking
			if self.rotations == 1:
				self.setupBlendNode(name = 'bottom_rotations',
											type = 1,
											src1 = self.leadAChain[2],
											src2 = self.leadBChain[2],
											tgt = self.followChain[2])
			if self.translations == 1:
				self.setupBlendNode(name = 'bottom_translations',
											type = 2,
											src1 = self.leadAChain[2],
											src2 = self.leadBChain[2],
											tgt = self.followChain[2])
		
		# Direct connections: Two chains only! Ignores leadBChain
		if self.type == 3:
			#@todo - setup direct connections
			pass
		
		return self.createdNodes

	def getDistance(self,a,b):
		"""
		Return the disatnce between a and b as a float using a distance dimension node.
		Defines: self.distVal
		"""		
		aPos = xform(a,query=True,ws=True,t=True)
		bPos = xform(b,query=True,ws=True,t=True)
		
		distNode = distanceDimension(sp=aPos,ep=bPos)
		
		self.distVal = distNode.distance
		print distNode
		print self.distVal
		delete(distNode)

	def setupBlendNode(self,name,type,src1,src2,tgt):
		"""
		Create and connect three objects via blendColor node
		"""
		# Rotations
		if type == 1: 
			type = 'rotate'
		else:
			type = 'translate'
			
		temp = createNode( 'blendColors' )
		blendNode = '%s_%s'%(self.prefix,name)
		rename( temp,blendNode )

		#blendNode attributes to connect
		nodeColor1 = (blendNode + ".color1")
		nodeColor2 = (blendNode + ".color2")
		nodeOutput = (blendNode + ".output")

		source1 = '%s.%s'%(src1,type)
		source2 = '%s.%s'%(src2,type)
		target = '%s.%s'%(tgt,type)

		connectAttr(source1, nodeColor1)
		connectAttr(source2, nodeColor2)
		connectAttr(nodeOutput, target)
		
		# Store name of created node to return to caller.
		self.createdNodes.append(blendNode)
		
	def loadFollow(self,*args):
		sel = ls(sl=True,fl=True)
		textFieldButtonGrp(self.followFld,e=True,text=sel[0])  
		
	def loadA(self,*args):
		sel = ls(sl=True,fl=True)
		textFieldButtonGrp(self.leadAFld,e=True,text=sel[0]) 
		 
	def loadB(self,*args):
		sel = ls(sl=True,fl=True)
		textFieldButtonGrp(self.leadBFld,e=True,text=sel[0])  
		