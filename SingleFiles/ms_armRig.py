from __future__ import with_statement # This line is only needed for 2008 and 2009
import pymel.core as pm
import pymel.core.datatypes as dt
from functools import partial
"""
Name: ms_armRig.py
Author: Mauricio Santos
Contact: mauriciosantoshoyos@gmail.com
Date Created:   15 Jan 2015

Description: 
	IK/FK arm rig based on three locators

To do: 

    Elbow pin/fk forearm setup
    IK/FK Matching setup/script
    Stretchy setup


Releases:


"""
__author__ = 'mauriciosantoshoyos@gmail.com'
__version__ = 0.9

import ms_makeStretchy as mks

if __name__ == "__main__":
    ms_armRig()

class ms_armRig():
    """
    IK/FK arm rig with:
    - elbow pin
    - matching
    - forearm twist joint
    """

    def __init__(self, *args):
        self.buildGUI()

    def buildGUI(self,*args):
        """
        Create the GUI
        """
        if(pm.window("msArmRigWin", exists=True)):
            pm.deleteUI("msArmRigWin", window=True)

        with pm.window("msArmRigWin", title="Arm Rig v%s" % __version__, menuBar=True, w=400, h=600, rtf=1) as mainWin:
            with pm.menu(label="Help",helpMenu=True) as m:		
                pm.menuItem( m, label='Directions', command=self.helpWin )

            with pm.columnLayout(adj=0) as col:
                # UI elements
                self.nameFld = pm.textFieldGrp(l='Name:', text='r_arm', adj=1)
                
                pm.separator(w=500, style='out')
                
                self.loc1Fld = pm.textFieldButtonGrp(l="Shoulder Locator:", bl="Load", text='locator1', adj=1)
                pm.textFieldButtonGrp( self.loc1Fld, e=1, bc=partial(self.loadText, self.loc1Fld))
                
                self.loc2Fld = pm.textFieldButtonGrp(l="Elbow Locator:", bl="Load", text='locator2', adj=1)
                pm.textFieldButtonGrp( self.loc2Fld, e=1, bc=partial(self.loadText, self.loc2Fld))
                
                self.loc3Fld = pm.textFieldButtonGrp(l="Wrist Locator:", bl="Load", text='locator3', adj=1)
                pm.textFieldButtonGrp( self.loc3Fld, e=1, bc=partial(self.loadText, self.loc3Fld))
                
                pm.separator(w=500, style='out')
                
                self.upperTorsoFld = pm.textFieldButtonGrp(l="Upper Torso:", bl="Load", text='joint4', adj=1)
                pm.textFieldButtonGrp( self.upperTorsoFld, e=1, bc=partial(self.loadText, self.upperTorsoFld))
                
                self.lowerTorsoFld = pm.textFieldButtonGrp(l="Lower Torso:", bl="Load", text='joint2', adj=1)
                pm.textFieldButtonGrp( self.lowerTorsoFld, e=1, bc=partial(self.loadText, self.lowerTorsoFld))
                
                self.worldFld = pm.textFieldButtonGrp(l="World Mover:", bl="Load", text='joint1', adj=1)
                pm.textFieldButtonGrp( self.worldFld, e=1, bc=partial(self.loadText, self.worldFld))  
                                
                pm.separator(w=500, style='out')
                
                self.handCntFld = pm.textFieldButtonGrp(l="Switch Control:", bl="Load", text='nurbsCircle1', adj=1)
                pm.textFieldButtonGrp( self.handCntFld, e=1, bc=partial(self.loadText, self.handCntFld))                
                
                pm.separator(w=500, style='out')
                
                self.nrFld = pm.radioButtonGrp(l="FK Control Normal Axis:", nrb=3, labelArray3=('X', 'Y', 'Z'), sl=1, adj=1)
                self.rFld = pm.floatFieldGrp(l="FK Control radius:", numberOfFields=1, v1=3, adj=1)

                pm.separator(w=500, style='out')

                self.aimFld = pm.radioButtonGrp(l=' Aim Axis:', nrb=3, labelArray3=('X', 'Y', 'Z'), sl=1, adj=1)
                self.aimPolarityFld = pm.radioButtonGrp(l=' Aim Polarity:', nrb=2, labelArray2=('+', '-'), sl=1, adj=1)
                self.upFld = pm.radioButtonGrp(l=' Up Axis:', nrb=3, labelArray3=('X', 'Y', 'Z'), sl=2, adj=1)
                self.upPolarityFld = pm.radioButtonGrp(l=' Up Polarity:', nrb=2, labelArray2=('+', '-'), sl=1, adj=1)

                pm.separator(w=500, style='out')

                self.buildFld = pm.radioButtonGrp(l='Rig Build Type:', nrb=2, labelArray2=('Positive', 'Negative'), sl=2, adj=1)
                #self.stretchyFld = pm.radioButtonGrp(l="Stretchy?", nrb=2, labelArray2=('Yes', 'No'), sl=2, adj=1)

                pm.separator(w=500, style='out')

                pm.button(label="Build Rig", c=self.createArm, w=500)
                          
                
            mainWin.show()

    def createArm(self, *args):
        """
          Main process: Sets up variables and calls sub-routines
        """
        #--- Create and initialize variables with UI data
        self.getUIData()

        #--- Create joint chains
        self.buildChains()
        
        #--- Connect the chains
        self.connectChains()
        
        #--- Build IK
        self.buildIK()
        
        #--- Setup FK controls
        self.setupFKControls()
        
        #--- Arm orientation setup
        self.armOrientSetup()
        
        #--- Stretchy setup
        #if stretchy == 1:
        #    self.strecthySetup()

        #--- setup hand control
        self.handControlSetup()

        #--- clean up
        self.cleanUp()

        
    def getUIData(self, *args):
        self.prefix = pm.textFieldGrp(self.nameFld, query=True, text=True)
        
        self.loc1 = pm.textFieldButtonGrp(self.loc1Fld, query=True, text=True)
        self.loc2 = pm.textFieldButtonGrp(self.loc2Fld, query=True, text=True)
        self.loc3 = pm.textFieldButtonGrp(self.loc3Fld, query=True, text=True)

        self.shoulder = pm.textFieldButtonGrp(self.upperTorsoFld, query=True, text=True)
        self.cog = pm.textFieldButtonGrp(self.lowerTorsoFld, query=True, text=True)
        self.world = pm.textFieldButtonGrp(self.worldFld, query=True, text=True)

        self.hand_cnt = pm.textFieldButtonGrp(self.handCntFld, query=True, text=True)

        self.aim = pm.radioButtonGrp(self.aimFld,q=True,sl=True)
        self.aimPolarity = pm.radioButtonGrp(self.aimPolarityFld,q=True,sl=True)
        self.up = pm.radioButtonGrp(self.upFld,q=True,sl=True)
        self.upPolarity = pm.radioButtonGrp(self.upPolarityFld,q=True,sl=True)

        self.normal = pm.radioButtonGrp(self.nrFld, query=True, sl=True)
        self.radius = pm.floatFieldGrp(self.rFld, query=True, value1=True)

        self.build = pm.radioButtonGrp(self.buildFld, query=True, sl=True)
        #self.stretchy = pm.radioButtonGrp(self.stretchyFld, query=True, sl=True)        

    def buildChains(self, *args):
        """
        Build joint chains based on locator positions.
        """
        self.jointChain = []
        self.ikChain = []
        self.fkChain = []

        loc1Pos = pm.xform(self.loc1, q=True, ws=True, t=True)
        loc2Pos = pm.xform(self.loc2, q=True, ws=True, t=True)
        loc3Pos = pm.xform(self.loc3, q=True, ws=True, t=True)

        jnt1='%s_shldrJnt'%self.prefix
        jnt2='%s_elbow1Jnt'%self.prefix
        jnt3='%s_wristJnt'%self.prefix

        self.jointChain.append(pm.PyNode(pm.joint(p=loc1Pos, n=jnt1))) 
        self.jointChain.append(pm.PyNode(pm.joint(p=loc2Pos, n=jnt2)))
        self.jointChain.append(pm.PyNode(pm.joint(p=loc3Pos, n=jnt3)))

        #--- Orient the chain
        self.orientChain()

        #--- Creating duplicate ik/fk joint chains
        for each in pm.duplicate(self.jointChain, rc=True):
            # Slice off number maya adds during duplication
            each.rename('%s_ik' % each[:-1])
            self.ikChain.append(pm.PyNode(each))

        for each in pm.duplicate(self.jointChain, rc=True):
            each.rename('%s_fk' % each[:-1])
            self.fkChain.append(pm.PyNode(each))

    def orientChain(self, *args):
        """
        Orient the joint chain
        """
        self.aimAxis = []
        self.upAxis = []
        
        # Get locators positions
        loc1Pos = pm.xform(self.loc1, q=True, ws=True, t=True)
        loc2Pos = pm.xform(self.loc2, q=True, ws=True, t=True)
        loc3Pos = pm.xform(self.loc3, q=True, ws=True, t=True)        

        # Get normal vector for plane made by three loc positions
        v1 = dt.Vector(loc1Pos[0]-loc2Pos[0], 
                       loc1Pos[1]-loc2Pos[1],
                       loc1Pos[2]-loc2Pos[2])
        
        v2 = dt.Vector(loc1Pos[0]-loc3Pos[0], 
                       loc1Pos[1]-loc3Pos[1],
                       loc1Pos[2]-loc3Pos[2])
        
        normal_v = v2.cross(v1)

        # Initialize variables based on user input
        if self.aimPolarity == 1:
            if self.aim == 1:
                self.aim = 'X' #Used in the fk control setup
                self.aimAxis = (1,0,0)
            elif self.aim == 2:
                self.aim = 'Y'
                self.aimAxis = (0,1,0)
            elif self.aim == 3:
                self.aim = 'Z'
                self.aimAxis = (0,0,1)
        else:
            if self.aim == 1:
                self.aim = 'X'
                self.aimAxis = (-1,0,0)
            elif self.aim == 2:
                self.aim = 'Y'
                self.aimAxis = (0,-1,0)
            elif self.aim == 3:
                self.aim = 'Z'
                self.aimAxis = (0,0,-1)

        if self.up == 1:
            self.upAxis = (1,0,0)
        elif self.up == 2:
            self.upAxis = (0,1,0)
        elif self.up == 3:
            self.upAxis = (0,0,1)

        if self.upPolarity == 1:
            self.upPolarity = 1
        elif self.upPolarity == 2:
            self.upPolarity = -1

        for joint in self.jointChain:
            # Get child of joint
            childJnt = pm.listRelatives(joint, c=True)
            
            # Set the last joint to "None" orientation and end the loop
            if not len(childJnt):
                if self.up == 1:
                    self.upAxis = "xup"
                elif self.up == 2:
                    self.upAxis = "yup"
                elif self.up == 3:
                    self.upAxis = "zup"

                pm.joint(joint, e=True, oj='none', secondaryAxisOrient=self.upAxis, zso=True, ch=True)
                break

            # Unparent child (aim target) so it retains its 
            # position during the reorientation of it's parent
            pm.parent(childJnt[0], w=True)

            # Zero Orients and Rotations on joint
            pm.setAttr(joint + ".rotate", 0, 0, 0)
            pm.setAttr(joint + ".jointOrient", 0, 0, 0)            
            
            #Create locator, snap to joint
            up_loc = pm.spaceLocator()
            self.snapping(up_loc, joint)
            
            #Match locator orientations to joint
            pm.delete(pm.orientConstraint(joint, up_loc))

            #Move locator 1 in normal direction
            pm.move(normal_v.x, normal_v.y, normal_v.z, up_loc, moveXYZ=True, r=1)

            #The Aim constriant
            pm.delete(pm.aimConstraint(childJnt[0],
                                       joint,
                                       aimVector=self.aimAxis,
                                       upVector=self.upAxis,
                                       worldUpType="object",
                                       worldUpObject=up_loc))
            pm.delete(up_loc)

            #Copy Joint Rotations and Paste to Joint Orients
            #and then Set joint Rotations to 0,0,0

            tempRotations = pm.getAttr(joint + ".rotate")
            pm.setAttr(joint + ".rotate", 0, 0, 0)
            pm.setAttr(joint + ".jointOrient", tempRotations[0], tempRotations[1], tempRotations[2])

            pm.parent(childJnt[0], joint)
            
    def jointOrientToPlane(self, jnt=None, normal=None, upAxis=None):
        ''' Orient given joint so it's up axis matches the normal vector passed in. '''
               

    def buildIK(self, *args):
        """
            Build the IK
        """
        #Setup variables
        if self.normal == 1:
            self.normal = (1, 0, 0)
        if self.normal == 2:
            self.normal = (0, 1, 0)
        if self.normal == 3:
            self.normal = (0, 0, 1)   

        #Create IK control
        self.ikControl = pm.circle(nr=self.normal, r=self.radius, n='%s_ikCnt'%self.prefix)
        pm.select(self.ikControl[0], r=True)
        pm.mel.eval("DeleteHistory;")
        pm.delete( pm.parentConstraint(self.ikChain[2], self.ikControl[0], mo=0) )
        self.zero(self.ikControl[0])               

        #Create RP IK
        self.arm_ikHandle = pm.ikHandle(sj=self.ikChain[0], ee=self.ikChain[2], solver='ikRPsolver', name=(self.prefix + '_armIkHandle'))
        pm.setAttr(self.arm_ikHandle[0] + '.visibility', 0)

        #Parent IK Handle to the ikWrist_cnt
        pm.parent(self.arm_ikHandle[0], self.ikControl[0])

        # Creates: self.pv_cnt
        self.createPoleVector()

    def setupFKControls(self, *args):
        """
            Create FK controllers
        """

        #shoulder
        temp = pm.PyNode(pm.circle(nr=self.normal, r=self.radius)[0])
        pm.parent(temp, self.fkChain[0]) #Parent transform under fk joint
        pm.move(0, 0, 0, temp) #Zero it so it snaps to FK position/orientation
        pm.parent(temp.getShape(), self.fkChain[0], s=True, r=True) #Parent shape to joints transform
        pm.delete(temp)   #Delete empty transform

        #elbow
        temp = pm.PyNode(pm.circle(nr=self.normal, r=self.radius)[0])
        pm.parent(temp, self.fkChain[1]) #Parent transform under fk joint
        pm.move(0, 0, 0, temp) #Zero it so it snaps to FK position/orientation
        pm.parent(temp.getShape(), self.fkChain[1], s=True, r=True) #Parent shape to joints transform
        pm.delete(temp)   #Delete empty transform

        #wrist
        temp = pm.PyNode(pm.circle(nr=self.normal, r=self.radius)[0])
        pm.parent(temp, self.fkChain[2]) #Parent transform under fk joint
        pm.move(0, 0, 0, temp) #Zero it so it snaps to FK position/orientation
        pm.parent(temp.getShape(), self.fkChain[2], s=True, r=True) #Parent shape to joints transform
        pm.delete(temp)   #Delete empty transform

        #
        # FK Length attributes setup/ Done using the translates of the child to avoid skewing that
        # occurs with scaling in a non-uniform manner (1,2,1)
        #
        pm.addAttr(self.fkChain[0], ln='length', min=0, dv=1, k=True)
        pm.addAttr(self.fkChain[1], ln='length', min=0, dv=1, k=True)

        #Get current translates value to set the max SDK as twice the default length
        val1 = pm.getAttr('%s.translate%s' % (self.fkChain[1], self.aim))
        val2 = pm.getAttr('%s.translate%s' % (self.fkChain[2], self.aim))

        #SDK to connect them
        pm.setDrivenKeyframe(self.fkChain[1], cd='%s.length' % self.fkChain[0], at='translate%s' % self.aim, dv=1) #Set default with current value in .tx
        pm.setDrivenKeyframe(self.fkChain[1], cd='%s.length' % self.fkChain[0], at='translate%s' % self.aim, dv=0, v=0)         #Set min
        pm.setDrivenKeyframe(self.fkChain[1], cd='%s.length' % self.fkChain[0], at='translate%s' % self.aim, dv=2, v=(val1 * 2)) #Set max

        pm.setDrivenKeyframe(self.fkChain[2], cd='%s.length' % self.fkChain[1], at='translate%s' % self.aim, dv=1) #Set default with current value in .tx
        pm.setDrivenKeyframe(self.fkChain[2], cd='%s.length' % self.fkChain[1], at='translate%s' % self.aim, dv=0, v=0)         #Set min
        pm.setDrivenKeyframe(self.fkChain[2], cd='%s.length' % self.fkChain[1], at='translate%s' % self.aim, dv=2, v=(val2 * 2))#Set max

    def armOrientSetup(self, *args):
        """
         Setup following rotations linked to : world, cog, shoulders
        """

        shldr_loc = '%s_shldrLoc' % self.prefix
        pm.spaceLocator(n=shldr_loc)

        shldr_torso_orient_loc = '%s_torsoLoc' % self.prefix #Follows back
        pm.spaceLocator(n=shldr_torso_orient_loc)

        shldr_cog_orient_loc = '%s_cogLoc' % self.prefix  #Follows body
        pm.spaceLocator(n=shldr_cog_orient_loc)        

        pm.delete(pm.pointConstraint(self.fkChain[0], shldr_loc, mo=0))
        pm.delete(pm.pointConstraint(self.fkChain[0], shldr_torso_orient_loc, mo=0))
        pm.delete(pm.pointConstraint(self.cog, shldr_cog_orient_loc, mo=0))

        #Place locators in the hierarchy
        pm.parent(shldr_loc, self.shoulder) #This is the locator that switches between the other two.The entire FK/IK/Bind arms parent'd to this guy.
        pm.parent(shldr_torso_orient_loc, self.shoulder) #Parent to the same joint that shldr_loc is parent'd to.
        pm.parent(shldr_cog_orient_loc, self.cog) #Parent to cog that will move the arm with the torso      

        pm.parent(self.fkChain[0], shldr_loc)
        pm.parent(self.ikChain[0], shldr_loc) #So the IK arm follows along
        pm.parent(self.jointChain[0], shldr_loc) #So this guy plays too

        # Create the constraint that will switch fk arm orientation behavior.
        rotConst = pm.PyNode( pm.orientConstraint(shldr_torso_orient_loc, 
                                       shldr_cog_orient_loc, 
                                       self.world, shldr_loc, 
                                       mo=True))

        #Create switching attribute
        fkChainRoot = pm.PyNode(self.fkChain[0])
        
        pm.addAttr(fkChainRoot, ln='FK_Arm_Follow', k=True)
        fkChainRoot.setAttr('FK_Arm_Follow', l=True)
        pm.addAttr(fkChainRoot, ln='World', k=True, min=0, max=1)
        pm.addAttr(fkChainRoot, ln='COG', k=True, min=0, max=1)
        pm.addAttr(fkChainRoot, ln='Torso', k=True, min=0, max=1)
        
        #SDK's to set this constraint
        attrs = pm.listAttr(rotConst)
        fkChainRoot.Torso >> rotConst.listAttr()[-3]
        fkChainRoot.COG >> rotConst.listAttr()[-2]
        fkChainRoot.World >> rotConst.listAttr()[-1]

    def stretchySetup(self, *args):
        #""" Comment this block out when building on negative quadrant. Creates strange .t values on IK chain. Need to figure out.
        #
        #--- Call ms_makeStretchy for ik setup
        #
        # Create dictionary to pass with apply()
        #buildAlong = 'positive'

        arguments = {'ikHandle':arm_ikHandle[0],
                     'solverType':1,
                     'aimAxis':aim,
                     'clusters':2,
                     'stretchVal':1,
                     'prefix':(prefix),
                     'jointChain':ikChain,
                     'kneeNum':self.elbowNum,
                     'build': build
                     }
        pargs = (1, 2)	#No purpose besides satisfying the required list argument for the apply call.

        select(clear=True)
        #Call script, passing dictionary as an argument using apply()
        apply(mks.ms_makeStretchy, pargs, arguments)

    def handControlSetup(self, *args):
        """
         Create attributes on hand_cnt and connect them as needed.
        """
        pm.addAttr(self.hand_cnt,ln='FK_IK',at='float',dv=0,min=0,max=1,k=True)

        # IK/FK blend color nodes
        pm.connectAttr( '%s.FK_IK'%self.hand_cnt, '%s.blender'%self.shldr_node1 )

        pm.connectAttr( '%s.FK_IK'%self.hand_cnt, '%s.blender'%self.elbow1_node1 )
        pm.connectAttr( '%s.FK_IK'%self.hand_cnt, '%s.blender'%self.elbow1_node2 )

        pm.connectAttr( '%s.FK_IK'%self.hand_cnt, '%s.blender'%self.wrist_node1 )
        pm.connectAttr( '%s.FK_IK'%self.hand_cnt, '%s.blender'%self.wrist_node2 )

        #IK/FK controls vis switch
        pm.connectAttr( '%s.FK_IK'%self.hand_cnt, '%s.visibility'%self.ikChain[0] )
        pm.connectAttr( '%s.FK_IK'%self.hand_cnt, '%s.visibility'%self.ikControl[0] )
        pm.setDrivenKeyframe(self.fkChain[0], cd='%s.FK_IK' % self.hand_cnt, at='visibility', dv=1, v=0)
        pm.setDrivenKeyframe(self.fkChain[0], cd='%s.FK_IK' % self.hand_cnt, at='visibility', dv=0, v=1)

        # Zero hand control and parent to the following joint chian.
        self.zero(self.hand_cnt)
        bufferNode = pm.listRelatives(self.hand_cnt,parent=True)
        pm.parentConstraint(self.jointChain[2],bufferNode,mo=True)

    def connectChains(self,*args):
        """
            Set elbows to only rotate in one axis, the upAxis.
            Create blend color nodes and connect ik/fk/bind joint chains.
        """

        #Shoulder blendColors creation
        self.shldr_node1 = pm.PyNode((pm.createNode( 'blendColors' )).rename('%s_shldrRotate' % self.prefix))

        #shldr_node1 attributes to connect
        self.ikChain[0].rotate >> self.shldr_node1.color1
        self.fkChain[0].rotate >> self.shldr_node1.color2
        self.shldr_node1.output >> self.jointChain[0].rotate

        #elbow1 blendColors creation
        self.elbow1_node1 = pm.PyNode((pm.createNode( 'blendColors' )).rename('%s_elbow1Rotate' % self.prefix))
        self.elbow1_node2 = pm.PyNode((pm.createNode( 'blendColors' )).rename('%s_elbow1Translate' % self.prefix))

        #elbow1_node1 attributes to connect
        self.ikChain[1].rotate >> self.elbow1_node1.color1
        self.fkChain[1].rotate >> self.elbow1_node1.color2
        self.elbow1_node1.output >> self.jointChain[1].rotate        
        
        #elbow1_node2 attributes to connect
        self.ikChain[1].translate >> self.elbow1_node2.color1
        self.fkChain[1].translate >> self.elbow1_node2.color2
        self.elbow1_node2.output >> self.jointChain[1].translate          

        #wrist blendColors creation
        self.wrist_node1 = pm.PyNode((pm.createNode( 'blendColors' )).rename('%s_elbow1Rotate' % self.prefix))
        self.wrist_node2 = pm.PyNode((pm.createNode( 'blendColors' )).rename('%s_elbow1Translate' % self.prefix))

        #wrist_node1 attributes to connect
        self.ikChain[2].rotate >> self.wrist_node1.color1
        self.fkChain[2].rotate >> self.wrist_node1.color2
        self.wrist_node1.output >> self.jointChain[2].rotate        
        
        #wrist_node2 attributes to connect
        self.ikChain[2].translate >> self.wrist_node2.color1
        self.fkChain[2].translate >> self.wrist_node2.color2
        self.wrist_node2.output >> self.jointChain[2].translate  

        #Lock elbow axis
        if self.up == 1:
            pm.setAttr('%s.rotateY'%self.fkChain[1],lock=True,k=False) 
            pm.setAttr('%s.rotateZ'%self.fkChain[1],lock=True,k=False) 
            pm.setAttr('%s.rotateY'%self.ikChain[1],lock=True,k=False) 
            pm.setAttr('%s.rotateZ'%self.ikChain[1],lock=True,k=False) 
        if self.up == 2:
            pm.setAttr('%s.rotateX'%self.fkChain[1],lock=True,k=False) 
            pm.setAttr('%s.rotateZ'%self.fkChain[1],lock=True,k=False) 
            pm.setAttr('%s.rotateX'%self.ikChain[1],lock=True,k=False) 
            pm.setAttr('%s.rotateZ'%self.ikChain[1],lock=True,k=False) 
        if self.up == 3:
            pm.setAttr('%s.rotateY'%self.fkChain[1],lock=True,k=False) 
            pm.setAttr('%s.rotateX'%self.fkChain[1],lock=True,k=False) 
            pm.setAttr('%s.rotateY'%self.ikChain[1],lock=True,k=False) 
            pm.setAttr('%s.rotateX'%self.ikChain[1],lock=True,k=False)     

    def createPoleVector(self,*args):
        """
        	Create the pole vector control curve.
        	Create plane with points on shoulder, elbow and wrist.
        	Translate elbow point of plane along the normal,
        	then snap the control curve to the point.
        	Zero controller and setup elbow attribute on ikControl
        """
        self.pv_cnt = '%s_pv_cnt' % self.prefix

        if self.up == 1:
            self.upAxis = (1,0,0)
        if self.up == 2:
            self.upAxis = (0,1,0)
        if self.up == 3:
            self.upAxis = (0,0,1)

        #Create the pole vector control curve
        melString = 'createNode transform -n "%s";' % self.pv_cnt 
        melString = melString + 'setAttr ".ove" yes;'
        melString = melString + 'setAttr ".ovc" 15;'
        melString = melString + 'createNode nurbsCurve -n "%sShape1" -p "%s";' % (self.pv_cnt,self.pv_cnt)
        melString = melString + 'setAttr -k off ".v";'
        melString = melString + 'setAttr ".cc" -type "nurbsCurve"'
        melString = melString + '	1 7 0 no 3'
        melString = melString + '	8 0 1 2 3 4 5 6 7'
        melString = melString + '	8'
        melString = melString + '	-2 0 0'
        melString = melString + '	1 0 1'
        melString = melString + '	1 0 -1'
        melString = melString + '	-2 0 0'
        melString = melString + '	1 1 0'
        melString = melString + '	1 0 0'
        melString = melString + '	1 -1 0'
        melString = melString + '	-2 0 0'

        pm.mel.eval( melString )

        #Get locators positions
        loc1Pos = pm.xform(self.loc1,q=True,ws=True,t=True)
        loc2Pos = pm.xform(self.loc2,q=True,ws=True,t=True)
        loc3Pos = pm.xform(self.loc3,q=True,ws=True,t=True)

        # Get Move vector
        mid_point = ((loc1Pos[0]+loc3Pos[0]) / 2.0, 
             (loc1Pos[1]+loc3Pos[1]) / 2.0,
             (loc1Pos[2]+loc3Pos[2]) / 2.0)
        move_vec = dt.Vector(loc2Pos[0]-mid_point[0],
                             loc2Pos[1]-mid_point[1],
                             loc2Pos[2]-mid_point[2])
        move_vec.normalize()
        move_vec *= 10
        
        #move pv_cnt to the vert
        pm.move(loc2Pos[0], loc2Pos[1], loc2Pos[2], self.pv_cnt, moveXYZ=True)
        pm.move(move_vec[0], move_vec[1], move_vec[2], self.pv_cnt, r=1, moveXYZ=True)
        self.zero(self.pv_cnt)

        #Create the constraint
        pm.poleVectorConstraint(self.pv_cnt, self.arm_ikHandle[0])

        #Get buffer group of pv, create new group and snap it to ikControl
        pv_buffer = pm.listRelatives(self.pv_cnt, parent=True)
        pv_parent = pm.group(n='%sprnt' % pv_buffer, world=True, em=True)
        self.snapping( pv_parent, self.ikControl[0] )

        #Create locator, snap to pv_parent
        locTemp = pm.spaceLocator()
        loc = pm.spaceLocator(n='%s_pvAim_loc'%self.prefix)
        self.snapping(locTemp, pv_buffer)
        self.snapping(loc, pv_parent)
        
        #Match locator orientations to pv_parent
        temp = pm.orientConstraint(pv_buffer, locTemp)
        pm.delete(temp)
        temp = pm.orientConstraint(pv_parent, loc)
        pm.delete(temp)

        #Move locator 1 in up direction
        if self.up == 1:
            pm.move(self.upPolarity, loc, x=1, r=1)
        if self.up == 2:
            pm.move(self.upPolarity, loc, y=1, r=1)
        if self.up == 3:
            pm.move(self.upPolarity, loc, z=1, r=1)

        #Aim buffer at elbow
        temp = pm.aimConstraint(self.jointChain[1],
                                pv_buffer,
                                aimVector=self.aimAxis,
                                upVector=self.upAxis,
                                worldUpType="object",
                                worldUpObject=locTemp)
        pm.delete(temp)
        pm.delete(locTemp)        

        #Aim pv_parent at shoulder 
        temp = pm.aimConstraint(self.jointChain[0],
                                pv_parent,
                                aimVector=self.aimAxis,
                                upVector=self.upAxis,
                                worldUpType="object",
                                worldUpObject=loc)

        #Hide the up locator
        pm.setAttr('%s.visibility'%loc, 0)

        #point constraint pv_parent to ik_control
        pm.pointConstraint(self.ikControl[0], pv_parent, mo=True)

        #PV elbow twist/ vis switch
        pm.addAttr(self.ikControl[0], ln='elbow', k=True, at='float')
        pm.connectAttr('%s.elbow' % self.ikControl[0], '%s.rotateX' % pv_parent, f=True)
        pm.addAttr(self.ikControl[0], ln='pv_vis', k=True, at='short',hasMinValue=True,hasMaxValue=True,min=0,max=1,dv=1)
        pm.connectAttr('%s.pv_vis' % self.ikControl[0], '%s.visibility' % self.pv_cnt, f=True)

        #Parent the buffer grp to the parent grp
        pm.parent(pv_buffer, pv_parent)

        #scale pv_cnt aim -1 so it points at the elbow
        pm.setAttr('%s.scale%s' % (self.pv_cnt, self.aim), -1)
        pm.makeIdentity(self.pv_cnt, scale=True, apply=True)

    def cleanUp(self,*args):
        """
            Lock and hide attributes as needed and delete setup locators
        """
        #FK Controls
        pm.setAttr('%s.translateX' % self.fkChain[0], lock=True, keyable=False)
        pm.setAttr('%s.translateY' % self.fkChain[0], lock=True, keyable=False)
        pm.setAttr('%s.translateZ' % self.fkChain[0], lock=True, keyable=False)

        pm.setAttr('%s.scaleX' % self.fkChain[0], lock=True, keyable=False)
        pm.setAttr('%s.scaleY' % self.fkChain[0], lock=True, keyable=False)
        pm.setAttr('%s.scaleZ' % self.fkChain[0], lock=True, keyable=False)
        pm.setAttr('%s.visibility' % self.fkChain[0], keyable=False)
        pm.setAttr('%s.radius' % self.fkChain[0], lock=True, cb=False)

        pm.setAttr('%s.translateX' % self.fkChain[1], keyable=False) #This channel connected to length
        pm.setAttr('%s.translateY' % self.fkChain[1], lock=True, keyable=False)
        pm.setAttr('%s.translateZ' % self.fkChain[1], lock=True, keyable=False)

        pm.setAttr('%s.scaleX' % self.fkChain[1], keyable=False) 
        pm.setAttr('%s.scaleY' % self.fkChain[1], lock=True, keyable=False)
        pm.setAttr('%s.scaleZ' % self.fkChain[1], lock=True, keyable=False)
        pm.setAttr('%s.visibility' % self.fkChain[1], lock=True, keyable=False)
        pm.setAttr('%s.radius' % self.fkChain[1], lock=True, cb=False)

        pm.setAttr('%s.translateX' % self.fkChain[2], keyable=False) #This channel connected to length
        pm.setAttr('%s.translateY' % self.fkChain[2], lock=True, keyable=False)
        pm.setAttr('%s.translateZ' % self.fkChain[2], lock=True, keyable=False)

        pm.setAttr('%s.scaleX' % self.fkChain[2], keyable=False) 
        pm.setAttr('%s.scaleY' % self.fkChain[2], lock=True, keyable=False)
        pm.setAttr('%s.scaleZ' % self.fkChain[2], lock=True, keyable=False)
        pm.setAttr('%s.visibility' % self.fkChain[2], lock=True, keyable=False)
        pm.setAttr('%s.radius' % self.fkChain[2], lock=True, cb=False)

        #Hand control
        pm.setAttr('%s.scaleX' % self.hand_cnt, lock=True, keyable=False) 
        pm.setAttr('%s.scaleY' % self.hand_cnt, lock=True, keyable=False)
        pm.setAttr('%s.scaleZ' % self.hand_cnt, lock=True, keyable=False)
        pm.setAttr('%s.visibility' % self.hand_cnt, keyable=False)

        #IK control
        pm.setAttr('%s.scaleX' % self.ikControl[0], lock=True, keyable=False)
        pm.setAttr('%s.scaleY' % self.ikControl[0], lock=True, keyable=False)
        pm.setAttr('%s.scaleZ' % self.ikControl[0], lock=True, keyable=False)
        pm.setAttr('%s.visibility' % self.ikControl[0], keyable=False)

        #pv_cnt
        pm.setAttr('%s.rotateX' % self.pv_cnt, lock=True, keyable=False)
        pm.setAttr('%s.rotateY' % self.pv_cnt, lock=True, keyable=False)
        pm.setAttr('%s.rotateZ' % self.pv_cnt, lock=True, keyable=False)        

        pm.setAttr('%s.scaleX' % self.pv_cnt, lock=True, keyable=False)
        pm.setAttr('%s.scaleY' % self.pv_cnt, lock=True, keyable=False)
        pm.setAttr('%s.scaleZ' % self.pv_cnt, lock=True, keyable=False)
        pm.setAttr('%s.visibility' % self.pv_cnt, keyable=False)

        #Delete setup locators
        pm.delete(self.loc1)
        pm.delete(self.loc2)
        pm.delete(self.loc3)


    def snapping(self,a,b,*args):
        """
            Snap a to b
        """

        pos = pm.xform( b, q=1, ws=True, t=1)
        pm.xform( a, ws=True, t=[pos[0], pos[1], pos[2]])

        rot = pm.xform( b, q=1, ws=True, ro=1)
        pm.xform( a, ws=True, ro=[rot[0], rot[1], rot[2]])

    def zero(self,obj,*args):
        """
            Zero object and create a buffer node for obj.
        """
        parent = pm.listRelatives(obj,parent=True)

        name = '%s_buffer'%obj
        zeroNode = pm.group(em=True,n=name)

        pos = pm.xform( obj, q=1, ws=True, t=1)
        pm.xform( zeroNode, ws=True, t=[pos[0], pos[1], pos[2]])

        rot = pm.xform( obj, q=1, ws=True, ro=1)
        pm.xform( zeroNode, ws=True, ro=[rot[0], rot[1], rot[2]])

        scale = pm.xform( obj, q=1, r=True, s=1)
        pm.xform( zeroNode, ws=True, s=[scale[0], scale[1], scale[2]])

        pm.parent(obj, zeroNode, a=True)
        try:
            pm.parent(zeroNode, parent)
        except:
            pass

    def loadText(self, fld=None, typ=None): 
        if typ:
            locName = pm.ls(sl=True, type=typ)
        else:
            locName = pm.ls(sl=True)
        pm.textFieldGrp(fld, edit=True, text=locName[0])


    def helpWin(self,*args):
        """
         Display the help window
        """
        if(pm.window('msArmRigHelpWin',exists=True)):
            pm.deleteUI('msArmRigHelpWin',window=True)

        with pm.window('msArmRigHelpWin',title="Arm Rig Help",rtf=True) as mainWin:
            with pm.columnLayout():
                pm.text('   Locators should be placed for:')
                pm.text('               Shoulder')
                pm.text('               Elbow')
                pm.text('               Wrist')
                pm.text('\n')
                pm.text('   Upper Torso: Shoulder insertion. Clavicle or upper back joint.')
                pm.text('   Lower Torso: COG or something following the root.')
                pm.text('   World Mover: World mover control or equivalent.')
                pm.text('   (Used for space switch setup).')
                pm.text('\n')
                pm.text('   Switch Control: Place IK / FK switch on this control, usually the Hand control.')
                pm.text('   Switch control should be in place and zeroed.')
                pm.text('\n')
                pm.text('   Note: Locators should not be zeroed. They should have their world space')
                pm.text('   values in their translate attributes in the channel box.')        
                pm.text('\n')

                mainWin.show()


