from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *
"""
Copyright (c) 2010 Mauricio Santos
Name: placeLocators.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created:   22 Oct 2010
Last Modified:  14 Mar 2010

$Revision: 135 $
$LastChangedDate: 2011-08-28 07:06:08 -0700 (Sun, 28 Aug 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/placeLocators.py $
$Id: placeLocators.py 135 2011-08-28 14:06:08Z mauricio $

Description: 
    -Given number of arms, fingers, legs, toes, create head[eyes, mouth(teeth, tongue, jaw), ears], arms, hands, legs,
    and feet place locators for user to provide placement data.
    
    -Defines standard names used by rig creation scripts
    

    
Used by: createFullRig.py

Ideas:
    -Instead of placing locators, place descriptive icons.
    Remember, a locator can be drawn as any openGL command!
    Complex: opneGL and custom icon creation via locators. Will make interface so much sweeter.
    Easy: Or draw it once manually, and copy the .ma instructions to replicate.
    Easiest: Use regular locators.

Uses:

Process:
    
Additional Notes: 

Example call:
    import placeLocators as pl
    pl.placeLocators()
    
Attributes:
    createdNodes = list of created nodes.

Keywords:
             
Requires:


Development notes:
        @todo - use standardNames.py for naming.

    
"""
class PlaceLocatorsError(): pass

class ConfigurationNotSupportedError( PlaceLocatorsError ):
    def __repr__(self,*args):
        return 'placeLocators(): The specifications you entered are currently not supported.'

