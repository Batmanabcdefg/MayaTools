
import maya.cmds as cmds
import maya.mel as mel

class RotationSetup():
	'''
		Rotation node setup.
		Creates a null node and adds attributes to it, updating them with expressions and direct connections.

		Attributes-----------------------------
		Input:
		- time
		- currentPosition: (x,y,z) <------ decomposeMatrix.translate <------- RotationCtrl.worldMatrix
		- radius: float
		- direction: "forward","reverse": enum
		- type: "time","animCurves*": enum: animCurves mode requires RotateCtrl.translatXYZ attributes to be animated(keyframed).

		Output: 
		- rotation: Float: Rotational value in degrees.

		Internal:
		- oldPosition:
		- moveVector
		- distance
otationSetup
		Expressions(Nodes?):----------------------------
		-getPreviousPosition
		-getMoveVector
		-getDistance
		-getRotation
----------------------------------------------------
import sys
path ='/Users/mauricioptkvp/Development/python/maya'
if path not in sys.path: sys.path.insert(0,path)

import RotationSetup
reload(RotationSetup)
RotationSetup.RotationSetup()
----------------------------------------------------
	'''
	def __init__(self,**keywords):
		''' 	Get initial keyword values
			Start logger '''
		if not keywords.has_key('ctrl'): raise Exception('No control passed in by caller.')
		self.ctrlName = keywords['ctrl']
		if not keywords.has_key('driven'): raise Exception('No driven object passed in by caller.')
		self.driven = keywords['driven']
		if not keywords.has_key('radius'): raise Exception('No radius passed in by caller.')
		self.radius = keywords['radius']
		
		
		self._main()
	
	def _main(self):
		''' 
			Call build methods
		    Log the runtime of the methods
		'''
		self._createNode()
		self._connectControl()
		self._setOldPosition()
		self._setMoveVector()
		self._setDistance()
		self._setRotation()

		# Connect rotation to object
		#cmds.connectAttr('%s.rotation'%self.node,'%s.rotateX'%self.driven,f=True)
		
	def _createNode(self):
		''' Create transform node and add the attributes. '''
		self.node = cmds.createNode('transform',n=self.ctrlName+'_rotateNode')
		
		cmds.addAttr(self.node,ln='time',dv=0.0)
		cmds.setAttr('%s.time'%self.node,k=True,l=False)
		
		cmds.addAttr(self.node,ln='type',attributeType='enum',enumName="time:animCurves")

		cmds.addAttr(self.node,ln='direction',attributeType='enum',enumName="forward:reverse")

		cmds.addAttr(self.node,ln='radius',dv=self.radius)
		cmds.setAttr('%s.radius'%self.node,k=True,l=False)
		
		cmds.addAttr(self.node,ln='reset',dv=1.0,min=0.0,max=1.0)
		cmds.setAttr('%s.reset'%self.node,k=True,l=False)

		cmds.addAttr( longName='currentPosition', numberOfChildren=3, attributeType='compound' )
		cmds.addAttr( longName='cpx', attributeType='double', parent='currentPosition' )
		cmds.addAttr( longName='cpy', attributeType='double', parent='currentPosition' )
		cmds.addAttr( longName='cpz', attributeType='double', parent='currentPosition' )
		cmds.setAttr('%s.currentPosition'%self.node,k=True,l=False)
		
		cmds.addAttr( longName='previousPosition', numberOfChildren=3, attributeType='compound' )
		cmds.addAttr( longName='ppx', attributeType='double', parent='previousPosition' )
		cmds.addAttr( longName='ppy', attributeType='double', parent='previousPosition' )
		cmds.addAttr( longName='ppz', attributeType='double', parent='previousPosition' )
		cmds.setAttr('%s.previousPosition'%self.node,k=True,l=False)
		
		cmds.addAttr( longName='moveVector', numberOfChildren=3, attributeType='compound' )
		cmds.addAttr( longName='mvx', attributeType='double', parent='moveVector' )
		cmds.addAttr( longName='mvy', attributeType='double', parent='moveVector' )
		cmds.addAttr( longName='mvz', attributeType='double', parent='moveVector' )
		cmds.setAttr('%s.moveVector'%self.node,k=True,l=False)
		
		cmds.addAttr(self.node,ln='distance',dv=0.0)
		cmds.setAttr('%s.distance'%self.node,k=True,l=False)
		
		cmds.addAttr(self.node,ln='rotation',dv=0.0)
		cmds.setAttr('%s.rotation'%self.node,k=True,l=False)
		
	def _connectControl(self):
		''' Connect time to time, world matrix of control to decomposeNode to currentPosition. '''
		# Create decompose matrix
		try:	
			# Time
			cmds.connectAttr('time1.outTime','%s.time'%self.node,f=True)
			
			# Decompose MAtrix: World MAtrix of control ---> currentPosition
			name = '%s_WM'%self.ctrlName
			decompNode = cmds.createNode('decomposeMatrix',n=name)
			
			cmds.connectAttr('%s.worldMatrix'%self.ctrlName,'%s.inputMatrix'%decompNode,f=True)
			cmds.connectAttr('%s.outputTranslate'%decompNode,'%s.currentPosition'%self.node,f=True)

		except Exception,e:
			raise Excption(e)
	
	def _setOldPosition(self):
		''' 
		Creates expression
		Exp: Using type, get the x,y,z of the position a frame ago or a frame later if time decreasing.
		'''
		exp = 'int $method = %s.type;\n'%self.node
		exp += 'float $time;\n'
		exp += 'if($method==0){\n'
		exp += '	$time = %s.time;\n'%self.node 
		exp += '	vector $pos=`getAttr -time ($time-1) %s.translate`;\n'%self.ctrlName
		exp += '	%s.ppx = $pos.x;\n'%self.node
		exp += '	%s.ppy = $pos.y;\n'%self.node
		exp += '	%s.ppz = $pos.z;\n'%self.node
		exp += '}\n'
		exp += 'if($method==1){\n'
		exp += '	$cTime = `currentTime -query`;\n'
		exp += '	if ($cTime > $time){//Check against previous value of $time\n'
		# What if the animCurve does not exist at that time? Perhaps evaluate 
		# the curve at the nearest keyframe
		exp += '	$time = $cTime; //Get values from future\n'
		exp += '	float $temp[] = `keyframe -at tx -t ($time-1) -q -eval %s`;\n'%(self.ctrlName)
		exp += '	%s.ppx = $temp[0];\n'%self.node
		exp += '	$temp = `keyframe -at ty -t ($time-1) -q -eval %s`;\n'%(self.ctrlName)
		exp += '	%s.ppy = $temp[0];\n'%self.node
		exp += '	$temp = `keyframe -at tz -t ($time-1) -q -eval %s`;\n'%(self.ctrlName)
		exp += '	%s.ppz = $temp[0];\n'%self.node
		exp += '	}\n'
		exp += '	else{\n'
		exp += '	$time = $cTime; //Get values from past\n'
		exp += '	float $temp[] = `keyframe -at tx -t ($time+1) -q -eval %s`;\n'%(self.ctrlName)
		exp += '	%s.ppx = $temp[0];\n'%self.node
		exp += '	$temp = `keyframe -at ty -t ($time+1) -q -eval %s`;\n'%(self.ctrlName)
		exp += '	%s.ppy = $temp[0];\n'%self.node
		exp += '	$temp = `keyframe -at tz -t ($time+1) -q -eval %s`;\n'%(self.ctrlName)
		exp += '	%s.ppz = $temp[0];\n'%self.node
		exp += '	}\n'
		exp += '}\n'
		exp += '//Todo: Get info from anim curve\n'

		cmds.expression(s=exp,n='%s_oldPosExp'%self.ctrlName)	
				
	def _setMoveVector(self):
		''' 
		Creates expression
		Exp: Using currentPosition, oldPosition, get moveVector. 
		'''
		exp = '%s.mvx = %s.cpx - %s.ppx;\n'%(self.node,self.node,self.node)
		exp += '%s.mvy = %s.cpy - %s.ppy;\n'%(self.node,self.node,self.node)
		exp += '%s.mvz = %s.cpz - %s.ppz;\n'%(self.node,self.node,self.node)

		cmds.expression(s=exp,n='%s_moveVecExp'%self.ctrlName)	
		
	def _setDistance(self):
		''' 
		Creates expression
		Exp: moveVector = currentPosition - oldPosition
		'''
		exp = 'vector $move = <<%s.mvx,%s.mvy,%s.mvz>>;\n'%(self.node,self.node,self.node)
		exp += '%s.distance = mag($move);\n'%self.node

		cmds.expression(s=exp,n='%s_distExp'%self.ctrlName)	
	
	def _setRotation(self):
		'''
		Creates expression
		Exp: rotation = (distance/radius) * 57.3 // theta = s/r, where theta=rotation in radians, s=arc length, r=radius
		'''
		exp = 'int $dir;\n'
		exp += 'int $method = %s.type;\n'%self.node
		exp += 'if($method==0){\n'
		exp += '	if(%s.direction==0){ $dir=1; }\n'%self.node
		exp += '	else{ $dir=-1; }\n'
		exp += '}\n'
		exp += 'else{\n'
		exp += '	float $time;\n'
		exp += '	float $cTime = `currentTime -query`;\n'
		exp += '	if($cTime>$time){  $time=$cTime; $dir=1; }//Check againt previous value of $time\n'
		exp += '	else{ $time=$cTime; $dir=-1; }\n}\n'
		exp += 'float $weight = %s.mvx + %s.mvy + %s.mvz;\n'%(self.node,self.node,self.node)
		exp += 'if($weight<1) $dir*=-1;\n'
		exp += 'if(%s.reset==0)%s.rotateX = 0;\n'%(self.node,self.driven)
		exp += 'else %s.rotation = (%s.distance/%s.radius)*57.3*%s.reset*($dir);\n'\
		%(self.node,self.node,self.node,self.node)
		exp += '%s.rotateX+=%s.rotation;\n'%(self.driven,self.node)
		cmds.expression(s=exp,n='%s_rotationExp'%self.ctrlName)
		
if __name__ == '__main__':
	RotationSetup(ctrl='nurbsCircle1',driven='pCylinder1',radius=2)
