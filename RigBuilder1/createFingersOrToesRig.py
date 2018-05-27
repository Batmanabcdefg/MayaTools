from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *

"""
Copyright (c) 2010 Mauricio Santos
Name: createFingersOrToesRig.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created:   22 Oct 2010

$Revision: 136 $
$LastChangedDate: 2011-08-29 01:35:29 -0700 (Mon, 29 Aug 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/createFingersOrToesRig.py $
$Id: createFingersOrToesRig.py 136 2011-08-29 08:35:29Z mauricio $

Description: 
    Given:
        Controller
        start + end joint for each finger
        Names for each finger
        
        Create attributes to drive the fingers on the controller, and FK controls
        on the finger joints.
    
Used by: createArmRig.py, createFootRig.

Uses:

Process:
    
Additional Notes: 

Example call:
    import createFingersOrToesRig
    temp = createFingersOrToesRig.createFingersOrToesRig( label = self.label,  
                                                       control = self.control,
                                                       attNames = attNames,
                                                       startJnts = startJnts,
                                                       endJnts = endJnts,
                                                       curl = self.curl,
                                                       twist = self.twist,
                                                       spread = self.spread,
                                                       fkNormal = self.fkNormal,
                                                       radius = self.radius )
        
    jointRoots = temp.createdNodes
    
Attributes:
    createdNodes = list of created nodes.

Keywords:
        self.label = keywords['label']
        self.control = keywords['control']
        
        # Ordered lists
        self.attNames = keywords['attNames']
        self.startJnts = keywords['startJnts']
        self.endJnts = keywords['endJnts']

        self.curl = keywords['aim']
        self.twist = keywords['twist']
        self.spread = keywords['spread']
        
        # (0.0, 0.0, 0.0)
        self.fkNormal = keywords['fkNormal']
             
Requires:

Development notes:

    @todo - 
    
"""
class createFingersOrToesRig():
    """
        Create attributes to drive the fingers on the controller, and FK controls
        on the finger joints.
    """
    def __init__(self,**keywords):
        # Used to store names of all created nodes, 
        # to be returned when the tool is done.
        self.createdNodes = [] 
        
        # Check if command line call
        if len(keywords):
            self.commandlineCall(keywords)
        else:
            self.buildGUI()
            
    def commandlineCall(self,keywords):
        """
        Verify and Store the data passed via command line keywords dictionary.
        """        
        self.label = keywords['label']
        self.control = keywords['control']
        
        # Ordered lists
        self.attNames = keywords['attNames']
        self.startJnts = keywords['startJnts']
        self.endJnts = keywords['endJnts']

        self.curl = keywords['curl']
        self.twist = keywords['twist']
        self.spread = keywords['spread']
        
        # (0.0, 0.0, 0.0)
        self.fkNormal = keywords['fkNormal']
        self.radius = keywords['radius']
        
        self.create()

    def buildGUI(self,*args):
        """
        Prompt user to enter the number of limbs.
        """
        if(window("createFingersOrToesRigWin",exists=True)):
                deleteUI("createFingersOrToesRigWin",window=True)
        
        with window("createFingersOrToesRigWin",title="Create Fingers Or Toes Rig v1.0",rtf=True) as mainWin:
            with formLayout() as form:
                
                text('How many joint chains?',font='boldLabelFont')
                
                with rowLayout(nc=2,cw2=(20,100)):
                    text(" ")
                    self.numChainsFld = intField(v=5)
        
                with rowLayout(nc=2,cw2=(50,100)):
                    text(" ")
                    button(label=' -=Continue=-',w=80,c=self.secondWindow)               

                form.redistribute()
            mainWin.show()

    def secondWindow(self,*args):
        """
        Create window with frames with info to be input per finger.
        """
        numFlds = intField(self.numChainsFld,query=True,value=True)

        #from pymel.core import *
        
        # Delete the initial window
        if(window('createFingersOrToesRigWin',exists=True)):
            deleteUI('createFingersOrToesRigWin',window=True)

        # Start second window
        if(window('createFingersOrToesRigWin2',exists=True)):
            deleteUI('createFingersOrToesRigWin2',window=True)

        with window('createFingersOrToesRigWin2',title='Create Fingers Or Toes Rig v1.0',rtf=True) as mainWin:
            with scrollLayout():
                with columnLayout():
    
                    self.labelFld = textFieldGrp(label='Main Label:',text='Fingers')
                    self.cntFld = textFieldButtonGrp(label='Hand or Foot control:',text='nurbsCircle2',bl='Load',bc=self.loadCnt)  
            
                    self.attNameFlds = []
                    self.startFlds = []
                    self.endFlds = []
                    
                    x = 0
                    while x < numFlds:
                        x = x + 1
                        
                        with frameLayout( label='Finger %i'%x,cll=True,cl=False ):
                            with columnLayout():
                                self.attNameFlds.append( textFieldGrp(label='Attribute name:') )
                                self.startFlds.append( textFieldButtonGrp(label='Start Bone:',bl='load' )  )
                                self.endFlds.append( textFieldButtonGrp(label='End Bone:',bl='load')  )
                    
                                startFldCmd = 'from pymel.core import *\nsel = ls(sl=True,fl=True)\ntextFieldButtonGrp("%s", edit=True, text=sel[0])' % self.startFlds[x-1]
                                textFieldButtonGrp( self.startFlds[x-1], edit=True,bc = startFldCmd)
                                endFldCmd = 'from pymel.core import *\nsel = ls(sl=True,fl=True)\ntextFieldButtonGrp("%s", edit=True, text=sel[0])' % self.endFlds[x-1]
                                textFieldButtonGrp( self.endFlds[x-1], edit=True,bc = endFldCmd)
                                   
                    text('  Orientation Information: ',font='boldLabelFont')
                    self.curlFld = radioButtonGrp(label='Curl Rotate Axis:',nrb=3,labelArray3=('x','y','z'),sl=3)
                    self.twistFld = radioButtonGrp(label='Twist Rotate Axis:',nrb=3,labelArray3=('x','y','z'),sl=1)
                    self.spreadFld = radioButtonGrp(label='Spread Rotate Axis:',nrb=3,labelArray3=('x','y','z'),sl=2)
                    self.radiusFld = floatFieldGrp(label='Controller Radius:',v1=0.5)
                        
                    with rowLayout(nc=2,cw2=(200,100)):
                        text(" ")
                        button(label='    -=Create=-',w=80,c=self.guiCall)
                        
            mainWin.show()
        
    def guiCall(self,*args):
        """
        Verify and Store the data passed via GUI.
        """    
        self.label = textFieldGrp(self.labelFld,query=True,text=True)
        self.control = textFieldButtonGrp(self.cntFld,query=True,text=True)
        
        self.attNames = []
        self.startJnts = []
        self.endJnts = []
        
        # Store values for each finger.
        for (nameFld,startJntFld,endJntFld) in zip(self.attNameFlds,self.startFlds,self.endFlds):
            #Get data for current limb
            self.attNames.append(textFieldGrp(nameFld,query=True,text=True))
            self.startJnts.append(textFieldButtonGrp(startJntFld,query=True,text=True))
            self.endJnts.append(textFieldButtonGrp(endJntFld,query=True,text=True))

        self.curlVal = radioButtonGrp(self.curlFld,query=True,select=True)
        self.twistVal = radioButtonGrp(self.twistFld,query=True,select=True)
        self.spreadVal = radioButtonGrp(self.spreadFld,query=True,select=True)
        
        self.radius = floatFieldGrp(self.radiusFld,query=True,v1=True)
        
        # Set aim, twist, spread, fkNormal
        self.curl = ' '
        self.twist = ' '
        self.spread = ' '

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
        
        self.create()

    def create(self,*args):
        """
        Given input, create the limb rigs.
        """

        # Create main attributes on control
        select(self.control,r=True)
        attList = attributeInfo(self.control,all=True)

        if(self.label not in attList):
            try:
                addAttr(longName=self.label,k=True)
                setAttr(self.control + '.' + self.label, lock=True)
            except:
                pass #Attribute already exists @ todo - Catch specific exemption
            
        # Create controller vis switch
        addAttr(longName='Control_Vis',k=True, min=0, max=1)
        
        # Create spread all
        addAttr(longName='spread_all',k=True, min=0.0, max=10.0)
        
        # Create tenson all
        addAttr(longName='tension_all',k=True, min=0.0, max=10.0)

        chainParent = ''
        # Iterate the attNames, startJnts, endJnts at the same time.
        for (name,startJnt,endJnt) in zip(self.attNames,self.startJnts,self.endJnts):
            #Get full chain
            chain = []

            #Get the hierarchy of startJnt, then store it until endJnt is found
            try:
                select(startJnt,r=True,hi=True)
                sel = ls(sl=True,fl=True,type='joint')
                tempChain = sel

                for each in tempChain:
                    if each == endJnt:
                        chain.append(each)
                        break
                    else:
                        chain.append(each)
            except:
                pass

            #Store parent of chain if it has one
            try:
                chainParent = listRelatives(chain[0],parent=True)
            except:
                pass

            #Unparent joints
            for each in chain:
                try:
                    parent(each,w=True)
                except:
                    pass

            # Create curve_jnts joints above main joints, then store joint names
            crvJoints = []
            for joint in chain:
                crvJntName = joint + '_crv_jnt'
                jnt = duplicate(joint,rr=True,po=True,n=crvJntName)
                crvJoints.append(jnt)
            
            # Create cntrl_attrs_jnts 
            cntrlJoints = []
            for joint in chain:
                cntrlJointsName = joint + '_cntrl_jnt'
                jnt = duplicate(joint,rr=True,po=True,n=cntrlJointsName)
                cntrlJoints.append(jnt)
                
            # Create tension_jnts 
            tensionJoints = []
            for joint in chain:
                tensionJointsName = joint + '_tension_jnt'
                jnt = duplicate(joint,rr=True,po=True,n=tensionJointsName)
                tensionJoints.append(jnt)
                
            # Create all_jnts 
            allJoints = []
            for joint in chain:
                allJointsName = joint + '_all_jnt'
                jnt = duplicate(joint,rr=True,po=True,n=allJointsName)
                allJoints.append(jnt)
            
            #Rebuild hierarchy
            x = 0
            while x < len(chain):
                #Parent: main_jnt > crv_jnt > cntrl_jnt > tension_jnt > all_jnt
                parent(chain[x],crvJoints[x])
                parent(crvJoints[x],cntrlJoints[x])
                parent(cntrlJoints[x],tensionJoints[x])
                parent(tensionJoints[x],allJoints[x])
                
                # If we are not at the root, parent the all joint to the main_jnt above it.
                if x != 0:
                    parent(allJoints[x],chain[x-1])
                    
                x = x + 1
                
            # Adding Curl atts on controller
            x= 0 
            while x < len(chain):
                addAttr(self.control, longName=name + '_curl_' + str(x+1),k=True)
                x = x + 1

            # Adding spread attr on controller
            addAttr(self.control, longName=name + '_spread',k=True)

            # Twist
            addAttr(self.control, longName= name + '_twist',k=True)
            
            # Tension
            addAttr(self.control, longName= name + '_tension',k=True)

            # Connect attributes to cntrlJoints rotate's ( aim = curl, up = spread )
            x = 0
            connectAttr( self.control + '.' + name + '_twist' , str(cntrlJoints[0][0]) + '.rotate' + self.twist ) 
            connectAttr( self.control + '.' + name + '_spread', str(cntrlJoints[0][0]) + '.rotate' + self.spread )
            while x < len(chain):
                connectAttr( self.control + '.' + name + '_curl_' + str(x+1) , str(cntrlJoints[x][0]) + '.rotate' + self.curl )
                x = x + 1
                
            #SDK attributes to tensionJoints rotate's ( aim = curl )
            x = 0
            while x < len(tensionJoints):
                # Root joint curls back
                if x == 0:
                    setDrivenKeyframe( tensionJoints[x], 
                                    cd=self.control + '.' + name + '_tension',
                                    at= "rotate%s"%self.curl,
                                    dv = 0,
                                    v = 0 )
                    setDrivenKeyframe( tensionJoints[x], 
                                    cd=self.control + '.' + name + '_tension',
                                    at= "rotate%s"%self.curl,
                                    dv = 10,
                                    v = 60 )
                    x += 1
                    continue
                
                # All oher joints curl forword
                setDrivenKeyframe( tensionJoints[x], 
                                cd=self.control + '.' + name + '_tension',
                                at= "rotate%s"%self.curl,
                                dv = 0,
                                v = 0 )
                setDrivenKeyframe( tensionJoints[x], 
                                cd=self.control + '.' + name + '_tension',
                                at= "rotate%s"%self.curl,
                                dv = 10,
                                v = -50 )
                    
                x = x + 1
                
            # SDK All tension
            x = 0
            while x < len(allJoints):
                # all_tension
                if x == 0:
                    setDrivenKeyframe( allJoints[x], 
                                    cd=self.control + '.tension_all',
                                    at= "rotate%s"%self.curl,
                                    dv = 0,
                                    v = 0 )
                    setDrivenKeyframe( allJoints[x], 
                                    cd=self.control + '.tension_all',
                                    at= "rotate%s"%self.curl,
                                    dv = 10,
                                    v = 60 )
                    x += 1
                    continue
                
                # All oher joints curl forword
                setDrivenKeyframe( allJoints[x], 
                                cd=self.control + '.tension_all',
                                at= "rotate%s"%self.curl,
                                dv = 0,
                                v = 0 )
                setDrivenKeyframe( allJoints[x], 
                                cd=self.control + '.tension_all',
                                at= "rotate%s"%self.curl,
                                dv = 10,
                                v = -50 )
                x += 1

            #Create fk controllers on joints
            #Duplicate FK control, parent it to chain joints, delete left over transform node
            temp = circle( nr=self.fkNormal, c=(0, 0, 0),r=self.radius )
            fkControl = temp[0]
            
            for each in chain:
                #Duplicate control
                tempCnt = duplicate(fkControl)
                #Select the shape
                tempShp = pickWalk(tempCnt,direction='down')
                parent(tempShp,each,r=True,s=True)
                delete(tempCnt)
                
                # Lock and hide unsed attributes
                setAttr('%s.translateX'%each, lock=True, keyable=False)
                setAttr('%s.translateY'%each, lock=True, keyable=False)
                setAttr('%s.translateZ'%each, lock=True, keyable=False)
                setAttr('%s.scaleX'%each, lock=True, keyable=False)
                setAttr('%s.scaleY'%each, lock=True, keyable=False)
                setAttr('%s.scaleZ'%each, lock=True, keyable=False)
                setAttr('%s.visibility'%each, lock=True, keyable=False)
                setAttr('%s.radius'%each, lock=True, keyable=False)
                
            # Delete original fk control
            delete(temp[0])
            
            # Connect root chains to vis switch
            connectAttr('%s.Control_Vis'%self.control,'%s.visibility'%crvJoints[0][0],f=True)             
                
            #Reparent chain to parent if it had one
            if len(chainParent):
                parent(allJoints[0],chainParent)
            
            if len(chainParent):
                self.createdNodes.append(chainParent)
            else:
                self.createdNodes.append(crvJoints[0][0])
                
            select(clear=True)

    def loadCnt(self, *args): 
        objName = ls(sl=True)
        textFieldGrp(self.cntFld, edit=True, text=objName[0])    

        
        