class placeLocators():
    """
    Places locators in default positions, to be placed by user to build rig.
    """
    def __init__(self,**keywords):
        # Used to store names of all created nodes, 
        # to be returned when the tool is done.
        self.createdNodes = {} 
        
        # Check if command line call
        if len(keywords):
            self.commandlineCall(keywords)
        else:
            self.buildGUI()
            
    def commandlineCall(self,keywords):
        """
        Verify and Store the data passed via command line keywords dictionary.
        """        
        self.head = keywords['head']
        self.back = keywords['back']
        self.hands = keywords['hands']
        self.feet = keywords['feet']
        
        self.numArms = keywords['numArms']
        self.numFingers = keywords['numFingers']
        self.numLegs = keywords['numLegs']
        self.numToes = keywords['numToes']
        
        self.createLocators()

    def buildGUI(self,*args):
        """
        Create GUI in Maya
        """
        if(window("msPlaceLocatorsWin",exists=True)):
                deleteUI("msPlaceLocatorsWin",window=True)
        
        with window("msPlaceLocatorsWin",title="Place Locators v1.0",rtf=True) as mainWin:
            with formLayout() as form:      
                self.headFld = radioButtonGrp(l="Head?:", nrb=2, labelArray2=('Yes', 'No'), sl=1)

                self.backFld = radioButtonGrp(l="Back?:", nrb=2, labelArray2=('Yes', 'No'), sl=1)    
                
                self.handsFld = radioButtonGrp (l="Hands?:", nrb=2, labelArray2=('Yes', 'No'), sl=1, cc = self.handsChange)
                
                self.feetFld = radioButtonGrp(l="Feet?:", nrb=2, labelArray2=('Yes', 'No'), sl=1, cc = self.feetChange)               
                
                with rowLayout(nc=2,cw2=(300,100)):
                    text('  How many total Arms? ( 0 or 2 ): ',fn='boldLabelFont')
                    self.numArmsFld = intField(value=2,min=0, max=2)
                    
                with rowLayout(nc=2,cw2=(300,100)):
                    text('  Fingers per hand? ( 0, 3, 4 or 5 ):',fn='boldLabelFont')
                    self.numFingersFld = intField(value=5,min=0, max=5)                   
            
                with rowLayout(nc=2,cw2=(300,100)):
                    text('  Legs? ( 0 or 2 ):',fn='boldLabelFont')
                    self.numLegsFld = intField(value=2,min=0, max=2)
                
                with rowLayout(nc=2,cw2=(300,100)):
                    text('  Toes per foot? ( 0, 3, 4 or 5 ):',fn='boldLabelFont')
                    self.numToesFld = intField(value=5,min=0, max=5)      
                                         
                with rowLayout(nc=2,cw2=(100,150)):
                    text(" ")
                    button(label="   -=Create Locators=-",c=self.guiCall,w=150)
                
                form.redistribute()
            mainWin.show()
            
    def guiCall(self,*args):
        """
        Verify and Store the data passed via GUI.
        @todo: Verify
        """    
        self.head = radioButtonGrp(self.headFld,q=True,sl=True)
        self.back = radioButtonGrp(self.backFld,q=True,sl=True)
        self.numArms = intField(self.numArmsFld,q=True,value=True)
        self.hands = radioButtonGrp(self.handsFld,q=True,sl=True)
        self.numFingers = intField(self.numFingersFld,q=True,value=True)
        self.numLegs = intField(self.numLegsFld,q=True,value=True)
        self.feet = radioButtonGrp(self.feetFld,q=True,sl=True)
        self.numToes = intField(self.numToesFld,q=True,value=True)
        
        self.createLocators()
        
    def createLocators(self,*args):
        """
        Places locators in default positions, to be placed by user to build rig.
        """
        # Initialize lists of locator names
        headLocators = []
        backLocators = []
        armLocators = []
        handLocators = []
        legLocators = []
        feetLocators = []
        
        # If they are selected, call them, passing relative parameters.
        if self.head == 1: 
            headLocators = self.createHead()
            self.createdNodes['head_locators'] = headLocators
            
        if self.back == 1: 
            backLocators = self.createBack()
            self.createdNodes['back_locators'] = backLocators
            
        if self.hands == 1: 
            handLocators = self.createHand(self.numArms, self.numFingers)
            self.createdNodes['hand_locators'] = handLocators
            
        if self.feet == 1: 
            feetLocators = self.createFoot( self.numLegs, self.numToes)
            self.createdNodes['feet_locators'] = feetLocators
            
        if self.numArms: 
            armLocators = self.createArm(self.numArms)
            self.createdNodes['arm_locators'] = armLocators            
            
        if self.numLegs: 
            legLocators = self.createLeg(self.numLegs)
            self.createdNodes['leg_locators'] = legLocators            

    def createHead(self,*args):
        """
        Create locators to be used to build a head rig.
        """
        
        mel.eval('createNode transform -n "head_loc";\
                setAttr ".t" -type "double3" 0 20.358882662669586 0 ;\
            createNode locator -n "head_locShape" -p "head_loc";\
                setAttr -k off ".v";\
            createNode transform -n "neck_loc";\
                setAttr ".t" -type "double3" 0 18.214995886599056 0 ;\
                setAttr ".s" -type "double3" 0.5 0.5 0.5 ;\
            createNode locator -n "neck_locShape" -p "neck_loc";\
                setAttr -k off ".v";\
            createNode transform -n "l_eye_loc";\
                setAttr ".t" -type "double3" 0.70686859465332752 20.896875638841678 1.8525372641201505 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
            createNode locator -n "l_eye_locShape" -p "l_eye_loc";\
                setAttr -k off ".v";\
            createNode transform -n "r_eye_loc";\
                setAttr ".t" -type "double3" -0.44441907537192493 20.896875638841678 1.8525372641201503 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
            createNode locator -n "r_eye_locShape" -p "r_eye_loc";\
                setAttr -k off ".v";\
            createNode transform -n "jaw_loc";\
                setAttr ".t" -type "double3" 0 19.530879791192 0.71423745588713516 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
            createNode locator -n "jaw_locShape" -p "jaw_loc";\
                setAttr -k off ".v";\
            createNode transform -n "l_ear_loc";\
                setAttr ".t" -type "double3" 1.4246791035231428 20.573595844472596 -0.33697361949059834 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
            createNode locator -n "l_ear_locShape" -p "l_ear_loc";\
                setAttr -k off ".v";\
            createNode transform -n "r_ear_loc";\
                setAttr ".t" -type "double3" -1.4039514080616287 20.573595844472596 -0.33697361949059818 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
            createNode locator -n "r_ear_locShape" -p "r_ear_loc";\
                setAttr -k off ".v";\
            createNode transform -n "tongue_loc_1";\
                setAttr ".t" -type "double3" 0 19.841296089680693 1.0564913234515965 ;\
                setAttr ".s" -type "double3" 0.1 0.1 0.1 ;\
            createNode locator -n "tongue_loc_1Shape" -p "tongue_loc_1";\
                setAttr -k off ".v";\
            createNode transform -n "tongue_loc_2";\
                setAttr ".t" -type "double3" 0 19.928849404639045 1.534054859588053 ;\
                setAttr ".s" -type "double3" 0.1 0.1 0.1 ;\
            createNode locator -n "tongue_loc_2Shape" -p "tongue_loc_2";\
                setAttr -k off ".v";\
            createNode transform -n "tongue_loc_3";\
                setAttr ".t" -type "double3" 0 19.729864597915522 1.9320244730350997 ;\
                setAttr ".s" -type "double3" 0.1 0.1 0.1 ;\
            createNode locator -n "tongue_loc_3Shape" -p "tongue_loc_3";\
                setAttr -k off ".v";' )
        
        names = ['head_loc','neck_loc','l_eye_loc','r_eye_loc','jaw_loc',
                 'l_ear_loc','r_ear_loc','tongue_loc_1','tongue_loc_2','tongue_loc_3']
        
        return names
        
    def createBack(self,*args):
        """
        Create locators to be used to build a back rig.
        """
        names = []

        mel.eval('createNode transform -n "root_loc";\
                setAttr ".t" -type "double3" 0 8.783050044447009 0 ;\
                setAttr ".s" -type "double3" 1 0.77153251913219267 1 ;\
            createNode locator -n "root_locShape" -p "root_loc";\
                setAttr -k off ".v";\
            createNode transform -n "back_end_loc";\
                setAttr ".t" -type "double3" 0 16.086156201255054 0 ;\
                setAttr ".s" -type "double3" 1 0.77153251913219267 1 ;\
            createNode locator -n "back_end_locShape" -p "back_end_loc";\
                setAttr -k off ".v";\
            createNode transform -n "back_loc_1";\
                setAttr ".t" -type "double3" 0 10.284391684565767 0 ;\
                setAttr ".s" -type "double3" 0.50865462615261459 0.39244358508377042 0.50865462615261459 ;\
            createNode locator -n "back_loc_1Shape" -p "back_loc_1";\
                setAttr -k off ".v";\
            createNode transform -n "back_loc_2";\
                setAttr ".t" -type "double3" 0 11.369193452174471 0 ;\
                setAttr ".s" -type "double3" 0.50865462615261459 0.39244358508377042 0.50865462615261459 ;\
            createNode locator -n "back_loc_2Shape" -p "back_loc_2";\
                setAttr -k off ".v";\
            createNode transform -n "back_loc_3";\
                setAttr ".t" -type "double3" 0 12.453995219783174 0 ;\
                setAttr ".s" -type "double3" 0.50865462615261459 0.39244358508377042 0.50865462615261459 ;\
            createNode locator -n "back_loc_3Shape" -p "back_loc_3";\
                setAttr -k off ".v";\
            createNode transform -n "back_loc_4";\
                setAttr ".t" -type "double3" 0 13.538796987391876 0 ;\
                setAttr ".s" -type "double3" 0.50865462615261459 0.39244358508377042 0.50865462615261459 ;\
            createNode locator -n "back_loc_4Shape" -p "back_loc_4";\
                setAttr -k off ".v";\
            createNode transform -n "back_loc_5";\
                setAttr ".t" -type "double3" 0 14.623598755000582 0 ;\
                setAttr ".s" -type "double3" 0.50865462615261459 0.39244358508377042 0.50865462615261459 ;\
            createNode locator -n "back_loc_5Shape" -p "back_loc_5";\
                setAttr -k off ".v";')
        
        names = ['root_loc','back_loc_1','back_loc_2','back_loc_3','back_loc_4','back_loc_5','back_end_loc']
        
        return names
    
    def createArm(self,numArms):
        """
        Create locators to be used to build an arm.
        """
        names = []
        
        if numArms == 2:
            # Create one arm on left side
            mel.eval('createNode transform -n "l_clav_loc";\
                setAttr ".t" -type "double3" 1 15 1.1902871660862053 ;\
            createNode locator -n "l_clav_locShape" -p "l_clav_loc";\
                setAttr -k off ".v";\
            createNode transform -n "l_shoulder_loc";\
                setAttr ".t" -type "double3" 3 16 0 ;\
            createNode locator -n "l_shoulder_locShape" -p "l_shoulder_loc";\
                setAttr -k off ".v";\
            createNode transform -n "l_elbow_loc";\
                setAttr ".t" -type "double3" 7 16 -1.2322188387552853 ;\
            createNode locator -n "l_elbow_locShape" -p "l_elbow_loc";\
                setAttr -k off ".v";\
            createNode transform -n "l_wrist_loc";\
                setAttr ".t" -type "double3" 11 16 0 ;\
            createNode locator -n "l_wrist_locShape" -p "l_wrist_loc";\
                setAttr -k off ".v";')
            
            names = ['l_clav_loc','l_shoulder_loc','l_elbow_loc','l_wrist_loc']
               
        return names

    def createHand(self,numArms,numFingers):
        """
        Create locators to be used to build a finger rig.
        """
        names = []
        
        if numFingers == 3:
            # Create three fingers on one side
            # Not supported yet
            raise ConfigurationNotSupportedError()
        
        if numFingers == 4:
            # Create four fingers on one side 
            mel.eval('createNode transform -n "l_palm_loc";\
                setAttr ".t" -type "double3" 11.221147969393273 15.999999999999998 0.63566274386481725 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 0 ;\
                setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 0 ;\
            createNode locator -n "l_palm_locShape" -p "l_palm_loc";\
                setAttr -k off ".v";\
            createNode transform -n "l_pinky_base_loc";\
                setAttr ".t" -type "double3" 11.221147969393273 15.999999999999998 0.63566274386481725 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 0 ;\
                setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 0 ;\
            createNode locator -n "l_pinky_base_locShape" -p "l_pinky_base_loc";\
                setAttr -k off ".v";\
            createNode transform -n "l_pinky_loc_1";\
                setAttr ".t" -type "double3" 13.158068600821803 15.999999999999998 -0.17074776654680113 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                setAttr ".rp" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 0 ;\
                setAttr ".spt" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 0 ;\
            createNode locator -n "l_pinky_loc_1Shape" -p "l_pinky_loc_1";\
                setAttr -k off ".v";\
            createNode transform -n "l_pinky_loc_2";\
                setAttr ".t" -type "double3" 14.026620051438167 15.999999999999998 -0.17074776654680113 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                setAttr ".rp" -type "double3" 1.4210854715202004e-014 -3.944304526105059e-030 0 ;\
                setAttr ".spt" -type "double3" 1.4210854715202004e-014 -3.944304526105059e-030 0 ;\
            createNode locator -n "l_pinky_loc_2Shape" -p "l_pinky_loc_2";\
                setAttr -k off ".v";\
            createNode transform -n "l_pinky_loc_3";\
                setAttr ".t" -type "double3" 14.94781098391006 15.999999999999998 -0.17074776654680113 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 0 ;\
                setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 0 ;\
            createNode locator -n "l_pinky_loc_3Shape" -p "l_pinky_loc_3";\
                setAttr -k off ".v";\
            createNode transform -n "l_pinky_loc_4";\
                setAttr ".t" -type "double3" 15.816362434526415 15.999999999999998 -0.17074776654680113 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                setAttr ".rp" -type "double3" 1.4210854715202004e-014 -3.944304526105059e-030 0 ;\
                setAttr ".spt" -type "double3" 1.4210854715202004e-014 -3.944304526105059e-030 0 ;\
            createNode locator -n "l_pinky_loc_4Shape" -p "l_pinky_loc_4";\
                setAttr -k off ".v";\
            createNode transform -n "l_middle_loc_1";\
                setAttr ".t" -type "double3" 13.158068600821803 15.999999999999998 0.71063300504974847 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                setAttr ".rp" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 0 ;\
                setAttr ".spt" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 0 ;\
            createNode locator -n "l_middle_loc_1Shape" -p "l_middle_loc_1";\
                setAttr -k off ".v";\
            createNode transform -n "l_middle_loc_2";\
                setAttr ".t" -type "double3" 14.381936553963058 15.999999999999998 0.71063300504974847 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 0 ;\
                setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 0 ;\
            createNode locator -n "l_middle_loc_2Shape" -p "l_middle_loc_2";\
                setAttr -k off ".v";\
            createNode transform -n "l_middle_loc_3";\
                setAttr ".t" -type "double3" 15.395246579682139 15.999999999999998 0.71063300504974847 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 0 ;\
                setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 0 ;\
            createNode locator -n "l_middle_loc_3Shape" -p "l_middle_loc_3";\
                setAttr -k off ".v";\
            createNode transform -n "l_middle_loc_4";\
                setAttr ".t" -type "double3" 16.605954662359473 15.999999999999998 0.71063300504974847 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 0 ;\
                setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 0 ;\
            createNode locator -n "l_middle_loc_4Shape" -p "l_middle_loc_4";\
                setAttr -k off ".v";\
            createNode transform -n "l_index_loc_1";\
                setAttr ".t" -type "double3" 13.158068600821803 15.999999999999998 1.552864714738339 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                setAttr ".rp" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 0 ;\
                setAttr ".spt" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 0 ;\
            createNode locator -n "l_index_loc_1Shape" -p "l_index_loc_1";\
                setAttr -k off ".v";\
            createNode transform -n "l_index_loc_2";\
                setAttr ".t" -type "double3" 14.276657590251972 15.999999999999998 1.552864714738339 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 0 ;\
                setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 0 ;\
            createNode locator -n "l_index_loc_2Shape" -p "l_index_loc_2";\
                setAttr -k off ".v";\
            createNode transform -n "l_index_loc_3";\
                setAttr ".t" -type "double3" 15.355766968290478 15.999999999999998 1.552864714738339 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 0 ;\
                setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 0 ;\
            createNode locator -n "l_index_loc_3Shape" -p "l_index_loc_3";\
                setAttr -k off ".v";\
            createNode transform -n "l_index_loc_4";\
                setAttr ".t" -type "double3" 16.461196087256752 15.999999999999998 1.552864714738339 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                setAttr ".rp" -type "double3" 1.4210854715202004e-014 -3.944304526105059e-030 0 ;\
                setAttr ".spt" -type "double3" 1.4210854715202004e-014 -3.944304526105059e-030 0 ;\
            createNode locator -n "l_index_loc_4Shape" -p "l_index_loc_4";\
                setAttr -k off ".v";\
            createNode transform -n "l_thumb_loc_1";\
                setAttr ".t" -type "double3" 11.93420064768058 15.999999999999998 1.6318239375216459 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 -8.8817841970012523e-016 ;\
                setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 -8.8817841970012523e-016 ;\
            createNode locator -n "l_thumb_loc_1Shape" -p "l_thumb_loc_1";\
                setAttr -k off ".v";\
            createNode transform -n "l_thumb_loc_2";\
                setAttr ".t" -type "double3" 12.539554689019251 15.999999999999998 2.4872155176741195 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                setAttr ".rp" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 8.8817841970012523e-016 ;\
                setAttr ".spt" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 8.8817841970012523e-016 ;\
            createNode locator -n "l_thumb_loc_2Shape" -p "l_thumb_loc_2";\
                setAttr -k off ".v";\
            createNode transform -n "l_thumb_loc_3";\
                setAttr ".t" -type "double3" 13.197548212213462 15.999999999999998 3.0136103362294895 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 0 ;\
                setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 0 ;\
            createNode locator -n "l_thumb_loc_3Shape" -p "l_thumb_loc_3";\
                setAttr -k off ".v";\
            createNode transform -n "l_thumb_loc_4";\
                setAttr ".t" -type "double3" 13.895021346799322 15.999999999999998 3.5005255433932052 ;\
                setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                setAttr ".rp" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 0 ;\
                setAttr ".spt" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 0 ;\
            createNode locator -n "l_thumb_loc_4Shape" -p "l_thumb_loc_4";\
                setAttr -k off ".v";')
            
            names = ['l_palm_loc', 'l_pinky_loc_1', 'l_pinky_loc_2',
                      'l_pinky_loc_3', 'l_pinky_loc_4', 'l_middle_loc_1', 
                      'l_middle_loc_2', 'l_middle_loc_3',
                      'l_middle_loc_4', 'l_index_loc_1', 'l_index_loc_2', 
                      'l_index_loc_3', 'l_index_loc_4', 'l_thumb_loc_1', 
                      'l_thumb_loc_2', 'l_thumb_loc_3', 'l_thumb_loc_4', 
                      'l_pinky_base_loc']
            
        
        if numFingers == 5:
            # Create five fingers on one side
            temp = mel.eval('createNode transform -n "l_palm_loc";\
                    setAttr ".t" -type "double3" 11.999999999999995 15.999999999999998 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 0 ;\
                    setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 0 ;\
                createNode locator -n "l_palm_locShape" -p "l_palm_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_pinky_base_loc";\
                    setAttr ".t" -type "double3" 11.999999999999995 15.999999999999998 0 ;\
                    setAttr ".s" -type "double3" 0.01 0.01 0.01 ;\
                    setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 0 ;\
                    setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 0 ;\
                createNode locator -n "l_pinky_base_locShape" -p "l_pinky_base_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_pinky_loc_1";\
                    setAttr ".t" -type "double3" 13.158068600821803 15.999999999999998 -1.0133100257190855 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 0 ;\
                    setAttr ".spt" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 0 ;\
                createNode locator -n "l_pinky_loc_1Shape" -p "l_pinky_loc_1";\
                    setAttr -k off ".v";\
                createNode transform -n "l_pinky_loc_2";\
                    setAttr ".t" -type "double3" 14.026620051438167 15.999999999999998 -1.0133100257190855 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 1.4210854715202004e-014 -3.944304526105059e-030 0 ;\
                    setAttr ".spt" -type "double3" 1.4210854715202004e-014 -3.944304526105059e-030 0 ;\
                createNode locator -n "l_pinky_loc_2Shape" -p "l_pinky_loc_2";\
                    setAttr -k off ".v";\
                createNode transform -n "l_pinky_loc_3";\
                    setAttr ".t" -type "double3" 14.94781098391006 15.999999999999998 -1.0133100257190855 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 0 ;\
                    setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 0 ;\
                createNode locator -n "l_pinky_loc_3Shape" -p "l_pinky_loc_3";\
                    setAttr -k off ".v";\
                createNode transform -n "l_pinky_loc_4";\
                    setAttr ".t" -type "double3" 15.816362434526415 15.999999999999998 -1.0133100257190855 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 1.4210854715202004e-014 -3.944304526105059e-030 0 ;\
                    setAttr ".spt" -type "double3" 1.4210854715202004e-014 -3.944304526105059e-030 0 ;\
                createNode locator -n "l_pinky_loc_4Shape" -p "l_pinky_loc_4";\
                    setAttr -k off ".v";\
                createNode transform -n "l_ring_loc_1";\
                    setAttr ".t" -type "double3" 13.158068600821803 15.999999999999998 -0.1842381864943794 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 -2.2204460492503131e-016 ;\
                    setAttr ".spt" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 -2.2204460492503131e-016 ;\
                createNode locator -n "l_ring_loc_1Shape" -p "l_ring_loc_1";\
                    setAttr -k off ".v";\
                createNode transform -n "l_ring_loc_2";\
                    setAttr ".t" -type "double3" 14.23717797886032 15.999999999999998 -0.1842381864943794 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 -2.2204460492503131e-016 ;\
                    setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 -2.2204460492503131e-016 ;\
                createNode locator -n "l_ring_loc_2Shape" -p "l_ring_loc_2";\
                    setAttr -k off ".v";\
                createNode transform -n "l_ring_loc_3";\
                    setAttr ".t" -type "double3" 15.211008393187747 15.999999999999998 -0.1842381864943794 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 -2.2204460492503131e-016 ;\
                    setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 -2.2204460492503131e-016 ;\
                createNode locator -n "l_ring_loc_3Shape" -p "l_ring_loc_3";\
                    setAttr -k off ".v";\
                createNode transform -n "l_ring_loc_4";\
                    setAttr ".t" -type "double3" 16.263798030298503 15.999999999999998 -0.1842381864943794 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 1.4210854715202004e-014 -3.944304526105059e-030 -2.2204460492503131e-016 ;\
                    setAttr ".spt" -type "double3" 1.4210854715202004e-014 -3.944304526105059e-030 -2.2204460492503131e-016 ;\
                createNode locator -n "l_ring_loc_4Shape" -p "l_ring_loc_4";\
                    setAttr -k off ".v";\
                createNode transform -n "l_middle_loc_1";\
                    setAttr ".t" -type "double3" 13.158068600821803 15.999999999999998 0.71063300504974847 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 0 ;\
                    setAttr ".spt" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 0 ;\
                createNode locator -n "l_middle_loc_1Shape" -p "l_middle_loc_1";\
                    setAttr -k off ".v";\
                createNode transform -n "l_middle_loc_2";\
                    setAttr ".t" -type "double3" 14.381936553963058 15.999999999999998 0.71063300504974847 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 0 ;\
                    setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 0 ;\
                createNode locator -n "l_middle_loc_2Shape" -p "l_middle_loc_2";\
                    setAttr -k off ".v";\
                createNode transform -n "l_middle_loc_3";\
                    setAttr ".t" -type "double3" 15.395246579682139 15.999999999999998 0.71063300504974847 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 0 ;\
                    setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 0 ;\
                createNode locator -n "l_middle_loc_3Shape" -p "l_middle_loc_3";\
                    setAttr -k off ".v";\
                createNode transform -n "l_middle_loc_4";\
                    setAttr ".t" -type "double3" 16.605954662359473 15.999999999999998 0.71063300504974847 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 0 ;\
                    setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 0 ;\
                createNode locator -n "l_middle_loc_4Shape" -p "l_middle_loc_4";\
                    setAttr -k off ".v";\
                createNode transform -n "l_index_loc_1";\
                    setAttr ".t" -type "double3" 13.158068600821803 15.999999999999998 1.552864714738339 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 0 ;\
                    setAttr ".spt" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 0 ;\
                createNode locator -n "l_index_loc_1Shape" -p "l_index_loc_1";\
                    setAttr -k off ".v";\
                createNode transform -n "l_index_loc_2";\
                    setAttr ".t" -type "double3" 14.276657590251972 15.999999999999998 1.552864714738339 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 0 ;\
                    setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 0 ;\
                createNode locator -n "l_index_loc_2Shape" -p "l_index_loc_2";\
                    setAttr -k off ".v";\
                createNode transform -n "l_index_loc_3";\
                    setAttr ".t" -type "double3" 15.355766968290478 15.999999999999998 1.552864714738339 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 0 ;\
                    setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 0 ;\
                createNode locator -n "l_index_loc_3Shape" -p "l_index_loc_3";\
                    setAttr -k off ".v";\
                createNode transform -n "l_index_loc_4";\
                    setAttr ".t" -type "double3" 16.461196087256752 15.999999999999998 1.552864714738339 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 1.4210854715202004e-014 -3.944304526105059e-030 0 ;\
                    setAttr ".spt" -type "double3" 1.4210854715202004e-014 -3.944304526105059e-030 0 ;\
                createNode locator -n "l_index_loc_4Shape" -p "l_index_loc_4";\
                    setAttr -k off ".v";\
                createNode transform -n "l_thumb_loc_1";\
                    setAttr ".t" -type "double3" 11.93420064768058 15.999999999999998 1.6318239375216459 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 -8.8817841970012523e-016 ;\
                    setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 -8.8817841970012523e-016 ;\
                createNode locator -n "l_thumb_loc_1Shape" -p "l_thumb_loc_1";\
                    setAttr -k off ".v";\
                createNode transform -n "l_thumb_loc_2";\
                    setAttr ".t" -type "double3" 12.539554689019251 15.999999999999998 2.4872155176741195 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 8.8817841970012523e-016 ;\
                    setAttr ".spt" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 8.8817841970012523e-016 ;\
                createNode locator -n "l_thumb_loc_2Shape" -p "l_thumb_loc_2";\
                    setAttr -k off ".v";\
                createNode transform -n "l_thumb_loc_3";\
                    setAttr ".t" -type "double3" 13.197548212213462 15.999999999999998 3.0136103362294895 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 0 -3.944304526105059e-030 0 ;\
                    setAttr ".spt" -type "double3" 0 -3.944304526105059e-030 0 ;\
                createNode locator -n "l_thumb_loc_3Shape" -p "l_thumb_loc_3";\
                    setAttr -k off ".v";\
                createNode transform -n "l_thumb_loc_4";\
                    setAttr ".t" -type "double3" 13.895021346799322 15.999999999999998 3.5005255433932052 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                    setAttr ".rp" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 0 ;\
                    setAttr ".spt" -type "double3" 7.1054273576010019e-015 -3.944304526105059e-030 0 ;\
                createNode locator -n "l_thumb_loc_4Shape" -p "l_thumb_loc_4";\
                    setAttr -k off ".v";')
            
            names = ['l_palm_loc', 'l_pinky_loc_1', 'l_pinky_loc_2',
                      'l_pinky_loc_3', 'l_pinky_loc_4', 'l_ring_loc_1',
                      'l_ring_loc_2', 'l_ring_loc_3', 'l_ring_loc_4', 
                      'l_middle_loc_1', 'l_middle_loc_2', 'l_middle_loc_3',
                      'l_middle_loc_4', 'l_index_loc_1', 'l_index_loc_2', 
                      'l_index_loc_3', 'l_index_loc_4', 'l_thumb_loc_1', 
                      'l_thumb_loc_2', 'l_thumb_loc_3', 'l_thumb_loc_4', 
                      'l_pinky_base_loc']
        
        return names
    
    def createLeg(self,numLegs):
        """
        Create locators to be used to build a leg rig.
        """
        names = []
        
        if numLegs == 2:
            mel.eval('createNode transform -n "l_thigh_loc";\
                    setAttr ".t" -type "double3" 2 8 0 ;\
                createNode locator -n "l_thigh_locShape" -p "l_thigh_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_knee_loc";\
                    setAttr ".t" -type "double3" 2 5 1.0337314695662729 ;\
                createNode locator -n "l_knee_locShape" -p "l_knee_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_ankle_loc";\
                    setAttr ".t" -type "double3" 2 2 0 ;\
                createNode locator -n "l_ankle_locShape" -p "l_ankle_loc";\
                    setAttr -k off ".v";')
            names = ["l_thigh_loc","l_knee_loc","l_ankle_loc"]     
        
        return names
    
    def createFoot(self,numLegs,numToes):
        """
        Create locators to be used to build a foot.
        Each new finger has it's base position offset 
        from the last.
        """
        names = []
        if self.numToes == 0:
            mel.eval('createNode transform -n "l_ball_loc";\
                    setAttr ".t" -type "double3" 2 0 2 ;\
                    setAttr ".s" -type "double3" 0.8 0.8 0.8 ;\
                createNode locator -n "l_ball_locShape" -p "l_ball_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_toe_loc";\
                    setAttr ".t" -type "double3" 2 0 8.7628432625793735 ;\
                    setAttr ".s" -type "double3" 0.8 0.8 0.8 ;\
                createNode locator -n "l_toe_locShape" -p "l_toe_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_outterBank_loc";\
                    setAttr ".t" -type "double3" 3.2839519153343839 0 2 ;\
                    setAttr ".s" -type "double3" 0.5 0.5 0.5 ;\
                createNode locator -n "l_outterBank_locShape" -p "l_outterBank_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_innerBank_loc";\
                    setAttr ".t" -type "double3" 0.39475361655773944 0 2 ;\
                    setAttr ".s" -type "double3" 0.5 0.5 0.5 ;\
                createNode locator -n "l_innerBank_locShape" -p "l_innerBank_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_heel_loc";\
                    setAttr ".t" -type "double3" 2 0 -1.0218203525852916 ;\
                    setAttr ".s" -type "double3" 0.5 0.5 0.5 ;\
                createNode locator -n "l_heel_locShape" -p "l_heel_loc";\
                    setAttr -k off ".v";\
                ')
            
            names = ["l_ball_loc","l_toe_loc","l_outterBank_loc","l_innerBank_loc","l_heel_loc" ]   
            
        if self.numToes == 3:
            mel.eval('createNode transform -n "l_ball_loc";\
                    setAttr ".t" -type "double3" 2 0 2 ;\
                    setAttr ".s" -type "double3" 0.8 0.8 0.8 ;\
                createNode locator -n "l_ball_locShape" -p "l_ball_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_toe_loc";\
                    setAttr ".t" -type "double3" 2 0 8.7628432625793735 ;\
                    setAttr ".s" -type "double3" 0.8 0.8 0.8 ;\
                createNode locator -n "l_toe_locShape" -p "l_toe_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_outterBank_loc";\
                    setAttr ".t" -type "double3" 3.2839519153343839 0 2 ;\
                    setAttr ".s" -type "double3" 0.5 0.5 0.5 ;\
                createNode locator -n "l_outterBank_locShape" -p "l_outterBank_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_innerBank_loc";\
                    setAttr ".t" -type "double3" 0.39475361655773944 0 2 ;\
                    setAttr ".s" -type "double3" 0.5 0.5 0.5 ;\
                createNode locator -n "l_innerBank_locShape" -p "l_innerBank_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_heel_loc";\
                    setAttr ".t" -type "double3" 2 0 -1.0218203525852916 ;\
                    setAttr ".s" -type "double3" 0.5 0.5 0.5 ;\
                createNode locator -n "l_heel_locShape" -p "l_heel_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_pinkyToe_loc_1";\
                    setAttr ".t" -type "double3" 3.826001067480318 0.83770666986241693 4.1903056459975145 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_pinkyToe_loc_1Shape" -p "l_pinkyToe_loc_1";\
                    setAttr -k off ".v";\
                createNode transform -n "l_pinkyToe_loc_2";\
                    setAttr ".t" -type "double3" 3.826001067480318 0.83770666986241693 5.0588570966138873 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_pinkyToe_loc_2Shape" -p "l_pinkyToe_loc_2";\
                    setAttr -k off ".v";\
                createNode transform -n "l_pinkyToe_loc_3";\
                    setAttr ".t" -type "double3" 3.8260010674803189 0.83770666986241693 5.980048029085764 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_pinkyToe_loc_3Shape" -p "l_pinkyToe_loc_3";\
                    setAttr -k off ".v";\
                createNode transform -n "l_pinkyToe_loc_4";\
                    setAttr ".t" -type "double3" 3.8260010674803189 0.83770666986241693 6.8485994797021332 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_pinkyToe_loc_4Shape" -p "l_pinkyToe_loc_4";\
                    setAttr -k off ".v";\
                createNode transform -n "l_middleToe_loc_1";\
                    setAttr ".t" -type "double3" 2.1020580367114845 0.83770666986241693 4.1903056459975145 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_middleToe_loc_1Shape" -p "l_middleToe_loc_1";\
                    setAttr -k off ".v";\
                createNode transform -n "l_middleToe_loc_2";\
                    setAttr ".t" -type "double3" 2.1020580367114849 0.83770666986241693 5.4141735991387625 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_middleToe_loc_2Shape" -p "l_middleToe_loc_2";\
                    setAttr -k off ".v";\
                createNode transform -n "l_middleToe_loc_3";\
                    setAttr ".t" -type "double3" 2.1020580367114854 0.83770666986241693 6.5607853118278205 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_middleToe_loc_3Shape" -p "l_middleToe_loc_3";\
                    setAttr -k off ".v";\
                createNode transform -n "l_middleToe_loc_4";\
                    setAttr ".t" -type "double3" 2.1020580367114863 0.83770666986241693 7.6381917075351771 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_middleToe_loc_4Shape" -p "l_middleToe_loc_4";\
                    setAttr -k off ".v";\
                createNode transform -n "l_thumbToe_loc_1";\
                    setAttr ".t" -type "double3" 0.38275991308142099 0.83770666986241693 4.1632769677218908 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_thumbToe_loc_1Shape" -p "l_thumbToe_loc_1";\
                    setAttr -k off ".v";\
                createNode transform -n "l_thumbToe_loc_2";\
                    setAttr ".t" -type "double3" 0.37500040692460446 0.83770666986241693 5.5854387411898392 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_thumbToe_loc_2Shape" -p "l_thumbToe_loc_2";\
                    setAttr -k off ".v";\
                createNode transform -n "l_thumbToe_loc_3";\
                    setAttr ".t" -type "double3" 0.42273767881787427 0.83770666986241693 6.734920266499647 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_thumbToe_loc_3Shape" -p "l_thumbToe_loc_3";\
                    setAttr -k off ".v";\
                createNode transform -n "l_thumbToe_loc_4";\
                    setAttr ".t" -type "double3" 0.4524894134248878 0.83770666986241693 7.927273688946511 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_thumbToe_loc_4Shape" -p "l_thumbToe_loc_4";\
                    setAttr -k off ".v";')
            
            names = ["l_ball_loc","l_toe_loc","l_outterBank_loc","l_innerBank_loc","l_heel_loc", "l_pinkyToe_loc_1",
                     "l_pinkyToe_loc_2", "l_pinkyToe_loc_3", "l_pinkyToe_loc_4", "l_middleToe_loc_1",
                     "l_middleToe_loc_2", "l_middleToe_loc_3", "l_middleToe_loc_4", "l_thumbToe_loc_1",
                     "l_thumbToe_loc_2", "l_thumbToe_loc_3", "l_thumbToe_loc_4"]     
            
        if self.numToes == 4:
            mel.eval('createNode transform -n "l_ball_loc";\
                    setAttr ".t" -type "double3" 2 0 2 ;\
                    setAttr ".s" -type "double3" 0.8 0.8 0.8 ;\
                createNode locator -n "l_ball_locShape" -p "l_ball_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_toe_loc";\
                    setAttr ".t" -type "double3" 2 0 8.7628432625793735 ;\
                    setAttr ".s" -type "double3" 0.8 0.8 0.8 ;\
                createNode locator -n "l_toe_locShape" -p "l_toe_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_outterBank_loc";\
                    setAttr ".t" -type "double3" 3.2839519153343839 0 2 ;\
                    setAttr ".s" -type "double3" 0.5 0.5 0.5 ;\
                createNode locator -n "l_outterBank_locShape" -p "l_outterBank_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_innerBank_loc";\
                    setAttr ".t" -type "double3" 0.39475361655773944 0 2 ;\
                    setAttr ".s" -type "double3" 0.5 0.5 0.5 ;\
                createNode locator -n "l_innerBank_locShape" -p "l_innerBank_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_heel_loc";\
                    setAttr ".t" -type "double3" 2 0 -1.0218203525852916 ;\
                    setAttr ".s" -type "double3" 0.5 0.5 0.5 ;\
                createNode locator -n "l_heel_locShape" -p "l_heel_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_pinkyToe_loc_1";\
                    setAttr ".t" -type "double3" 3.826001067480318 0.83770666986241693 4.1903056459975145 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_pinkyToe_loc_1Shape" -p "l_pinkyToe_loc_1";\
                    setAttr -k off ".v";\
                createNode transform -n "l_pinkyToe_loc_2";\
                    setAttr ".t" -type "double3" 3.826001067480318 0.83770666986241693 5.0588570966138873 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_pinkyToe_loc_2Shape" -p "l_pinkyToe_loc_2";\
                    setAttr -k off ".v";\
                createNode transform -n "l_pinkyToe_loc_3";\
                    setAttr ".t" -type "double3" 3.8260010674803189 0.83770666986241693 5.980048029085764 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_pinkyToe_loc_3Shape" -p "l_pinkyToe_loc_3";\
                    setAttr -k off ".v";\
                createNode transform -n "l_pinkyToe_loc_4";\
                    setAttr ".t" -type "double3" 3.8260010674803189 0.83770666986241693 6.8485994797021332 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_pinkyToe_loc_4Shape" -p "l_pinkyToe_loc_4";\
                    setAttr -k off ".v";\
                createNode transform -n "l_middleToe_loc_1";\
                    setAttr ".t" -type "double3" 2.1020580367114845 0.83770666986241693 4.1903056459975145 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_middleToe_loc_1Shape" -p "l_middleToe_loc_1";\
                    setAttr -k off ".v";\
                createNode transform -n "l_middleToe_loc_2";\
                    setAttr ".t" -type "double3" 2.1020580367114849 0.83770666986241693 5.4141735991387625 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_middleToe_loc_2Shape" -p "l_middleToe_loc_2";\
                    setAttr -k off ".v";\
                createNode transform -n "l_middleToe_loc_3";\
                    setAttr ".t" -type "double3" 2.1020580367114854 0.83770666986241693 6.5607853118278205 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_middleToe_loc_3Shape" -p "l_middleToe_loc_3";\
                    setAttr -k off ".v";\
                createNode transform -n "l_middleToe_loc_4";\
                    setAttr ".t" -type "double3" 2.1020580367114863 0.83770666986241693 7.6381917075351771 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_middleToe_loc_4Shape" -p "l_middleToe_loc_4";\
                    setAttr -k off ".v";\
                createNode transform -n "l_indexToe_loc_1";\
                    setAttr ".t" -type "double3" 1.2598263270228935 0.83770666986241693 4.1903056459975145 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_indexToe_loc_1Shape" -p "l_indexToe_loc_1";\
                    setAttr -k off ".v";\
                createNode transform -n "l_indexToe_loc_2";\
                    setAttr ".t" -type "double3" 1.2598263270228935 0.83770666986241693 5.5220207805261667 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_indexToe_loc_2Shape" -p "l_indexToe_loc_2";\
                    setAttr -k off ".v";\
                createNode transform -n "l_indexToe_loc_3";\
                    setAttr ".t" -type "double3" 1.259826327022894 0.83770666986241693 6.6243944486419588 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_indexToe_loc_3Shape" -p "l_indexToe_loc_3";\
                    setAttr -k off ".v";\
                createNode transform -n "l_indexToe_loc_4";\
                    setAttr ".t" -type "double3" 1.2598263270228944 0.83770666986241693 7.7707323389387186 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_indexToe_loc_4Shape" -p "l_indexToe_loc_4";\
                    setAttr -k off ".v";\
                createNode transform -n "l_thumbToe_loc_1";\
                    setAttr ".t" -type "double3" 0.38275991308142099 0.83770666986241693 4.1632769677218908 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_thumbToe_loc_1Shape" -p "l_thumbToe_loc_1";\
                    setAttr -k off ".v";\
                createNode transform -n "l_thumbToe_loc_2";\
                    setAttr ".t" -type "double3" 0.37500040692460446 0.83770666986241693 5.5854387411898392 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_thumbToe_loc_2Shape" -p "l_thumbToe_loc_2";\
                    setAttr -k off ".v";\
                createNode transform -n "l_thumbToe_loc_3";\
                    setAttr ".t" -type "double3" 0.42273767881787427 0.83770666986241693 6.734920266499647 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_thumbToe_loc_3Shape" -p "l_thumbToe_loc_3";\
                    setAttr -k off ".v";\
                createNode transform -n "l_thumbToe_loc_4";\
                    setAttr ".t" -type "double3" 0.4524894134248878 0.83770666986241693 7.927273688946511 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_thumbToe_loc_4Shape" -p "l_thumbToe_loc_4";\
                    setAttr -k off ".v";')
            
            names = ["l_ball_loc","l_toe_loc","l_outterBank_loc","l_innerBank_loc","l_heel_loc", "l_pinkyToe_loc_1",
                     "l_pinkyToe_loc_2", "l_pinkyToe_loc_3", "l_pinkyToe_loc_4", "l_middleToe_loc_1",
                     "l_middleToe_loc_2", "l_middleToe_loc_3", "l_middleToe_loc_4", "l_indexToe_loc_1",
                     "l_indexToe_loc_2", "l_indexToe_loc_3", "l_indexToe_loc_4", "l_thumbToe_loc_1",
                     "l_thumbToe_loc_2", "l_thumbToe_loc_3", "l_thumbToe_loc_4"]            
            
        if self.numToes == 5:
            mel.eval('createNode transform -n "l_ball_loc";\
                    setAttr ".t" -type "double3" 2 0 2 ;\
                    setAttr ".s" -type "double3" 0.8 0.8 0.8 ;\
                createNode locator -n "l_ball_locShape" -p "l_ball_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_toe_loc";\
                    setAttr ".t" -type "double3" 2 0 8.7628432625793735 ;\
                    setAttr ".s" -type "double3" 0.8 0.8 0.8 ;\
                createNode locator -n "l_toe_locShape" -p "l_toe_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_outterBank_loc";\
                    setAttr ".t" -type "double3" 3.2839519153343839 0 2 ;\
                    setAttr ".s" -type "double3" 0.5 0.5 0.5 ;\
                createNode locator -n "l_outterBank_locShape" -p "l_outterBank_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_innerBank_loc";\
                    setAttr ".t" -type "double3" 0.39475361655773944 0 2 ;\
                    setAttr ".s" -type "double3" 0.5 0.5 0.5 ;\
                createNode locator -n "l_innerBank_locShape" -p "l_innerBank_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_heel_loc";\
                    setAttr ".t" -type "double3" 2 0 -1.0218203525852916 ;\
                    setAttr ".s" -type "double3" 0.5 0.5 0.5 ;\
                createNode locator -n "l_heel_locShape" -p "l_heel_loc";\
                    setAttr -k off ".v";\
                createNode transform -n "l_pinkyToe_loc_1";\
                    setAttr ".t" -type "double3" 3.826001067480318 0.83770666986241693 4.1903056459975145 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_pinkyToe_loc_1Shape" -p "l_pinkyToe_loc_1";\
                    setAttr -k off ".v";\
                createNode transform -n "l_pinkyToe_loc_2";\
                    setAttr ".t" -type "double3" 3.826001067480318 0.83770666986241693 5.0588570966138873 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_pinkyToe_loc_2Shape" -p "l_pinkyToe_loc_2";\
                    setAttr -k off ".v";\
                createNode transform -n "l_pinkyToe_loc_3";\
                    setAttr ".t" -type "double3" 3.8260010674803189 0.83770666986241693 5.980048029085764 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_pinkyToe_loc_3Shape" -p "l_pinkyToe_loc_3";\
                    setAttr -k off ".v";\
                createNode transform -n "l_pinkyToe_loc_4";\
                    setAttr ".t" -type "double3" 3.8260010674803189 0.83770666986241693 6.8485994797021332 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_pinkyToe_loc_4Shape" -p "l_pinkyToe_loc_4";\
                    setAttr -k off ".v";\
                createNode transform -n "l_ringToe_loc_1";\
                    setAttr ".t" -type "double3" 2.9969292282556119 0.83770666986241693 4.1903056459975145 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_ringToe_loc_1Shape" -p "l_ringToe_loc_1";\
                createNode transform -n "l_ringToe_loc_2";\
                    setAttr ".t" -type "double3" 2.9969292282556124 0.83770666986241693 5.2694150240360242 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_ringToe_loc_2Shape" -p "l_ringToe_loc_2";\
                    setAttr -k off ".v";\
                createNode transform -n "l_ringToe_loc_3";\
                    setAttr ".t" -type "double3" 2.9969292282556124 0.83770666986241693 6.3172923347273722 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_ringToe_loc_3Shape" -p "l_ringToe_loc_3";\
                    setAttr -k off ".v";\
                createNode transform -n "l_ringToe_loc_4";\
                    setAttr ".t" -type "double3" 2.9969292282556133 0.83770666986241693 7.2960350754742214 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_ringToe_loc_4Shape" -p "l_ringToe_loc_4";\
                    setAttr -k off ".v";\
                createNode transform -n "l_middleToe_loc_1";\
                    setAttr ".t" -type "double3" 2.1020580367114845 0.83770666986241693 4.1903056459975145 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_middleToe_loc_1Shape" -p "l_middleToe_loc_1";\
                    setAttr -k off ".v";\
                createNode transform -n "l_middleToe_loc_2";\
                    setAttr ".t" -type "double3" 2.1020580367114849 0.83770666986241693 5.4141735991387625 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_middleToe_loc_2Shape" -p "l_middleToe_loc_2";\
                    setAttr -k off ".v";\
                createNode transform -n "l_middleToe_loc_3";\
                    setAttr ".t" -type "double3" 2.1020580367114854 0.83770666986241693 6.5607853118278205 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_middleToe_loc_3Shape" -p "l_middleToe_loc_3";\
                    setAttr -k off ".v";\
                createNode transform -n "l_middleToe_loc_4";\
                    setAttr ".t" -type "double3" 2.1020580367114863 0.83770666986241693 7.6381917075351771 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_middleToe_loc_4Shape" -p "l_middleToe_loc_4";\
                    setAttr -k off ".v";\
                createNode transform -n "l_indexToe_loc_1";\
                    setAttr ".t" -type "double3" 1.2598263270228935 0.83770666986241693 4.1903056459975145 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_indexToe_loc_1Shape" -p "l_indexToe_loc_1";\
                    setAttr -k off ".v";\
                createNode transform -n "l_indexToe_loc_2";\
                    setAttr ".t" -type "double3" 1.2598263270228935 0.83770666986241693 5.5220207805261667 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_indexToe_loc_2Shape" -p "l_indexToe_loc_2";\
                    setAttr -k off ".v";\
                createNode transform -n "l_indexToe_loc_3";\
                    setAttr ".t" -type "double3" 1.259826327022894 0.83770666986241693 6.6243944486419588 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_indexToe_loc_3Shape" -p "l_indexToe_loc_3";\
                    setAttr -k off ".v";\
                createNode transform -n "l_indexToe_loc_4";\
                    setAttr ".t" -type "double3" 1.2598263270228944 0.83770666986241693 7.7707323389387186 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_indexToe_loc_4Shape" -p "l_indexToe_loc_4";\
                    setAttr -k off ".v";\
                createNode transform -n "l_thumbToe_loc_1";\
                    setAttr ".t" -type "double3" 0.38275991308142099 0.83770666986241693 4.1632769677218908 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_thumbToe_loc_1Shape" -p "l_thumbToe_loc_1";\
                    setAttr -k off ".v";\
                createNode transform -n "l_thumbToe_loc_2";\
                    setAttr ".t" -type "double3" 0.37500040692460446 0.83770666986241693 5.5854387411898392 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_thumbToe_loc_2Shape" -p "l_thumbToe_loc_2";\
                    setAttr -k off ".v";\
                createNode transform -n "l_thumbToe_loc_3";\
                    setAttr ".t" -type "double3" 0.42273767881787427 0.83770666986241693 6.734920266499647 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_thumbToe_loc_3Shape" -p "l_thumbToe_loc_3";\
                    setAttr -k off ".v";\
                createNode transform -n "l_thumbToe_loc_4";\
                    setAttr ".t" -type "double3" 0.4524894134248878 0.83770666986241693 7.927273688946511 ;\
                    setAttr ".r" -type "double3" 0 -89.999999999999972 0 ;\
                    setAttr ".s" -type "double3" 0.3 0.3 0.3 ;\
                createNode locator -n "l_thumbToe_loc_4Shape" -p "l_thumbToe_loc_4";\
                    setAttr -k off ".v";')
            
            names = ["l_ball_loc","l_toe_loc","l_outterBank_loc","l_innerBank_loc","l_heel_loc", "l_pinkyToe_loc_1",
                     "l_pinkyToe_loc_2", "l_pinkyToe_loc_3", "l_pinkyToe_loc_4", "l_ringToe_loc_1",
                     "l_ringToe_loc_2", "l_ringToe_loc_3", "l_ringToe_loc_4", "l_middleToe_loc_1",
                     "l_middleToe_loc_2", "l_middleToe_loc_3", "l_middleToe_loc_4", "l_indexToe_loc_1",
                     "l_indexToe_loc_2", "l_indexToe_loc_3", "l_indexToe_loc_4", "l_thumbToe_loc_1",
                     "l_thumbToe_loc_2", "l_thumbToe_loc_3", "l_thumbToe_loc_4"]
        
        return names
        
    #--- GUI radio button on/off state
    def handsChange(self,*args):
        """
        Execute when Hands option is changed.
        Disables Finger gui inputs.
        """
        selected = radioButtonGrp (self.handsFld,query=True,sl=True)
        if selected == 1:
            intField(self.numFingersFld,edit=True,ed=True, bgc=(0.15, 0.15, 0.15))
        if selected == 2:
            intField(self.numFingersFld,edit=True,ed=False, bgc=(0.5, 0.5, 0.5))
            
    def feetChange(self,*args):
        """
        Execute when Feet option is changed.
        Disables Toes gui inputs.
        """
        selected = radioButtonGrp (self.feetFld,query=True,sl=True)
        if selected == 1:
            intField(self.numToesFld,edit=True,ed=True, bgc=(0.15, 0.15, 0.15))
        if selected == 2:
            intField(self.numToesFld,edit=True,ed=False, bgc=(0.5, 0.5, 0.5))
        