
import maya.cmds as cmds
import maya.mel as mel

class RotationControlSetup():
	'''
	drivectrl = Control whose movement causes rotation of tire.(Zero'd with frozen transforms.)
	attrctrl = Control to add Auto on/off switch attribute onto.
	driven = transform to get rotationX driven by expression.(Zero'd with frozen transforms.)
	radius = Radius of wheel.
	----------------------------------------------------
	import sys
	path ='/Users/mauricioptkvp/Development/python/maya'
	if path not in sys.path: sys.path.insert(0,path)
	
	import RotationControlSetup
	reload( RotationControlSetup )
	RotationControlSetup.RotationControlSetup( drivectrl='nurbsCircle1',attrctrl='nurbsCircle1',driven='pCylinder1',radius=1 )
	----------------------------------------------------
	'''
	def __init__(self,**keywords):
		''' Perform entire setup. '''
		if not keywords.has_key('drivectrl'): raise Exception('No drive control passed in by caller.')
		drivectrl = keywords['drivectrl']
		if not keywords.has_key('attrctrl'): raise Exception('No attribute control passed in by caller.')
		attrctrl = keywords['attrctrl']
		if not keywords.has_key('driven'): raise Exception('No driven object passed in by caller.')
		driven = keywords['driven']
		if not keywords.has_key('radius'): raise Exception('No radius passed in by caller.')
		radius = keywords['radius']
		
		# Setup heirarchy
		try:
			cmds.select(driven,r=True)
			rGrp = cmds.group(n='%s_RotationSpinGrp'%drivectrl)
			cmds.select(rGrp,r=True)
			tGrp = cmds.group(n='%s_TransformSpinGrp'%drivectrl)
			cmds.select(tGrp,r=True)
			rootGrp = cmds.group(n='%s_SpinTopGrp'%drivectrl)
			
			cmds.parent(drivectrl,rootGrp)
			
		except Exception,e:
			raise Exception(e)
			
		# Constraint tGrp to drivectrl
		try:
			cmds.pointConstraint(drivectrl,tGrp,mo=True)
			cmds.orientConstraint(drivectrl,tGrp,mo=True)
		except Exception,e:
			raise Exception(e)
			
		# Add attributes to attrctrl
		try:
			cmds.addAttr(attrctrl,ln='%sSpinRate'%driven,dv=1)
			cmds.setAttr('%s.%sSpinRate'%(attrctrl,driven),k=True,l=False)
			
			cmds.addAttr(attrctrl,ln='%sManualSpin'%driven,dv=0)
			cmds.setAttr('%s.%sManualSpin'%(attrctrl,driven),k=True,l=False)
			
		except Exception,e:
			raise Exception(e)
			
		# Create the rotation expression
		# Global vector to hold old position between evaluations of expression.
		oldpos = '%soldtanspos'%drivectrl
		
		# The expression string
		exp = ''
		exp += 'global vector $%s =<<0,0,0>>;\n'%oldpos
		exp += 'float $radius = %s;\n'%radius
		exp += '$rate = %s.%sSpinRate;\n'%(attrctrl,driven)
		exp += '$manual = %s.%sManualSpin;\n'%(attrctrl,driven)
		exp += '$distance = 0.0;\n'
		exp += '$dctrl = 1;\n'
		exp += '$dctrly=1;\n'
		exp += 'int $revdir=1 ;\n'
		exp += 'vector $changetrans = `getAttr %s.translate`;\n'%tGrp
		exp += 'float $cx = $changetrans.x-$%s.x ;\n'%oldpos
		exp += 'float $cy = $changetrans.y-$%s.y ;\n'%oldpos
		exp += 'float $cz = $changetrans.z-$%s.z ;\n\n'%oldpos
		
		exp += 'float $distance = sqrt($cx*$cx + $cy*$cy + $cz*$cz);\n\n'
		
		exp += '$angltrd = %s.rotateY%%360;\n\n'%tGrp
		
		exp += 'if (($changetrans.y != $%s.y)&& \n'%oldpos
		exp += '	($changetrans.x == $%s.x)&&\n'%oldpos
		exp += '	($changetrans.z == $%s.z))\n'%oldpos
		exp += '	{\n'
		exp += '		manipMoveContext -e -mode 4 Move;\n'
		exp += '	}\n'
		exp += 'else{		\n'
		exp += '	if ($angltrd==0)\n'
		exp += '	{\n'
		exp += '		if ($changetrans.z > $%s.z) $dctrl=1;\n'%oldpos
		exp += '		else $dctrl=-1;\n'
		exp += '	}\n'
		exp += '	if (($angltrd>0 && $angltrd<=90)||\n'
		exp += '	($angltrd<-180 && $angltrd>=-270))\n'
		exp += '	{\n'
		exp += '		if ($changetrans.x > $%s.x) $dctrl=1*$dctrl;\n'%oldpos
		exp += '		else $dctrl=-1*$dctrl;\n'
		exp += '	}\n'
		exp += '	if (($angltrd>90 && $angltrd<=180)||\n'
		exp += '	($angltrd<-90 && $angltrd>=-180))\n'
		exp += '	{\n'
		exp += '		if ($changetrans.z > $%s.z) $dctrl=-1*$dctrl;\n'%oldpos
		exp += '		else $dctrl=1*$dctrl;\n'
		exp += '	}\n'
		exp += '	if (($angltrd>180 && $angltrd<=270)||\n'
		exp += '	($angltrd<0 && $angltrd>=-90))\n'
		exp += '	{\n'
		exp += '		if ($changetrans.x > $%s.x) $dctrl=-1*$dctrl;\n'%oldpos
		exp += '		else $dctrl=1*$dctrl;\n'
		exp += '	}\n'
		exp += '	if (($angltrd>270 && $angltrd<=360)||\n'
		exp += '	($angltrd<-270 && $angltrd>=-360))\n'
		exp += '	{\n'
		exp += '		if ($changetrans.z > $%s.z) $dctrl=1*$dctrl;\n'%oldpos
		exp += '		else $dctrl=-1*$dctrl;\n'
		exp += '	}\n'
		exp += '	if ($manual==0){\n'
		exp += '		%s.rotateX = %s.rotateX + $manual + ( $rate * (($dctrly*($dctrl * (( $distance / (6.2831 * $radius)) * 360.0) ) ) ) );\n'%(rGrp,rGrp)
		exp += '	}\n'
		exp += '	else{ %s.rotateX = $manual; }\n'%rGrp
		exp += '	manipMoveContext -e -mode 4 Move;\n'
		exp += '}\n\n'
		
		exp += '$%s=<<%s.translateX,%s.translateY,%s.translateZ>>\n'%(oldpos,tGrp,tGrp,tGrp)
		
		cmds.expression(s=exp,n='%sRotationExp'%attrctrl)

