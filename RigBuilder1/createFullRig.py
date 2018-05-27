from __future__ import with_statement #--- This line is only needed for 2008 and 2009
from pymel.core import *

"""
Copyright (c) 2010, 2011 Mauricio Santos-Hoyos
Name: createFullRig.py
Version: 1.1
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created: 22 Oct 2010

$Revision: 148 $
$LastChangedDate: 2011-09-27 00:43:14 -0700 (Tue, 27 Sep 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/createFullRig.py $
$Id: createFullRig.py 148 2011-09-27 07:43:14Z mauricio $

Description: 
	-Prompt user for: character name, and the number of arms, fingers, legs, 
		toes.
	-Given: number of arms, fingers, legs, toes, create head[eyes, mouth(teeth,
		tounge,jaw),ears],arms,hands,legs,feet locators for user to provide 
		placement data.
	-Build a finalized rig based on given locators and user (gui) data.
	
	Note: Mirrors rig across YZ plane.
	Note: All function calls return self.createdNodes, which is a dictionary: 
			'standard_object_names':'created_object_names'


@todo - 

		- Zero translation values on ears/teeth cnt's
		- Palm joint / Hand cup setup
		- Turn stretchy on/off (float)
		- Re-order attributes
		- FK Back controllers follow IK stretch via pointOnCurve node
		- solve mystery: // Error: Skin on hips_jnt_bind was bound at a different
		  pose. Go to the bindPose to attach new skins. // 
			-Temp fix: Change parents of bind_joints_grp
		- Set color for FK controls
		- IK/FK Matching for legs ---> AutoGUI 
		- Poses ---> AutoGUI
		- Back volume fix
		- Eliminate use of locators. Simply draw all joints once to place and orient.
		- Make rig scalable by accounting for distance dimension values changing 
			during scale. (Stretchy arms/legs IK) Back is scalable.
		- Support asymmetrical rig by placing locators for both sides,
			as an option that can be turned on or off. Right now only supporting 
			symmetrical builds, only placing left side locators, and assuming the 
			right side is the opposite, so redundant input can be avoided by client.
			- prompt user for mirroring plane, ie: YZ, XY,...
		

Additional Notes:

Left off @ self.lockAndHide


		
Example call:
	import createFullRig
	createFullRig.createFullRig()

"""
__author__ = 'Mauricio Santos'

import datetime

#--- Tools						Status							
import standardNames		#--- -- Done
import placeLocators		#--- -- Done			
import createControllers	#--- -- Done
import createArmRig			#--- -- Done					
import createHandRig		#--- -- Done
import createLegRig			#--- -- Done				
import createFootRig		#--- -- Done
import createBackRig		#--- -- Done					
import createHeadRig		#--- -- Done
import connectJointChains   #--- -- Done			
import createBindJoints		#--- -- Done
import createRigJoints		#--- -- Done
import connectJointChains   #--- -- Done
import jointLinker			#--- -- Done
import commonMayaLib		#--- -- Done
import AutoGUI				#--- -- In progress ---> Ik/Fk Matching & poses
import orientSwitch		    #--- -- Done

#--- During development.
reload( standardNames )
reload( placeLocators )			
reload( createControllers )	
reload( createArmRig )		
reload( createHandRig )		
reload( createLegRig )		
reload( createFootRig )		
reload( createBackRig )		
reload( createHeadRig )		
reload( connectJointChains )
reload( createBindJoints )
reload( createRigJoints )
reload( connectJointChains )
reload( jointLinker )
reload( AutoGUI )
reload( orientSwitch )


class createFullRigError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


class createGUIFileError(createFullRigError):
	def __str__(self):
           return "Error creating GUI file. " \
                "Ensure a directory was specified for the GUI file."

