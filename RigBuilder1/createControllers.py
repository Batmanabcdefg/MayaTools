from __future__ import with_statement # This line is only needed for 2008 and 2009
from pymel.core import *
"""
Copyright (c) 2010 Mauricio Santos
Name: createControllers.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created:   22 Oct 2010

$Revision: 147 $
$LastChangedDate: 2011-09-18 20:41:07 -0700 (Sun, 18 Sep 2011) $
$Author: mauricio $
$HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/Dev/RigBuilder/createControllers.py $
$Id: createControllers.py 147 2011-09-19 03:41:07Z mauricio $

Description: 
    -Places zero'd controller curves in scene based on locator positions.
    -Relies on locator names defined in: placeLocators.py
    -Controllers are created around their pivot positions. You should only move them around in
        component mode, via vertices because of constraint systems used for the rig.
    
Used by: createRig.py

Uses:

Process:
    
Additional Notes: 

Example call:
    import createControllers as cc
    cc.createControllers()
    
Attributes:
    createdNodes = dictionary of controller buffer nodes.

Keywords:
             
Requires:


Development notes:

    @todo -   
    - Teeth, Ears: get position from locator in scene, vs being built into the draw cnt cmd.


Notes: 
Index color values: 1-32
    blue = 6
    red = 13


"""
import datetime

import commonMayaLib as cml
import standardNames

reload( cml )
reload( standardNames )

