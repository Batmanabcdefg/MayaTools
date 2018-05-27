"""
Copyright (c) 2009 Mauricio Santos
Name: ms_backRig.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 19 June 2009
Last Modified: 14 November 2009
License: LGNU
Description: 
		This is the interface (GUI) that calls the existing scripts.
		Scripts:
		A couple different ways to build a back rig consolidated into one script.
		Methods:
			Jason Schleifer IK/FK 2001 Master Class Method (Stretchy IK Spline on FK joints, Shoulders, hips controls. No mid back.)
			Ribbon Spine: All pros of above and mid-back. Cons: Requires Unlimited. If that's not an issue, use this one!
To do: 
		Tab'd interface:
			Ik Back: Done
			Ribbon: Not done
		
		Make rig scripts: 
			ms_jsBackMethod.py : Started
				-Rotate Order support
				-Working on adding auto clavicle
			ms_rbbnSpine.py:
		
Additional Notes:


Development Notes:
    

"""

import maya.cmds as mc

#Import back rig scripts
import ms_ikSplineBack as misb


#Reload to include recent updates during development.
reload( misb )


class ms_backRig():
	def __init__(self,*args):
        ##########################################################
        # --------Tab interface to different back rig scripts----#
        ##########################################################
        
		if(mc.window('ms_backRigWin',exists=True)):
		    mc.deleteUI('ms_backRigWin',window=True)
		    
		mc.window('ms_backRigWin',title='Back Rig Scripts Interface v1.0',rtf=True)
		mc.columnLayout()
		self.prefixFld = mc.textFieldGrp(label='Prefix:',text='test_')
		
		tabs = mc.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
		
		#
		# Start IK Spline Rig Tab
		#
		ikTab = mc.columnLayout(w=450)
		
		mc.frameLayout(label='Prerequisites:',cll=True,cl=True,fn='boldLabelFont',w=450)
		mc.columnLayout()
		mc.text(" -Neck, arm, rib joints disconnected.") 
		mc.text(" -All controllers are in place, zero'd and oriented correctly.")
		mc.text(" -Controls have a buffer group above them in hierarchy.")
		mc.text(" -Rotate orders are set on controllers.")
		mc.text(" -Initial joints are placed, oriented.")  
		
		mc.setParent('..')
		mc.setParent('..')
		
		
		mc.frameLayout(label='Controls',fn='boldLabelFont',cll=False,w=450)
		mc.columnLayout()
		self.shldrsCtrFld = mc.textFieldButtonGrp( label='Shoulder:',bl='Load',bc=self.loadShldr,text='upperBack_cnt')
		self.hipsCtrFld = mc.textFieldButtonGrp( label='Hips:',bl='Load',bc=self.loadHips,text='hip_cnt')
		self.bodyCtrFld = mc.textFieldButtonGrp( label='Body/COG:',bl='Load',bc=self.loadBody,text='cog_cnt')
		self.scaleCtrFld = mc.textFieldButtonGrp( label='World mover:',bl='Load',bc=self.loadScale,text='world_cnt')
		mc.setParent('..')
		mc.setParent('..')
		
		mc.frameLayout(label='Joints',fn='boldLabelFont',cll=False,w=450)
		mc.columnLayout()
		self.baseJntFld = mc.textFieldButtonGrp( label='Base:',bl='Load',bc=self.loadBaseJnt,text='back1')
		self.endJntFld = mc.textFieldButtonGrp( label='End:',bl='Load',bc=self.loadEndJnt,text='back6')
		mc.setParent('..')
		mc.setParent('..')
		
		mc.frameLayout(label='Options',fn='boldLabelFont',cll=False)
		mc.columnLayout()
		self.numSpansField = mc.radioButtonGrp(label="Spans on the curve?",nrb=3,labelArray3=('2','3','4'),sl=1)
		
		mc.frameLayout(label='Advanced Twist',fn='smallBoldLabelFont',cll=False,w=450)
		mc.columnLayout() 
		
		mc.rowLayout(nc=2,cw2=(100,200) )
		mc.text(' ')
		self.advUpTypeFld = mc.optionMenu(label='World Up Type')
		mc.menuItem(label='Scene Up')
		mc.menuItem(label='Object Up')
		mc.menuItem(label='Object Up (Start/End)')
		mc.menuItem(label='Object Rotation Up')
		mc.menuItem(label='Object Rotation Up (Start/End)')
		mc.menuItem(label='Vector')
		mc.menuItem(label='Vector (Start/End)')
		mc.menuItem(label='Relative')
		#Set default: Object Rotation Up (Start/End)
		mc.optionMenu(self.advUpTypeFld,edit=True,sl=5)
		mc.setParent('..')
		
		mc.rowLayout(nc=2,cw2=(100,200) )
		mc.text(' ')
		self.advUpAxisFld = mc.optionMenu(label='Up Axis')
		mc.menuItem(label='Positive Y')
		mc.menuItem(label='Negative Y')
		mc.menuItem(label='Closest Y')
		mc.menuItem(label='Positive Z')
		mc.menuItem(label='Negative Z')
		mc.menuItem(label='Closests Z')
		#Set default: Up Axis: Negative Z
		mc.optionMenu(self.advUpAxisFld,edit=True,sl=1)
		mc.setParent('..')
		
		self.upVecFld = mc.floatFieldGrp(numberOfFields=3, label='Up Vector',value1=1)
		self.upVec2Fld = mc.floatFieldGrp(numberOfFields=3, label='Up Vector 2',value1=1)
		mc.setParent('..')
		mc.setParent('..')
		
		mc.frameLayout(label='Stretchy',fn='smallBoldLabelFont',cll=False,w=450)
		mc.columnLayout()
		self.stretchyAxisFld = mc.radioButtonGrp(label='Stretchy Along',labelArray3=['X','Y','Z'],nrb=3,sl=1)
		mc.setParent('..')
		mc.setParent('..')
		
		mc.frameLayout(label='Squash/Stretch',fn='smallBoldLabelFont',cll=False,w=450)
		mc.columnLayout()
		self.squashAxisFld =  mc.checkBoxGrp( numberOfCheckBoxes=3, label='Scale Along', labelArray3=['X', 'Y', 'Z'],va3=[0,1,1] )
		mc.setParent('..')
		mc.setParent('..')
		
		mc.frameLayout(label='FK',fn='smallBoldLabelFont',cll=False,w=450)
		mc.columnLayout()
		self.fkOnOffFld = mc.radioButtonGrp(label='On?',labelArray2=['Yes','No'],nrb=2,sl=1)
		self.numFKJntsFld =  mc.intFieldGrp(label='Number of joints:',extraLabel='(2-6)',v1=4)
		self.fkCntRadiusFld =  mc.floatFieldGrp(label='Controller Radius:',v1=1)
		mc.setParent('..')
		mc.setParent('..')
		
		mc.frameLayout(label='Movable Pivot',fn='smallBoldLabelFont',cll=False,w=450)
		mc.columnLayout()
		self.mvPivOnOffFld = mc.radioButtonGrp(label='Create on Body/COG?',labelArray2=['Yes','No'],nrb=2,sl=2)
		mc.setParent('..')
		mc.setParent('..')
		
		mc.setParent('..')
		mc.setParent('..')
		
		mc.rowLayout(nc=2,cw2=(180,200) )
		mc.text(' ')
		mc.button(label='    Create Rig',w=100,c=self.createIKBack)
		mc.setParent('..')
		
		mc.setParent('..') 
		#
		# End IK Spline Rig Tab
		#
		
		#
		# Start Ribbon Spine Tab
		#
		rbbnTab = mc.columnLayout(w=450)
		
		mc.text('Under construction.')
		
		mc.setParent( '..' )
		#
		# End Ribbon Spine Tab
		#
		
		
		mc.tabLayout( tabs, edit=True, tabLabel=((ikTab, 'IKSpline'), (rbbnTab, 'Ribbon')) )
		mc.showWindow('ms_backRigWin')
		#
		# End Ribbon Spine Tab
		#
		
		
		
		
	def createIKBack(self,*args):
		"""
			Create IK spline back with user options.
		"""
		prefix = mc.textFieldGrp(self.prefixFld,query=True,text=True)
		
		shldrCnt = mc.textFieldButtonGrp(self.shldrsCtrFld,query=True,text=True)
		hipsCnt = mc.textFieldButtonGrp(self.hipsCtrFld,query=True,text=True)
		bodyCnt = mc.textFieldButtonGrp(self.bodyCtrFld,query=True,text=True)
		scaleCnt = mc.textFieldButtonGrp(self.scaleCtrFld,query=True,text=True)
		
		baseJnt = mc.textFieldButtonGrp(self.baseJntFld,query=True,text=True)
		endJnt = mc.textFieldButtonGrp(self.endJntFld,query=True,text=True)
		
		numSpans = mc.radioButtonGrp(self.numSpansField,query=True,sl=True)
		
		worldUpType = mc.optionMenu(self.advUpTypeFld,query=True,sl=True)
		upAxis = mc.optionMenu(self.advUpAxisFld,query=True,sl=True)
		upVecX = mc.floatFieldGrp(self.upVecFld,query=True,v1=True)
		upVecY = mc.floatFieldGrp(self.upVecFld,query=True,v2=True)
		upVecZ = mc.floatFieldGrp(self.upVecFld,query=True,v3=True)
		upVec2X = mc.floatFieldGrp(self.upVec2Fld,query=True,v1=True)
		upVec2Y = mc.floatFieldGrp(self.upVec2Fld,query=True,v2=True)
		upVec2Z = mc.floatFieldGrp(self.upVec2Fld,query=True,v3=True)
		
		stretchyAxis = mc.radioButtonGrp(self.stretchyAxisFld,query=True,sl=True)

		squashAxisX = mc.checkBoxGrp(self.squashAxisFld,query=True,v1=True)
		squashAxisY = mc.checkBoxGrp(self.squashAxisFld,query=True,v2=True)
		squashAxisZ = mc.checkBoxGrp(self.squashAxisFld,query=True,v3=True)
		
		fkOnOff = mc.radioButtonGrp(self.fkOnOffFld,query=True,sl=True)
		numFkJnts = mc.intFieldGrp(self.numFKJntsFld,query=True,v=True)
		radius = mc.floatFieldGrp(self.fkCntRadiusFld,query=True,v=True)
		
		mvPivOnOff = mc.radioButtonGrp(self.mvPivOnOffFld,query=True,sl=True)
		
		#Get rotate order from body controller. Should be set correctly by user.
		rotateOrder = mc.getAttr(bodyCnt + ".rotateOrder")
		
		#Create dictionary to pass with apply()
		arguments = { 'prefix':prefix,
					  'shldrCnt':shldrCnt,
					  'hipsCnt':hipsCnt,
					  'bodyCnt':bodyCnt,
					  'scaleCnt':scaleCnt,
					  'baseJnt':baseJnt,
					  'endJnt':endJnt,
					  'numSpans':numSpans,
					  'worldUpType':worldUpType,
					  'upAxis':upAxis,
					  'upVecX':upVecX,
					  'upVecY':upVecY,
					  'upVecZ':upVecZ,
					  'upVec2X':upVec2X,
					  'upVec2Y':upVec2Y,
					  'upVec2Z':upVec2Z,
					  'stretchyAxis':stretchyAxis,
					  'squashAxisX':squashAxisX,
					  'squashAxisY':squashAxisY,
					  'squashAxisZ':squashAxisZ,
					  'fkOnOff':fkOnOff,
					  'numFkJnts':numFkJnts,
					  'radius':radius,
					  'mvPivOnOff':mvPivOnOff,
					  'rotateOrder':rotateOrder
					}
		pargs=(1,2)	#No purpose besides satisfying the required list argument for the apply call.
				  
		#Call script, passing dictionary as an argument using apply()
		apply(misb.ms_ikSplineBack,pargs,arguments)



		
	#
	# Ik Spline Back Rig Tab Load Functions
	#
	def loadShldr(self,*args):
		sel = mc.ls(sl=True,fl=True)
		mc.textFieldButtonGrp(self.shldrsCtrFld,edit=True,text=sel[0])	
	def loadHips(self,*args):
		sel = mc.ls(sl=True,fl=True)
		mc.textFieldButtonGrp(self.hipsCtrFld,edit=True,text=sel[0])
	def loadBody(self,*args):
		sel = mc.ls(sl=True,fl=True)
		mc.textFieldButtonGrp(self.bodyCtrFld,edit=True,text=sel[0])
	def loadScale(self,*args):
		sel = mc.ls(sl=True,fl=True)
		mc.textFieldButtonGrp(self.scaleCtrFld,edit=True,text=sel[0])	
	def loadBaseJnt(self,*args):
		sel = mc.ls(sl=True,fl=True)
		mc.textFieldButtonGrp(self.baseJntFld,edit=True,text=sel[0])
	def loadEndJnt(self,*args):
		sel = mc.ls(sl=True,fl=True)
		mc.textFieldButtonGrp(self.endJntFld,edit=True,text=sel[0])	
        
        
        
        
        
        
        
        
        
    