class createFullRig():
	"""
	Builds:
		- Control Rig
		- GUI Interface
	
	Internal methods call order:
	- createGUI()
	- callStep2()
	- createLocators()
	- createJoints()
	- callBuildScripts()
		- self.createHead()
		- self.createBack()
		- self.createArms()			
		- self.createHand()
		- self.createLeg()
		- self.createFoot()
		- self.createBindRig()
		- self.createRigGUI()
		- self.finishRig()
			- self.controllerVisSwitch()
			- self.lockAndHide()
			- self.orientConstraintOnHands()
			- self.orientConstraintOnHead()
			- self.patch01()
			- self.patch02()
	"""

	def __init__(self,*args):
		"""
		Run the initial prompt method.
		"""
		#--- Main version of the rig
		self.version = '1.3'
		
		#--- Library of common maya functions
		self.lib = commonMayaLib.commonMayaLib()
		
		#--- Create standard names object
		self.sNames = standardNames.standardNames()		
		
		self.createGUI()
		
	def createGUI(self,*args):
		"""
		- Main interface for rig creation script.
		- No command line interface.
		- Prompt user for rig build data via GUI.
		"""
		if(window('cfr_queryWin',exists=True)):
			deleteUI('cfr_queryWin',window=True)
			
		with window('cfr_queryWin',title=' Create Full Rig: Step 1 of 3, v%s'%self.version,rtf=True) as mainWin:
			with columnLayout():
				with columnLayout():
					self.nameField = textFieldGrp( label="Character Name (namespace): ", text='base_hm', cw = (1,200) )
					text('		Naming Notes:',font='boldLabelFont')
					text(' 		- A trailing underscore will lead to double underscores in naming.\n\n')				
					
					with frameLayout(label='Main options',cll=True,cl=False,w=500):
						with columnLayout():
							self.headFld = radioButtonGrp(l="Head?:", nrb=2, labelArray2=('Yes', 'No'), sl=1)
			
							self.backFld = radioButtonGrp(l="Back?:", nrb=2, labelArray2=('Yes', 'No'), sl=1)	
							
							self.handsFld = radioButtonGrp(l="Hands?:", nrb=2, labelArray2=('Yes', 'No'), sl=1)
							
							self.feetFld = radioButtonGrp(l="Feet?:", nrb=2, labelArray2=('Yes', 'No'), sl=1)			
							
							with rowLayout(nc=3,cw3=(200,10,30)):
								text('  How many total Arms? ( 0 -OR- 2 ): ')
								text(' ')
								self.numArmsFld = intField(value=2,min=0, max=2)
					
							with rowLayout(nc=3,cw3=(200,10,30)):
								text('  Legs? ( 0 -OR- 2 ):')
								text(' ')
								self.numLegsFld = intField(value=2,min=0, max=2)	
							with rowLayout(nc=3,cw3=(200,10,30)):
								text('  Controller scale:')
								text(' ')
								self.cntScaleFld = floatField(value=0.5,min=0)  
								
					with frameLayout(label='GUI file options',cll=True,cl=False,w=500):
						with columnLayout():
							#---@todo - Verify directory 
							tempDir = mel.eval('getenv TEMP;')
							self.saveToDirFld = textFieldButtonGrp(label='Save GUI to:',
																   bc=self.loadDir,
																   bl='Browse',
																   text = 'C:/Users/msantos/Desktop',#---tempDir,
																   cw2 = (100,200))
							self.selTypeFld = radioButtonGrp(l="Selection Type:", 
															 nrb=3, 
															 labelArray3=('add', 'tgl', 'replace'), 
															 sl=2)
					#--- @todo - 
					with frameLayout(label='Joint orient options',cll=True,cl=True,w=500):
						with columnLayout():
							self.aimFld = radioButtonGrp(l="Aim Axis:", nrb=3, labelArray3=('X', 'Y', 'Z'), sl=1)
							self.aimPolarityFld = radioButtonGrp(l="Aim Polarity:", nrb=2, labelArray2=('+', '-'), sl=1)
							self.upFld = radioButtonGrp(l="Up Axis:", nrb=3, labelArray3=('X', 'Y', 'Z'), sl=2)
							self.upPolarityFld = radioButtonGrp(l="Up Polarity:", nrb=2, labelArray2=('+', '-'), sl=1)
					
					with frameLayout(label='Arm Fk Controller options',cll=True,cl=True,w=500):
						with columnLayout():
							self.fkNormalFld = radioButtonGrp(l="Normal Axis:", nrb=3, labelArray3=('X', 'Y', 'Z'), sl=1)	
							with rowLayout(nc=3,cw3=(100,80,100)):
								text(' ')
								text('  Radius:')
								self.fkRadiusFld = floatField(value=0.1,min=0)

										
							with rowLayout(nc=2,cw2=(100,100)):
								text(' ')
								self.rotateOrderFld = optionMenu(label="Rotate Order:   ")
								menuItem(label="xyz")
								menuItem(label="yzx")
								menuItem(label="zxy")
								menuItem(label="xzy")
								menuItem(label="yxz")
								menuItem(label="zyx")
								optionMenu(self.rotateOrderFld,edit=True,sl=4)	
								
					with frameLayout(label='Fingers/Toes options',cll=True,cl=True,w=500):
						with columnLayout():
							
							with rowLayout(nc=2,cw2=(300,100)):
								text('  Fingers per hand? ( 0 -OR- 5 ):')
								self.numFingersFld = intField(value=5,min=0, max=5)	
							text('\n  Character wearing shoes? Select 0 toes.')	
							with rowLayout(nc=2,cw2=(300,100)):
								text('  Toes per foot? ( 0 -OR- 5 ):')
								self.numToesFld = intField(value=0,min=0, max=5)  								
															
							text('  Orientation Information: ',font='boldLabelFont')
							self.curlFld = radioButtonGrp(label='Curl Rotate Axis:',nrb=3,labelArray3=('x','y','z'),sl=3)
							self.twistFld = radioButtonGrp(label='Twist Rotate Axis:',nrb=3,labelArray3=('x','y','z'),sl=1)
							self.spreadFld = radioButtonGrp(label='Spread Rotate Axis:',nrb=3,labelArray3=('x','y','z'),sl=2)
			
					with frameLayout(label='Back options',cll=True,cl=True,w=500):
						with columnLayout():
							text('\n	  ---Note: Only change FK back options---	 \n',font='boldLabelFont')
							self.numSpansField = radioButtonGrp(label="Spans on the IK curve?",nrb=3,labelArray3=('2','3','4'),sl=1)	   
							with rowLayout(nc=2,cw2=(100,200) ):
								text(' ')
								self.backAdvUpTypeFld = optionMenu(label='World Up Type')
								menuItem(label='Scene Up')
								menuItem(label='Object Up')
								menuItem(label='Object Up (Start/End)')
								menuItem(label='Object Rotation Up')
								menuItem(label='Object Rotation Up (Start/End)')
								menuItem(label='Vector')
								menuItem(label='Vector (Start/End)')
								menuItem(label='Relative')
								#---Set default: Object Rotation Up (Start/End)
								optionMenu(self.backAdvUpTypeFld,edit=True,sl=5)
							
							with rowLayout(nc=2,cw2=(100,200) ):
								text(' ')
								self.advBackUpAxisFld = optionMenu(label='Up Axis')
								menuItem(label='Positive Y')
								menuItem(label='Negative Y')
								menuItem(label='Closest Y')
								menuItem(label='Positive Z')
								menuItem(label='Negative Z')
								menuItem(label='Closests Z')
								#---Set default: Up Axis: Negative Z
								optionMenu(self.advBackUpAxisFld,edit=True,sl=1)
							
							self.backUpVecFld = floatFieldGrp(numberOfFields=3, label='Up Vector',value1=1)
							self.backUpVec2Fld = floatFieldGrp(numberOfFields=3, label='Up Vector 2',value1=1)
							
							with rowLayout(nc=2,cw2=(100,100)):
								text(' ')
								self.backRotateOrderFld = optionMenu(label=" Back Rotate Order:   ")
								menuItem(label="xyz")
								menuItem(label="yzx")
								menuItem(label="zxy")
								menuItem(label="xzy")
								menuItem(label="yxz")
								menuItem(label="zyx")
								optionMenu(self.backRotateOrderFld,edit=True,sl=4)
							
							self.backStretchyAxisFld = radioButtonGrp(label='Stretchy Along',labelArray3=['X','Y','Z'],nrb=3,sl=1)					  
							self.backSquashAxisFld =  checkBoxGrp( numberOfCheckBoxes=3, label='Squash/Stretch along:', labelArray3=['X', 'Y', 'Z'],va3=[0,1,1] )
							
							text('\n	 FK Back options:   ',fn='boldLabelFont')
							self.backFkOnOffFld = radioButtonGrp(label='On?',labelArray2=['Yes','No'],nrb=2,sl=1)
							self.numBackFKJntsFld =  intFieldGrp(label='Number of joints:',extraLabel='(2-6)',v1=6)
							self.backNormalAxisFld = radioButtonGrp(label='Fk controllers normal:',labelArray3=['X','Y','Z'],nrb=3,sl=1)
							self.backFkCntRadiusFld =  floatFieldGrp(label='Controller Radius:',v1=.5)	
											 
					with rowLayout(nc=2,cw2=(200,100)):
						text(" ")
						button(label='Continue',c=self.callStep2,w=100)
						
					text('\n ')	
				
				mainWin.show()
	
	def callStep2(self,*args):
		"""
		Initialize all GUI data
		
		Translate GUI data to command data if needed.(i.e. RotateOrder shown below)
				
		Given data, place all necessary locators. One side only for now.
		Will support two side in the future, if the need for asymmetrical rigs comes up.
		"""
				
		#---Store GUI data
		self.name = textFieldGrp(self.nameField,query=True,text=True)
		
		self.head = radioButtonGrp(self.headFld,q=True,sl=True)
		self.back = radioButtonGrp(self.backFld,q=True,sl=True)
		self.hands = radioButtonGrp(self.handsFld,q=True,sl=True)
		self.feet = radioButtonGrp(self.feetFld,q=True,sl=True)
		
		self.numArms = intField(self.numArmsFld,q=True,value=True)
		self.numFingers = intField(self.numFingersFld,q=True,value=True)
		self.numLegs = intField(self.numLegsFld,q=True,value=True)
		self.numToes = intField(self.numToesFld,q=True,value=True)
		
		self.scale = floatField(self.cntScaleFld,q=True,value=True)
		
		#--- GUI options
		self.saveToDir = textFieldButtonGrp(self.saveToDirFld,query=True,text=True)
		self.selTypeVal = radioButtonGrp(self.selTypeFld,q=True,sl=True)
		
		self.selType = 0
		if self.selTypeVal == 1:
			self.selType = 'add'
		if self.selTypeVal == 2:
			self.selType = 'tgl'
		if self.selTypeVal == 3:
			self.selType = 'replace'

		#--- Joint orientation options
		self.aimAxis = radioButtonGrp(self.aimFld,q=True,sl=True)
		self.aimPolarity = radioButtonGrp(self.aimPolarityFld,q=True,sl=True)
		self.upAxis = radioButtonGrp(self.upFld,q=True,sl=True)
		self.upPolarity = radioButtonGrp(self.upPolarityFld,q=True,sl=True)
		
		#--- Arms/Legs Fk Controller options
		self.fkNormal = radioButtonGrp(self.fkNormalFld,q=True,sl=True)
		self.fkRadius = floatField(self.fkRadiusFld,q=True,value=True)
		self.rotateOrder = optionMenu(self.rotateOrderFld,query=True,sl=True)
		
		#--- Finger/Toes options
		self.curlVal = radioButtonGrp(self.curlFld,query=True,select=True)
		self.twistVal = radioButtonGrp(self.twistFld,query=True,select=True)
		self.spreadVal = radioButtonGrp(self.spreadFld,query=True,select=True)
		
		#--- Back options
		self.numSpans = radioButtonGrp(self.numSpansField,query=True,sl=True)
		
		self.worldUpType = optionMenu(self.backAdvUpTypeFld,query=True,sl=True)
		self.backUpAxis = optionMenu(self.advBackUpAxisFld,query=True,sl=True)
		
		self.upVecX = floatFieldGrp(self.backUpVecFld,query=True,value1=True)
		self.upVecY = floatFieldGrp(self.backUpVecFld,query=True,value2=True)
		self.upVecZ = floatFieldGrp(self.backUpVecFld,query=True,value3=True)
		
		self.upVec2X = floatFieldGrp(self.backUpVec2Fld,query=True,value1=True)
		self.upVec2Y = floatFieldGrp(self.backUpVec2Fld,query=True,value2=True)
		self.upVec2Z = floatFieldGrp(self.backUpVec2Fld,query=True,value3=True)  

		self.backStretchyAxis = radioButtonGrp(self.backStretchyAxisFld,query=True,sl=True)
		
		self.squashAxisX = checkBoxGrp(self.backSquashAxisFld,query=True,v1=True)
		self.squashAxisY = checkBoxGrp(self.backSquashAxisFld,query=True,v2=True)
		self.squashAxisZ = checkBoxGrp(self.backSquashAxisFld,query=True,v3=True)

		self.curlField = radioButtonGrp(label='Curl Rotate Axis:',nrb=3,labelArray3=('x','y','z'),sl=3)
		self.twistField = radioButtonGrp(label='Twist Rotate Axis:',nrb=3,labelArray3=('x','y','z'),sl=1)
		self.spreadField = radioButtonGrp(label='Spread Rotate Axis:',nrb=3,labelArray3=('x','y','z'),sl=2)

		self.fkOnOff = radioButtonGrp(self.backFkOnOffFld,query=True,sl=True)
		self.numBackFkJnts = intFieldGrp(self.numBackFKJntsFld,query=True,v=True)
		self.backNormal = radioButtonGrp(self.backNormalAxisFld,query=True,sl=True)
		self.backFkRadius = floatFieldGrp(self.backFkCntRadiusFld,query=True,v=True)
		self.backRotateOrder = optionMenu(self.backRotateOrderFld,query=True,sl=True)
		
		#--- Delete initial window
		if(window('cfr_queryWin',exists=True)):
			deleteUI('cfr_queryWin',window=True)
		
		#--- Translating GUI data to command data
		if self.rotateOrder == 1: 
			self.rotateOrder = 'xyz'
			self.rotateOrderInt = 0
		if self.rotateOrder == 2: 
			self.rotateOrder = 'yzx'
			self.rotateOrderInt = 1
		if self.rotateOrder == 3: 
			self.rotateOrder = 'zxy'
			self.rotateOrderInt = 2
		if self.rotateOrder == 4: 
			self.rotateOrder = 'xzy'
			self.rotateOrderInt = 3
		if self.rotateOrder == 5: 
			self.rotateOrder = 'yxz'
			self.rotateOrderInt = 4
		if self.rotateOrder == 6: 
			self.rotateOrder = 'zyx'   
			self.rotateOrderInt = 5	
		
		#--- BackRig specific	
		if self.backRotateOrder == 1: 
			self.backRotateOrder = 'xyz'
			self.backRotateOrderInt = 0
		if self.backRotateOrder == 2: 
			self.backRotateOrder = 'yzx'
			self.backRotateOrderInt = 1
		if self.backRotateOrder == 3: 
			self.backRotateOrder = 'zxy'
			self.backRotateOrderInt = 2
		if self.backRotateOrder == 4: 
			self.backRotateOrder = 'xzy'
			self.backRotateOrderInt = 3
		if self.backRotateOrder == 5: 
			self.backRotateOrder = 'yxz'
			self.backRotateOrderInt = 4
		if self.backRotateOrder == 6: 
			self.backRotateOrder = 'zyx'   
			self.backRotateOrderInt = 5	
			
		#--- HandRig specific
		self.curl = ''
		self.twist = ''
		self.spread = ''

		if self.curlVal == 1:
			self.curl = 'X'
		if self.curlVal == 2:
			self.curl = 'Y'
		if self.curlVal == 3:
			self.curl = 'Z'

		if self.twistVal == 1:
			self.twist = 'X'
			self.fkNormal = (1,0,0)
		if self.twistVal == 2:
			self.twist = 'Y'
			self.fkNormal = (0,1,0)
		if self.twistVal == 3:
			self.twist = 'Z'
			self.fkNormal = (0,0,1)

		if self.spreadVal == 1:
			self.spread = 'X'
		if self.spreadVal == 2:
			self.spread = 'Y'
		if self.spreadVal == 3:
			self.spread = 'Z'
	
		self.createLocators()
	
	def createLocators(self,*args):
		"""
		Place the locators in scene and prompt user to position them.
		"""
		#--- Place the locators
		pl = placeLocators.placeLocators(head = self.head,
									back = self.back,
									hands = self.hands,
									feet = self.feet,
									numArms = self.numArms,
									numFingers = self.numFingers,
									numLegs = self.numLegs,				
									numToes = self.numToes )
		
		#--- Save the dictionary of locator name lists.
		self.locators = pl.createdNodes
		
		#--- If locator names are returned
		self.allLocators = []
		
		if len(self.locators):	
			#--- @Todo - catch specific excemptions	
			try:#--- Head 
				self.allLocators.append(self.locators['head_locators'])
			except:
				pass

			try:#--- Back
				self.allLocators.append(self.locators['back_locators'])
			except:
				pass
			
			try:#--- Arm
				self.allLocators.append(self.locators['arm_locators'])
			except:
				pass
			
			try:#--- Hand
				self.allLocators.append(self.locators['hand_locators'])
			except:
				pass
			
			try:#--- Leg
				self.allLocators.append(self.locators['leg_locators'])
			except:
				pass	
			
			try:#--- Foot
				self.allLocators.append(self.locators['feet_locators'])
			except:
				pass				
														
			#--- Group them
			groupName = self.name +'_loc_grp'
			group(em=True,name=groupName)
			for each in self.allLocators:
				if len(each):
					parent(each,groupName)
			
			#--- Center the pivot of the group
			select(groupName,replace=True)
			mel.eval('CenterPivot;')
			
			#--- Create master scale controller
			self.scaleCntrl = self.createLocatorScaleControl()
			
			#--- Make the group a child of the controller curve
			parent(groupName,self.scaleCntrl)
				
		#--- Prompt user to press 'continue' once they have placed the locators.
		if(window('cfr_mainWin',exists=True)):
			deleteUI('cfr_mainWin',window=True)
			
		with window('cfr_mainWin',title='Create Full Rig: Step 2',rtf=True) as mainWin:
			with columnLayout() as mainLayout:
				text("\n	Create Full Rig: Step 2",fn='boldLabelFont',w=400)
				text("	Place locators at desired positions.")
				text("	Click 'Continue' when locators are in place.")
				
				with rowLayout(nc=2,cw2=(200,100)):
					text(" ")
					button(label='Continue',c=self.createJoints) 
				
				text(' ')
 			   
	   		mainWin.show()

	#------ Create the joints and prompt user to verify their orientation
	def createJoints(self,*args):
		"""
		Create the joints and prompt user to verify their orientation 
		"""
		#--- Delete prompt window
		if(window('cfr_mainWin',exists=True)):
			deleteUI('cfr_mainWin',window=True)
			
		#--- Hide locators
		setAttr('%s.visibility'%self.scaleCntrl[0],0)
		
		#--- Create the left side joints and prompt user to verify their orientation.
		temp = createRigJoints.createRigJoints(orientation = 'xyz',side=1, numToes = self.numToes)
		self.rigJoints = temp.rigJoints
		
		#--- Prompt user to press 'continue' once they have verified the orientations of the joints
		if(window('cfr_jointOrientWin',exists=True)):
			deleteUI('cfr_jointOrientWin',window=True)
			
		with window('cfr_jointOrientWin',title='Create Full Rig: Step 3',rtf=True) as mainWin:
			with columnLayout() as mainLayout:
				text("\n	Create Full Rig: Step 2",fn='boldLabelFont',w=400)
				text("	Verify the orientations of the joint chains.")
				text("				 Click 'Continue' when done.")
				
				with rowLayout(nc=2,cw2=(200,100)):
					text(" ")
					button( label='Continue', c = self.callBuildScripts ) 
				
				text(' ')
 			   
	   		mainWin.show()
	
	#------ Generate command line calls based on user options
	def callBuildScripts(self,*args):
		"""
		Call methods that issue command line calls to rig building scripts.
		"""
		#--- Delete prompt window
		if(window('cfr_jointOrientWin',exists=True)):
			deleteUI('cfr_jointOrientWin',window=True)
		
		#--- Create the right side joints
		temp = createRigJoints.createRigJoints(orientation = 'xyz',side=2, numToes=self.numToes)
		for joint in temp.rigJoints:
			self.rigJoints.append( joint )
		
		#--- Create the controllers
		#--- Using names defined in standardNames.py
		cnts = createControllers.createControllers( prefix = self.name, scale = self.scale, version = self.version )
		self.controls = cnts.createdNodes
		
		#--- Build the rigs
		self.createHead()
		self.createBack()
		self.createArms()			
		
		self.createLeg()
		self.createFoot()

		#--- Create joints for binding that follow the motion rig
		self.createBindRig()
		
		self.createHand()
		
		# Create locators for animators to parent things to
		self.createLimbLocators()
		
		#--- Create a GUI for the created rig using AutoGUI
		try:
			self.createRigGUI()
		except IOError:
			print "I/O error({0}): {1}".format(errno, strerror)
        
			#---raise createGUIFileError()
		
		#--- Finalize the build
		self.finishRig()

	def finishRig(self,*args):
		"""
		Stitch the various rigs together
		"""
		#--- Delete the prompt window
		if(window('frp_win',exists=True)):
			deleteUI('frp_win',window=True)		
		
		#--- Stamp with current date, rig version
		self.stampMainControl( )
		
		#--- Set legs to Ik
		setAttr( '%s.FK_IK'%self.sNames.controlNames['left_foot'],1 )
		setAttr( '%s.FK_IK'%self.sNames.controlNames['right_foot'],1 )
		
		#--- Create group for the three leg chains
		grp = group(em=True,name='leg_jnts_grp')  
			
		#--- Parent leg chains to it
		parent(self.leftLegNodes['left_ikChain'][0],grp)
		parent(self.leftLegNodes['left_fkChain'][0],grp)
		parent(self.leftLegNodes['left_followChain'][0],grp)
		parent(self.rightLegNodes['right_ikChain'][0],grp)
		parent(self.rightLegNodes['right_fkChain'][0],grp)
		parent(self.rightLegNodes['right_followChain'][0],grp)
		
		#--- Parent constrain grp to hips control, than parent to do_not_translate grp.
		parentConstraint(self.sNames.controlNames['hip'],grp,mo=True)
		parent(grp,'%s_doNotTranslate'%self.name)
		
		#--- Parent clav control buffer nodes to shoulder control
		parent('%s_buffer'%self.sNames.controlNames['left_clav'], self.sNames.controlNames['shoulder'])
		parent('%s_buffer'%self.sNames.controlNames['right_clav'], self.sNames.controlNames['shoulder'])
		
		#--- Parent controllers
		cntGrp = group(em=True,n='controls_grp')
		parent('%s_buffer'%self.sNames.controlNames['main'],cntGrp)
		
		#--- Parent clav joint to doNotTranslate
		parent(self.leftArmNodes['clavJnt'],'controls_grp')
		parent(self.rightArmNodes['clavJnt'],'controls_grp')
		
		#--- Ik controller buffer buffer nodes to main cnt
		parent('%s_buffer_buffer'%self.sNames.controlNames['right_footIk'],self.sNames.controlNames['main'])
		parent('%s_buffer_buffer'%self.sNames.controlNames['left_footIk'],self.sNames.controlNames['main'])
		parent('%s_buffer_buffer'%self.sNames.controlNames['right_armIk'],self.sNames.controlNames['main'])
		parent('%s_buffer_buffer'%self.sNames.controlNames['left_armIk'],self.sNames.controlNames['main'])
		
		parent('%s_buffer'%self.sNames.controlNames['geo_vis'], self.sNames.controlNames['main'])
		parent('%s_buffer'%self.sNames.controlNames['cnt_vis'], self.sNames.controlNames['main'])
		
		#--- Parent root to cog
		parent( self.sNames.rootJoint, self.sNames.controlNames['cog'])
		
		#--- Place all no-translate groups into a single no translate groups
		parent(self.leftArmNodes['distGrp'],self.backNodes['noTouchGrp'])
		parent(self.rightArmNodes['distGrp'],self.backNodes['noTouchGrp'])
		parent(self.leftLegNodes['distGrp'],self.backNodes['noTouchGrp'])
		parent(self.rightLegNodes['distGrp'],self.backNodes['noTouchGrp'])		
		
		#--- Create/organize additional groups
		topNode = group(em=True,n='%s_Rig'%self.name)
		skinNode = 'bind_joints_grp'
		
		#--- Parent everything to the top node
		parent('controls_grp', topNode)
		parent(self.backNodes['noTouchGrp'], topNode)
		parent(skinNode,topNode)
		
		#--- Create orientation attributes on controls
		#self.orientConstraintOnHands()
		self.orientConstraintOnHead()
		
		#--- Setup visibility switching on controls
		self.controllerVisSwitch(self)
		
		#--- Lock and hide nodes / channels not to be animated.
		self.lockAndHide()
		
		#--- PATCHES: See methods for descriptions/info.
		self.patch01()
		self.patch02()


		
	def stampMainControl(self):
		date = datetime.date.today( )
		print 'Date: ',date.today()
		# Add the attributes
		addAttr(self.sNames.controlNames['main'],at='enum',ln="Created",en=str( date.today()) + ' // yyyy-mm-dd ' )
		setAttr(self.sNames.controlNames['main'] + ".Created",keyable=True)#,type='string')
		setAttr(self.sNames.controlNames['main'] + ".Created",lock=True)
		
		addAttr(self.sNames.controlNames['main'],at='enum',ln="Version",en=self.version)
		setAttr(self.sNames.controlNames['main'] + ".Version",keyable=True)
		setAttr(self.sNames.controlNames['main'] + ".Version",lock=True)
		
	#------ Command line calls	to other tools
	def createLimbLocators(self,*args):
		"""
		Create locators at:
		- Hands
		- Cog
		- Head
		"""
		l_hand_pos = xform(self.sNames.controlNames['left_hand'],query=True,ws=True,t=True)
		r_hand_pos = xform(self.sNames.controlNames['right_hand'],query=True,ws=True,t=True)
		cog_pos = xform(self.sNames.controlNames['cog'],query=True,ws=True,t=True)
		head_pos = xform(self.sNames.headJoints['head'],query=True,ws=True,t=True)
		
		s1 = spaceLocator( n=self.sNames.controlNames['left_hand']+'_loc', p = l_hand_pos )
		s2 = spaceLocator( n=self.sNames.controlNames['right_hand']+'_loc', p = r_hand_pos )
		s3 = spaceLocator( n=self.sNames.controlNames['cog']+'_loc', p = cog_pos )
		s4 = spaceLocator( n=self.sNames.controlNames['head']+'_loc', p = head_pos )
		
		parent(s1, self.sNames.controlNames['left_hand'])
		parent(s2, self.sNames.controlNames['right_hand'])
		parent(s3, self.sNames.controlNames['cog'])
		parent(s4, self.sNames.controlNames['head'])
		
		self.lib.zero(s1)
		self.lib.zero(s2)    
		self.lib.zero(s3)    
		self.lib.zero(s4)    
		
		select(s1,r=True)
		mel.eval('CenterPivot;')    
		select(s1+'_buffer',r=True)
		mel.eval('CenterPivot;')   
		
		select(s2,r=True)
		mel.eval('CenterPivot;')    
		select(s2+'_buffer',r=True)
		mel.eval('CenterPivot;')   
		
		select(s3,r=True)
		mel.eval('CenterPivot;')    
		select(s3+'_buffer',r=True)
		mel.eval('CenterPivot;')   
		
		select(s4,r=True)
		mel.eval('CenterPivot;')  
		select(s4+'_buffer',r=True)
		mel.eval('CenterPivot;')     
		
		
		
	
	def createHead(self,*args):
		"""
		Call createHeadRig()
		@todo: 
		- Call: createFaceRig()
		"""
		temp = createHeadRig.createHeadRig( prefix=self.name,
									 rotateOrder = self.rotateOrder,
									 normal = self.fkNormal,
									 radius = self.fkRadius )
		
		self.headNodes = temp.createdNodes
		
		#--- Setup teeth controls
		# Parent the top teeth to the head
		bfr_node = self.sNames.controlNames['top_teeth'] +'_buffer'
		parent( bfr_node, self.sNames.controlNames['head'] )
		# Parent the bottom teeth to the jaw
		bfr_node = self.sNames.controlNames['btm_teeth'] +'_buffer'
		parent( bfr_node, self.sNames.controlNames['jaw'] )
		
		#--- Setup ear controls
		# Parent the left ear to the head
		bfr_node = self.sNames.controlNames['left_ear'] +'_buffer'
		parent( bfr_node, self.sNames.controlNames['head'] )
		# Parent the right ear to the head
		bfr_node = self.sNames.controlNames['right_ear'] +'_buffer'
		parent( bfr_node, self.sNames.controlNames['head'] )
		
		# zero ear controllers
		self.lib.zero( self.sNames.controlNames['left_ear'] )
		self.lib.zero( self.sNames.controlNames['right_ear'] )
		
		#--- Set eyes to follow aim controllers
		setAttr('%s.aim'%self.sNames.controlNames['head'],1)
		
	def createBack(self,*args):
		"""
		Call createBackRig()
		"""
		temp = createBackRig.createBackRig( prefix = self.name,
								shldrCnt = self.sNames.controlNames['shoulder'],
								hipsCnt = self.sNames.controlNames['hip'],
								bodyCnt = self.sNames.controlNames['cog'],
								scaleCnt = self.sNames.controlNames['main'],
								numSpans = self.numSpans,
								worldUpType = self.worldUpType,
								aim = self.aimAxis,
								aimPolarity = self.aimPolarity,
								up = self.upAxis,
								upPolarity = self.upPolarity,
								upAxis = self.backUpAxis,
								upVecX = self.upVecX,
								upVecY = self.upVecY,
								upVecZ = self.upVecZ,
								upVec2X = self.upVec2X,
								upVec2Y = self.upVec2Y,
								upVec2Z = self.upVec2Z,
								stretchyAxis = self.backStretchyAxis,
								squashAxisX = self.squashAxisX,
								squashAxisY = self.squashAxisY,
								squashAxisZ = self.squashAxisZ,
								fkOnOff = self.fkOnOff,
								numFkJnts = self.numBackFkJnts,
								fkNormal = self.backNormal,
								radius = self.backFkRadius,
								mvPivOnOff = 2,
								rotateOrder = self.backRotateOrderInt )
		
		self.backNodes = temp.createdNodes
	
	def createArms(self,*args):
		"""
		Call createArmRig()
		"""
		#--- Left arm
		temp = createArmRig.createArmRig(	prefix = 'l_arm',
										side = 1,
										shoulder = self.sNames.controlNames['shoulder'],
										cog = self.sNames.controlNames['cog'],
										head = self.sNames.controlNames['head'],
										world = self.sNames.controlNames['main'],
										hips = self.sNames.controlNames['hip'],
										hand = self.sNames.controlNames['left_hand'],
										aim_axis = self.aimAxis,
										aim_polarity = self.aimPolarity,
										up_axis = self.upAxis,
										up_polarity = self.upPolarity,
										fkNormal_axis = self.fkNormal,
										fkRadius = self.fkRadius,
										rotateOrder = self.rotateOrder )
		
		self.leftArmNodes = temp.createdNodes
		
		#--- right Arm
		temp = createArmRig.createArmRig(	prefix = 'r_arm',
											side = 2,
											shoulder = self.sNames.controlNames['shoulder'],
											cog = self.sNames.controlNames['cog'],
											head = self.sNames.controlNames['head'],
											world = self.sNames.controlNames['main'],
											hips = self.sNames.controlNames['hip'],
											hand = self.sNames.controlNames['right_hand'],
											aim_axis = self.aimAxis,
											aim_polarity = self.aimPolarity,
											up_axis = self.upAxis,
											up_polarity = self.upPolarity,
											fkNormal_axis = self.fkNormal,
											fkRadius = self.fkRadius,
											rotateOrder = self.rotateOrder )
			
		self.rightArmNodes = temp.createdNodes

	def createHand(self,*args):
		"""
		Call createHandRig()
		@Todo - pass armNodes parameters to command line call
		"""		
		select(clear=True)
		#------ Creates both hand rigs
		createHandRig.createHandRig(   l_wristFollowJnt = self.leftArmNodes['left_followChain'][2],
									   r_wristFollowJnt = self.rightArmNodes['right_followChain'][2],
									   curl = self.curl,
									   twist = self.twist,
									   spread = self.spread,
									   fkNormal = self.fkNormal,
									   radius = self.fkRadius/2.0  )	
		


	def createLeg(self,*args):
		"""
		Call createLegRig()
		"""
		#--- Left leg
		temp = createLegRig.createLegRig(	prefix = 'l_leg',
										side = 1,
										cog_cntrl = self.sNames.controlNames['cog'],
										hips_cntrl = self.sNames.controlNames['hip'],
										world_cntrl = self.sNames.controlNames['main'],
										foot_cntrl = self.sNames.controlNames['left_foot'],
										aim_axis = self.aimAxis,
										aim_polarity = self.aimPolarity,
										up_axis = self.upAxis,
										up_polarity = self.upPolarity,
										fkNormal_axis = self.fkNormal,
										fkRadius = self.fkRadius,
										rotateOrder = self.rotateOrder )
		
		self.leftLegNodes = temp.createdNodes
		
		#--- Right leg
		temp = createLegRig.createLegRig(	prefix = 'r_leg',
										side = 2,
										cog_cntrl = self.sNames.controlNames['cog'],
										hips_cntrl = self.sNames.controlNames['hip'],
										world_cntrl = self.sNames.controlNames['main'],
										foot_cntrl = self.sNames.controlNames['right_foot'],
										aim_axis = self.aimAxis,
										aim_polarity = self.aimPolarity,
										up_axis = self.upAxis,
										up_polarity = self.upPolarity,
										fkNormal_axis = self.fkNormal,
										fkRadius = self.fkRadius,
										rotateOrder = self.rotateOrder )
		
		self.rightLegNodes = temp.createdNodes	
					
	def createFoot(self,*args):
		"""
		Call createFootRig()
		"""		
		#--- Mirror left feet heel and bank locators
		rightOutterBank_loc = duplicate('l_outterBank_loc',rc=True)
		rightInnerBank_loc = duplicate('l_innerBank_loc',rc=True)
		rightHeel_loc = duplicate('l_heel_loc',rc=True)
		
		grp = group(em=True)
		parent(rightOutterBank_loc,rightInnerBank_loc,rightHeel_loc,grp)
		setAttr('%s.scaleX'%grp,-1)	
		
		select(clear=True)
		#--- Left foot
		temp = createFootRig.createFootRig(  prefix = 'l_foot',
												side = 1,
												numToes = self.numToes,
												followAnkleJnt = self.leftLegNodes['followAnkleJnt'],
												ikAnkleJnt = self.leftLegNodes['ikAnkleJnt'],
												fkAnkleJnt = self.leftLegNodes['fkAnkleJnt'],
												ballJnt = self.sNames.feetJoints['left_footBall'],
												toeJnt = self.sNames.feetJoints['left_footToe'],
												legIkHandle = self.leftLegNodes['legIkHandle'],
												ikCnt = self.leftLegNodes['ikCnt'],
												footCnt = self.leftLegNodes['footCnt'],
												heelLoc = 'l_heel_loc',
												outterBankLoc = 'l_outterBank_loc',
												innerBankLoc = 'l_innerBank_loc',
												upAxis = self.upAxis,
												aimAxis = self.aimAxis,
												fkNormal = self.fkNormal,
												fkRadius = self.fkRadius,
												outterBankVal = -80,
												innerBankVal = 80 )
		self.leftFootNodes = temp.createdNodes
		
		#--- Right foot
		temp = createFootRig.createFootRig(  prefix = 'r_foot',
												side = 2,
												numToes = self.numToes,
												followAnkleJnt = self.rightLegNodes['followAnkleJnt'],
												ikAnkleJnt = self.rightLegNodes['ikAnkleJnt'],
												fkAnkleJnt = self.rightLegNodes['fkAnkleJnt'],
												ballJnt = self.sNames.feetJoints['right_footBall'],
												toeJnt = self.sNames.feetJoints['right_footToe'],
												legIkHandle = self.rightLegNodes['legIkHandle'],
												ikCnt = self.rightLegNodes['ikCnt'],
												footCnt = self.rightLegNodes['footCnt'],
												heelLoc = rightHeel_loc,
												outterBankLoc = rightOutterBank_loc,
												innerBankLoc = rightInnerBank_loc,
												upAxis = self.upAxis,
												aimAxis = self.aimAxis,
												fkNormal = self.fkNormal,
												fkRadius = self.fkRadius,
												outterBankVal = 80,
												innerBankVal = -80 )
		self.rightFootNodes = temp.createdNodes
		
		delete(grp)
		
	def createProxyGeo(self,*args):
		"""
		Given geo:
			-Draw slice planes.
			-Prompt user to verify their placement.
			-Reduce geo.
			-Cut at edges nearest to planes. 
		"""
		#---@todo
		pass
	
	def connectProxyGeo(self,*args):
		"""
		
		"""
		#---@Todo
		pass
	
	def controllerVisSwitch(self,*args):
		"""
		Setup vis switch for controllers.
		"""		
		#------ Head: Create Head vis switch attribute
		addAttr(self.sNames.controlNames['cnt_vis'],
			  	 at='long',
			     longName='head',k=True,
			     hasMaxValue=True, hasMinValue=True,
			     defaultValue=1,
			     maxValue=1,minValue=0)
		
		#--- Direct connect to visibility of head related controllers
		connectAttr('%s.head'%self.sNames.controlNames['cnt_vis'],
				     '%s.visibility'%self.sNames.controlNames['head'],f=True)
		
		#------ Torso: Create Torso vis switch attribute
		addAttr(self.sNames.controlNames['cnt_vis'],
			  	 at='long',
			     longName='torso',k=True,
			     hasMaxValue=True, hasMinValue=True,
			     defaultValue=1,
			     maxValue=1,minValue=0)
		
		#--- Direct connect to visibility of torso related controllers
		connectAttr('%s.torso'%self.sNames.controlNames['cnt_vis'],
				     '%s.visibility'%self.sNames.controlNames['cog'],f=True)

		
		#------ L_Arm: Create Torso vis switch attribute
		addAttr(self.sNames.controlNames['cnt_vis'],
			  	 at='long',
			     longName='l_arm',k=True,
			     hasMaxValue=True, hasMinValue=True,
			     defaultValue=1,
			     maxValue=1,minValue=0)
		
		#--- Direct connect to visibility of l_arm related controllers
		connectAttr('%s.l_arm'%self.sNames.controlNames['cnt_vis'],
				     '%s.visibility'%self.leftArmNodes['ikCntBuffer'],f=True)
		
		connectAttr('%s.l_arm'%self.sNames.controlNames['cnt_vis'],
		     '%s.visibility'%self.leftArmNodes['handCntBuffer'][0],f=True)

		fkParent = listRelatives(self.leftArmNodes['left_fkChain'][0],parent=True)
		connectAttr('%s.l_arm'%self.sNames.controlNames['cnt_vis'],
		     '%s.visibility'%fkParent[0],f=True)
		
		#------ R_Arm: Create Torso vis switch attribute
		addAttr(self.sNames.controlNames['cnt_vis'],
			  	 at='long',
			     longName='r_arm',k=True,
			     hasMaxValue=True, hasMinValue=True,
			     defaultValue=1,
			     maxValue=1,minValue=0)
		
		#--- Direct connect to visibility of l_arm related controllers
		connectAttr('%s.r_arm'%self.sNames.controlNames['cnt_vis'],
				     '%s.visibility'%self.rightArmNodes['ikCntBuffer'],f=True)
		
		connectAttr('%s.r_arm'%self.sNames.controlNames['cnt_vis'],
		     '%s.visibility'%self.rightArmNodes['handCntBuffer'][0],f=True)

		fkParent = listRelatives(self.rightArmNodes['right_fkChain'][0],parent=True)
		connectAttr('%s.r_arm'%self.sNames.controlNames['cnt_vis'],
		     '%s.visibility'%fkParent[0],f=True)
		
		#------ Legs: Create Legs vis switch attribute
		addAttr(self.sNames.controlNames['cnt_vis'],
			  	 at='long',
			     longName='legs',k=True,
			     hasMaxValue=True, hasMinValue=True,
			     defaultValue=1,
			     maxValue=1,minValue=0)
		
		#--- Direct connect to visibility of legs related controllers
		connectAttr('%s.legs'%self.sNames.controlNames['cnt_vis'],
				     'leg_jnts_grp.visibility',f=True)
		connectAttr('%s.legs'%self.sNames.controlNames['cnt_vis'],
				     '%s.visibility'%self.leftLegNodes['buffer'],f=True)
		connectAttr('%s.legs'%self.sNames.controlNames['cnt_vis'],
				     '%s.visibility'%self.rightLegNodes['buffer'],f=True)
		
	        
	def lockAndHide(self,*args):
		"""
		Lock and hide nodes/channels not to be animated.
		"""
		#--- Main control scale to zero
		setAttr('%s.scaleX'%self.sNames.controlNames['main'],lock=True,keyable=False)
		setAttr('%s.scaleY'%self.sNames.controlNames['main'],lock=True,keyable=False)
		setAttr('%s.scaleZ'%self.sNames.controlNames['main'],lock=True,keyable=False)
		
		#--- Eyes follow
		setAttr('%s.visibility' % self.sNames.controlNames['eyes_follow'], lock=True, keyable=False)
		
		#--- Hand controls
		setAttr('%s.visibility' % self.sNames.controlNames['left_hand'], lock=True, keyable=False)
		setAttr('%s.visibility' % self.sNames.controlNames['right_hand'], lock=True, keyable=False)
		
		#--- Arm controls
		setAttr('%s.visibility' % self.leftArmNodes['left_fkChain'][0], lock=True, keyable=False)
		setAttr('%s.visibility' % self.rightArmNodes['right_fkChain'][0], lock=True, keyable=False)
		
	def geoVisSwitch(self,*args):
		"""
		Setup vis switch for controllers.
		"""
		#---@todo
		pass
	
	def createBindRig(self,*args):
		"""
		Creates the bind joints that follow the motion rig.
		Draw joints on locators.
		"""
		#--- Create the joints
		#---@Todo - 
		createBindJoints.createBindJoints(orientation = 'xyz',numToes = self.numToes)
		
		#--- Select all the joints in the bind group
		select('bind_joints_grp',replace=True,hi=True)
		bindJoints = ls(sl=True)
		
		#--- Select tongue rig joints
		tongueJnts = []
		temp = ls('tongue_*_jnt')
		for each in temp:
			if 'off' not in each:
				tongueJnts.append(each)
				
		#--- Add to rig joints
		for each in tongueJnts:
			self.rigJoints.append(each)
		
		#--- Delete the locators
		delete(self.scaleCntrl)
		
		#--- Connect the bind joints to the rig.
		jointLinker.jointLinker(srcJoints = self.rigJoints,
					  tgtJoints = bindJoints,
					  cType = 2, #---1=None,2=parent,3=point,4=orient,5=scale
					  slop = .1,
					  offsetVal = 1,
					  connectType = 1, #---1=Location, 2=Name
					  drivenPrefix = '',
					  driverPrefix = '',
					  namespace = ':',
					  tVal = 0,
					  rVal = 0,
					  sVal = 0 )
	
		#--- Clean up the hip bind joint
		children = listRelatives(self.sNames.hipJoint + '_' + self.sNames.suffix['bind'])
		for child in children:
			if objectType( child, isType = 'parentConstraint' ):
				delete(child)
		parentConstraint(self.sNames.hipJoint, self.sNames.hipJoint + '_' + self.sNames.suffix['bind'])
		
		#--- @ Todo - Add scale constraints to back bind joints 