class createControllers():
    """
    Creates controllers for both sides of the rig.
    """
    def __init__(self,**keywords):
        # standardNames object
        self.sNames = standardNames.standardNames()
        
        # Create library instance
        self.lib = cml.commonMayaLib()
        
        # Used to store names of all created nodes, 
        # associated to default labels.
        # to be returned when the tool is done.
        self.createdNodes = {} 
        
        # Command line call
        self.commandlineCall(keywords)

            
    def commandlineCall(self,keywords):
        """
        Verify and Store the data passed via command line keywords dictionary.
        """      
        self.version = keywords['version']
        
        # Used for cog/hip location 
        self.prefix = keywords['prefix']
        self.scale = keywords['scale']
               
        self.createControllers()
        
    def createControllers(self,*args):
        """
        Places zero'd controller curves in scene.
        """
        # Set/Get positions
        mainPos = ['0','0','0']
        geoVisPos = ['5','0','-1']
        controlVisPos = ['5','0','1']
        rootPos = xform('root_loc',q=True,ws=True,t=True)
        shoulderPos = xform('back_end_loc',q=True,ws=True,t=True)
        l_handPos = xform('l_wrist_loc',q=True,ws=True,t=True)
        r_handPos = xform(self.sNames.armJoints['right_wrist'],q=True,ws=True,t=True)
        l_footPos = xform(self.sNames.legJoints['left_ankle'],q=True,ws=True,t=True)
        r_footPos = xform(self.sNames.legJoints['right_ankle'],q=True,ws=True,t=True)
        
        l_foot_ball_pos = xform(self.sNames.feetJoints['left_footBall'],q=True,ws=True,t=True)
        r_foot_ball_pos = xform(self.sNames.feetJoints['right_footBall'],q=True,ws=True,t=True)
        
        head_pos = xform('head_loc',q=True,ws=True,t=True)
        l_eye_pos = xform('l_eye_loc',q=True,ws=True,t=True)
        r_eye_pos = xform('r_eye_loc',q=True,ws=True,t=True)
        
        l_clav_pos = xform('l_clav_loc',q=True,ws=True,t=True)
        r_clav_pos = xform(self.sNames.armJoints['right_clav'],q=True,ws=True,t=True)
        
        # Determine the position of the following controllers
        # based on the Y of the eye locators.
        follow_pos = (0,l_eye_pos[1],5)
        
        jaw_pos = xform('jaw_loc',q=True,ws=True,t=True)

        #--- Create the controllers
        self.createMain(mainPos)
        self.createGeoVis(geoVisPos)
        self.createControlVis(controlVisPos)
        self.createCog(rootPos)
        self.createHips(rootPos)
        self.createShoulder(shoulderPos)
        self.createRightFoot(r_footPos)
        self.createLeftFoot(l_footPos)
        self.createRightHand(r_handPos)
        self.createLeftHand(l_handPos)
        self.createLeftClav(l_clav_pos)
        self.createRightClav(r_clav_pos)
        self.createHead(head_pos)
        self.createJaw(jaw_pos)
        self.createTeeth() #Position in .ma data @todo - Get position from locator/joint
        self.createEars() #Position in .ma data
        self.createEyes(l_eye_pos,r_eye_pos,follow_pos)
        self.createLeftToeCnt(l_foot_ball_pos)
        self.createRightToeCnt(r_foot_ball_pos)
        
        
    def createMain(self,pos):
        # Create it
        mel.eval('createNode transform -n "%s";\
                    setAttr ".ove" yes;\
                    setAttr ".ovc" 13;\
                    createNode nurbsCurve -n "%sShape" -p "%s";\
                    setAttr -k off ".v";\
                    setAttr ".ove" yes;\
                    setAttr ".ovc" 29;\
                    setAttr ".cc" -type "nurbsCurve" \
                        1 24 0 no 3\
                        25 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24\
                        25\
                        -6.6552011263022957 0 0\
                        -3.9931206757813777 0 -2.6620804505209184\
                        -3.9931206757813777 0 -1.3310402252604592\
                        -3.3179279684062521 0 -3.3179279684062521\
                        -1.3310402252604592 0 -3.9931206757813777\
                        -2.6620804505209184 0 -3.9931206757813777\
                        0 0 -6.6552011263022957\
                        2.6620804505209184 0 -3.9931206757813777\
                        1.3310402252604592 0 -3.9931206757813777\
                        3.3179279684062521 0 -3.3179279684062521\
                        3.9931206757813777 0 -1.3310402252604592\
                        3.9931206757813777 0 -2.6620804505209184\
                        6.6552011263022957 0 0\
                        3.9931206757813777 0 2.6620804505209184\
                        3.9931206757813777 0 1.3310402252604592\
                        3.3179279684062521 0 3.3179279684062521\
                        1.3310402252604592 0 3.9931206757813777\
                        2.6620804505209184 0 3.9931206757813777\
                        0 0 6.6552011263022957\
                        -2.6620804505209184 0 3.9931206757813777\
                        -1.3310402252604592 0 3.9931206757813777\
                        -3.3179279684062521 0 3.3179279684062521\
                        -3.9931206757813777 0 1.3310402252604592\
                        -3.9931206757813777 0 2.6620804505209184\
                        -6.6552011263022957 0 0\
                        ;'%(self.sNames.controlNames['main'],self.sNames.controlNames['main'],self.sNames.controlNames['main']))
        
        setAttr('%s.scaleX'%self.sNames.controlNames['main'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['main'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['main'],self.scale)
        
        # Set it up
        self.processControl(self.sNames.controlNames['main'],self.sNames.controlNames['main'],pos)
        
    def createEars(self):  
        """ create the ear controls. """
        
        mel.eval('createNode transform -n "%s";\
            setAttr ".rp" -type "double3" 1.4246791035231414 20.573595844472592 -0.3369736194905979 ;\
            setAttr ".sp" -type "double3" 1.4246791035231414 20.573595844472592 -0.3369736194905979 ;\
            createNode nurbsCurve -n "%sShape" -p "%s";\
            setAttr -k off ".v";\
            setAttr ".ove" yes;\
            setAttr ".ovc" 6;\
            setAttr ".cc" -type "nurbsCurve" \
                3 8 2 no 3\
                13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                11\
                1.2372308296463885 20.250090004407465 -0.35371415329089717\
                1.2331104577570309 20.573595844472592 -0.35371415329089728\
                1.2372308296463883 20.897101684537724 -0.35371415329089728\
                1.1046731940726362 21.127692938249787 -0.35371415329089706\
                1.5470232357932827 21.069883198379006 -0.35371415329089756\
                1.7446850129736471 20.573595844472592 -0.35371415329089689\
                1.5470232357932832 20.077308490566182 -0.35371415329089728\
                1.1046731940726366 20.019498750695401 -0.35371415329089723\
                1.2372308296463885 20.250090004407465 -0.35371415329089717\
                1.2331104577570309 20.573595844472592 -0.35371415329089728\
                1.2372308296463883 20.897101684537724 -0.35371415329089728\
                ;\
            createNode transform -n "%s";\
            setAttr ".rp" -type "double3" -1.40395140806163 20.573595844472592 -0.33697361949059773 ;\
            setAttr ".sp" -type "double3" -1.40395140806163 20.573595844472592 -0.33697361949059773 ;\
            createNode nurbsCurve -n "%sShape" -p "%s";\
            setAttr -k off ".v";\
            setAttr ".ove" yes;\
            setAttr ".ovc" 17;\
            setAttr ".cc" -type "nurbsCurve"\
                3 8 2 no 3\
                13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                11\
                -1.2165031341848769 20.897101684537724 -0.35371415329089723\
                -1.212382762295519 20.573595844472592 -0.35371415329089717\
                -1.2165031341848767 20.250090004407465 -0.35371415329089706\
                -1.0839454986111243 20.019498750695401 -0.35371415329089739\
                -1.5262955403317713 20.077308490566182 -0.35371415329089712\
                -1.7239573175121348 20.573595844472592 -0.35371415329089717\
                -1.5262955403317715 21.069883198379006 -0.35371415329089695\
                -1.083945498611125 21.127692938249787 -0.35371415329089695\
                -1.2165031341848769 20.897101684537724 -0.35371415329089723\
                -1.212382762295519 20.573595844472592 -0.35371415329089717\
                -1.2165031341848767 20.250090004407465 -0.35371415329089706\
                ;'%(self.sNames.controlNames['left_ear'],self.sNames.controlNames['left_ear'],self.sNames.controlNames['left_ear'],
            self.sNames.controlNames['right_ear'],self.sNames.controlNames['right_ear'],self.sNames.controlNames['right_ear']))
            
        # Set scale to user defined value
        setAttr('%s.scaleX'%self.sNames.controlNames['left_ear'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['left_ear'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['left_ear'],self.scale)
        setAttr('%s.scaleX'%self.sNames.controlNames['right_ear'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['right_ear'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['right_ear'],self.scale)

        # Set it up
        self.processControl(self.sNames.controlNames['left_ear'],self.sNames.controlNames['left_ear']) 
        self.processControl(self.sNames.controlNames['right_ear'],self.sNames.controlNames['right_ear']) 

    def createTeeth(self):
        mel.eval('createNode transform -n "%s";\
            setAttr ".rp" -type "double3" 3.944304526105059e-31 19.253300579162893 0.71423745588713516 ;\
            setAttr ".sp" -type "double3" 3.944304526105059e-31 19.253300579162893 0.71423745588713516 ;\
            createNode nurbsCurve -n "%sShape" -p "%s";\
            setAttr -k off ".v";\
            setAttr ".ove" yes;\
            setAttr ".ovc" 17;\
            setAttr ".cc" -type "nurbsCurve" \
            3 8 2 no 3\
            13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
            11\
            0.647011680130258 19.253300579162893 0.3728219757342276\
            -1.2643170607829287e-16 19.253300579162893 1.052524460665206\
            -0.64701168013025612 19.253300579162893 0.37282197573422715\
            -1.1081941875543879 19.253300579162893 0.10770670458672305\
            -0.99257470781282708 19.253300579162893 0.9924067880280163\
            -3.3392053635905155e-16 19.253300579162893 1.3877303423887442\
            0.9925747078128262 19.253300579162893 0.99240678802801652\
            1.1081941875543879 19.253300579162893 0.10770670458672382\
            0.647011680130258 19.253300579162893 0.3728219757342276\
            -1.2643170607829287e-16 19.253300579162893 1.052524460665206\
            -0.64701168013025612 19.253300579162893 0.37282197573422715\
            ;\
            createNode transform -n "%s";\
            setAttr ".rp" -type "double3" 3.944304526105059e-31 19.744013876751698 0.71423745588713516 ;\
            setAttr ".sp" -type "double3" 3.944304526105059e-31 19.744013876751698 0.71423745588713516 ;\
            createNode nurbsCurve -n "%sShape" -p "%s";\
            setAttr -k off ".v";\
            setAttr ".ove" yes;\
            setAttr ".ovc" 6;\
            setAttr ".cc" -type "nurbsCurve" \
            3 8 2 no 3\
            13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
            11\
            0.647011680130258 19.744013876751698 0.3728219757342276\
            -1.2643170607829287e-16 19.744013876751698 1.052524460665206\
            -0.64701168013025612 19.744013876751698 0.37282197573422715\
            -1.1081941875543879 19.744013876751698 0.10770670458672305\
            -0.99257470781282708 19.744013876751698 0.9924067880280163\
            -3.3392053635905155e-16 19.744013876751698 1.3877303423887442\
            0.9925747078128262 19.744013876751698 0.99240678802801652\
            1.1081941875543879 19.744013876751698 0.10770670458672382\
            0.647011680130258 19.744013876751698 0.3728219757342276\
            -1.2643170607829287e-16 19.744013876751698 1.052524460665206\
            -0.64701168013025612 19.744013876751698 0.37282197573422715\
            ;'%(self.sNames.controlNames['btm_teeth'],self.sNames.controlNames['btm_teeth'],self.sNames.controlNames['btm_teeth'],
                self.sNames.controlNames['top_teeth'],self.sNames.controlNames['top_teeth'],self.sNames.controlNames['top_teeth']) )
        
        # Set scale to user defined value
        setAttr('%s.scaleX'%self.sNames.controlNames['btm_teeth'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['btm_teeth'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['btm_teeth'],self.scale)
        setAttr('%s.scaleX'%self.sNames.controlNames['top_teeth'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['top_teeth'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['top_teeth'],self.scale)

        # Set it up
        self.processControl(self.sNames.controlNames['top_teeth'],self.sNames.controlNames['top_teeth']) 
        self.processControl(self.sNames.controlNames['btm_teeth'],self.sNames.controlNames['btm_teeth']) 
                    
        
    def createGeoVis(self,pos):
        # Create it
        mel.eval('createNode transform -n "%s";\
                    setAttr ".ove" yes;\
                    setAttr ".ovc" 13;\
                    createNode nurbsCurve -n "%sShape" -p "%s";\
                    setAttr -k off ".v";\
                    setAttr ".ove" yes;\
                    setAttr ".ovc" 22;\
                    setAttr ".cc" -type "nurbsCurve" \
                        1 56 0 no 3\
                        57 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27\
                         28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54\
                         55 56\
                        57\
                        -0.66709634235343518 9.3056398122807719e-020 0.00020954437995515868\
                        -0.65438862287336608 -8.7204028011814265e-018 -0.019636601402960651\
                        -0.57151741973242121 -2.2660560969401521e-017 -0.051027046968901549\
                        -0.48496227334815245 -4.6158101046226823e-017 -0.10393880333595841\
                        -0.40028679277350881 -7.4022903798084351e-017 -0.16668476098096738\
                        -0.31454870773114463 -1.0012014813632042e-016 -0.22545053091950576\
                        -0.22100447490405462 -1.2044706989296686e-016 -0.27122268954391682\
                        -0.11937882053929695 -1.3415843805390695e-016 -0.30209794581409155\
                        0 -1.4045876881394412e-016 -0.3162850294456987\
                        0.065683980689907953 -1.3604058008617852e-016 -0.30633615289168986\
                        0.1269179235839461 -1.2477649168159302e-016 -0.28097168072091006\
                        0.17964227081929909 -1.069388165210537e-016 -0.24080480711782964\
                        0.21980914442237948 -8.3524620701826799e-017 -0.18808072533450459\
                        0.24517308568910343 -5.6331287386009535e-017 -0.12684678244046643\
                        0.25405245602266613 -2.7161622417240218e-017 -0.061162536298530579\
                        0.24517308568910343 2.0078775133952477e-018 0.0045213382105662179\
                        0.21980914442237948 2.9201257982965033e-017 0.065755387285415523\
                        0.17964227081929909 5.2615453802191941e-017 0.11847946906874059\
                        0.1269179235839461 7.0453246847112594e-017 0.15864660812384893\
                        0.065683980689907953 8.1717099482935417e-017 0.18401054939057285\
                        0 8.5660214153952035e-017 0.19288965427210764\
                        -0.065683980689907953 8.1717099482935417e-017 0.18401054939057285\
                        -0.1269179235839461 7.0453246847112594e-017 0.15864660812384893\
                        -0.17964227081929909 5.2615453802191941e-017 0.11847946906874059\
                        -0.21980914442237948 2.9201257982965033e-017 0.065755387285415523\
                        -0.24517308568910343 2.0078775133952477e-018 0.0045213382105662179\
                        -0.25405245602266613 -2.7161622417240218e-017 -0.061162536298530579\
                        -0.24517308568910343 -5.6331287386009535e-017 -0.12684678244046643\
                        -0.21980914442237948 -8.3524620701826799e-017 -0.18808072533450459\
                        -0.17964227081929909 -1.069388165210537e-016 -0.24080480711782964\
                        -0.1269179235839461 -1.2477649168159302e-016 -0.28097168072091006\
                        -0.065683980689907953 -1.3604058008617852e-016 -0.30633615289168986\
                        0 -1.4045876881394412e-016 -0.3162850294456987\
                        0.12004935236179559 -1.3371177413305785e-016 -0.30109214808034362\
                        0.22435713401654778 -1.1836263826233766e-016 -0.26652896678642635\
                        0.31723083502113919 -9.9077932321005823e-017 -0.22310366954076052\
                        0.39592833592726767 -7.7447327191260876e-017 -0.17439587693970168\
                        0.47155163689817975 -5.3900275674278111e-017 -0.12137263072092296\
                        0.55575965645167535 -3.1147293349915983e-017 -0.070137469362140575\
                        0.6510359637608728 -1.0507082061454142e-017 -0.023659845428358049\
                        0.66671913502177615 -7.4444576230092059e-020 -0.00016763428288479854\
                        0.65271229331711944 9.9115301669886579e-018 0.022318781783360775\
                        0.56380603832165888 2.8616079914056353e-017 0.064437683418874264\
                        0.4785922210344154 5.2709171885347142e-017 0.11869050343092841\
                        0.39726939957226493 7.7298439217644501e-017 0.17406061102845236\
                        0.31723083502113919 9.9077932321005823e-017 0.22310366954076052\
                        0.22435713401654778 1.1836263826233766e-016 0.26652896678642635\
                        0.12004935236179559 1.3371189201743915e-016 0.30109241353237148\
                        0 1.4045794362327481e-016 0.31628317128150329\
                        -0.12004935236179559 1.3371189201743915e-016 0.30109241353237148\
                        -0.22435713401654778 1.1836263826233766e-016 0.26652896678642635\
                        -0.31857189866613639 9.8333492452923986e-017 0.22142733998451397\
                        -0.40363971733802989 7.3427351903618851e-017 0.16534369733597007\
                        -0.48362120970315525 4.7944756729623273e-017 0.10796199427095023\
                        -0.56347077241040966 2.5936096388961678e-017 0.05840289701638654\
                        -0.65237702740587011 9.4648544577014118e-018 0.021312957504410028\
                        -0.66709634235343518 9.3056398122807719e-020 0.00020954437995515868\
                        ;'%(self.sNames.controlNames['geo_vis'],self.sNames.controlNames['geo_vis'],self.sNames.controlNames['geo_vis']))
        
        setAttr('%s.scaleX'%self.sNames.controlNames['geo_vis'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['geo_vis'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['geo_vis'],self.scale)
        
        # Set it up
        self.processControl(self.sNames.controlNames['geo_vis'],self.sNames.controlNames['geo_vis'],pos)

    def createControlVis(self,pos):
        # Create it
        mel.eval('createNode transform -n "%s";\
                    setAttr ".ove" yes;\
                    setAttr ".ovc" 13;\
                createNode nurbsCurve -n "%sShape" -p "%s";\
                    setAttr -k off ".v";\
                    setAttr ".ove" yes;\
                    setAttr ".ovc" 24;\
                    setAttr ".cc" -type "nurbsCurve" \
                        1 56 0 no 3\
                        57 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27\
                         28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54\
                         55 56\
                        57\
                        -0.66709634235343518 9.3056398122807719e-020 0.00020954437995515868\
                        -0.65438862287336608 -8.7204028011814265e-018 -0.019636601402960651\
                        -0.57151741973242121 -2.2660560969401521e-017 -0.051027046968901549\
                        -0.48496227334815245 -4.6158101046226823e-017 -0.10393880333595841\
                        -0.40028679277350881 -7.4022903798084351e-017 -0.16668476098096738\
                        -0.31454870773114463 -1.0012014813632042e-016 -0.22545053091950576\
                        -0.22100447490405462 -1.2044706989296686e-016 -0.27122268954391682\
                        -0.11937882053929695 -1.3415843805390695e-016 -0.30209794581409155\
                        0 -1.4045876881394412e-016 -0.3162850294456987\
                        0.065683980689907953 -1.3604058008617852e-016 -0.30633615289168986\
                        0.1269179235839461 -1.2477649168159302e-016 -0.28097168072091006\
                        0.17964227081929909 -1.069388165210537e-016 -0.24080480711782964\
                        0.21980914442237948 -8.3524620701826799e-017 -0.18808072533450459\
                        0.24517308568910343 -5.6331287386009535e-017 -0.12684678244046643\
                        0.25405245602266613 -2.7161622417240218e-017 -0.061162536298530579\
                        0.24517308568910343 2.0078775133952477e-018 0.0045213382105662179\
                        0.21980914442237948 2.9201257982965033e-017 0.065755387285415523\
                        0.17964227081929909 5.2615453802191941e-017 0.11847946906874059\
                        0.1269179235839461 7.0453246847112594e-017 0.15864660812384893\
                        0.065683980689907953 8.1717099482935417e-017 0.18401054939057285\
                        0 8.5660214153952035e-017 0.19288965427210764\
                        -0.065683980689907953 8.1717099482935417e-017 0.18401054939057285\
                        -0.1269179235839461 7.0453246847112594e-017 0.15864660812384893\
                        -0.17964227081929909 5.2615453802191941e-017 0.11847946906874059\
                        -0.21980914442237948 2.9201257982965033e-017 0.065755387285415523\
                        -0.24517308568910343 2.0078775133952477e-018 0.0045213382105662179\
                        -0.25405245602266613 -2.7161622417240218e-017 -0.061162536298530579\
                        -0.24517308568910343 -5.6331287386009535e-017 -0.12684678244046643\
                        -0.21980914442237948 -8.3524620701826799e-017 -0.18808072533450459\
                        -0.17964227081929909 -1.069388165210537e-016 -0.24080480711782964\
                        -0.1269179235839461 -1.2477649168159302e-016 -0.28097168072091006\
                        -0.065683980689907953 -1.3604058008617852e-016 -0.30633615289168986\
                        0 -1.4045876881394412e-016 -0.3162850294456987\
                        0.12004935236179559 -1.3371177413305785e-016 -0.30109214808034362\
                        0.22435713401654778 -1.1836263826233766e-016 -0.26652896678642635\
                        0.31723083502113919 -9.9077932321005823e-017 -0.22310366954076052\
                        0.39592833592726767 -7.7447327191260876e-017 -0.17439587693970168\
                        0.47155163689817975 -5.3900275674278111e-017 -0.12137263072092296\
                        0.55575965645167535 -3.1147293349915983e-017 -0.070137469362140575\
                        0.6510359637608728 -1.0507082061454142e-017 -0.023659845428358049\
                        0.66671913502177615 -7.4444576230092059e-020 -0.00016763428288479854\
                        0.65271229331711944 9.9115301669886579e-018 0.022318781783360775\
                        0.56380603832165888 2.8616079914056353e-017 0.064437683418874264\
                        0.4785922210344154 5.2709171885347142e-017 0.11869050343092841\
                        0.39726939957226493 7.7298439217644501e-017 0.17406061102845236\
                        0.31723083502113919 9.9077932321005823e-017 0.22310366954076052\
                        0.22435713401654778 1.1836263826233766e-016 0.26652896678642635\
                        0.12004935236179559 1.3371189201743915e-016 0.30109241353237148\
                        0 1.4045794362327481e-016 0.31628317128150329\
                        -0.12004935236179559 1.3371189201743915e-016 0.30109241353237148\
                        -0.22435713401654778 1.1836263826233766e-016 0.26652896678642635\
                        -0.31857189866613639 9.8333492452923986e-017 0.22142733998451397\
                        -0.40363971733802989 7.3427351903618851e-017 0.16534369733597007\
                        -0.48362120970315525 4.7944756729623273e-017 0.10796199427095023\
                        -0.56347077241040966 2.5936096388961678e-017 0.05840289701638654\
                        -0.65237702740587011 9.4648544577014118e-018 0.021312957504410028\
                        -0.66709634235343518 9.3056398122807719e-020 0.00020954437995515868\
                        ;'%(self.sNames.controlNames['cnt_vis'],self.sNames.controlNames['cnt_vis'],self.sNames.controlNames['cnt_vis']))

        setAttr('%s.scaleX'%self.sNames.controlNames['cnt_vis'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['cnt_vis'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['cnt_vis'],self.scale)

        # Set it up
        self.processControl(self.sNames.controlNames['cnt_vis'],self.sNames.controlNames['cnt_vis'],pos)

    def createCog(self,pos):
        # Create it
        mel.eval('createNode transform -n "%s";\
                        setAttr ".ove" yes;\
                        setAttr ".ovc" 13;\
                    createNode nurbsCurve -n "%sShape" -p "%s";\
                        setAttr -k off ".v";\
                        setAttr ".ove" yes;\
                        setAttr ".ovc" 22;\
                        setAttr ".cc" -type "nurbsCurve" \
                            1 16 0 no 3\
                            17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16\
                            17\
                            3.0256134625159068 0.98223993295180545 1.7790861870100279\
                            3.0256134625159068 0.98223993295180545 -1.7790861870100279\
                            -3.0256134625158988 0.98223993295183432 -1.7790861870100279\
                            -3.0256134625158988 0.98223993295183432 1.7790861870100279\
                            3.0256134625159068 0.98223993295180545 1.7790861870100279\
                            2.1404071683060226 -0.98223993295183265 1.2165588346789564\
                            2.1404071683060226 -0.98223993295183043 -1.2165588346789564\
                            3.0256134625159068 0.98223993295180545 -1.7790861870100279\
                            3.0256134625159068 0.98223993295180545 1.7790861870100279\
                            2.1404071683060226 -0.98223993295183265 1.2165588346789564\
                            -2.1404071683060293 -0.98223993295181233 1.2165588346789564\
                            -3.0256134625158988 0.98223993295183432 1.7790861870100279\
                            -3.0256134625158988 0.98223993295183432 -1.7790861870100279\
                            -2.1404071683060293 -0.98223993295181233 -1.2165588346789564\
                            -2.1404071683060293 -0.98223993295181233 1.2165588346789564\
                            -2.1404071683060293 -0.98223993295181233 -1.2165588346789564\
                            2.1404071683060226 -0.98223993295183043 -1.2165588346789564\
                            ;'%(self.sNames.controlNames['cog'],
                                self.sNames.controlNames['cog'],
                                self.sNames.controlNames['cog']))
        
        # Set scale to user defined value
        setAttr('%s.scaleX'%self.sNames.controlNames['cog'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['cog'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['cog'],self.scale)

        # Set it up
        self.processControl(self.sNames.controlNames['cog'],self.sNames.controlNames['cog'],pos) 
        
        # Lock and hide scale
        setAttr('%s.scaleX'%self.sNames.controlNames['cog'], lock=True, keyable=False)
        setAttr('%s.scaleY'%self.sNames.controlNames['cog'], lock=True, keyable=False)
        setAttr('%s.scaleZ'%self.sNames.controlNames['cog'], lock=True, keyable=False)
        
    def createHips(self,pos):
        # Create it
        mel.eval('createNode transform -n "%s";\
                        setAttr ".ove" yes;\
                        setAttr ".ovc" 13;\
                    createNode nurbsCurve -n "%sShape" -p "%s";\
                        setAttr -k off ".v";\
                        setAttr ".ove" yes;\
                        setAttr ".ovc" 13;\
                        setAttr ".cc" -type "nurbsCurve" \
                            1 16 0 no 3\
                            17 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16\
                            17\
                            1.8185793678087661 0.59038647812555067 1.0693399779361257\
                            1.8185793678087661 0.59038647812555067 -1.0693399779361257\
                            -1.8185793678087612 0.59038647812556799 -1.0693399779361257\
                            -1.8185793678087612 0.59038647812556799 1.0693399779361257\
                            1.8185793678087661 0.59038647812555067 1.0693399779361257\
                            1.2865160613591939 -0.59038647812556699 0.73122651782257997\
                            1.2865160613591939 -0.59038647812556566 -0.73122651782257997\
                            1.8185793678087661 0.59038647812555067 -1.0693399779361257\
                            1.8185793678087661 0.59038647812555067 1.0693399779361257\
                            1.2865160613591939 -0.59038647812556699 0.73122651782257997\
                            -1.2865160613591979 -0.59038647812555478 0.73122651782257997\
                            -1.8185793678087612 0.59038647812556799 1.0693399779361257\
                            -1.8185793678087612 0.59038647812556799 -1.0693399779361257\
                            -1.2865160613591979 -0.59038647812555478 -0.73122651782257997\
                            -1.2865160613591979 -0.59038647812555478 0.73122651782257997\
                            -1.2865160613591979 -0.59038647812555478 -0.73122651782257997\
                            1.2865160613591939 -0.59038647812556566 -0.73122651782257997\
                            ;'%(self.sNames.controlNames['hip'],
                            self.sNames.controlNames['hip'],
                            self.sNames.controlNames['hip']))
        
        setAttr('%s.scaleX'%self.sNames.controlNames['hip'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['hip'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['hip'],self.scale)
        
        # Set it up
        self.processControl(self.sNames.controlNames['hip'],self.sNames.controlNames['hip'],pos)       

    def createShoulder(self,pos):
        # Create it
        mel.eval('createNode transform -n "%s";\
                        createNode nurbsCurve -n "%sShape" -p "%s";\
                            setAttr -k off ".v";\
                            setAttr ".ove" yes;\
                            setAttr ".ovc" 17;\
                            setAttr ".cc" -type "nurbsCurve" \
                                3 8 0 no 3\
                                13 0 0 0 1 2 3 4 5 6 7 8 8 8\
                                11\
                                1.5000000000000475 -0.28450893268232602 -3.161013638317154e-008\
                                1.0191458026509925 -0.39370507131265231 -2.1476891877422454e-008\
                                0.057437407952881443 -0.61209734857330078 -1.2104028659242597e-009\
                                -1.7297496318114944 -0.26710167302456511 3.6451747846866905e-008\
                                -2.1384388807069454 -0.026549555422319428 4.5064229777480732e-008\
                                -1.7164948453608264 0.37329989471384173 3.6172424108576625e-008\
                                0.0044182621502317663 0.24040357266085413 -9.3107912763616835e-011\
                                1.6988217967599424 0.37213941073665818 -3.579999245752306e-008\
                                2.2002945508100247 -0.02190761951358448 -4.6367740556167893e-008\
                                1.7334315169366723 -0.19697516162607226 -3.6529337774169599e-008\
                                1.499999999999994 -0.28450893268231608 -3.1610136383170409e-008\
                                ;'%(self.sNames.controlNames['shoulder']+'_ik',
                                self.sNames.controlNames['shoulder']+'_ik',
                                self.sNames.controlNames['shoulder']+'_ik'))
        
        setAttr('%s_ik.scaleX'%self.sNames.controlNames['shoulder'],self.scale)
        setAttr('%s_ik.scaleY'%self.sNames.controlNames['shoulder'],self.scale)
        setAttr('%s_ik.scaleZ'%self.sNames.controlNames['shoulder'],self.scale)
                
        # Set it up
        self.processControl(self.sNames.controlNames['shoulder']+'_ik',self.sNames.controlNames['shoulder']+'_ik',pos)   

    def createRightFoot(self,pos):
        # Create it
        mel.eval('createNode transform -n "%s";\
                    setAttr ".ove" yes;\
                    setAttr ".ovc" 12;\
                    createNode nurbsCurve -n "%sShape" -p "%s";\
                    setAttr -k off ".v";\
                    setAttr ".ove" yes;\
                    setAttr ".ovc" 6;\
                    setAttr ".cc" -type "nurbsCurve" \
                        3 25 2 no 3\
                        30 -0.10000000000000001 -0.050000000000000003 0 1 2 3 4 5 6 7 8 9 10 11 12\
                         13 14 15 16 17 18 19 20 21 22 22.050000000000001 22.100000000000001 22.150000000000002\
                         23.150000000000002 24.150000000000002\
                        28\
                        -0.68163822508352545 1.6496644861033396 0\
                        -0.45758944267264179 1.6497582100499701 0\
                        -0.03347098415264186 1.6499328774050541 0\
                        0.71433803788122685 1.6498481162232217 0\
                        0.71433803788122685 1.6498481162232217 0\
                        0.71433803788122685 1.6498481162232217 0\
                        0.56593167676158396 1.0291757049618886 0\
                        0.81550748203889711 0.51349545305280553 0\
                        1.0600471530659963 -0.027453847473223658 0\
                        0.96985512660750373 -0.5785202086368082 0\
                        0.78639957141567562 -0.683253088669599 0\
                        -0.34421447674995664 -0.68325284759749927 0\
                        -1.8100106103413569 -0.68325282962489808 0\
                        -2.5707354100966548 -0.68325285357885668 0\
                        -2.8279959628701961 -0.68325136275581333 0\
                        -3.0204088912776679 -0.68325136275581333 0\
                        -2.9920260571635273 -0.29191264364446051 0\
                        -2.9026847718970146 -0.064212450766500839 0\
                        -2.6125796185017829 -0.0036243663809616966 0\
                        -1.3284135277150213 0.3308311936608942 0\
                        -0.87880554524818943 0.6021597194074837 0\
                        -0.69386761827958943 1.0047010866501924 0\
                        -0.65312740798167412 1.4211384314451343 0\
                        -0.68163822508352545 1.6496644861033396 0\
                        -0.67613006705534184 1.6496660514034442 0\
                        -0.68163822508352545 1.6496644861033396 0\
                        -0.45758944267264179 1.6497582100499701 0\
                        -0.03347098415264186 1.6499328774050541 0\
                        ;'%(self.sNames.controlNames['right_foot'],
                            self.sNames.controlNames['right_foot'],
                            self.sNames.controlNames['right_foot']))
        
        setAttr('%s.scaleX'%self.sNames.controlNames['right_foot'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['right_foot'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['right_foot'],self.scale)
                
        # Set it up
        self.processControl(self.sNames.controlNames['right_foot'],self.sNames.controlNames['right_foot'],pos)  
        
    def createLeftFoot(self,pos):
        # Create it
        mel.eval('createNode transform -n "%s";\
                    setAttr ".ove" yes;\
                    setAttr ".ovc" 13;\
                    createNode nurbsCurve -n "%sShape" -p "%s";\
                    setAttr -k off ".v";\
                    setAttr ".ove" yes;\
                    setAttr ".ovc" 13;\
                    setAttr ".cc" -type "nurbsCurve" \
                        3 25 2 no 3\
                        30 -0.10000000000000001 -0.050000000000000003 0 1 2 3 4 5 6 7 8 9 10 11 12\
                         13 14 15 16 17 18 19 20 21 22 22.050000000000001 22.100000000000001 22.150000000000002\
                         23.150000000000002 24.150000000000002\
                        28\
                        0.68163822508352545 1.6496644861033396 0\
                        0.45758944267264179 1.6497582100499701 0\
                        0.03347098415264186 1.6499328774050541 0\
                        -0.71433803788122685 1.6498481162232217 0\
                        -0.71433803788122685 1.6498481162232217 0\
                        -0.71433803788122685 1.6498481162232217 0\
                        -0.56593167676158396 1.0291757049618886 0\
                        -0.81550748203889711 0.51349545305280553 0\
                        -1.0600471530659963 -0.027453847473223658 0\
                        -0.96985512660750373 -0.5785202086368082 0\
                        -0.78639957141567562 -0.683253088669599 0\
                        0.34421447674995664 -0.68325284759749927 0\
                        1.8100106103413569 -0.68325282962489808 0\
                        2.5707354100966548 -0.68325285357885668 0\
                        2.8279959628701961 -0.68325136275581333 0\
                        3.0204088912776679 -0.68325136275581333 0\
                        2.9920260571635273 -0.29191264364446051 0\
                        2.9026847718970146 -0.064212450766500839 0\
                        2.6125796185017829 -0.0036243663809616966 0\
                        1.3284135277150213 0.3308311936608942 0\
                        0.87880554524818943 0.6021597194074837 0\
                        0.69386761827958943 1.0047010866501924 0\
                        0.65312740798167412 1.4211384314451343 0\
                        0.68163822508352545 1.6496644861033396 0\
                        0.67613006705534184 1.6496660514034442 0\
                        0.68163822508352545 1.6496644861033396 0\
                        0.45758944267264179 1.6497582100499701 0\
                        0.03347098415264186 1.6499328774050541 0\
                        ;'%(self.sNames.controlNames['left_foot'],self.sNames.controlNames['left_foot'],self.sNames.controlNames['left_foot']))

        setAttr('%s.scaleX'%self.sNames.controlNames['left_foot'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['left_foot'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['left_foot'],self.scale)
        
        # Set it up
        self.processControl(self.sNames.controlNames['left_foot'],self.sNames.controlNames['left_foot'],pos) 
 
    def createLeftToeCnt(self,pos):
        # Create it
        mel.eval('createNode transform -n "%s";\
                                setAttr ".ove" yes;\
                                setAttr ".ovc" 13;\
                                createNode nurbsCurve -n "%sShape" -p "%s";\
                                setAttr -k off ".v";\
                                setAttr ".cc" -type "nurbsCurve" \
                                    1 25 0 no 3\
                                    26 0 0.37689 0.75376699999999996 1.130657 1.5075460000000001 1.884423 2.2613129999999999\
                                     2.6382029999999999 3.0150800000000002 3.3919700000000002 3.768859 4.1457369999999996\
                                     4.5226249999999997 4.8995129999999998 5.2763910000000003 5.6532799999999996 6.0301710000000002\
                                     6.4070470000000004 6.7839369999999999 7.1608270000000003 7.5377039999999997 7.9145940000000001\
                                     8.2914840000000005 8.6683610000000009 9.0452510000000004 19.157319000000001\
                                    26\
                                    0 2.8587745093816909e-16 1.2874775815187656\
                                    -0.047553464272015213 2.8730482134552955e-16 1.2939058863534738\
                                    -0.09188520053322681 2.913821945753731e-16 1.3124417810937243\
                                    -0.13163815673896748 2.9783921583347539e-16 1.3554228266413404\
                                    -0.20111096978262952 3.0631483721885999e-16 1.4293324700151877\
                                    -0.2947442912208223 3.1615846008262137e-16 1.4608250798487949\
                                    -0.34076171948740519 3.2671745026971759e-16 1.4714045872901387\
                                    -0.29474412883635581 3.372764404568138e-16 1.4819841096999158\
                                    -0.20111112345592777 3.4712003504965668e-16 1.5134765140671596\
                                    -0.13077278149510707 3.5559568470595983e-16 1.587605307327999\
                                    -0.090303285436987249 3.6206550385327156e-16 1.6658517414736462\
                                    -0.047261909282496926 3.6551165739917568e-16 1.7445795680838987\
                                    0 3.6759874658121028e-16 1.7799986454062144\
                                    0.047261909282496926 3.6551165739917568e-16 1.7445795680838987\
                                    0.090303285436987249 3.6206550385327156e-16 1.6658517414736462\
                                    0.13077278149510707 3.5559568470595983e-16 1.587605307327999\
                                    0.20111112345592777 3.4712003504965668e-16 1.5134765140671596\
                                    0.29474412883635581 3.372764404568138e-16 1.4819841096999158\
                                    0.34076171948740519 3.2671745026971759e-16 1.4714045872901387\
                                    0.2947442912208223 3.1615846008262137e-16 1.4608250798487949\
                                    0.20111096978262952 3.0631483721885999e-16 1.4293324700151877\
                                    0.13163815673896748 2.9783921583347539e-16 1.3554228266413404\
                                    0.09188520053322681 2.913821945753731e-16 1.3124417810937243\
                                    0.047553464272015213 2.8730482134552955e-16 1.2939058863534738\
                                    0 2.8587745093816909e-16 1.2874775815187656\
                                    0 0 0\
                                    ;\
                            createNode nurbsCurve -n "%s1Shape" -p "%s";\
                                setAttr -k off ".v";\
                                setAttr ".cc" -type "nurbsCurve" \
                                    1 25 0 no 3\
                                    26 0 0.37689 0.75376699999999996 1.130657 1.5075460000000001 1.884423 2.2613129999999999\
                                     2.6382029999999999 3.0150800000000002 3.3919700000000002 3.768859 4.1457369999999996\
                                     4.5226249999999997 4.8995129999999998 5.2763910000000003 5.6532799999999996 6.0301710000000002\
                                     6.4070470000000004 6.7839369999999999 7.1608270000000003 7.5377039999999997 7.9145940000000001\
                                     8.2914840000000005 8.6683610000000009 9.0452510000000004 19.157319000000001\
                                    26\
                                    2.8636380164238621e-16 0.0010951644251418328 1.2874775815187656\
                                    3.056445086240939e-16 0.041297304396916937 1.2939058863534738\
                                    3.2636566208137243e-16 0.078775765612073306 1.3122687429120476\
                                    3.4726796960967201e-16 0.11130365854393356 1.339982257866638\
                                    3.6903037191682938e-16 0.14122282934805808 1.3754534380521506\
                                    3.8771158529267687e-16 0.16112331062881233 1.4181840566469075\
                                    4.0157623574299934e-16 0.16856699918143964 1.4714045872901389\
                                    4.0882955705255751e-16 0.16112329123110664 1.5246251931474248\
                                    4.0983557884051062e-16 0.14122284982341371 1.5673555601167521\
                                    4.065324450843542e-16 0.11469938752979866 1.6046859121551609\
                                    3.9024765224321075e-16 0.063489438438701765 1.6692739038339999\
                                    3.7093953800910835e-16 0.010829874803551109 1.7459011050068667\
                                    3.6755711035024337e-16 -1.6322814671021183e-31 1.7805449264428443\
                                    3.613206769205401e-16 -0.010829874803551109 1.7459011050068667\
                                    3.5591319875895299e-16 -0.014490780859233679 1.6692739038339999\
                                    3.4853396261039881e-16 -0.016762777182045004 1.6032471638672419\
                                    3.398816335563212e-16 -0.017029103885360712 1.5632896605024673\
                                    3.3006080110786421e-16 -0.016913365752027253 1.5189580515621539\
                                    3.1947531638660001e-16 -0.016973026139130452 1.4714045872901387\
                                    3.0894282073367178e-16 -0.016913365752027253 1.4238511230181234\
                                    2.9885934617164359e-16 -0.0173822479326863 1.379519386756912\
                                    2.9021200234950567e-16 -0.017641683405834281 1.3413485814439605\
                                    2.857233820627496e-16 -0.01308620602693746 1.3054069766161487\
                                    2.8534401703603021e-16 -0.0047676309300104481 1.2939058863534738\
                                    2.8636380164238621e-16 0.0010951644251418328 1.2874775815187656\
                                    0 0 0\
                                    ;'%(self.sNames.controlNames['left_toe'],self.sNames.controlNames['left_toe'],self.sNames.controlNames['left_toe'],
                                        self.sNames.controlNames['left_toe'],self.sNames.controlNames['left_toe']))

        setAttr('%s.scaleX'%self.sNames.controlNames['left_toe'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['left_toe'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['left_toe'],self.scale)
        
        # Set it up
        self.processControl(self.sNames.controlNames['left_toe'],self.sNames.controlNames['left_toe'],pos) 
        
    def createRightToeCnt(self,pos):
                # Create it
        mel.eval('createNode transform -n "%s";\
                                setAttr ".ove" yes;\
                                setAttr ".ovc" 6;\
                                createNode nurbsCurve -n "%sShape" -p "%s";\
                                setAttr -k off ".v";\
                                setAttr ".cc" -type "nurbsCurve" \
                                    1 25 0 no 3\
                                    26 0 0.37689 0.75376699999999996 1.130657 1.5075460000000001 1.884423 2.2613129999999999\
                                     2.6382029999999999 3.0150800000000002 3.3919700000000002 3.768859 4.1457369999999996\
                                     4.5226249999999997 4.8995129999999998 5.2763910000000003 5.6532799999999996 6.0301710000000002\
                                     6.4070470000000004 6.7839369999999999 7.1608270000000003 7.5377039999999997 7.9145940000000001\
                                     8.2914840000000005 8.6683610000000009 9.0452510000000004 19.157319000000001\
                                    26\
                                    0 2.8587745093816909e-16 1.2874775815187656\
                                    -0.047553464272015213 2.8730482134552955e-16 1.2939058863534738\
                                    -0.09188520053322681 2.913821945753731e-16 1.3124417810937243\
                                    -0.13163815673896748 2.9783921583347539e-16 1.3554228266413404\
                                    -0.20111096978262952 3.0631483721885999e-16 1.4293324700151877\
                                    -0.2947442912208223 3.1615846008262137e-16 1.4608250798487949\
                                    -0.34076171948740519 3.2671745026971759e-16 1.4714045872901387\
                                    -0.29474412883635581 3.372764404568138e-16 1.4819841096999158\
                                    -0.20111112345592777 3.4712003504965668e-16 1.5134765140671596\
                                    -0.13077278149510707 3.5559568470595983e-16 1.587605307327999\
                                    -0.090303285436987249 3.6206550385327156e-16 1.6658517414736462\
                                    -0.047261909282496926 3.6551165739917568e-16 1.7445795680838987\
                                    0 3.6759874658121028e-16 1.7799986454062144\
                                    0.047261909282496926 3.6551165739917568e-16 1.7445795680838987\
                                    0.090303285436987249 3.6206550385327156e-16 1.6658517414736462\
                                    0.13077278149510707 3.5559568470595983e-16 1.587605307327999\
                                    0.20111112345592777 3.4712003504965668e-16 1.5134765140671596\
                                    0.29474412883635581 3.372764404568138e-16 1.4819841096999158\
                                    0.34076171948740519 3.2671745026971759e-16 1.4714045872901387\
                                    0.2947442912208223 3.1615846008262137e-16 1.4608250798487949\
                                    0.20111096978262952 3.0631483721885999e-16 1.4293324700151877\
                                    0.13163815673896748 2.9783921583347539e-16 1.3554228266413404\
                                    0.09188520053322681 2.913821945753731e-16 1.3124417810937243\
                                    0.047553464272015213 2.8730482134552955e-16 1.2939058863534738\
                                    0 2.8587745093816909e-16 1.2874775815187656\
                                    0 0 0\
                                    ;\
                            createNode nurbsCurve -n "%s1Shape" -p "%s";\
                                setAttr -k off ".v";\
                                setAttr ".cc" -type "nurbsCurve" \
                                    1 25 0 no 3\
                                    26 0 0.37689 0.75376699999999996 1.130657 1.5075460000000001 1.884423 2.2613129999999999\
                                     2.6382029999999999 3.0150800000000002 3.3919700000000002 3.768859 4.1457369999999996\
                                     4.5226249999999997 4.8995129999999998 5.2763910000000003 5.6532799999999996 6.0301710000000002\
                                     6.4070470000000004 6.7839369999999999 7.1608270000000003 7.5377039999999997 7.9145940000000001\
                                     8.2914840000000005 8.6683610000000009 9.0452510000000004 19.157319000000001\
                                    26\
                                    2.8636380164238621e-16 0.0010951644251418328 1.2874775815187656\
                                    3.056445086240939e-16 0.041297304396916937 1.2939058863534738\
                                    3.2636566208137243e-16 0.078775765612073306 1.3122687429120476\
                                    3.4726796960967201e-16 0.11130365854393356 1.339982257866638\
                                    3.6903037191682938e-16 0.14122282934805808 1.3754534380521506\
                                    3.8771158529267687e-16 0.16112331062881233 1.4181840566469075\
                                    4.0157623574299934e-16 0.16856699918143964 1.4714045872901389\
                                    4.0882955705255751e-16 0.16112329123110664 1.5246251931474248\
                                    4.0983557884051062e-16 0.14122284982341371 1.5673555601167521\
                                    4.065324450843542e-16 0.11469938752979866 1.6046859121551609\
                                    3.9024765224321075e-16 0.063489438438701765 1.6692739038339999\
                                    3.7093953800910835e-16 0.010829874803551109 1.7459011050068667\
                                    3.6755711035024337e-16 -1.6322814671021183e-31 1.7805449264428443\
                                    3.613206769205401e-16 -0.010829874803551109 1.7459011050068667\
                                    3.5591319875895299e-16 -0.014490780859233679 1.6692739038339999\
                                    3.4853396261039881e-16 -0.016762777182045004 1.6032471638672419\
                                    3.398816335563212e-16 -0.017029103885360712 1.5632896605024673\
                                    3.3006080110786421e-16 -0.016913365752027253 1.5189580515621539\
                                    3.1947531638660001e-16 -0.016973026139130452 1.4714045872901387\
                                    3.0894282073367178e-16 -0.016913365752027253 1.4238511230181234\
                                    2.9885934617164359e-16 -0.0173822479326863 1.379519386756912\
                                    2.9021200234950567e-16 -0.017641683405834281 1.3413485814439605\
                                    2.857233820627496e-16 -0.01308620602693746 1.3054069766161487\
                                    2.8534401703603021e-16 -0.0047676309300104481 1.2939058863534738\
                                    2.8636380164238621e-16 0.0010951644251418328 1.2874775815187656\
                                    0 0 0\
                                    ;'%(self.sNames.controlNames['right_toe'],self.sNames.controlNames['right_toe'],self.sNames.controlNames['right_toe'],
                                        self.sNames.controlNames['right_toe'],self.sNames.controlNames['right_toe']))

        setAttr('%s.scaleX'%self.sNames.controlNames['right_toe'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['right_toe'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['right_toe'],self.scale)
        
        # Set it up
        self.processControl(self.sNames.controlNames['right_toe'],self.sNames.controlNames['right_toe'],pos) 
               
    def createRightHand(self,pos):
        # Create it
        mel.eval('createNode transform -n "%s";\
                        setAttr ".ove" yes;\
                        setAttr ".ovc" 6;\
                        createNode nurbsCurve -n "%sShape" -p "%s";\
                        setAttr -k off ".v";\
                        setAttr ".cc" -type "nurbsCurve" \
                            1 81 0 no 3\
                            82 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27\
                             28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54\
                             55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81\
                            82\
                            0.36695969108692367 0.29407570173461911 0\
                            0.39280652609824157 0.41516145097594398 0\
                            0.45329411191482294 0.65523088546894848 0\
                            0.53110071134083203 0.90939869264399553 0\
                            0.55184899259649267 1.0261084556036888 0\
                            0.54666192228257759 1.1324438055769108 0\
                            0.52072657071300166 1.2206245456307503 0\
                            0.46626192387893123 1.285463333092651 0\
                            0.39621155382544382 1.3137755585204332 0\
                            0.32102313801338411 1.2932440747428442 0\
                            0.26655849117931374 1.2543406388505194 0\
                            0.20761408942146922 1.1727248314743703 0\
                            0.17047417572828319 1.0551685778590902 0\
                            0.15873633538599904 0.93114217237311625 0\
                            0.14636662299707359 0.68209007754809636 0\
                            0.13561853395543358 0.56492493094099605 0\
                            0.11872630633612948 0.50480502928948612 0\
                            0.076173264657169545 0.45537792787553522 0\
                            0.030545566282290042 0.47627600638363238 0\
                            -0.0049336405986566707 0.52788007041344709 0\
                            -0.017196697343847323 0.65176730063397548 0\
                            -0.0084387873622146989 0.89862391245555773 0\
                            -0.0024080970527868154 1.1458029969078398 0\
                            -0.032342860952887374 1.2657129738968584 0\
                            -0.070602713377016901 1.3373343085904437 0\
                            -0.14062857115283287 1.391798955424514 0\
                            -0.21349322304164109 1.4116980224381801 0\
                            -0.26771247474035642 1.391798955424514 0\
                            -0.31635763449658888 1.3472604192541682 0\
                            -0.34551907416636551 1.2958374737204814 0\
                            -0.36478245611241916 1.234908122188533 0\
                            -0.3721960583148225 1.1112717342761753 0\
                            -0.32326519434439749 0.86847081497465128 0\
                            -0.26207328908272381 0.62729887270371421 0\
                            -0.23731561627593972 0.51007680314068815 0\
                            -0.24177712317078059 0.44774698347777853 0\
                            -0.26497881106271054 0.3962344319512705 0\
                            -0.31958345023814888 0.41403089025800954 0\
                            -0.36320250363717521 0.46023408244088604 0\
                            -0.46383657018266372 0.68364170472469776 0\
                            -0.49134152459913344 0.80378345891703185 0\
                            -0.5430074140404082 0.91596090173527789 0\
                            -0.58931274071358231 0.97942455041981147 0\
                            -0.66452566880331343 1.0131406436395805 0\
                            -0.74808693395065162 1.009314821812352 0\
                            -0.78642250207692188 0.96386333947806602 0\
                            -0.8066734564544934 0.90160160947535484 0\
                            -0.79612582337247739 0.78113574850047618 0\
                            -0.74480419525316577 0.66753986188097691 0\
                            -0.63183255463836541 0.4478118048342874 0\
                            -0.57158791272937204 0.20805639985411811 0\
                            -0.52410681380389168 -0.16032282446862209 0\
                            -0.45645646809307805 -0.39781465678515532 0\
                            -0.3903332372811944 -0.50222906126485978 0\
                            -0.3003489383080194 -0.58701811916489577 0\
                            -0.19386787646197265 -0.6498558876928856 0\
                            -0.076793425282256703 -0.68971911543536735 0\
                            0.045980675173348078 -0.70408085892305761 0\
                            0.16842467695631094 -0.68744219719833244 0\
                            0.28224253586805714 -0.63931043347999605 0\
                            0.38214913248398585 -0.56639866354633051 0\
                            0.54280096619068663 -0.37867846632435226 0\
                            0.65594500982510928 -0.15882539666153855 0\
                            0.69772373588829295 -0.042672607122268343 0\
                            0.75986862403410371 0.063967512170001878 0\
                            0.86242200192126517 0.13233851884435557 0\
                            0.97139650712377767 0.1911265867423845 0\
                            1.0548371173932445 0.28113104025497826 0\
                            1.0861202308748037 0.34659843145983077 0\
                            1.0964943715026341 0.41921796057192467 0\
                            1.0809331605608885 0.47627600638363238 0\
                            1.0368426543546483 0.53333405219534002 0\
                            0.95903632728728005 0.55667600478727863 0\
                            0.89160386848910134 0.55408233345100066 0\
                            0.82354307830661155 0.53804340545330309 0\
                            0.72023526698445173 0.47107967587593019 0\
                            0.63318890066951794 0.38127295473655265 0\
                            0.55807157046270528 0.28594280036187975 0\
                            0.51035215772653053 0.22988866850013753 0\
                            0.46007747622242967 0.2169388322063216 0\
                            0.40142313641703048 0.24545015180052382 0\
                            0.36695969108692367 0.29407570173461911 0;'\
                            %(self.sNames.controlNames['right_hand'],self.sNames.controlNames['right_hand'],self.sNames.controlNames['right_hand']))  

        setAttr('%s.scaleX'%self.sNames.controlNames['right_hand'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['right_hand'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['right_hand'],self.scale)
        
        # Set it up
        self.processHandControl(self.sNames.controlNames['right_hand'],
                                self.sNames.armJoints['right_wrist'],
                                pos)         
        
    def createLeftHand(self,pos):
        # Create it
        mel.eval('createNode transform -n "%s";\
                        setAttr ".ove" yes;\
                        setAttr ".ovc" 13;\
                        createNode nurbsCurve -n "%sShape" -p "%s";\
                        setAttr -k off ".v";\
                        setAttr ".cc" -type "nurbsCurve" \
                            1 81 0 no 3\
                            82 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27\
                             28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54\
                             55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81\
                            82\
                            -0.36695969108692367 0.29407570173461911 0\
                            -0.39280652609824157 0.41516145097594398 0\
                            -0.45329411191482294 0.65523088546894848 0\
                            -0.53110071134083203 0.90939869264399553 0\
                            -0.55184899259649267 1.0261084556036888 0\
                            -0.54666192228257759 1.1324438055769108 0\
                            -0.52072657071300166 1.2206245456307503 0\
                            -0.46626192387893123 1.285463333092651 0\
                            -0.39621155382544382 1.3137755585204332 0\
                            -0.32102313801338411 1.2932440747428442 0\
                            -0.26655849117931374 1.2543406388505194 0\
                            -0.20761408942146922 1.1727248314743703 0\
                            -0.17047417572828319 1.0551685778590902 0\
                            -0.15873633538599904 0.93114217237311625 0\
                            -0.14636662299707359 0.68209007754809636 0\
                            -0.13561853395543358 0.56492493094099605 0\
                            -0.11872630633612948 0.50480502928948612 0\
                            -0.076173264657169545 0.45537792787553522 0\
                            -0.030545566282290042 0.47627600638363238 0\
                            0.0049336405986566707 0.52788007041344709 0\
                            0.017196697343847323 0.65176730063397548 0\
                            0.0084387873622146989 0.89862391245555773 0\
                            0.0024080970527868154 1.1458029969078398 0\
                            0.032342860952887374 1.2657129738968584 0\
                            0.070602713377016901 1.3373343085904437 0\
                            0.14062857115283287 1.391798955424514 0\
                            0.21349322304164109 1.4116980224381801 0\
                            0.26771247474035642 1.391798955424514 0\
                            0.31635763449658888 1.3472604192541682 0\
                            0.34551907416636551 1.2958374737204814 0\
                            0.36478245611241916 1.234908122188533 0\
                            0.3721960583148225 1.1112717342761753 0\
                            0.32326519434439749 0.86847081497465128 0\
                            0.26207328908272381 0.62729887270371421 0\
                            0.23731561627593972 0.51007680314068815 0\
                            0.24177712317078059 0.44774698347777853 0\
                            0.26497881106271054 0.3962344319512705 0\
                            0.31958345023814888 0.41403089025800954 0\
                            0.36320250363717521 0.46023408244088604 0\
                            0.46383657018266372 0.68364170472469776 0\
                            0.49134152459913344 0.80378345891703185 0\
                            0.5430074140404082 0.91596090173527789 0\
                            0.58931274071358231 0.97942455041981147 0\
                            0.66452566880331343 1.0131406436395805 0\
                            0.74808693395065162 1.009314821812352 0\
                            0.78642250207692188 0.96386333947806602 0\
                            0.8066734564544934 0.90160160947535484 0\
                            0.79612582337247739 0.78113574850047618 0\
                            0.74480419525316577 0.66753986188097691 0\
                            0.63183255463836541 0.4478118048342874 0\
                            0.57158791272937204 0.20805639985411811 0\
                            0.52410681380389168 -0.16032282446862209 0\
                            0.45645646809307805 -0.39781465678515532 0\
                            0.3903332372811944 -0.50222906126485978 0\
                            0.3003489383080194 -0.58701811916489577 0\
                            0.19386787646197265 -0.6498558876928856 0\
                            0.076793425282256703 -0.68971911543536735 0\
                            -0.045980675173348078 -0.70408085892305761 0\
                            -0.16842467695631094 -0.68744219719833244 0\
                            -0.28224253586805714 -0.63931043347999605 0\
                            -0.38214913248398585 -0.56639866354633051 0\
                            -0.54280096619068663 -0.37867846632435226 0\
                            -0.65594500982510928 -0.15882539666153855 0\
                            -0.69772373588829295 -0.042672607122268343 0\
                            -0.75986862403410371 0.063967512170001878 0\
                            -0.86242200192126517 0.13233851884435557 0\
                            -0.97139650712377767 0.1911265867423845 0\
                            -1.0548371173932445 0.28113104025497826 0\
                            -1.0861202308748037 0.34659843145983077 0\
                            -1.0964943715026341 0.41921796057192467 0\
                            -1.0809331605608885 0.47627600638363238 0\
                            -1.0368426543546483 0.53333405219534002 0\
                            -0.95903632728728005 0.55667600478727863 0\
                            -0.89160386848910134 0.55408233345100066 0\
                            -0.82354307830661155 0.53804340545330309 0\
                            -0.72023526698445173 0.47107967587593019 0\
                            -0.63318890066951794 0.38127295473655265 0\
                            -0.55807157046270528 0.28594280036187975 0\
                            -0.51035215772653053 0.22988866850013753 0\
                            -0.46007747622242967 0.2169388322063216 0\
                            -0.40142313641703048 0.24545015180052382 0\
                            -0.36695969108692367 0.29407570173461911 0;'\
                            %(self.sNames.controlNames['left_hand'],self.sNames.controlNames['left_hand'],self.sNames.controlNames['left_hand']))
        
        setAttr('%s.scaleX'%self.sNames.controlNames['left_hand'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['left_hand'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['left_hand'],self.scale)



        # Set it up
        self.processHandControl(self.sNames.controlNames['left_hand'],
                                self.sNames.armJoints['left_wrist'],
                                pos)  
        
    def createEyes(self,l_pos,r_pos,follow_pos):
        """
        Create Follow on FK eye controls.
        """
        
        mel.eval('createNode transform -n "%s";\
                    setAttr ".ove" yes;\
                    setAttr ".ovc" 15;\
                createNode nurbsCurve -n "%sShape" -p "%s";\
                    setAttr -k off ".v";\
                    setAttr ".ove" yes;\
                    setAttr ".ovc" 15;\
                    setAttr ".cc" -type "nurbsCurve" \
                        1 52 0 no 3\
                        53 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27\
                         28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52\
                        53\
                        0 0.45992507866995752 0\
                        0 0.42491558168160037 0.17600550888065536\
                        0 0.32521624260307769 0.32521624260307769\
                        0 0.17600550888065536 0.42491558168160037\
                        0 0 0.45992507866995752\
                        0 -0.17600550888065536 0.42491558168160037\
                        0 -0.32521624260307769 0.32521624260307769\
                        0 -0.42491558168160037 0.17600550888065536\
                        0 -0.45992507866995752 0\
                        0 -0.42491558168160037 -0.17600550888065536\
                        0 -0.32521624260307769 -0.32521624260307769\
                        0 -0.17600550888065536 -0.42491558168160037\
                        0 0 -0.45992507866995752\
                        0 0.17600550888065536 -0.42491558168160037\
                        0 0.32521624260307769 -0.32521624260307769\
                        0 0.42491558168160037 -0.17600550888065536\
                        0 0.45992507866995752 0\
                        0.17600550888065536 0.42491558168160037 0\
                        0.32521624260307769 0.32521624260307769 0\
                        0.42491558168160037 0.17600550888065536 0\
                        0.45992507866995752 0 0\
                        0.42491558168160037 -0.17600550888065536 0\
                        0.32521624260307769 -0.32521624260307769 0\
                        0.17600550888065536 -0.42491558168160037 0\
                        0 -0.45992507866995752 0\
                        -0.17600550888065536 -0.42491558168160037 0\
                        -0.32521624260307769 -0.32521624260307769 0\
                        -0.42491558168160037 -0.17600550888065536 0\
                        -0.45992507866995752 0 0\
                        -0.42491558168160037 0.17600550888065536 0\
                        -0.32521624260307769 0.32521624260307769 0\
                        -0.17600550888065536 0.42491558168160037 0\
                        0 0.45992507866995752 0\
                        0 0.42491558168160037 -0.17600550888065536\
                        0 0.32521624260307769 -0.32521624260307769\
                        0 0.17600550888065536 -0.42491558168160037\
                        0 0 -0.45992507866995752\
                        -0.17600550888065536 0 -0.42491558168160037\
                        -0.32521624260307769 0 -0.32521624260307769\
                        -0.42491558168160037 0 -0.17600550888065536\
                        -0.45992507866995752 0 0\
                        -0.42491558168160037 0 0.17600550888065536\
                        -0.32521624260307769 0 0.32521624260307769\
                        -0.17600550888065536 0 0.42491558168160037\
                        0 0 0.45992507866995752\
                        0.17600550888065536 0 0.42491558168160037\
                        0.32521624260307769 0 0.32521624260307769\
                        0.42491558168160037 0 0.17600550888065536\
                        0.45992507866995752 0 0\
                        0.42491558168160037 0 -0.17600550888065536\
                        0.32521624260307769 0 -0.32521624260307769\
                        0.17600550888065536 0 -0.42491558168160037\
                        0 0 -0.45992507866995752\
                        ;'%(self.sNames.controlNames['right_eye_fk'],
                            self.sNames.controlNames['right_eye_fk'],
                            self.sNames.controlNames['right_eye_fk']))
        
        setAttr('%s.scaleX'%self.sNames.controlNames['right_eye_fk'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['right_eye_fk'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['right_eye_fk'],self.scale)
        
        mel.eval('createNode transform -n "%s";\
                    setAttr ".ove" yes;\
                    setAttr ".ovc" 15;\
                createNode nurbsCurve -n "%sShape" -p "%s";\
                    setAttr -k off ".v";\
                    setAttr ".ove" yes;\
                    setAttr ".ovc" 4;\
                    setAttr ".cc" -type "nurbsCurve" \
                        1 52 0 no 3\
                        53 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27\
                         28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52\
                        53\
                        0 0.45992507866995752 0\
                        0 0.42491558168160037 0.17600550888065536\
                        0 0.32521624260307769 0.32521624260307769\
                        0 0.17600550888065536 0.42491558168160037\
                        0 0 0.45992507866995752\
                        0 -0.17600550888065536 0.42491558168160037\
                        0 -0.32521624260307769 0.32521624260307769\
                        0 -0.42491558168160037 0.17600550888065536\
                        0 -0.45992507866995752 0\
                        0 -0.42491558168160037 -0.17600550888065536\
                        0 -0.32521624260307769 -0.32521624260307769\
                        0 -0.17600550888065536 -0.42491558168160037\
                        0 0 -0.45992507866995752\
                        0 0.17600550888065536 -0.42491558168160037\
                        0 0.32521624260307769 -0.32521624260307769\
                        0 0.42491558168160037 -0.17600550888065536\
                        0 0.45992507866995752 0\
                        0.17600550888065536 0.42491558168160037 0\
                        0.32521624260307769 0.32521624260307769 0\
                        0.42491558168160037 0.17600550888065536 0\
                        0.45992507866995752 0 0\
                        0.42491558168160037 -0.17600550888065536 0\
                        0.32521624260307769 -0.32521624260307769 0\
                        0.17600550888065536 -0.42491558168160037 0\
                        0 -0.45992507866995752 0\
                        -0.17600550888065536 -0.42491558168160037 0\
                        -0.32521624260307769 -0.32521624260307769 0\
                        -0.42491558168160037 -0.17600550888065536 0\
                        -0.45992507866995752 0 0\
                        -0.42491558168160037 0.17600550888065536 0\
                        -0.32521624260307769 0.32521624260307769 0\
                        -0.17600550888065536 0.42491558168160037 0\
                        0 0.45992507866995752 0\
                        0 0.42491558168160037 -0.17600550888065536\
                        0 0.32521624260307769 -0.32521624260307769\
                        0 0.17600550888065536 -0.42491558168160037\
                        0 0 -0.45992507866995752\
                        -0.17600550888065536 0 -0.42491558168160037\
                        -0.32521624260307769 0 -0.32521624260307769\
                        -0.42491558168160037 0 -0.17600550888065536\
                        -0.45992507866995752 0 0\
                        -0.42491558168160037 0 0.17600550888065536\
                        -0.32521624260307769 0 0.32521624260307769\
                        -0.17600550888065536 0 0.42491558168160037\
                        0 0 0.45992507866995752\
                        0.17600550888065536 0 0.42491558168160037\
                        0.32521624260307769 0 0.32521624260307769\
                        0.42491558168160037 0 0.17600550888065536\
                        0.45992507866995752 0 0\
                        0.42491558168160037 0 -0.17600550888065536\
                        0.32521624260307769 0 -0.32521624260307769\
                        0.17600550888065536 0 -0.42491558168160037\
                        0 0 -0.45992507866995752\
                        ;'%(self.sNames.controlNames['left_eye_fk'],
                            self.sNames.controlNames['left_eye_fk'],
                            self.sNames.controlNames['left_eye_fk']))
        
        setAttr('%s.scaleX'%self.sNames.controlNames['left_eye_fk'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['left_eye_fk'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['left_eye_fk'],self.scale)
        
        mel.eval('createNode transform -n "%s";\
                        setAttr ".rp" -type "double3" 0 -1.1102230246251565e-016 2.4651903288156619e-032 ;\
                        setAttr ".sp" -type "double3" 0 -1.1102230246251565e-016 2.4651903288156619e-032 ;\
                    createNode nurbsCurve -n "%sShape" -p "%s";\
                        setAttr -k off ".v";\
                        setAttr ".cc" -type "nurbsCurve" \
                            3 8 2 no 3\
                            13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                            11\
                            2.8113891996069014 1.1704898855173616 -1.8822912961178822e-016\
                            -4.5360319023563308e-016 1.6553226707191855 -2.6619618793067429e-016\
                            -2.8113891996068983 1.1704898855173622 -1.8822912961178835e-016\
                            -3.9759047351933168 4.7967109707098437e-016 -7.7136995559509044e-032\
                            -2.8113891996068991 -1.170489885517362 1.882291296117883e-016\
                            -1.1980176909410914e-015 -1.6553226707191857 2.6619618793067433e-016\
                            2.8113891996068965 -1.1704898855173624 1.8822912961178837e-016\
                            3.9759047351933168 -8.8907703553826068e-016 1.4297449181564368e-031\
                            2.8113891996069014 1.1704898855173616 -1.8822912961178822e-016\
                            -4.5360319023563308e-016 1.6553226707191855 -2.6619618793067429e-016\
                            -2.8113891996068983 1.1704898855173622 -1.8822912961178835e-016\
                            ;\
                    createNode transform -n "%s" -p "%s";\
                        setAttr ".rp" -type "double3" 2 0 0 ;\
                        setAttr ".sp" -type "double3" 2 0 0 ;\
                    createNode nurbsCurve -n "%sShape" -p "%s";\
                        setAttr -k off ".v";\
                        setAttr ".ove" yes;\
                        setAttr ".ovc" 12;\
                        setAttr ".cc" -type "nurbsCurve" \
                            3 8 2 no 3\
                            13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                            11\
                            2.5468856201507162 0.54688562015071507 -8.7945915254681845e-017\
                            2 0.77341306108396268 -1.2437430610848605e-016\
                            1.4531143798492847 0.54688562015071551 -8.7945915254681895e-017\
                            1.2265869389160375 2.7962690706633726e-016 -3.6040562310779004e-032\
                            1.4531143798492843 -0.54688562015071529 8.7945915254681895e-017\
                            1.9999999999999996 -0.77341306108396268 1.2437430610848605e-016\
                            2.5468856201507153 -0.54688562015071529 8.7945915254681895e-017\
                            2.7734130610839625 -3.5989051260045327e-016 6.6801682432113469e-032\
                            2.5468856201507162 0.54688562015071507 -8.7945915254681845e-017\
                            2 0.77341306108396268 -1.2437430610848605e-016\
                            1.4531143798492847 0.54688562015071551 -8.7945915254681895e-017\
                            ;\
                    createNode transform -n "%s" -p "%s";\
                        setAttr ".rp" -type "double3" -2 -5.5511151231257827e-017 0 ;\
                        setAttr ".sp" -type "double3" -2 -5.5511151231257827e-017 0 ;\
                    createNode nurbsCurve -n "%sShape" -p "%s";\
                        setAttr -k off ".v";\
                        setAttr ".cc" -type "nurbsCurve" \
                            3 8 2 no 3\
                            13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                            11\
                            -1.453114379849284 0.54688562015071507 -8.7945915254681845e-017\
                            -2 0.77341306108396268 -1.2437430610848605e-016\
                            -2.5468856201507153 0.5468856201507154 -8.7945915254681895e-017\
                            -2.7734130610839625 2.2411575583507943e-016 -3.6040562310779004e-032\
                            -2.5468856201507157 -0.54688562015071529 8.7945915254681895e-017\
                            -2.0000000000000004 -0.77341306108396279 1.2437430610848605e-016\
                            -1.4531143798492849 -0.5468856201507154 8.7945915254681895e-017\
                            -1.2265869389160373 -4.154016638317111e-016 6.6801682432113469e-032\
                            -1.453114379849284 0.54688562015071507 -8.7945915254681845e-017\
                            -2 0.77341306108396268 -1.2437430610848605e-016\
                            -2.5468856201507153 0.5468856201507154 -8.7945915254681895e-017\
                            ;'%(self.sNames.controlNames['eyes_follow'],
                                self.sNames.controlNames['eyes_follow'],
                                self.sNames.controlNames['eyes_follow'],
                                self.sNames.controlNames['left_eye_aim'],
                                self.sNames.controlNames['eyes_follow'],
                                self.sNames.controlNames['left_eye_aim'],
                                self.sNames.controlNames['left_eye_aim'],
                                self.sNames.controlNames['right_eye_aim'],
                                self.sNames.controlNames['eyes_follow'],
                                self.sNames.controlNames['right_eye_aim'],
                                self.sNames.controlNames['right_eye_aim']) )

        setAttr('%s.scaleX'%self.sNames.controlNames['eyes_follow'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['eyes_follow'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['eyes_follow'],self.scale)

        # Set it up
        self.processControl(self.sNames.controlNames['eyes_follow'],self.sNames.controlNames['eyes_follow'],follow_pos)
        self.processControl(self.sNames.controlNames['right_eye_fk'],self.sNames.controlNames['right_eye_fk'],r_pos)
        self.processControl(self.sNames.controlNames['left_eye_fk'],self.sNames.controlNames['left_eye_fk'],l_pos)
        
    def createHead(self,pos):
        mel.eval('createNode transform -n "%s";\
                        setAttr ".ove" yes;\
                        setAttr ".ovc" 17;\
                        setAttr ".t" -type "double3" 0 0 0 ;\
                        setAttr ".r" -type "double3" 180 0 90 ;\
                        setAttr ".ra" -type "double3" -180 0 90 ;\
                        createNode nurbsCurve -n "%sShape" -p "%s";\
                            setAttr -k off ".v";\
                            setAttr ".cc" -type "nurbsCurve" \
                                    1 52 0 no 3\
                                    53 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27\
                                     28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52\
                                    53\
                                    -3.1486257321938338e-08 -2.9858931330710741e-15 -1.494140792741524\
                                    0.57176672038801346 -0.0042143854282205833 -1.3804068076469673\
                                    1.0564886927370691 -0.0077871800863681681 -1.0565174357966289\
                                    1.3803692871025408 -0.010174443101528739 -0.57178231007743785\
                                    1.4941002069011085 -0.011012732282902102 -3.1485401956363016e-08\
                                    1.3803693112010516 -0.010174443101526452 0.57178225189997145\
                                    1.0564887372653751 -0.0077871800863639458 1.0565173912695327\
                                    0.57176677856706037 -0.0042143854282150669 1.3804067835491112\
                                    3.1486257321938338e-08 2.9858931330710737e-15 1.494140792741524\
                                    -0.57176672038801346 0.0042143854282205833 1.3804068076469673\
                                    -1.0564886927370691 0.0077871800863681681 1.0565174357966289\
                                    -1.3803692871025408 0.010174443101528739 0.57178231007743785\
                                    -1.4941002069011085 0.011012732282902102 3.1485401956363016e-08\
                                    -1.3803693112010516 0.010174443101526452 -0.57178225189997145\
                                    -1.0564887372653751 0.0077871800863639458 -1.0565173912695327\
                                    -0.57176677856706037 0.0042143854282150669 -1.3804067835491112\
                                    -3.1486257321938338e-08 -2.9858931330710741e-15 -1.494140792741524\
                                    -0.0042144145177411448 -0.57176674947753969 -1.3804067955092276\
                                    -0.0077872023505188371 -1.0564887150012243 -1.0565174133689783\
                                    -0.010174455150782776 -1.3803692991517973 -0.57178228077429438\
                                    -0.011012732282901854 -1.4941002069011085 2.3207589666778782e-10\
                                    -0.010174431052271954 -1.3803692991517951 0.57178228120311492\
                                    -0.0077871578222129248 -1.0564887150012199 1.0565174136971833\
                                    -0.0042143563386943163 -0.57176674947753414 1.3804067956868509\
                                    3.1486257321938338e-08 2.9858931330710737e-15 1.494140792741524\
                                    0.0042144145177411448 0.57176674947753969 1.3804067955092276\
                                    0.0077872023505188371 1.0564887150012243 1.0565174133689783\
                                    0.010174455150782776 1.3803692991517973 0.57178228077429438\
                                    0.011012732282901854 1.4941002069011085 -2.3207589666778782e-10\
                                    0.010174431052271954 1.3803692991517951 -0.57178228120311492\
                                    0.0077871578222129248 1.0564887150012199 -1.0565174136971833\
                                    0.0042143563386943163 0.57176674947753414 -1.3804067956868509\
                                    -3.1486257321938338e-08 -2.9858931330710741e-15 -1.494140792741524\
                                    -0.57176677856706037 0.0042143854282150669 -1.3804067835491112\
                                    -1.0564887372653751 0.0077871800863639458 -1.0565173912695327\
                                    -1.3803693112010516 0.010174443101526452 -0.57178225189997145\
                                    -1.4941002069011085 0.011012732282902102 3.1485401956363016e-08\
                                    -1.3761549137235785 0.58194119257906451 2.8999921659080147e-08\
                                    -1.0487015349148563 1.0642758950875881 2.2099445630092918e-08\
                                    -0.56159230637600954 1.3845836845800139 1.1834517797453435e-08\
                                    0.011012732282901854 1.4941002069011085 -2.3207589666778782e-10\
                                    0.58194119257906429 1.3761549137235785 -1.2263338356280306e-08\
                                    1.0642758950875879 1.0487015349148561 -2.2427650612223051e-08\
                                    1.3845836845800139 0.56159230637600932 -2.9177544659809187e-08\
                                    1.4941002069011085 -0.011012732282902102 -3.1485401956363016e-08\
                                    1.3761549137235785 -0.58194119257906451 -2.8999921659080147e-08\
                                    1.0487015349148563 -1.0642758950875881 -2.2099445630092918e-08\
                                    0.56159230637600954 -1.3845836845800139 -1.1834517797453435e-08\
                                    -0.011012732282901854 -1.4941002069011085 2.3207589666778782e-10\
                                    -0.58194119257906429 -1.3761549137235785 1.2263338356280306e-08\
                                    -1.0642758950875879 -1.0487015349148561 2.2427650612223051e-08\
                                    -1.3845836845800139 -0.56159230637600932 2.9177544659809187e-08\
                                    -1.4941002069011085 0.011012732282902102 3.1485401956363016e-08\
                                ;'%(self.sNames.controlNames['head'],
                                self.sNames.controlNames['head'],
                                self.sNames.controlNames['head']) )

        setAttr('%s.scaleX'%self.sNames.controlNames['head'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['head'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['head'],self.scale)
        
        # Set it up
        # Zero'd by createHeadRig()
        self.processControl(self.sNames.controlNames['head'],self.sNames.controlNames['head'],pos)
        
    def createJaw(self,pos):
        mel.eval('createNode transform -n "%s";\
                        setAttr ".ove" yes;\
                        setAttr ".ovc" 17;\
                        setAttr ".r" -type "double3" 4.1347365622449708e-015 39.715395408733556 -90.000000000000057 ;\
                    createNode nurbsCurve -n "%sShape" -p "%s";\
                        setAttr -k off ".v";\
                        setAttr ".cc" -type "nurbsCurve" \
                            1 25 0 no 3\
                            26 0 0.37689 0.75376699999999996 1.130657 1.5075460000000001 1.884423 2.2613129999999999\
                             2.6382029999999999 3.0150800000000002 3.3919700000000002 3.768859 4.1457369999999996\
                             4.5226249999999997 4.8995129999999998 5.2763910000000003 5.6532799999999996 6.0301710000000002\
                             6.4070470000000004 6.7839369999999999 7.1608270000000003 7.5377039999999997 7.9145940000000001\
                             8.2914840000000005 8.6683610000000009 9.0452510000000004 19.157319000000001\
                            26\
                            0 5.7175490187633818e-016 2.5749551630375311\
                            -0.095106928544030425 5.746096426910591e-016 2.5878117727069476\
                            -0.18377040106645362 5.827643891507462e-016 2.6245374858240953\
                            -0.26011201169235643 5.9567843166695079e-016 2.682697162887921\
                            -0.31827168875618217 6.1262967443771998e-016 2.759038773513824\
                            -0.35499740187332968 6.3231692016524274e-016 2.8477022460362469\
                            -0.36785401154274661 6.5343490053943517e-016 2.9428091745802774\
                            -0.35499740187332968 6.745528809136276e-016 3.0379161031243078\
                            -0.31827168875618217 6.9424007009931335e-016 3.1265793210049346\
                            -0.26011201169235643 7.1119136941191965e-016 3.2029211862726341\
                            -0.18377040106645362 7.2410535538628704e-016 3.2610806086946629\
                            -0.095106928544030425 7.3226021492964845e-016 3.2978068310954041\
                            0 7.3511422070048675e-016 3.3106601304214647\
                            0.095106928544030425 7.3226021492964845e-016 3.2978068310954041\
                            0.18377040106645362 7.2410535538628704e-016 3.2610806086946629\
                            0.26011201169235643 7.1119136941191965e-016 3.2029211862726341\
                            0.31827168875618217 6.9424007009931335e-016 3.1265793210049346\
                            0.35499740187332968 6.745528809136276e-016 3.0379161031243078\
                            0.36785401154274661 6.5343490053943517e-016 2.9428091745802774\
                            0.35499740187332968 6.3231692016524274e-016 2.8477022460362469\
                            0.31827168875618217 6.1262967443771998e-016 2.759038773513824\
                            0.26011201169235643 5.9567843166695079e-016 2.682697162887921\
                            0.18377040106645362 5.827643891507462e-016 2.6245374858240953\
                            0.095106928544030425 5.746096426910591e-016 2.5878117727069476\
                            0 5.7175490187633818e-016 2.5749551630375311\
                            0 0 0\
                            ;'%(self.sNames.controlNames['jaw'],self.sNames.controlNames['jaw'],self.sNames.controlNames['jaw'])) 
           
        setAttr('%s.scaleX'%self.sNames.controlNames['jaw'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['jaw'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['jaw'],self.scale)
           
        # Set it up
        self.processControl(self.sNames.controlNames['jaw'],self.sNames.controlNames['jaw'],pos)
        
    def createLeftClav(self,pos):
        mel.eval('createNode transform -n "%s";\
                        setAttr ".ove" yes;\
                        setAttr ".ovc" 13;\
                    createNode nurbsCurve -n "%sShape" -p "%s";\
                        setAttr -k off ".v";\
                        setAttr ".ove" yes;\
                        setAttr ".ovc" 13;\
                        setAttr ".cc" -type "nurbsCurve" \
                            1 55 0 no 3\
                            56 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27\
                             28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54\
                             55\
                            56\
                            0.32018766080030103 0.9030577041421507 1.5538934496433225e-008\
                            0.31957434471047597 0.88277099286287419 -0.27498161066742521\
                            0.31548157337362503 0.8301512516391667 -0.5286056432850017\
                            0.30545060027545506 0.75653415198066087 -0.75394169207359207\
                            0.28783917736091968 0.67007373296266137 -0.94927372260245024\
                            0.26163276332165425 0.57686358159899376 -1.1140477030998164\
                            0.22672651194342058 0.48210118998427248 -1.2494025194609064\
                            0.18404793532407168 0.39030879385218759 -1.3605533135929024\
                            0.13281102949150744 0.30657842072945202 -1.4488986497040692\
                            0.071811433520735893 0.23979386787597295 -1.5114826642666361\
                            0 0.21047825707893894 -1.5362992807357139\
                            -0.071811433520735893 0.23979386787597295 -1.5114826642666361\
                            -0.13281102949150744 0.30657842072945202 -1.4488986497040692\
                            -0.18404793532407168 0.39030879385218759 -1.3605533135929024\
                            -0.22672651194342058 0.48210118998427248 -1.2494025194609064\
                            -0.26163276332165425 0.57686358159899376 -1.1140477030998164\
                            -0.28783917736091968 0.67007373296266137 -0.94927372260245024\
                            -0.30545060027545506 0.75653415198066087 -0.75394169207359207\
                            -0.31548157337362503 0.8301512516391667 -0.5286056432850017\
                            -0.31957434471047597 0.88277099286287419 -0.27498161066742521\
                            -0.32018766080030103 0.9030577041421507 1.5538934496433225e-008\
                            -0.31439199506879595 1.0409260835768337 0\
                            -0.29362799039868398 1.1729422412168466 0\
                            -0.26003094615968053 1.293154861042644 0\
                            -0.21506905198580897 1.3963112413200407 0\
                            -0.16070800307669345 1.4779011791855095 0\
                            -0.0993229430829871 1.5343601138071725 0\
                            -0.033597078502472059 1.5632205989856809 0\
                            0.033597078502472059 1.5632205989856809 0\
                            0.0993229430829871 1.5343601138071725 0\
                            0.16070800307669345 1.4779011791855095 0\
                            0.21506905198580897 1.3963112413200407 0\
                            0.26003094615968053 1.293154861042644 0\
                            0.29362799039868398 1.1729422412168466 0\
                            0.31439199506879595 1.0409260835768337 0\
                            0.32018766080030103 0.9030577041421507 1.5538934496433225e-008\
                            0.31957434471047597 0.88277099286287419 0.27498161066742521\
                            0.31548157337362503 0.83015054382327447 0.5286056432850017\
                            0.30545060027545506 0.75653485979655299 0.75394169207359207\
                            0.28783917736091968 0.67007373296266137 0.94927449316124246\
                            0.26163276332165425 0.57686428941488532 1.1140469325410245\
                            0.22672651194342058 0.48210048216838058 1.2494040605784915\
                            0.18404793532407168 0.39031091729986361 1.360551772475318\
                            0.13281102949150744 0.30657417383410052 1.448901731939239\
                            0.071811433520735893 0.23979953040310864 1.511478811472674\
                            0 0.21044640536380113 1.5363208563819022\
                            -0.071811433520735893 0.23979953040310864 1.511478811472674\
                            -0.13281102949150744 0.30657417383410052 1.448901731939239\
                            -0.18404793532407168 0.39031091729986361 1.360551772475318\
                            -0.22672651194342058 0.48210048216838058 1.2494040605784915\
                            -0.26163276332165425 0.57686428941488532 1.1140469325410245\
                            -0.28783917736091968 0.67007373296266137 0.94927449316124246\
                            -0.30545060027545506 0.75653485979655299 0.75394169207359207\
                            -0.31548157337362503 0.83015054382327447 0.5286056432850017\
                            -0.31957434471047597 0.88277099286287419 0.27498161066742521\
                            -0.32018766080030103 0.9030577041421507 1.5538934496433225e-008\
                            ;'%(self.sNames.controlNames['left_clav'],
                                self.sNames.controlNames['left_clav'],
                                self.sNames.controlNames['left_clav']))
        
        setAttr('%s.scaleX'%self.sNames.controlNames['left_clav'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['left_clav'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['left_clav'],self.scale)
        
        # Set it up
        self.processControl(self.sNames.controlNames['left_clav'],self.sNames.controlNames['left_clav'],pos)
        
    def createRightClav(self,pos):
        mel.eval('createNode transform -n "%s";\
                        setAttr ".ove" yes;\
                        setAttr ".ovc" 6;\
                        setAttr ".r" -type "double3" -180 0 0 ;\
                        setAttr ".ra" -type "double3" 0 0 -179.99999999999997 ;\
                        createNode nurbsCurve -n "%sShape" -p "%s";\
                        setAttr -k off ".v";\
                        setAttr ".ove" yes;\
                        setAttr ".ovc" 6;\
                        setAttr ".cc" -type "nurbsCurve" \
                            1 55 0 no 3\
                            56 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27\
                             28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54\
                             55\
                            56\
                            0.32018766080030103 0.9030577041421507 1.5538934496433225e-008\
                            0.31957434471047597 0.88277099286287419 -0.27498161066742521\
                            0.31548157337362503 0.8301512516391667 -0.5286056432850017\
                            0.30545060027545506 0.75653415198066087 -0.75394169207359207\
                            0.28783917736091968 0.67007373296266137 -0.94927372260245024\
                            0.26163276332165425 0.57686358159899376 -1.1140477030998164\
                            0.22672651194342058 0.48210118998427248 -1.2494025194609064\
                            0.18404793532407168 0.39030879385218759 -1.3605533135929024\
                            0.13281102949150744 0.30657842072945202 -1.4488986497040692\
                            0.071811433520735893 0.23979386787597295 -1.5114826642666361\
                            0 0.21047825707893894 -1.5362992807357139\
                            -0.071811433520735893 0.23979386787597295 -1.5114826642666361\
                            -0.13281102949150744 0.30657842072945202 -1.4488986497040692\
                            -0.18404793532407168 0.39030879385218759 -1.3605533135929024\
                            -0.22672651194342058 0.48210118998427248 -1.2494025194609064\
                            -0.26163276332165425 0.57686358159899376 -1.1140477030998164\
                            -0.28783917736091968 0.67007373296266137 -0.94927372260245024\
                            -0.30545060027545506 0.75653415198066087 -0.75394169207359207\
                            -0.31548157337362503 0.8301512516391667 -0.5286056432850017\
                            -0.31957434471047597 0.88277099286287419 -0.27498161066742521\
                            -0.32018766080030103 0.9030577041421507 1.5538934496433225e-008\
                            -0.31439199506879595 1.0409260835768337 0\
                            -0.29362799039868398 1.1729422412168466 0\
                            -0.26003094615968053 1.293154861042644 0\
                            -0.21506905198580897 1.3963112413200407 0\
                            -0.16070800307669345 1.4779011791855095 0\
                            -0.0993229430829871 1.5343601138071725 0\
                            -0.033597078502472059 1.5632205989856809 0\
                            0.033597078502472059 1.5632205989856809 0\
                            0.0993229430829871 1.5343601138071725 0\
                            0.16070800307669345 1.4779011791855095 0\
                            0.21506905198580897 1.3963112413200407 0\
                            0.26003094615968053 1.293154861042644 0\
                            0.29362799039868398 1.1729422412168466 0\
                            0.31439199506879595 1.0409260835768337 0\
                            0.32018766080030103 0.9030577041421507 1.5538934496433225e-008\
                            0.31957434471047597 0.88277099286287419 0.27498161066742521\
                            0.31548157337362503 0.83015054382327447 0.5286056432850017\
                            0.30545060027545506 0.75653485979655299 0.75394169207359207\
                            0.28783917736091968 0.67007373296266137 0.94927449316124246\
                            0.26163276332165425 0.57686428941488532 1.1140469325410245\
                            0.22672651194342058 0.48210048216838058 1.2494040605784915\
                            0.18404793532407168 0.39031091729986361 1.360551772475318\
                            0.13281102949150744 0.30657417383410052 1.448901731939239\
                            0.071811433520735893 0.23979953040310864 1.511478811472674\
                            0 0.21044640536380113 1.5363208563819022\
                            -0.071811433520735893 0.23979953040310864 1.511478811472674\
                            -0.13281102949150744 0.30657417383410052 1.448901731939239\
                            -0.18404793532407168 0.39031091729986361 1.360551772475318\
                            -0.22672651194342058 0.48210048216838058 1.2494040605784915\
                            -0.26163276332165425 0.57686428941488532 1.1140469325410245\
                            -0.28783917736091968 0.67007373296266137 0.94927449316124246\
                            -0.30545060027545506 0.75653485979655299 0.75394169207359207\
                            -0.31548157337362503 0.83015054382327447 0.5286056432850017\
                            -0.31957434471047597 0.88277099286287419 0.27498161066742521\
                            -0.32018766080030103 0.9030577041421507 1.5538934496433225e-008\
                            ;'%(self.sNames.controlNames['right_clav'],
                                self.sNames.controlNames['right_clav'],
                                self.sNames.controlNames['right_clav']))
        
        setAttr('%s.scaleX'%self.sNames.controlNames['right_clav'],self.scale)
        setAttr('%s.scaleY'%self.sNames.controlNames['right_clav'],self.scale)
        setAttr('%s.scaleZ'%self.sNames.controlNames['right_clav'],self.scale)
        
        # Set it up
        self.processControl(self.sNames.controlNames['right_clav'],self.sNames.controlNames['right_clav'],pos)        
        
    def processControl(self,cnt,key,pos=0):
        """
        Place control, zero it and add it to the return dictionary.
        """        
        # Place it
        if pos != 0:
            move(cnt, pos[0],pos[1],pos[2],ws=True)
        
        # Zero it
        self.lib.zero(cnt)      
        
        # Store the buffer node
        bufferNode = listRelatives(cnt,parent=True)  
        
        # Dictionary key is cnt
        self.createdNodes[cnt] = bufferNode
        
    def processHandControl(self,cnt,wrist,pos):
        """
        Zero control and add it to the return dictionary.
        """      
        #@todo - Figure this out so twist can work based on hand control
#        # Snap/Parent to wrist and freeze it's transformations to match orientations
#        temp = pointConstraint(cnt,wrist,mo=False)
#        delete(temp)
#        parent(cnt,wrist)
#        makeIdentity(cnt,apply=False,t=1,r=1,s=1)
#        
#        # Unparent
#        parent(cnt,w=True)
             
        # Place it
        move(cnt, pos[0],pos[1],pos[2],ws=True)
             
        # Zero it
        self.lib.zero(cnt)      
        
        # Store the buffer node
        bufferNode = listRelatives(cnt,parent=True)  
        
        # Dictionary key is cnt
        self.createdNodes[cnt] = bufferNode          