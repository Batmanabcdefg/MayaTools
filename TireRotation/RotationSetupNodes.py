
import maya.cmds as cmds
import maya.mel as mel

class RotationSetupNodes():
	'''
		Rotation node setup.
		Creates a null node and adds attributes to it, updating them with expressions and direct connections.

		Attributes-----------------------------
		Input:
		- time
		- frontPosition: (x,y,z) <------ decomposeMatrix.translate <------- front_loc.worldMatrix
		- backPosition: (x,y,z) <------ decomposeMatrix.translate <------- back_loc.worldMatrix
		- motionVector: (x,y,z) <------ vector << Fx - Bx, Fz - Bz>>
		- rotationFactor: 
			if( (Fx+Fz) >= (Bx+Bz) ) { rotationFactor=1; }
			else{ rotationFactor=-1; }
		- direction: "forward","reverse": enum
		- auto_type: "time","driver_control", "off": enum: animCurves mode requires RotateCtrl.translatXYZ attributes to be animated(keyframed).

		Output: 
		- rotation: Float: Rotational value in degrees.

		Methods:
		_connectFront(): Create DecompMatrix from front_loc 
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
		#self._createNode()
		#self._connectControl()
		self.spinExp()
		'''
		self._setOldPosition()
		self._setMoveVector()
		self._setDistance()
		self._setRotation()
		'''
		# Connect rotation to object
		#cmds.connectAttr('%s.rotation'%self.node,'%s.rotateX'%self.driven,f=True)
		
	def _createNode(self):
		''' Create transform node and add the attributes. '''
		self.node = cmds.createNode('transform',n=self.ctrlName+'_tireSpinNode')

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
		
		cmds.addAttr( longName='motionVector', numberOfChildren=3, attributeType='compound' )
		cmds.addAttr( longName='mvx', attributeType='double', parent='motionVector' )
		cmds.addAttr( longName='mvy', attributeType='double', parent='motionVector' )
		cmds.addAttr( longName='mvz', attributeType='double', parent='motionVector' )
		cmds.setAttr('%s.motionVector'%self.node,k=True,l=False)
		
		cmds.addAttr(self.node,ln='auto',attributeType='enum',enumName="off:on",dv=1)

		cmds.addAttr(self.node,ln='radius',dv=self.radius)
		cmds.setAttr('%s.radius'%self.node,k=True,l=False)
		
		cmds.addAttr(self.node,ln='driverDirectionAngle',dv=0.0)
		cmds.setAttr('%s.driverDirectionAngle'%self.node,k=True,l=False)
		
		cmds.addAttr(self.node,ln='rotationDirectionFactor',dv=0.0)
		cmds.setAttr('%s.rotationDirectionFactor'%self.node,k=True,l=False)
		
		cmds.addAttr(self.node,ln='distance',dv=0.0)
		cmds.setAttr('%s.distance'%self.node,k=True,l=False)
		
		
		#--- Output
		cmds.addAttr(self.node,ln='rotation',dv=0.0)
		cmds.setAttr('%s.rotation'%self.node,k=True,l=False)
		
	def _connectControl(self):
		''' Connect time to time, world matrix of control to decomposeNode to currentPosition. '''
		# Create decompose matrix
		try:	
			# Time
			#cmds.connectAttr('time1.outTime','%s.time'%self.node,f=True)
			
			# Decompose Matrix: World Matrix of control ---> currentPosition
			name = '%s_WM'%self.ctrlName
			decompNode = cmds.createNode('decomposeMatrix',n=name)
			
			cmds.connectAttr('%s.worldMatrix'%self.ctrlName,'%s.inputMatrix'%decompNode,f=True)
			cmds.connectAttr('%s.outputTranslate'%decompNode,'%s.currentPosition'%self.node,f=True)
			
			# Decompose Matrix: World Matrix of control ---> driverDirectionAngle
			cmds.connectAttr('%s.outputRotateY'%decompNode,'%s.driverDirectionAngle'%self.node,f=True)

		except Exception,e:
			raise Excption(e)
			
	def spinExp(self):
		#print self.node
		exp = '// Rotational value\n'
		exp += '$drvAngl = %s.rotateY %% 360;\n\n'%(self.ctrlName)
		exp += 'float $radius = %s;\n'%self.radius
		exp += 'int $rotationDirectionFactor;\n'
		exp += 'vector $previousPos = <<0,0,0>>;\n'
		exp += 'vector $currentPos = `xform -query -ws -t %s`;\n'%self.ctrlName#<<%s.tx,%s.ty,%s.tz>>;\n'%(self.ctrlName,self.ctrlName,self.ctrlName)
		exp += '// Setup motionVector\n'
		exp += 'vector $moveVector = <<$currentPos.x-$previousPos.x,$currentPos.y-$previousPos.y,$currentPos.z-$previousPos.z>>;\n'
		exp += '// Distance setup\n\n'
		exp += 'float $distance = sqrt(($moveVector.x*$moveVector.x)+($moveVector.y*$moveVector.y)+($moveVector.z*$moveVector.z));\n'
		exp += '// Check if change is only in Y\n\n'
		exp += 'if( ($moveVector.y != $previousPos.y)&&($moveVector.x==$previousPos.x)&&($moveVector.z==$previousPos.z) )\n'
		exp += '{ manipMoveContext -e -mode 4 Move; }\n\n'
		exp += '// Check angle of driver to determine rotationDirectionFactor\n'
		exp += 'else{\n'
		exp += 'if($drvAngl==0){ if($currentPos.z>$previousPos.z){ $rotationDirectionFactor=1; }else{$rotationDirectionFactor=-1;} }\n\n'
		exp += 'if( (($drvAngl>0)&&($drvAngl<=90))||(($drvAngl<-180)&&($drvAngl>=-270)) )\n'
		exp += '{ if($currentPos.x>$previousPos.x){ $rotationDirectionFactor*=1; }else{$rotationDirectionFactor*=-1;} }\n\n'
		exp += 'if( (($drvAngl>90)&&($drvAngl<=180))||(($drvAngl<-90)&&($drvAngl>=-180)) )\n'
		exp += '{ if($currentPos.z>$previousPos.z){ $rotationDirectionFactor*=-1; }else{$rotationDirectionFactor*=1;} }\n\n'
		exp += 'if( (($drvAngl>180)&&($drvAngl<=270))||(($drvAngl<0)&&($drvAngl>=90)) )\n'
		exp += '{ if($currentPos.x>$previousPos.x){ $rotationDirectionFactor*=-1; }else{$rotationDirectionFactor*=1;} }\n\n'
		exp += 'if( (($drvAngl>270)&&($drvAngl<=360))||(($drvAngl<-270)&&($drvAngl>=-360)) )\n'
		exp += '{ if($currentPos.z>$previousPos.z){ $rotationDirectionFactor*=1; }else{$rotationDirectionFactor*=-1;} }\n\n'
		exp += '%s.rx += $rotationDirectionFactor*(($distance/($radius*6.2831))*360);\n'%(self.driven)
		exp += 'manipMoveContext -e -mode 4 Move;\n'
		exp += '}//end else\n\n'
		exp += '// Set previousPosition to current\n'
		exp += '$previousPos = <<$currentPos.x,$currentPos.y,$currentPos.z>>;\n\n'
		exp += '// Reset rotation values when they get too big\n'
		exp += 'if(%s.rx>1080){%s.rx=0;}\n'%(self.driven,self.driven)
		exp += 'if(%s.rx<-1080){%s.rx=0;}\n'%(self.driven,self.driven)
		
		cmds.expression(s=exp,n='SpinExp')
	
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
	RotationSetupNodes(ctrl='nurbsCircle1',driven='pCylinder1',radius=2)