#		scaleConstraint(self.sNames.backJoints['back1'], self.sNames.backJoints['back1']+'_'+self.sNames.suffix['bind'],skip="y")
#		scaleConstraint(self.sNames.backJoints['back2'], self.sNames.backJoints['back2']+'_'+self.sNames.suffix['bind'],skip="y")
#		scaleConstraint(self.sNames.backJoints['back3'], self.sNames.backJoints['back3']+'_'+self.sNames.suffix['bind'],skip="y")
#		scaleConstraint(self.sNames.backJoints['back4'], self.sNames.backJoints['back4']+'_'+self.sNames.suffix['bind'],skip="y")
#		scaleConstraint(self.sNames.backJoints['back5'], self.sNames.backJoints['back5']+'_'+self.sNames.suffix['bind'],skip="y")
		
	def orientConstraintOnHead(self, *args):
		"""
		Create an orient constrain on the head control to either follow the rig world
		orientations or those of the bind neck (local).
		"""
		#--- Left hand
		constObj = pickWalk(self.sNames.controlNames['head'], direction='up')
				
		orientSwitch.orientSwitch(   constObj=constObj,
							control=self.sNames.controlNames['head'],
							attName='orientation',
							op1Name='local',
							op2Name='world',
							op3Name='',
							op4Name='',
							op5Name='',
							op6Name='',
							op7Name='',
							op8Name='',
							object1=self.sNames.headJoints['neck1'] + '_' + self.sNames.suffix['bind'],
							object2=self.sNames.controlNames['main'],
							object3='',
							object4='',
							object5='',
							object6='',
							object7='',
							object8=''  )
		
		#--- Set world attr to 1
		setAttr( '%s.world'%self.sNames.controlNames['head'],1)
	
	
	def createRigGUI(self,*args):
		"""
		Use AutoGUI command line call to build gui for the rig
		"""
		#--- Set up groups dictionary. { "group name":objects[] } 
		grpsDict = {}
		grpsDict['Head'] =( self.sNames.controlNames['head'],
							  self.sNames.headJoints['neck2'],
							  self.sNames.headJoints['neck1'],
							  self.sNames.controlNames['jaw'],
							  self.sNames.controlNames['eyes_follow'],
							  self.sNames.controlNames['left_eye_aim'],
							  self.sNames.controlNames['right_eye_aim'],
							  self.sNames.controlNames['left_eye_fk'],
							  self.sNames.controlNames['right_eye_fk'],
							   )
		
		grpsDict['Torso'] = ( self.sNames.controlNames['shoulder'],
							  self.backNodes['fkJoints'][4],
							  self.backNodes['fkJoints'][3],
							  self.backNodes['fkJoints'][2],
							  self.backNodes['fkJoints'][1],
							  self.backNodes['fkJoints'][0],
							  self.sNames.controlNames['cog'],
							  self.sNames.controlNames['hip']) 	
							  
		grpsDict['L_Arm'] = ( self.sNames.controlNames['left_clav'],
							  self.sNames.controlNames['left_fkShoulder'],
							  self.sNames.controlNames['left_fkElbow'],
							  self.sNames.controlNames['left_fkWrist'],
							  self.sNames.controlNames['left_armIk'],
							  self.sNames.controlNames['left_hand'] )
		
		grpsDict['R_Arm'] = ( self.sNames.controlNames['right_clav'],
							  self.sNames.controlNames['right_fkShoulder'],
							  self.sNames.controlNames['right_fkElbow'],
							  self.sNames.controlNames['right_fkWrist'],
							  self.sNames.controlNames['right_armIk'],
							  self.sNames.controlNames['right_hand'] )
		
		grpsDict['L_Leg'] = ( self.sNames.controlNames['left_foot'],
							  self.sNames.controlNames['left_footIk'],
							  self.sNames.controlNames['left_fkThigh'],
					          self.sNames.controlNames['left_fkKnee'],
					          self.sNames.controlNames['left_fkAnkle'],
					          self.sNames.controlNames['left_fkFootBall'],
					          self.sNames.controlNames['left_fkFootToe']
							  ) 
		
		grpsDict['R_Leg'] = ( self.sNames.controlNames['right_foot'],
							  self.sNames.controlNames['right_footIk'],
							  self.sNames.controlNames['right_fkThigh'],
					          self.sNames.controlNames['right_fkKnee'],
					          self.sNames.controlNames['right_fkAnkle'],
					          self.sNames.controlNames['right_fkFootBall'],
					          self.sNames.controlNames['right_fkFootToe']
							  ) 
#	
#		grpsDict['Misc'] = ( self.sNames.controlNames['main'],
#							  self.sNames.controlNames['geo_vis'],
#							  self.sNames.controlNames['cnt_vis']) 
		
		temp = AutoGUI.AutoGUI(  guiName = self.name,				 #--- Name of the GUI
							selType = self.selType,			 #--- add, replace, or tgl. Defines behavior of selection buttons.
							saveToDir = self.saveToDir,	  #--- Directory to write the GUI file to
							ikFkMatch = 1,					 #--- 0, 1 = no/yes. Include ikFkMatching in GUI?
							groups = grpsDict,				  #--- Dict: { "group name":objects[] }  
							joint_up = self.upAxis,
							l_handCnt = self.sNames.controlNames['left_hand'],
							l_ikChain = self.leftArmNodes['left_ikChain'],
							l_fkChain = self.leftArmNodes['left_fkChain'],
							r_handCnt = self.sNames.controlNames['right_hand'],
							r_ikChain = self.rightArmNodes['right_ikChain'],
							r_fkChain = self.rightArmNodes['right_fkChain'] ) 
		
		#Parent distance dimension groups to do not translate
		#parent(temp.createdNodes['left_arm_match_distNode'],'%s_doNotTranslate'%self.name)
		#parent(temp.createdNodes['right_arm_match_distNode'],'%s_doNotTranslate'%self.name)

	def createLocatorScaleControl(self,*args):
		"""
		Create a circle at the origin that can be used to scale all the locators at once.
		"""
		cntName = self.name + "_locators_main_control"
		controller = circle(c=(0,0,0),nr=(0,1,0),s=8,n=cntName,r=5)
		
		return controller
	
	def loadDir(self,*args):
		"""
		Load directory to save GUI file to.
		"""
		dir = promptForFolder()
		textFieldButtonGrp(self.saveToDirFld,e=True,text=dir)
	
	#------ Patches		
	def patch01(self,*args):
		"""
		Issue: On script completion, 14 distance dimension nodes left in world space.
		
		Temp patch: group/parent them by name
		
		@Todo: Take care of in Ik/FK matching setup code. 
		"""
		x = 1
		nodes = []
		while x < 13:
			nodes.append('distanceDimension' + str(x) )
			x = x + 1
		
		#--- Group them	
		group(em=True,n='ikfk_switch_nodes_grp')
		for each in nodes:
			try:
				parent(each,'ikfk_switch_nodes_grp')
			except:
				pass
		
		#--- Parent them to do not translate node
		parent('ikfk_switch_nodes_grp','%s_doNotTranslate'%self.name)
	
	def patch02(self,*args):
		"""
		Issue 1 - Neck Bind Joint parentConstraint set to two joints.
		Fix - Set parentConstraint weight value of unwanted parent to 0.		
		"""
		#--- Fix 1
		setAttr("backEnd_jnt_bind_parentConstraint1.backEnd_jntW1", 0)	