"""
Copyright (c) 2011 Mauricio Santos
Name: createFaceRig.py
Version: 1.0
Author: Mauricio Santos
Contact: mauricioptkvp@hotmail.com
Date Created:   17 August 2011


$HeadURL: file:///C:/SVN_Repos/Tools/Maya/RigBuilder/createFaceRig.py $
$Id: createFaceRig.py 17 2011-08-29 22:48:09Z msantos $

Description: 
 Creates a joint based face rig. Parent or constrain the top node of the face rig to the head controller

Process:
    - Draw joints:
        - Eyes: 6
        - Brows: 3
        - Mouth: 8
        - Cheeks: 2
        - Nose: 1
        - Chin: 1
    - Prompt user to place the joints (v2: and select the template geometry)
    - v2 Constrain the joints to the template geometry
    - Draw control curves
    - Organize hierarchy
    - Create SDKs
    
Example call:

        temp = createFaceRig.createFaceRig()
    
      
Attributes:

Keywords:

             
Requires:


Development notes:


"""

import maya.cmds as cmds
import maya.mel as mel
class createFaceRig():
    """
    Description: 
     Creates a joint based face rig. Parent or constrain the top node of the face rig to the head controller
    
    Process:
        - Draw joints:
            - Eyes: 2
            _ Eye Lids: 4
            - Brows: 7
            - Mouth: 8
            - Cheeks: 2
            - Nose: 1
            - Chin: 1
        - Prompt user to place the joints
        - Draw control curves
        - Organize hierarchy
        - Create SDKs
    """
    def __init__(self):
        #--- Position of the controller curves
        self.control_height = 7.1
        self.control_x_pos = .8
        
        #--- Joint Names
        # Eyes
        self.l_eye = 'fr_l_eye_bind_jnt'
        self.r_eye = 'fr_r_eye_bind_jnt'
        
        # Eyelids
        self.l_top_eyeLid = 'fr_l_top_eyeLid_bind_jnt'
        self.l_btm_eyeLid = 'fr_l_btm_eyeLid_bind_jnt'
        
        self.r_top_eyeLid = 'fr_r_top_eyeLid_bind_jnt'
        self.r_btm_eyeLid = 'fr_r_btm_eyeLid_bind_jnt'
        
        # Brows
        self.l_brow_01 = 'fr_l_brow_bind_jnt_01'
        self.l_brow_02 = 'fr_l_brow_bind_jnt_02'
        self.l_brow_03 = 'fr_l_brow_bind_jnt_03'
        
        self.mid_brow = 'fr_mid_bow_bind_jnt'
        
        self.r_brow_01 = 'fr_r_brow_bind_jnt_01'
        self.r_brow_02 = 'fr_r_brow_bind_jnt_02'
        self.r_brow_03 = 'fr_r_brow_bind_jnt_03'
        
        # Cheek
        self.l_cheek = 'fr_l_cheek_bind_jnt'
        self.r_cheek = 'fr_r_cheek_bind_jnt'
        
        # Mouth
        self.l_top_lip = 'fr_l_top_lip_bind_jnt'
        self.mid_top_lip = 'fr_mid_top_lip_bind_jnt'
        self.r_top_lip = 'fr_r_top_lip_bind_jnt'
        
        self.l_mouth_crnr = 'fr_l_mouth_crnr_bind_jnt'
        self.r_mouth_crnr = 'fr_r_mouth_crnr_bind_jnt'
        
        self.l_btm_lip = 'fr_l_btm_lip_bind_jnt'
        self.mid_btm_lip = 'fr_mid_btm_lip_bind_jnt'
        self.r_btm_lip = 'fr_r_btm_lip_bind_jnt'
        
        # Nose
        self.nose = 'fr_nose_bind_jnt'
        
        # Chin
        self.jaw = 'fr_jaw_bind_jnt'
        
        # Ears
        self.l_ear = 'fr_l_ear_bind_jnt'
        self.r_ear = 'fr_r_ear_bind_jnt'
        
        #--- Control Names
        # Boundry controls
        self.boundry_cnts = ['fr_r_eye_cnt_boundry',
                         'fr_r_cheek_cnt_boundry',
                         'fr_r_brow_boundry',
                         'fr_mouth_cnt_boundry',
                         'fr_jaw_cnt_boundry',
                         'fr_l_eye_cnt_boundry',
                         'fr_l_cheek_cnt_boundry',
                         'fr_l_brow_boundry']
        
        # Eyes
        self.l_eye_cnt = 'fr_l_eye_cnt'
        self.r_eye_cnt = 'fr_r_eye_cnt'
        
        # Eyelids
        self.l_top_eyeLid_cnt = 'fr_l_eye_top_lid_cnt'
        self.l_btm_eyeLid_cnt = 'fr_l_eye_btm_lid_cnt'
        
        self.r_top_eyeLid_cnt = 'fr_r_eye_top_lid_cnt'
        self.r_btm_eyeLid_cnt = 'fr_r_eye_btm_lid_cnt'
        
        # Brows
        self.l_brow_01_cnt = 'fr_l_brow_01_cnt'
        self.l_brow_02_cnt = 'fr_l_brow_02_cnt'
        self.l_brow_03_cnt = 'fr_l_brow_03_cnt'
        
        self.mid_brow_cnt = 'fr_mid_brow_cnt'
        
        self.r_brow_01_cnt = 'fr_r_brow_01_cnt'
        self.r_brow_02_cnt = 'fr_r_brow_02_cnt'
        self.r_brow_03_cnt = 'fr_r_brow_03_cnt'
        
        # Cheek
        self.l_cheek_cnt = 'fr_l_cheek_cnt'
        self.r_cheek_cnt = 'fr_r_cheek_cnt'
        
        # Mouth
        self.l_top_lip_cnt = 'fr_l_top_lip_cnt'
        self.mid_top_lip_cnt = 'fr_mid_top_lip_cnt'
        self.r_top_lip_cnt = 'fr_r_top_lip_cnt'
        
        self.l_mouth_crnr_cnt = 'fr_l_corner_lip_cnt'
        self.r_mouth_crnr_cnt = 'fr_r_corner_lip_cnt'
        
        self.l_btm_lip_cnt = 'fr_l_btm_lip_cnt'
        self.mid_btm_lip_cnt = 'fr_mid_btm_lip_cnt'
        self.r_btm_lip_cnt = 'fr_r_btm_lip_cnt'
        
        # Nose
        self.nose_cnt = 'fr_nose_cnt'
        
        # Chin
        self.jaw_cnt = 'fr_jaw_cnt'
        
        # Ears
        self.l_ear_cnt = 'fr_l_ear_cnt'
        self.r_ear_cnt = 'fr_r_ear_cnt'
        
        # Call methods
        self.createJoints()
        
    def createJoints(self):
        """
        Create joints:
            - Eyes: 2
            _ Eye Lids: 4
            - Brows: 7
            - Mouth: 8
            - Cheeks: 2
            - Nose: 1
            - Chin: 1
        """
        # Eyes
        cmds.select(clear=True)
        cmds.joint( p = (.2,.2,0), n = self.l_eye, radius = 0.5 )
        cmds.select(clear=True)
        cmds.joint( p = (-0.2,.2,0), n = self.r_eye, radius = 0.5 )
        
        # Eyelids
        cmds.select(clear=True)
        cmds.joint( p = (.2,.2,0), n = self.l_top_eyeLid, radius = 0.5 )
        cmds.select(clear=True)
        cmds.joint( p = (.2,.2,0), n = self.l_btm_eyeLid, radius = 0.5 )
        
        cmds.select(clear=True)
        cmds.joint( p = (-0.2,.2,0), n = self.r_top_eyeLid, radius = 0.5 )
        cmds.select(clear=True)
        cmds.joint( p = (-0.2,.2,0), n = self.r_btm_eyeLid, radius = 0.5 )
        
        # Brows
        cmds.select(clear=True)
        cmds.joint( p = (.3,.3,0), n = self.l_brow_01, radius = 0.5 )
        cmds.select(clear=True)
        cmds.joint( p = (.2,.3,0), n = self.l_brow_02, radius = 0.5 )
        cmds.select(clear=True)
        cmds.joint( p = (.1,.3,0), n = self.l_brow_03, radius = 0.5 )
        
        cmds.select(clear=True)
        cmds.joint( p = (0,.3,0), n = self.mid_brow, radius = 0.5 )
        
        cmds.select(clear=True)
        cmds.joint( p = (-0.1,.3,0), n = self.r_brow_03, radius = 0.5 )
        cmds.select(clear=True)
        cmds.joint( p = (-0.2,.3,0), n = self.r_brow_02, radius = 0.5 )
        cmds.select(clear=True)
        cmds.joint( p = (-0.3,.3,0), n = self.r_brow_01, radius = 0.5 )
        
        # Cheek
        cmds.select(clear=True)
        cmds.joint( p = (.2,.1,0), n = self.l_cheek, radius = 0.5 )
        cmds.select(clear=True)
        cmds.joint( p = (-0.2,.1,0), n = self.r_cheek, radius = 0.5 )
        
        # Mouth
        cmds.select(clear=True)
        cmds.joint( p = (.1,-0.1,0), n = self.l_top_lip, radius = 0.5 )
        cmds.select(clear=True)
        cmds.joint( p = (0,-0.1,0), n = self.mid_top_lip, radius = 0.5 )
        cmds.select(clear=True)
        cmds.joint( p = (-0.1,-0.1,0), n = self.r_top_lip, radius = 0.5 )
        
        cmds.select(clear=True)
        cmds.joint( p = (.2,-0.2,0), n = self.l_mouth_crnr, radius = 0.5 )
        cmds.select(clear=True)
        cmds.joint( p = (-0.2,-0.2,0), n = self.r_mouth_crnr, radius = 0.5 )
        
        cmds.select(clear=True)
        cmds.joint( p = (.1,-0.3,0), n = self.l_btm_lip, radius = 0.5 )
        cmds.select(clear=True)
        cmds.joint( p = (0,-0.3,0), n = self.mid_btm_lip, radius = 0.5 )
        cmds.select(clear=True)
        cmds.joint( p = (-0.1,-0.3,0), n = self.r_btm_lip, radius = 0.5 )
        
        # Nose
        cmds.select(clear=True)
        cmds.joint( p = (0,0,0), n = self.nose, radius = 0.5 )
        
        # Jaw
        cmds.select(clear=True)
        cmds.joint( p = (0,-0.4,0), n = self.jaw, radius = 0.5 )
        
        # Ears
        cmds.select(clear=True)
        cmds.joint( p = (.4,.2,0), n = self.l_ear, radius = 0.5 )
        cmds.select(clear=True)
        cmds.joint( p = (-0.4,.2,0), n = self.r_ear, radius = 0.5 )
        
        #--- Group the joints
        cmds.group( self.l_eye,
            self.r_eye,
            self.l_top_eyeLid,
            self.l_btm_eyeLid,
            self.r_top_eyeLid,
            self.r_btm_eyeLid,
            self.l_brow_01,
            self.l_brow_02,
            self.l_brow_03,
            self.mid_brow,
            self.r_brow_01,
            self.r_brow_02,
            self.r_brow_03,
            self.l_cheek,
            self.r_cheek,
            self.l_top_lip,
            self.mid_top_lip,
            self.r_top_lip,
            self.l_mouth_crnr,
            self.r_mouth_crnr,
            self.l_btm_lip,
            self.mid_btm_lip,
            self.r_btm_lip,
            self.nose,
            self.jaw,
            self.r_ear,
            self.l_ear,
            n='faceRig_joints_grp' )
            
        # Translate the group up 
        cmds.setAttr('faceRig_joints_grp.translateY',7)
        cmds.setAttr('faceRig_joints_grp.translateZ',0.5)
        
        
        
        # Call the next method
        self.promptUser()
    
    def promptUser(self):
        """ 
            Prompt user to place joints. 
            Calls: finishRig()
        """
        if cmds.window('promptWin',exists=True):
            cmds.deleteUI('promptWin',window=True)
        win = cmds.window('promptWin', title = 'Create Face Rig: Place Joints')
        
        cmds.columnLayout()
        cmds.rowLayout(nc=2,cw2=(50,50))
        cmds.text(' ')
        cmds.text('Place the joints, then press the button to continue.')
        cmds.setParent('..')
        
        cmds.rowLayout(nc=2,cw2=(100,100))
        cmds.text(' ')
        cmds.button(label='     Joints placed! ',c=self.finishRig)
        
        cmds.showWindow(win)
        
    def finishRig(self,*args):
        """
        Calls remaining methods that need to run to build the rig.
        """
        
        cmds.deleteUI('promptWin',window=True)
        
        self.drawCurveInterface()
        self.organizeHeirarchy()
        self.createConnections()
    
    def drawCurveInterface(self):
        """ Draw control curve interface. """
        
        mel_cmd = 'createNode transform -n "fr_nose_cnt";\
                setAttr ".rp" -type "double3" 0.00099955541628593547 -0.00017976362420402126 -9.7013598017661314e-17 ;\
                setAttr ".sp" -type "double3" 0.00099955541628593547 -0.00017976362420402126 -9.7013598017661314e-17 ;\
            createNode nurbsCurve -n "fr_nose_cntShape" -p "fr_nose_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    0.035634028302787162 0.10141142841057997 -4.9777296000996873e-17\
                    0.00099955541628592983 0.10814568060224902 -4.5908243929242841e-17\
                    -0.033634917470215256 0.10141142841057998 -4.9777296000996861e-17\
                    -0.049798446278202874 0.017042483789210711 -4.0717186323392698e-17\
                    -0.040373731959867466 -0.012020967442964978 -5.5744701234654177e-17\
                    0.00099955541628592246 -0.0052425313397169646 -1.0226111168713293e-16\
                    0.042372853689769729 -0.012020951303630388 -5.5744694067349831e-17\
                    0.051797557110774897 0.017042483789210694 -4.0717186323392698e-17\
                    0.035634028302787162 0.10141142841057997 -4.9777296000996873e-17\
                    0.00099955541628592983 0.10814568060224902 -4.5908243929242841e-17\
                    -0.033634917470215256 0.10141142841057998 -4.9777296000996861e-17\
                    ;\
            createNode transform -n "fr_mid_top_lip_cnt";\
                setAttr ".rp" -type "double3" 1.1102230246251565e-16 -0.26976258829785849 -1.3972519744220539e-16 ;\
                setAttr ".sp" -type "double3" 1.1102230246251565e-16 -0.26976258829785849 -1.3972519744220539e-16 ;\
            createNode nurbsCurve -n "fr_mid_top_lip_cntShape" -p "fr_mid_top_lip_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    0.016082361226137459 -0.25368022707172116 -1.3159843374285075e-16\
                    1.0842749617965814e-16 -0.24701869493687184 -1.282322180003767e-16\
                    -0.016082361226137223 -0.25368022707172111 -1.3159843374285075e-16\
                    -0.022743893360986506 -0.26976258829785849 -1.3972519744220539e-16\
                    -0.016082361226137227 -0.28584494952399581 -1.4785196114156004e-16\
                    1.041691235203359e-16 -0.29250648165884513 -1.5121817688403409e-16\
                    0.016082361226137435 -0.28584494952399586 -1.4785196114156004e-16\
                    0.022743893360986728 -0.26976258829785849 -1.3972519744220539e-16\
                    0.016082361226137459 -0.25368022707172116 -1.3159843374285075e-16\
                    1.0842749617965814e-16 -0.24701869493687184 -1.282322180003767e-16\
                    -0.016082361226137223 -0.25368022707172111 -1.3159843374285075e-16\
                    ;\
            createNode transform -n "fr_mid_btm_lip_cnt";\
                setAttr ".rp" -type "double3" 1.1102230246251565e-16 -0.3283453089219357 -1.6574115155501617e-16 ;\
                setAttr ".sp" -type "double3" 1.1102230246251565e-16 -0.3283453089219357 -1.6574115155501617e-16 ;\
            createNode nurbsCurve -n "fr_mid_btm_lip_cntShape14" -p "fr_mid_btm_lip_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    0.016082361226137459 -0.31226294769579838 -1.5761438785566152e-16\
                    1.0842749617965814e-16 -0.30560141556094905 -1.5424817211318748e-16\
                    -0.016082361226137223 -0.31226294769579832 -1.5761438785566152e-16\
                    -0.022743893360986506 -0.3283453089219357 -1.6574115155501617e-16\
                    -0.016082361226137227 -0.34442767014807302 -1.7386791525437082e-16\
                    1.041691235203359e-16 -0.35108920228292234 -1.7723413099684487e-16\
                    0.016082361226137435 -0.34442767014807307 -1.7386791525437082e-16\
                    0.022743893360986728 -0.3283453089219357 -1.6574115155501617e-16\
                    0.016082361226137459 -0.31226294769579838 -1.5761438785566152e-16\
                    1.0842749617965814e-16 -0.30560141556094905 -1.5424817211318748e-16\
                    -0.016082361226137223 -0.31226294769579832 -1.5761438785566152e-16\
                    ;\
            createNode transform -n "fr_jaw_cnt";\
                setAttr ".rp" -type "double3" -1.1102230246251181e-16 -0.52237823026947794 -1.5200781448793429e-16 ;\
                setAttr ".sp" -type "double3" -1.1102230246251181e-16 -0.52237823026947794 -1.5200781448793429e-16 ;\
            createNode nurbsCurve -n "fr_jaw_cntShape" -p "fr_jaw_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    0.021940633288545206 -0.5004375969809326 -1.4092073967081009e-16\
                    -1.1456231081740834e-16 -0.49134948910576254 -1.3632832291451201e-16\
                    -0.021940633288545407 -0.5004375969809326 -1.4092073967081007e-16\
                    -0.031028741163715474 -0.52237823026947794 -1.5200781448793429e-16\
                    -0.021940633288545414 -0.54431886355802328 -1.6309488930505849e-16\
                    -1.2037186773572392e-16 -0.5534069714331934 -1.6768730606135657e-16\
                    0.021940633288545175 -0.54431886355802328 -1.6309488930505852e-16\
                    0.031028741163715252 -0.52237823026947794 -1.5200781448793429e-16\
                    0.021940633288545206 -0.5004375969809326 -1.4092073967081009e-16\
                    -1.1456231081740834e-16 -0.49134948910576254 -1.3632832291451201e-16\
                    -0.021940633288545407 -0.5004375969809326 -1.4092073967081007e-16\
                    ;\
            createNode transform -n "fr_mid_brow_cnt";\
                setAttr ".rp" -type "double3" -0.00098449336872119542 0.5763185837432685 1.5395030841888058e-17 ;\
                setAttr ".sp" -type "double3" -0.00098449336872119542 0.5763185837432685 1.5395030841888058e-17 ;\
            createNode nurbsCurve -n "fr_mid_brow_cntShape" -p "fr_mid_brow_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    0.010411250207489725 0.58771432731947937 2.1153545647027023e-17\
                    -0.00098449336872119715 0.59243459886207206 2.3538800578441851e-17\
                    -0.012380236944932104 0.58771432731947937 2.1153545647027026e-17\
                    -0.01710050848752474 0.5763185837432685 1.5395030841888061e-17\
                    -0.012380236944932108 0.56492284016705763 9.6365160367490909e-18\
                    -0.00098449336872120019 0.56020256862446494 7.2512611053342638e-18\
                    0.010411250207489706 0.56492284016705763 9.6365160367490878e-18\
                    0.015131521750082349 0.5763185837432685 1.5395030841888054e-17\
                    0.010411250207489725 0.58771432731947937 2.1153545647027023e-17\
                    -0.00098449336872119715 0.59243459886207206 2.3538800578441851e-17\
                    -0.012380236944932104 0.58771432731947937 2.1153545647027026e-17\
                    ;\
            createNode transform -n "fr_r_top_lip_cnt";\
                setAttr ".rp" -type "double3" -0.053252140857643071 -0.26976258829785849 -1.3972519744220542e-16 ;\
                setAttr ".sp" -type "double3" -0.053252140857643071 -0.26976258829785849 -1.3972519744220542e-16 ;\
            createNode nurbsCurve -n "fr_r_top_lip_cntShape" -p "fr_r_top_lip_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    -0.037169779631505723 -0.25368022707172116 -1.3159843374285077e-16\
                    -0.053252140857643071 -0.24701869493687184 -1.2823221800037673e-16\
                    -0.069334502083780405 -0.25368022707172111 -1.3159843374285077e-16\
                    -0.075996034218629688 -0.26976258829785849 -1.3972519744220542e-16\
                    -0.069334502083780405 -0.28584494952399581 -1.4785196114156007e-16\
                    -0.053252140857643078 -0.29250648165884513 -1.5121817688403411e-16\
                    -0.03716977963150575 -0.28584494952399586 -1.4785196114156007e-16\
                    -0.030508247496656454 -0.26976258829785849 -1.3972519744220542e-16\
                    -0.037169779631505723 -0.25368022707172116 -1.3159843374285077e-16\
                    -0.053252140857643071 -0.24701869493687184 -1.2823221800037673e-16\
                    -0.069334502083780405 -0.25368022707172111 -1.3159843374285077e-16\
                    ;\
            createNode transform -n "fr_r_corner_lip_cnt";\
                setAttr ".rp" -type "double3" -0.10643339049206502 -0.30491222067230694 -1.5533476990989133e-16 ;\
                setAttr ".sp" -type "double3" -0.10643339049206502 -0.30491222067230694 -1.5533476990989133e-16 ;\
            createNode nurbsCurve -n "fr_r_corner_lip_cntShape" -p "fr_r_corner_lip_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    -0.090351029265927668 -0.28882985944616962 -1.4720800621053668e-16\
                    -0.10643339049206502 -0.2821683273113203 -1.4384179046806264e-16\
                    -0.12251575171820235 -0.28882985944616957 -1.4720800621053668e-16\
                    -0.12917728385305163 -0.30491222067230694 -1.5533476990989133e-16\
                    -0.12251575171820235 -0.32099458189844426 -1.6346153360924598e-16\
                    -0.10643339049206502 -0.32765611403329359 -1.6682774935172003e-16\
                    -0.090351029265927696 -0.32099458189844432 -1.6346153360924598e-16\
                    -0.0836894971310784 -0.30491222067230694 -1.5533476990989133e-16\
                    -0.090351029265927668 -0.28882985944616962 -1.4720800621053668e-16\
                    -0.10643339049206502 -0.2821683273113203 -1.4384179046806264e-16\
                    -0.12251575171820235 -0.28882985944616957 -1.4720800621053668e-16\
                    ;\
            createNode transform -n "fr_r_btm_lip_cnt";\
                setAttr ".rp" -type "double3" -0.053252140857643071 -0.3283453089219357 -1.6574115155501622e-16 ;\
                setAttr ".sp" -type "double3" -0.053252140857643071 -0.3283453089219357 -1.6574115155501622e-16 ;\
            createNode nurbsCurve -n "fr_r_btm_lip_cntShape" -p "fr_r_btm_lip_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    -0.037169779631505723 -0.31226294769579838 -1.5761438785566157e-16\
                    -0.053252140857643071 -0.30560141556094905 -1.5424817211318753e-16\
                    -0.069334502083780405 -0.31226294769579832 -1.5761438785566157e-16\
                    -0.075996034218629688 -0.3283453089219357 -1.6574115155501622e-16\
                    -0.069334502083780405 -0.34442767014807302 -1.7386791525437087e-16\
                    -0.053252140857643078 -0.35108920228292234 -1.7723413099684491e-16\
                    -0.03716977963150575 -0.34442767014807307 -1.7386791525437087e-16\
                    -0.030508247496656454 -0.3283453089219357 -1.6574115155501622e-16\
                    -0.037169779631505723 -0.31226294769579838 -1.5761438785566157e-16\
                    -0.053252140857643071 -0.30560141556094905 -1.5424817211318753e-16\
                    -0.069334502083780405 -0.31226294769579832 -1.5761438785566157e-16\
                    ;\
            createNode transform -n "fr_r_eye_top_lid_cnt";\
                setAttr ".rp" -type "double3" -0.16825030145385911 0.45620678651420388 1.0566274441949991e-16 ;\
                setAttr ".sp" -type "double3" -0.16825030145385911 0.45620678651420388 1.0566274441949991e-16 ;\
            createNode nurbsCurve -n "fr_r_eye_top_lid_cntShape" -p "fr_r_eye_top_lid_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    -0.11730165640220319 0.48003545542895371 1.1574035943782108e-16\
                    -0.16825030145385911 0.4892031987468301 1.0578804489078197e-16\
                    -0.21919894650551497 0.48003541861211657 1.1574028552217453e-16\
                    -0.24030256627044372 0.44154122571965443 1.0537810561117146e-16\
                    -0.219198946505515 0.42215499508817955 9.5585208985211184e-17\
                    -0.16825030145385914 0.44531413308814871 1.0506434297447407e-16\
                    -0.11730165640220327 0.42215482998534037 9.5585129401178392e-17\
                    -0.096198036637274484 0.44154119343641968 1.0537810289034605e-16\
                    -0.11730165640220319 0.48003545542895371 1.1574035943782108e-16\
                    -0.16825030145385911 0.4892031987468301 1.0578804489078197e-16\
                    -0.21919894650551497 0.48003541861211657 1.1574028552217453e-16\
                    ;\
            createNode transform -n "fr_r_eye_btm_lid_cnt";\
                setAttr ".rp" -type "double3" -0.16825030145385911 0.18275559786750772 -1.5773977879177464e-17 ;\
                setAttr ".sp" -type "double3" -0.16825030145385911 0.18275559786750772 -1.5773977879177464e-17 ;\
            createNode nurbsCurve -n "fr_r_eye_btm_lid_cntShape" -p "fr_r_eye_btm_lid_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    -0.11730165640220319 0.1904440131082685 -9.2399308757357721e-18\
                    -0.16825030145385911 0.16371371514616762 -1.9818343756995024e-17\
                    -0.21919894650551497 0.19044380301814404 -9.240024174493141e-18\
                    -0.24030256627044372 0.18275559786750775 -1.5773977879177455e-17\
                    -0.219198946505515 0.13957187285611306 -3.807110895203633e-17\
                    -0.16825030145385914 0.12909176149566434 -4.4017437345010308e-17\
                    -0.11730165640220327 0.13957183449486199 -3.8071125987854017e-17\
                    -0.096198036637274484 0.1827555978675077 -1.5773977879177482e-17\
                    -0.11730165640220319 0.1904440131082685 -9.2399308757357721e-18\
                    -0.16825030145385911 0.16371371514616762 -1.9818343756995024e-17\
                    -0.21919894650551497 0.19044380301814404 -9.240024174493141e-18\
                    ;\
            createNode transform -n "fr_r_eye_cnt_boundry";\
                setAttr ".rp" -type "double3" -0.16825030145385889 0.31398845330661285 4.250511719914372e-17 ;\
                setAttr ".sp" -type "double3" -0.16825030145385889 0.31398845330661285 4.250511719914372e-17 ;\
            createNode nurbsCurve -n "fr_r_eye_cnt_boundryShape" -p "fr_r_eye_cnt_boundry";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    -0.097727574361055503 0.38451118039941617 7.8141770950325547e-17\
                    -0.16825030145385889 0.4137226504167919 9.2902956251659136e-17\
                    -0.23877302854666221 0.38451118039941623 7.8141770950325572e-17\
                    -0.26798449856403783 0.3139884533066129 4.2505117199143732e-17\
                    -0.23877302854666221 0.24346572621380949 6.8684634479618738e-18\
                    -0.16825030145385891 0.21425425619643376 -7.8927218533717022e-18\
                    -0.097727574361055614 0.24346572621380946 6.8684634479618615e-18\
                    -0.068516104343679912 0.31398845330661279 4.2505117199143695e-17\
                    -0.097727574361055503 0.38451118039941617 7.8141770950325547e-17\
                    -0.16825030145385889 0.4137226504167919 9.2902956251659136e-17\
                    -0.23877302854666221 0.38451118039941623 7.8141770950325572e-17\
                    ;\
            createNode transform -n "fr_r_eye_cnt";\
                setAttr ".rp" -type "double3" -0.16825030145385889 0.31398845330661285 4.250511719914372e-17 ;\
                setAttr ".sp" -type "double3" -0.16825030145385889 0.31398845330661285 4.250511719914372e-17 ;\
            createNode nurbsCurve -n "fr_r_eye_cntShape" -p "fr_r_eye_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    -0.14279470492786867 0.33944404983260307 5.5368378686929729e-17\
                    -0.16825030145385889 0.34998810315196571 6.069651605152223e-17\
                    -0.19370589797984911 0.33944404983260307 5.5368378686929741e-17\
                    -0.2042499512992117 0.31398845330661285 4.2505117199143726e-17\
                    -0.19370589797984911 0.28853285678062263 2.9641855711357705e-17\
                    -0.16825030145385889 0.27798880346125998 2.4313718346765209e-17\
                    -0.14279470492786869 0.28853285678062263 2.9641855711357698e-17\
                    -0.13225065160850608 0.31398845330661285 4.2505117199143708e-17\
                    -0.14279470492786867 0.33944404983260307 5.5368378686929729e-17\
                    -0.16825030145385889 0.34998810315196571 6.069651605152223e-17\
                    -0.19370589797984911 0.33944404983260307 5.5368378686929741e-17\
                    ;\
            createNode transform -n "fr_r_cheek_cnt";\
                setAttr ".rp" -type "double3" -0.24524278723186471 -0.078368051996255517 -2.8412377133224908e-17 ;\
                setAttr ".sp" -type "double3" -0.24524278723186471 -0.078368051996255517 -2.8412377133224908e-17 ;\
            createNode nurbsCurve -n "fr_r_cheek_cntShape" -p "fr_r_cheek_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    -0.2233021539433194 -0.056427418707710203 -1.73253023161007e-17\
                    -0.24524278723186471 -0.047339310832540116 -1.2732885559802637e-17\
                    -0.26718342052041 -0.056427418707710196 -1.7325302316100694e-17\
                    -0.27627152839558006 -0.078368051996255503 -2.8412377133224902e-17\
                    -0.26718342052041 -0.10030868528480083 -3.9499451950349123e-17\
                    -0.24524278723186471 -0.10939679315997092 -4.4091868706647183e-17\
                    -0.22330215394331943 -0.10030868528480084 -3.9499451950349123e-17\
                    -0.21421404606814934 -0.078368051996255531 -2.8412377133224915e-17\
                    -0.2233021539433194 -0.056427418707710203 -1.73253023161007e-17\
                    -0.24524278723186471 -0.047339310832540116 -1.2732885559802637e-17\
                    -0.26718342052041 -0.056427418707710196 -1.7325302316100694e-17\
                    ;\
            createNode transform -n "fr_r_cheek_cnt_boundry";\
                setAttr ".rp" -type "double3" -0.23274487760658441 -0.094131183060117252 -1.3873640963925353e-16 ;\
                setAttr ".sp" -type "double3" -0.23274487760658441 -0.094131183060117252 -1.3873640963925353e-16 ;\
            createNode nurbsCurve -n "fr_r_cheek_cnt_boundryShape" -p "fr_r_cheek_cnt_boundry";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    -0.14673382229970164 0.0028526665634009685 -1.0636274873060902e-16\
                    -0.23493943646991178 0.011832980832754914 -9.2953139318580755e-17\
                    -0.33192328609343102 -0.0037310100265792734 -1.06362748730609e-16\
                    -0.34309815922611014 -0.11168765396673633 -1.3873640963925351e-16\
                    -0.31217225632348511 -0.17355856177701889 -1.7111007054789804e-16\
                    -0.2305503187432571 -0.18253887604637031 -1.8451967995992631e-16\
                    -0.1796522052496119 -0.13186194337379786 -1.7111007054789804e-16\
                    -0.1421426257570047 -0.094131183060117307 -1.3873640963925356e-16\
                    -0.14673382229970164 0.0028526665634009685 -1.0636274873060902e-16\
                    -0.23493943646991178 0.011832980832754914 -9.2953139318580755e-17\
                    -0.33192328609343102 -0.0037310100265792734 -1.06362748730609e-16\
                    ;\
            createNode transform -n "fr_r_brow_boundry";\
                setAttr ".rp" -type "double3" -0.17852610292294099 0.5778081672334654 -6.0728724883994361e-16 ;\
                setAttr ".sp" -type "double3" -0.17852610292294099 0.5778081672334654 -6.0728724883994361e-16 ;\
            createNode nurbsCurve -n "fr_r_brow_boundryShape" -p "fr_r_brow_boundry";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 12 1 no 3\
                    17 0 0 0 0.53333333333333333 2.1333333333333333 2.6666666666666665 3.2000000000000002\
                     3.7333333333333329 4.2666666666666666 4.7999999999999998 5.8666666666666663 6.4000000000000004\
                     6.9333333333333336 7.4666666666666659 8 8 8\
                    15\
                    -0.28054452923155032 0.61768697576527321 -6.4465676032777249e-16\
                    -0.26449156340499491 0.61768535697734639 -6.4717873691691467e-16\
                    -0.045926921188597591 0.61767098856252367 -6.206445077193229e-16\
                    -0.039255304524303813 0.6176671878317388 -6.1779459156233684e-16\
                    -0.039255686391576172 0.61512935402849933 -6.0726085523037063e-16\
                    -0.039251414418595726 0.53342452452957689 -5.7997463586375604e-16\
                    -0.039251327529085861 0.53087674359321013 -5.8351199299670087e-16\
                    -0.046452789417386897 0.53087973887844642 -5.6991870401596153e-16\
                    -0.29497772131525812 0.53091239918529665 -6.0798100717561023e-16\
                    -0.30044719205319792 0.53090888582337692 -5.8543089123663301e-16\
                    -0.30044791112324576 0.53361648895323754 -5.9584572075961595e-16\
                    -0.30036042068481161 0.61564126740544511 -6.3212394934725091e-16\
                    -0.30025210628210403 0.61768873316143524 -6.1221381186967642e-16\
                    -0.29659749505810579 0.61768859455320002 -6.4213478373863022e-16\
                    -0.28054452923155032 0.61768697576527321 -6.4465676032777249e-16\
                    ;\
            createNode transform -n "fr_r_brow_01_cnt";\
                setAttr ".rp" -type "double3" -0.24958943362593922 0.5763185837432685 1.5395030841886615e-17 ;\
                setAttr ".sp" -type "double3" -0.24958943362593922 0.5763185837432685 1.5395030841886615e-17 ;\
            createNode nurbsCurve -n "fr_r_brow_01_cntShape" -p "fr_r_brow_01_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    -0.23819369004972829 0.58771432731947937 2.1153545647025581e-17\
                    -0.24958943362593922 0.59243459886207206 2.3538800578440409e-17\
                    -0.26098517720215014 0.58771432731947937 2.1153545647025584e-17\
                    -0.26570544874474278 0.5763185837432685 1.5395030841886619e-17\
                    -0.26098517720215014 0.56492284016705763 9.6365160367476487e-18\
                    -0.24958943362593922 0.56020256862446494 7.2512611053328217e-18\
                    -0.23819369004972832 0.56492284016705763 9.6365160367476456e-18\
                    -0.23347341850713568 0.5763185837432685 1.5395030841886612e-17\
                    -0.23819369004972829 0.58771432731947937 2.1153545647025581e-17\
                    -0.24958943362593922 0.59243459886207206 2.3538800578440409e-17\
                    -0.26098517720215014 0.58771432731947937 2.1153545647025584e-17\
                    ;\
            createNode transform -n "fr_r_brow_02_cnt";\
                setAttr ".rp" -type "double3" -0.17255788979339692 0.5763185837432685 1.539503084188807e-17 ;\
                setAttr ".sp" -type "double3" -0.17255788979339692 0.5763185837432685 1.539503084188807e-17 ;\
            createNode nurbsCurve -n "fr_r_brow_02_cntShape" -p "fr_r_brow_02_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    -0.161162146217186 0.58771432731947937 2.1153545647027035e-17\
                    -0.17255788979339692 0.59243459886207206 2.3538800578441864e-17\
                    -0.18395363336960782 0.58771432731947937 2.1153545647027038e-17\
                    -0.18867390491220046 0.5763185837432685 1.5395030841888073e-17\
                    -0.18395363336960785 0.56492284016705763 9.6365160367491032e-18\
                    -0.17255788979339692 0.56020256862446494 7.2512611053342762e-18\
                    -0.16116214621718603 0.56492284016705763 9.6365160367491001e-18\
                    -0.15644187467459339 0.5763185837432685 1.5395030841888067e-17\
                    -0.161162146217186 0.58771432731947937 2.1153545647027035e-17\
                    -0.17255788979339692 0.59243459886207206 2.3538800578441864e-17\
                    -0.18395363336960782 0.58771432731947937 2.1153545647027038e-17\
                    ;\
            createNode transform -n "fr_r_brow_03_cnt";\
                setAttr ".rp" -type "double3" -0.098091810495783305 0.5763185837432685 1.539503084188807e-17 ;\
                setAttr ".sp" -type "double3" -0.098091810495783305 0.5763185837432685 1.539503084188807e-17 ;\
            createNode nurbsCurve -n "fr_r_brow_03_cntShape" -p "fr_r_brow_03_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    -0.086696066919572379 0.58771432731947937 2.1153545647027035e-17\
                    -0.098091810495783305 0.59243459886207206 2.3538800578441864e-17\
                    -0.10948755407199422 0.58771432731947937 2.1153545647027038e-17\
                    -0.11420782561458685 0.5763185837432685 1.5395030841888073e-17\
                    -0.10948755407199422 0.56492284016705763 9.6365160367491032e-18\
                    -0.098091810495783305 0.56020256862446494 7.2512611053342762e-18\
                    -0.086696066919572407 0.56492284016705763 9.6365160367491001e-18\
                    -0.081975795376979757 0.5763185837432685 1.5395030841888067e-17\
                    -0.086696066919572379 0.58771432731947937 2.1153545647027035e-17\
                    -0.098091810495783305 0.59243459886207206 2.3538800578441864e-17\
                    -0.10948755407199422 0.58771432731947937 2.1153545647027038e-17\
                    ;\
            createNode transform -n "fr_mouth_cnt_boundry";\
                setAttr ".rp" -type "double3" 5.0852929445548278e-16 -0.28883807524767224 2.5866630250674998e-16 ;\
                setAttr ".sp" -type "double3" 5.0852929445548278e-16 -0.28883807524767224 2.5866630250674998e-16 ;\
            createNode nurbsCurve -n "fr_mouth_cnt_boundryShape" -p "fr_mouth_cnt_boundry";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 12 1 no 3\
                    17 0 0 0 0.53333333333333333 2.1333333333333333 2.6666666666666665 3.2000000000000002\
                     3.7333333333333329 4.2666666666666666 4.7999999999999998 5.8666666666666663 6.4000000000000004\
                     6.9333333333333336 7.4666666666666659 8 8 8\
                    15\
                    -0.17599004950593633 -0.19247870571603282 1.6665770589351035e-16\
                    -0.1482973830655975 -0.19248261720160059 1.6230821003245013e-16\
                    0.19709014248472967 -0.19251733567601015 1.9788825484836069e-16\
                    0.2085992216728548 -0.19252651940129381 2.0280721613696791e-16\
                    0.20859856292087639 -0.198658700232654 2.2273157444522064e-16\
                    0.20860593242032396 -0.39608249868758111 3.262337218838101e-16\
                    0.20860608231176705 -0.40223871482772006 3.2189117432224283e-16\
                    0.19618297719148883 -0.40223147730464537 3.4533863019593979e-16\
                    -0.20088847502817025 -0.40215256003773919 2.8985909025909491e-16\
                    -0.21032375511207865 -0.40216104939216035 3.2876229353215263e-16\
                    -0.21032499556616027 -0.39561865406640334 3.0892580424215138e-16\
                    -0.21017406747259473 -0.19742176131513411 1.8969073282028837e-16\
                    -0.20998721635378759 -0.19247445931067567 2.2262320627954192e-16\
                    -0.20368271594627516 -0.19247479423046504 1.7100720175457057e-16\
                    -0.17599004950593627 -0.19247870571603282 1.6665770589351035e-16\
                    ;\
            createNode transform -n "fr_r_ear_cnt";\
                setAttr ".rp" -type "double3" -0.52678902578821274 0.31527161692207795 -3.4496053817471169e-16 ;\
                setAttr ".sp" -type "double3" -0.52678902578821274 0.31527161692207795 -3.4496053817471169e-16 ;\
            createNode nurbsCurve -n "fr_r_ear_cntShape" -p "fr_r_ear_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 12 0 no 3\
                    17 0 0 0 0.53333333333333333 2.1333333333333333 2.6666666666666665 3.2000000000000002\
                     3.7333333333333329 4.2666666666666666 4.7999999999999998 5.8666666666666663 6.4000000000000004\
                     6.9333333333333336 7.4666666666666659 8 8 8\
                    15\
                    -0.54462876679389649 0.52573998877550265 -5.5160149370465525e-16\
                    -0.48468759856797938 0.53084035932104978 -5.5513853144139388e-16\
                    -0.36652969035237554 0.48290299545452564 -4.8167449636572508e-16\
                    -0.35717134620124547 0.48289633810151322 -4.7767556518742518e-16\
                    -0.35717188185032944 0.4784510731061814 -4.620150745656568e-16\
                    -0.35716588951063599 0.14143750119741536 -2.0321796932519058e-16\
                    -0.35716576762984198 0.13697481282209778 -2.0729167611630144e-16\
                    -0.36726733103390519 0.13698005935817711 -1.8822527640640988e-16\
                    -0.46997076669737536 0.16040257378712713 -5.0257665570670014e-16\
                    -0.54284499078788895 0.26239323026040318 -1.2496161331873326e-16\
                    -0.57007413030326315 0.43127924972604104 -3.1062515909665089e-16\
                    -0.57242471809210949 0.51195031777355804 -5.2310919012135982e-16\
                    -0.5722727843842742 0.5155366550043986 -4.9589480433191417e-16\
                    -0.56714642426892148 0.51553641221847024 -5.3786520578068888e-16\
                    -0.54462876679389638 0.52573998877550265 -5.5160149370465525e-16\
                    ;\
            createNode transform -n "fr_jaw_cnt_boundry";\
                setAttr ".rp" -type "double3" 7.3690599620745023e-16 -0.5148097380819614 4.844573511990581e-16 ;\
                setAttr ".sp" -type "double3" 7.3690599620745023e-16 -0.5148097380819614 4.844573511990581e-16 ;\
            createNode nurbsCurve -n "fr_jaw_cnt_boundryShape" -p "fr_jaw_cnt_boundry";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 12 1 no 3\
                    17 0 0 0 0.53333333333333333 2.1333333333333333 2.6666666666666665 3.2000000000000002\
                     3.7333333333333329 4.2666666666666666 4.7999999999999998 5.8666666666666663 6.4000000000000004\
                     6.9333333333333336 7.4666666666666659 8 8 8\
                    15\
                    -0.086132494459545475 -0.42739087395016712 4.0089290337707933e-16\
                    -0.072579237071194763 -0.42739442251661236 3.9704137287961953e-16\
                    0.096459235355943029 -0.42742591970896671 4.2854937283372607e-16\
                    0.10209197256005538 -0.42743425134123769 4.3290546661180563e-16\
                    0.10209165015574166 -0.43299747041929787 4.506819859286294e-16\
                    0.10209525691289716 -0.61210370884115861 5.4661422929718336e-16\
                    0.10209533027229406 -0.61768873316143569 5.4290216176772065e-16\
                    0.096015253381886531 -0.61768216715701496 5.6366546387366684e-16\
                    -0.098318203278684582 -0.61761057206598358 5.1453487800458522e-16\
                    -0.10293598827183041 -0.6176182737531607 5.4898507085053679e-16\
                    -0.10293659537095114 -0.61168290108666512 5.3127747365645489e-16\
                    -0.10286272861985184 -0.43187529832855465 4.2139648010323975e-16\
                    -0.10277128053514137 -0.4273870215387745 4.5045202047748881e-16\
                    -0.099685751847896173 -0.42738732538372187 4.0474443387453918e-16\
                    -0.086132494459545447 -0.42739087395016712 4.0089290337707933e-16\
                    ;\
            createNode transform -n "fr_l_top_lip_cnt";\
                setAttr ".rp" -type "double3" 0.053252140857643293 -0.26976258829785849 -1.3972519744220542e-16 ;\
                setAttr ".sp" -type "double3" 0.053252140857643293 -0.26976258829785849 -1.3972519744220542e-16 ;\
            createNode nurbsCurve -n "fr_l_top_lip_cntShape" -p "fr_l_top_lip_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    0.037169779631505945 -0.25368022707172116 -1.3159843374285077e-16\
                    0.0532521408576433 -0.24701869493687184 -1.2823221800037673e-16\
                    0.069334502083780628 -0.25368022707172116 -1.3159843374285077e-16\
                    0.07599603421862991 -0.26976258829785849 -1.3972519744220542e-16\
                    0.069334502083780628 -0.28584494952399581 -1.4785196114156007e-16\
                    0.0532521408576433 -0.29250648165884513 -1.5121817688403411e-16\
                    0.037169779631505966 -0.28584494952399581 -1.4785196114156007e-16\
                    0.030508247496656676 -0.26976258829785849 -1.3972519744220542e-16\
                    0.037169779631505945 -0.25368022707172116 -1.3159843374285077e-16\
                    0.0532521408576433 -0.24701869493687184 -1.2823221800037673e-16\
                    0.069334502083780628 -0.25368022707172116 -1.3159843374285077e-16\
                    ;\
            createNode transform -n "fr_l_corner_lip_cnt";\
                setAttr ".rp" -type "double3" 0.10643339049206524 -0.30491222067230694 -1.5533476990989133e-16 ;\
                setAttr ".sp" -type "double3" 0.10643339049206524 -0.30491222067230694 -1.5533476990989133e-16 ;\
            createNode nurbsCurve -n "fr_l_corner_lip_cntShape" -p "fr_l_corner_lip_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    0.09035102926592789 -0.28882985944616962 -1.4720800621053668e-16\
                    0.10643339049206524 -0.2821683273113203 -1.4384179046806264e-16\
                    0.12251575171820257 -0.28882985944616962 -1.4720800621053668e-16\
                    0.12917728385305186 -0.30491222067230694 -1.5533476990989133e-16\
                    0.12251575171820257 -0.32099458189844426 -1.6346153360924598e-16\
                    0.10643339049206524 -0.32765611403329359 -1.6682774935172003e-16\
                    0.090351029265927918 -0.32099458189844426 -1.6346153360924598e-16\
                    0.083689497131078622 -0.30491222067230694 -1.5533476990989133e-16\
                    0.09035102926592789 -0.28882985944616962 -1.4720800621053668e-16\
                    0.10643339049206524 -0.2821683273113203 -1.4384179046806264e-16\
                    0.12251575171820257 -0.28882985944616962 -1.4720800621053668e-16\
                    ;\
            createNode transform -n "fr_l_btm_lip_cnt";\
                setAttr ".rp" -type "double3" 0.053252140857643293 -0.3283453089219357 -1.6574115155501622e-16 ;\
                setAttr ".sp" -type "double3" 0.053252140857643293 -0.3283453089219357 -1.6574115155501622e-16 ;\
            createNode nurbsCurve -n "fr_l_btm_lip_cntShape" -p "fr_l_btm_lip_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    0.037169779631505945 -0.31226294769579838 -1.5761438785566157e-16\
                    0.0532521408576433 -0.30560141556094905 -1.5424817211318753e-16\
                    0.069334502083780628 -0.31226294769579838 -1.5761438785566157e-16\
                    0.07599603421862991 -0.3283453089219357 -1.6574115155501622e-16\
                    0.069334502083780628 -0.34442767014807302 -1.7386791525437087e-16\
                    0.0532521408576433 -0.35108920228292234 -1.7723413099684491e-16\
                    0.037169779631505966 -0.34442767014807302 -1.7386791525437087e-16\
                    0.030508247496656676 -0.3283453089219357 -1.6574115155501622e-16\
                    0.037169779631505945 -0.31226294769579838 -1.5761438785566157e-16\
                    0.0532521408576433 -0.30560141556094905 -1.5424817211318753e-16\
                    0.069334502083780628 -0.31226294769579838 -1.5761438785566157e-16\
                    ;\
            createNode transform -n "fr_l_eye_top_lid_cnt";\
                setAttr ".rp" -type "double3" 0.16825030145385933 0.45620678651420388 1.0566274441949991e-16 ;\
                setAttr ".sp" -type "double3" 0.16825030145385933 0.45620678651420388 1.0566274441949991e-16 ;\
            createNode nurbsCurve -n "fr_l_eye_top_lid_cntShape" -p "fr_l_eye_top_lid_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    0.11730165640220341 0.48003545542895371 1.1574035943782108e-16\
                    0.16825030145385933 0.4892031987468301 1.0578804489078197e-16\
                    0.21919894650551519 0.48003541861211657 1.1574028552217453e-16\
                    0.24030256627044394 0.44154122571965443 1.0537810561117146e-16\
                    0.21919894650551522 0.42215499508817955 9.5585208985211184e-17\
                    0.16825030145385936 0.44531413308814871 1.0506434297447407e-16\
                    0.11730165640220348 0.42215482998534037 9.5585129401178392e-17\
                    0.096198036637274706 0.44154119343641968 1.0537810289034605e-16\
                    0.11730165640220341 0.48003545542895371 1.1574035943782108e-16\
                    0.16825030145385933 0.4892031987468301 1.0578804489078197e-16\
                    0.21919894650551519 0.48003541861211657 1.1574028552217453e-16\
                    ;\
            createNode transform -n "fr_l_eye_btm_lid_cnt";\
                setAttr ".rp" -type "double3" 0.16825030145385933 0.18275559786750772 -1.5773977879177464e-17 ;\
                setAttr ".sp" -type "double3" 0.16825030145385933 0.18275559786750772 -1.5773977879177464e-17 ;\
            createNode nurbsCurve -n "fr_l_eye_btm_lid_cntShape" -p "fr_l_eye_btm_lid_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    0.11730165640220341 0.19044401310826853 -9.2399308757357721e-18\
                    0.16825030145385933 0.16371371514616764 -1.9818343756995024e-17\
                    0.21919894650551519 0.19044380301814404 -9.2400241744931425e-18\
                    0.24030256627044394 0.18275559786750772 -1.5773977879177455e-17\
                    0.21919894650551522 0.13957187285611306 -3.807110895203633e-17\
                    0.16825030145385936 0.12909176149566437 -4.4017437345010308e-17\
                    0.11730165640220348 0.13957183449486199 -3.8071125987854011e-17\
                    0.096198036637274706 0.1827555978675077 -1.5773977879177482e-17\
                    0.11730165640220341 0.19044401310826853 -9.2399308757357721e-18\
                    0.16825030145385933 0.16371371514616764 -1.9818343756995024e-17\
                    0.21919894650551519 0.19044380301814404 -9.2400241744931425e-18\
                    ;\
            createNode transform -n "fr_l_eye_cnt_boundry";\
                setAttr ".rp" -type "double3" 0.16825030145385911 0.31398845330661285 4.250511719914372e-17 ;\
                setAttr ".sp" -type "double3" 0.16825030145385911 0.31398845330661285 4.250511719914372e-17 ;\
            createNode nurbsCurve -n "fr_l_eye_cnt_boundryShape" -p "fr_l_eye_cnt_boundry";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    0.097727574361055738 0.38451118039941617 7.8141770950325547e-17\
                    0.16825030145385914 0.4137226504167919 9.2902956251659123e-17\
                    0.23877302854666244 0.38451118039941623 7.8141770950325572e-17\
                    0.26798449856403805 0.31398845330661285 4.2505117199143732e-17\
                    0.23877302854666244 0.24346572621380946 6.86846344796188e-18\
                    0.16825030145385914 0.21425425619643379 -7.8927218533717022e-18\
                    0.097727574361055822 0.24346572621380946 6.8684634479618615e-18\
                    0.068516104343680134 0.31398845330661279 4.2505117199143695e-17\
                    0.097727574361055738 0.38451118039941617 7.8141770950325547e-17\
                    0.16825030145385914 0.4137226504167919 9.2902956251659123e-17\
                    0.23877302854666244 0.38451118039941623 7.8141770950325572e-17\
                    ;\
            createNode transform -n "fr_l_eye_cnt";\
                setAttr ".rp" -type "double3" 0.16825030145385911 0.31398845330661285 4.250511719914372e-17 ;\
                setAttr ".sp" -type "double3" 0.16825030145385911 0.31398845330661285 4.250511719914372e-17 ;\
            createNode nurbsCurve -n "fr_l_eye_cntShape" -p "fr_l_eye_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    0.14279470492786889 0.33944404983260307 5.5368378686929729e-17\
                    0.16825030145385911 0.34998810315196566 6.069651605152223e-17\
                    0.19370589797984933 0.33944404983260307 5.5368378686929741e-17\
                    0.20424995129921192 0.31398845330661285 4.2505117199143726e-17\
                    0.19370589797984933 0.28853285678062263 2.9641855711357705e-17\
                    0.16825030145385911 0.27798880346126004 2.4313718346765209e-17\
                    0.14279470492786892 0.28853285678062263 2.9641855711357698e-17\
                    0.1322506516085063 0.31398845330661285 4.2505117199143708e-17\
                    0.14279470492786889 0.33944404983260307 5.5368378686929729e-17\
                    0.16825030145385911 0.34998810315196566 6.069651605152223e-17\
                    0.19370589797984933 0.33944404983260307 5.5368378686929741e-17\
                    ;\
            createNode transform -n "fr_l_cheek_cnt";\
                setAttr ".rp" -type "double3" 0.24524278723186493 -0.078368051996255517 -2.8412377133224908e-17 ;\
                setAttr ".sp" -type "double3" 0.24524278723186493 -0.078368051996255517 -2.8412377133224908e-17 ;\
            createNode nurbsCurve -n "fr_l_cheek_cntShape" -p "fr_l_cheek_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    0.22330215394331962 -0.05642741870771021 -1.73253023161007e-17\
                    0.24524278723186493 -0.04733931083254013 -1.2732885559802637e-17\
                    0.26718342052041022 -0.056427418707710203 -1.7325302316100694e-17\
                    0.27627152839558028 -0.078368051996255517 -2.8412377133224902e-17\
                    0.26718342052041022 -0.10030868528480083 -3.9499451950349123e-17\
                    0.24524278723186493 -0.10939679315997092 -4.4091868706647177e-17\
                    0.22330215394331965 -0.10030868528480083 -3.9499451950349123e-17\
                    0.21421404606814956 -0.078368051996255531 -2.8412377133224915e-17\
                    0.22330215394331962 -0.05642741870771021 -1.73253023161007e-17\
                    0.24524278723186493 -0.04733931083254013 -1.2732885559802637e-17\
                    0.26718342052041022 -0.056427418707710203 -1.7325302316100694e-17\
                    ;\
            createNode transform -n "fr_l_cheek_cnt_boundry";\
                setAttr ".rp" -type "double3" 0.23274487760658463 -0.094131183060117252 -1.3873640963925353e-16 ;\
                setAttr ".sp" -type "double3" 0.23274487760658463 -0.094131183060117252 -1.3873640963925353e-16 ;\
            createNode nurbsCurve -n "fr_l_cheek_cnt_boundryShape" -p "fr_l_cheek_cnt_boundry";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    0.14673382229970189 0.0028526665634009546 -1.0636274873060901e-16\
                    0.234939436469912 0.0118329808327549 -9.2953139318580755e-17\
                    0.33192328609343125 -0.0037310100265793011 -1.06362748730609e-16\
                    0.34309815922611037 -0.11168765396673634 -1.3873640963925351e-16\
                    0.31217225632348528 -0.17355856177701889 -1.7111007054789804e-16\
                    0.23055031874325729 -0.18253887604637031 -1.8451967995992631e-16\
                    0.17965220524961212 -0.13186194337379786 -1.7111007054789804e-16\
                    0.14214262575700493 -0.094131183060117293 -1.3873640963925356e-16\
                    0.14673382229970189 0.0028526665634009546 -1.0636274873060901e-16\
                    0.234939436469912 0.0118329808327549 -9.2953139318580755e-17\
                    0.33192328609343125 -0.0037310100265793011 -1.06362748730609e-16\
                    ;\
            createNode transform -n "fr_l_brow_boundry";\
                setAttr ".rp" -type "double3" 0.17852610292294122 0.5778081672334654 -6.0728724883994361e-16 ;\
                setAttr ".sp" -type "double3" 0.17852610292294122 0.5778081672334654 -6.0728724883994361e-16 ;\
            createNode nurbsCurve -n "fr_l_brow_boundryShape" -p "fr_l_brow_boundry";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 12 1 no 3\
                    17 0 0 0 0.53333333333333333 2.1333333333333333 2.6666666666666665 3.2000000000000002\
                     3.7333333333333329 4.2666666666666666 4.7999999999999998 5.8666666666666663 6.4000000000000004\
                     6.9333333333333336 7.4666666666666659 8 8 8\
                    15\
                    0.28054452923155049 0.61768697576527332 -6.3137444889978312e-16\
                    0.26449156340499508 0.6176853569773465 -6.338969646536138e-16\
                    0.045926921188597786 0.61767098856252356 -6.0736752109951117e-16\
                    0.039255304524304008 0.61766718783173868 -6.0451887084017336e-16\
                    0.039255686391576367 0.61512935402849922 -5.9483040296451578e-16\
                    0.039251414418596003 0.53342452452957667 -5.9475735847773413e-16\
                    0.039251327529086139 0.53087674359321002 -5.9914329712785557e-16\
                    0.046452789417387175 0.53087973887844631 -5.8554901051672578e-16\
                    0.29497772131525835 0.53091239918529676 -6.2360043560897748e-16\
                    0.30044719205319814 0.53090888582337703 -6.0105148985458947e-16\
                    0.30044791112324598 0.53361648895323766 -6.1056450637667684e-16\
                    0.30036042068481178 0.61564126740544522 -6.1952299567608635e-16\
                    0.30025210628210419 0.61768873316143535 -5.9893091511118234e-16\
                    0.29659749505810595 0.61768859455320013 -6.2885193314595234e-16\
                    0.28054452923155049 0.61768697576527332 -6.3137444889978312e-16\
                    ;\
            createNode transform -n "fr_l_brow_01_cnt";\
                setAttr ".rp" -type "double3" 0.24958943362593944 0.5763185837432685 1.5395030841886615e-17 ;\
                setAttr ".sp" -type "double3" 0.24958943362593944 0.5763185837432685 1.5395030841886615e-17 ;\
            createNode nurbsCurve -n "fr_l_brow_01_cntShape" -p "fr_l_brow_01_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    0.23819369004972851 0.58771432731947937 2.1153545647025581e-17\
                    0.24958943362593944 0.59243459886207206 2.3538800578440409e-17\
                    0.26098517720215036 0.58771432731947937 2.1153545647025584e-17\
                    0.265705448744743 0.5763185837432685 1.5395030841886619e-17\
                    0.26098517720215036 0.56492284016705763 9.6365160367476487e-18\
                    0.24958943362593944 0.56020256862446494 7.2512611053328217e-18\
                    0.23819369004972854 0.56492284016705763 9.6365160367476456e-18\
                    0.2334734185071359 0.5763185837432685 1.5395030841886612e-17\
                    0.23819369004972851 0.58771432731947937 2.1153545647025581e-17\
                    0.24958943362593944 0.59243459886207206 2.3538800578440409e-17\
                    0.26098517720215036 0.58771432731947937 2.1153545647025584e-17\
                    ;\
            createNode transform -n "fr_l_brow_02_cnt";\
                setAttr ".rp" -type "double3" 0.17255788979339715 0.5763185837432685 1.539503084188807e-17 ;\
                setAttr ".sp" -type "double3" 0.17255788979339715 0.5763185837432685 1.539503084188807e-17 ;\
            createNode nurbsCurve -n "fr_l_brow_02_cntShape" -p "fr_l_brow_02_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    0.16116214621718622 0.58771432731947937 2.1153545647027035e-17\
                    0.17255788979339715 0.59243459886207206 2.3538800578441864e-17\
                    0.18395363336960804 0.58771432731947937 2.1153545647027038e-17\
                    0.18867390491220068 0.5763185837432685 1.5395030841888073e-17\
                    0.18395363336960804 0.56492284016705763 9.6365160367491032e-18\
                    0.17255788979339715 0.56020256862446494 7.2512611053342762e-18\
                    0.16116214621718625 0.56492284016705763 9.6365160367491001e-18\
                    0.15644187467459361 0.5763185837432685 1.5395030841888067e-17\
                    0.16116214621718622 0.58771432731947937 2.1153545647027035e-17\
                    0.17255788979339715 0.59243459886207206 2.3538800578441864e-17\
                    0.18395363336960804 0.58771432731947937 2.1153545647027038e-17\
                    ;\
            createNode transform -n "fr_l_brow_03_cnt";\
                setAttr ".rp" -type "double3" 0.098091810495783527 0.5763185837432685 1.539503084188807e-17 ;\
                setAttr ".sp" -type "double3" 0.098091810495783527 0.5763185837432685 1.539503084188807e-17 ;\
            createNode nurbsCurve -n "fr_l_brow_03_cntShape" -p "fr_l_brow_03_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 8 2 no 3\
                    13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\
                    11\
                    0.086696066919572601 0.58771432731947937 2.1153545647027035e-17\
                    0.098091810495783527 0.59243459886207206 2.3538800578441864e-17\
                    0.10948755407199444 0.58771432731947937 2.1153545647027038e-17\
                    0.11420782561458707 0.5763185837432685 1.5395030841888073e-17\
                    0.10948755407199444 0.56492284016705763 9.6365160367491032e-18\
                    0.098091810495783527 0.56020256862446494 7.2512611053342762e-18\
                    0.086696066919572629 0.56492284016705763 9.6365160367491001e-18\
                    0.081975795376979979 0.5763185837432685 1.5395030841888067e-17\
                    0.086696066919572601 0.58771432731947937 2.1153545647027035e-17\
                    0.098091810495783527 0.59243459886207206 2.3538800578441864e-17\
                    0.10948755407199444 0.58771432731947937 2.1153545647027038e-17\
                    ;\
            createNode transform -n "fr_l_ear_cnt";\
                setAttr ".rp" -type "double3" 0.52678902578821296 0.31527161692207795 -3.4496053817471169e-16 ;\
                setAttr ".sp" -type "double3" 0.52678902578821296 0.31527161692207795 -3.4496053817471169e-16 ;\
            createNode nurbsCurve -n "fr_l_ear_cntShape" -p "fr_l_ear_cnt";\
                setAttr -k off ".v";\
                setAttr ".cc" -type "nurbsCurve"\
                    3 12 0 no 3\
                    17 0 0 0 0.53333333333333333 2.1333333333333333 2.6666666666666665 3.2000000000000002\
                     3.7333333333333329 4.2666666666666666 4.7999999999999998 5.8666666666666663 6.4000000000000004\
                     6.9333333333333336 7.4666666666666659 8 8 8\
                    15\
                    0.54462876679389649 0.52573998877550265 -4.8150144398854283e-16\
                    0.48468759856797938 0.53084035932104967 -4.8333971708114556e-16\
                    0.36652969035237559 0.48290299545452547 -4.2584203153681145e-16\
                    0.35717134620124552 0.48289633810151311 -4.2184531770249093e-16\
                    0.3571718818503295 0.47845107310618129 -4.0766539774523572e-16\
                    0.35716588951063638 0.14143750119741519 -2.6111636064805294e-16\
                    0.35716576762984237 0.13697481282209761 -2.6667644125496517e-16\
                    0.36726733103390552 0.13698005935817695 -2.476082940975272e-16\
                    0.46997076669737575 0.16040257378712708 -5.5415840895372688e-16\
                    0.54284499078788917 0.26239323026040323 -1.4257365403178018e-16\
                    0.57007413030326326 0.43127924972604109 -2.7198685560528467e-16\
                    0.57242471809210949 0.51195031777355804 -4.5760202347975678e-16\
                    0.57227278438427431 0.5155366550043986 -4.2919314743998628e-16\
                    0.56714642426892148 0.51553641221847024 -4.7116362975271931e-16\
                    0.54462876679389638 0.52573998877550265 -4.8150144398854283e-16\
                    ;'

        mel.eval( mel_cmd )

        # Group the curves and translate up and to the side of head
        cmds.group(self.l_eye_cnt,
            self.r_eye_cnt,
            self.l_top_eyeLid_cnt,
            self.l_btm_eyeLid_cnt,
            self.r_top_eyeLid_cnt,
            self.r_btm_eyeLid_cnt,
            self.l_brow_01_cnt,
            self.l_brow_02_cnt,
            self.l_brow_03_cnt,
            self.mid_brow_cnt,
            self.r_brow_01_cnt,
            self.r_brow_02_cnt,
            self.r_brow_03_cnt,
            self.l_cheek_cnt,
            self.r_cheek_cnt,
            self.l_top_lip_cnt,
            self.mid_top_lip_cnt,
            self.r_top_lip_cnt,
            self.l_mouth_crnr_cnt,
            self.r_mouth_crnr_cnt,
            self.l_btm_lip_cnt,
            self.mid_btm_lip_cnt,
            self.r_btm_lip_cnt,
            self.nose_cnt,
            self.jaw_cnt,
            self.r_ear_cnt,
            self.l_ear_cnt,
            name='faceRig_controls')
        
        # Parent the boundry curves to the group and template them
        for cnt in self.boundry_cnts:
            cmds.parent(cnt,'faceRig_controls')
            cmds.setAttr('%sShape.template'%cnt,1)
        
        # Move curves into position
        cmds.setAttr('faceRig_controls.translateY',self.control_height)
        cmds.setAttr('faceRig_controls.translateX',self.control_x_pos)
        
        # Scale curves down a bit
        cmds.setAttr('faceRig_controls.scaleX',.5)
        cmds.setAttr('faceRig_controls.scaleY',.5)
        cmds.setAttr('faceRig_controls.scaleZ',.5)
        
        # Lock translateZ's
        cmds.select('faceRig_controls',r=True,hi=True)
        sel = cmds.ls(sl=True)
        for cnt in sel:
            if cnt == self.jaw_cnt:
                continue
            if 'Shape' in cnt:
                continue
            if '_lip_' in cnt:
                cmds.setAttr('%s.scaleX'%cnt,lock=True,keyable=False)
                cmds.setAttr('%s.scaleY'%cnt,lock=True,keyable=False)
                cmds.setAttr('%s.scaleZ'%cnt,lock=True,keyable=False)
                cmds.setAttr('%s.visibility'%cnt,lock=True,keyable=False)
                continue
            if '_brow_' in cnt:
                cmds.setAttr('%s.scaleX'%cnt,lock=True,keyable=False)
                cmds.setAttr('%s.scaleY'%cnt,lock=True,keyable=False)
                cmds.setAttr('%s.scaleZ'%cnt,lock=True,keyable=False)
                cmds.setAttr('%s.visibility'%cnt,lock=True,keyable=False)
                continue
            if '_ear_' in cnt:
                cmds.setAttr('%s.scaleX'%cnt,lock=True,keyable=False)
                cmds.setAttr('%s.scaleY'%cnt,lock=True,keyable=False)
                cmds.setAttr('%s.scaleZ'%cnt,lock=True,keyable=False)
                cmds.setAttr('%s.visibility'%cnt,lock=True,keyable=False)
                continue
                
            cmds.setAttr('%s.translateZ'%cnt,lock=True,keyable=False)
            cmds.setAttr('%s.rotateX'%cnt,lock=True,keyable=False)
            cmds.setAttr('%s.rotateY'%cnt,lock=True,keyable=False)
            cmds.setAttr('%s.rotateZ'%cnt,lock=True,keyable=False)
            cmds.setAttr('%s.scaleX'%cnt,lock=True,keyable=False)
            cmds.setAttr('%s.scaleY'%cnt,lock=True,keyable=False)
            cmds.setAttr('%s.scaleZ'%cnt,lock=True,keyable=False)
            cmds.setAttr('%s.visibility'%cnt,lock=True,keyable=False)
            
        # Group btm lip controls
        cmds.group(self.l_btm_lip,n=self.l_btm_lip + '_buffer_grp')
        cmds.xform(self.l_btm_lip + '_buffer_grp', cp=True)
        cmds.group(self.mid_btm_lip,n=self.mid_btm_lip + '_buffer_grp')
        cmds.xform(self.mid_btm_lip + '_buffer_grp', cp=True)
        cmds.group(self.r_btm_lip,n=self.r_btm_lip + '_buffer_grp')
        cmds.xform(self.r_btm_lip + '_buffer_grp', cp=True)
        
        # Grp btm lip buffer grps to a single grp that will be parent coinstrained to jaw joint
        cmds.group( self.l_btm_lip + '_buffer_grp',
                    self.mid_btm_lip + '_buffer_grp',
                    self.r_btm_lip + '_buffer_grp',
                    n='btm_lip_jnts_grp' )
        
        cmds.group(self.l_mouth_crnr,n=self.l_mouth_crnr + '_buffer_grp')
        cmds.xform(self.l_mouth_crnr + '_buffer_grp', cp=True)
        cmds.group(self.r_mouth_crnr,n=self.r_mouth_crnr + '_buffer_grp')
        cmds.xform(self.r_mouth_crnr + '_buffer_grp', cp=True)
        
        cmds.group(self.r_mouth_crnr + '_buffer_grp', self.l_mouth_crnr + '_buffer_grp', n='mouth_corner_jnts_grp')

    def organizeHeirarchy(self):
        """ Group and parent to organize rig under one node. """
        cmds.group('faceRig_controls','faceRig_joints_grp',name='faceRig_grp')
        
        
    def createConnections(self):
        """ Create the SDK's for the controller curves """
        #--- Eye lids SDKs
        # Left side
        cmds.setDrivenKeyframe( '%s.rotateX'%self.l_top_eyeLid, cd='%s.translateY'%self.l_top_eyeLid_cnt, dv=0,v=0, ott='linear', itt='linear')
        cmds.setDrivenKeyframe( '%s.rotateX'%self.l_top_eyeLid, cd='%s.translateY'%self.l_top_eyeLid_cnt, dv=.1,v=-80, ott='linear', itt='linear')
        cmds.setDrivenKeyframe( '%s.rotateX'%self.l_top_eyeLid, cd='%s.translateY'%self.l_top_eyeLid_cnt, dv=-.1,v=80, ott='linear', itt='linear')
        
        cmds.setDrivenKeyframe( '%s.rotateX'%self.l_btm_eyeLid, cd='%s.translateY'%self.l_btm_eyeLid_cnt, dv=0,v=0, ott='linear', itt='linear')
        cmds.setDrivenKeyframe( '%s.rotateX'%self.l_btm_eyeLid, cd='%s.translateY'%self.l_btm_eyeLid_cnt, dv=.1,v=-80, ott='linear', itt='linear')
        cmds.setDrivenKeyframe( '%s.rotateX'%self.l_btm_eyeLid, cd='%s.translateY'%self.l_btm_eyeLid_cnt, dv=-.1,v=80, ott='linear', itt='linear')
        
        # Right side
        cmds.setDrivenKeyframe( '%s.rotateX'%self.r_top_eyeLid, cd='%s.translateY'%self.r_top_eyeLid_cnt, dv=0,v=0, ott='linear', itt='linear')
        cmds.setDrivenKeyframe( '%s.rotateX'%self.r_top_eyeLid, cd='%s.translateY'%self.r_top_eyeLid_cnt, dv=.1,v=-80, ott='linear', itt='linear')
        cmds.setDrivenKeyframe( '%s.rotateX'%self.r_top_eyeLid, cd='%s.translateY'%self.r_top_eyeLid_cnt, dv=-.1,v=80, ott='linear', itt='linear')
        
        cmds.setDrivenKeyframe( '%s.rotateX'%self.r_btm_eyeLid, cd='%s.translateY'%self.r_btm_eyeLid_cnt, dv=0,v=0, ott='linear', itt='linear')
        cmds.setDrivenKeyframe( '%s.rotateX'%self.r_btm_eyeLid, cd='%s.translateY'%self.r_btm_eyeLid_cnt, dv=.1,v=-80, ott='linear', itt='linear')
        cmds.setDrivenKeyframe( '%s.rotateX'%self.r_btm_eyeLid, cd='%s.translateY'%self.r_btm_eyeLid_cnt, dv=-.1,v=80, ott='linear', itt='linear')
        
        #--- Eyes SDKs
        cmds.setDrivenKeyframe( '%s.rotateX'%self.l_eye, cd='%s.translateY'%self.l_eye_cnt, dv=0,v=0, ott='linear', itt='linear')
        cmds.setDrivenKeyframe( '%s.rotateX'%self.l_eye, cd='%s.translateY'%self.l_eye_cnt, dv=-0.1,v=75, ott='linear', itt='linear')
        cmds.setDrivenKeyframe( '%s.rotateX'%self.l_eye, cd='%s.translateY'%self.l_eye_cnt, dv=0.1,v=-75, ott='linear', itt='linear')
        
        cmds.setDrivenKeyframe( '%s.rotateX'%self.r_eye, cd='%s.translateY'%self.r_eye_cnt, dv=0,v=0, ott='linear', itt='linear')
        cmds.setDrivenKeyframe( '%s.rotateX'%self.r_eye, cd='%s.translateY'%self.r_eye_cnt, dv=-0.1,v=75, ott='linear', itt='linear')
        cmds.setDrivenKeyframe( '%s.rotateX'%self.r_eye, cd='%s.translateY'%self.r_eye_cnt, dv=0.1,v=-75, ott='linear', itt='linear')
        
        cmds.setDrivenKeyframe( '%s.rotateY'%self.l_eye, cd='%s.translateX'%self.l_eye_cnt, dv=0,v=0, ott='linear', itt='linear')
        cmds.setDrivenKeyframe( '%s.rotateY'%self.l_eye, cd='%s.translateX'%self.l_eye_cnt, dv=0.1,v=75, ott='linear', itt='linear')        
        cmds.setDrivenKeyframe( '%s.rotateY'%self.l_eye, cd='%s.translateX'%self.l_eye_cnt, dv=-0.1,v=-75, ott='linear', itt='linear')
        
        cmds.setDrivenKeyframe( '%s.rotateY'%self.r_eye, cd='%s.translateX'%self.r_eye_cnt, dv=0,v=0, ott='linear', itt='linear')
        cmds.setDrivenKeyframe( '%s.rotateY'%self.r_eye, cd='%s.translateX'%self.r_eye_cnt, dv=0.1,v=75, ott='linear', itt='linear')        
        cmds.setDrivenKeyframe( '%s.rotateY'%self.r_eye, cd='%s.translateX'%self.r_eye_cnt, dv=-0.1,v=-75, ott='linear', itt='linear')

        #--- Jaw
        #--- Snap cpntrol pivot to joint location
        pos = cmds.xform(self.jaw,query=True,t=True,ws=True)
        cmds.move(pos[0],pos[1],pos[2],'%s.scalePivot'%self.jaw_cnt)
        cmds.move(pos[0],pos[1],pos[2],'%s.rotatePivot'%self.jaw_cnt)
        
        cmds.parentConstraint(self.jaw_cnt,self.jaw,mo=True)
        
#        #--- Jaw SDKs
#        cmds.setDrivenKeyframe( '%s.rotateY'%self.jaw, cd='%s.translateX'%self.jaw_cnt, dv=0,v=0, ott='linear', itt='linear')
#        cmds.setDrivenKeyframe( '%s.rotateY'%self.jaw, cd='%s.translateX'%self.jaw_cnt, dv=0.1,v=45, ott='linear', itt='linear')
#        cmds.setDrivenKeyframe( '%s.rotateY'%self.jaw, cd='%s.translateX'%self.jaw_cnt, dv=-0.1,v=-45, ott='linear', itt='linear')
#        
#        cmds.setDrivenKeyframe( '%s.rotateX'%self.jaw, cd='%s.translateY'%self.jaw_cnt, dv=0,v=0, ott='linear', itt='linear')
#        cmds.setDrivenKeyframe( '%s.rotateX'%self.jaw, cd='%s.translateY'%self.jaw_cnt, dv=0.1,v=-20, ott='linear', itt='linear')
#        cmds.setDrivenKeyframe( '%s.rotateX'%self.jaw, cd='%s.translateY'%self.jaw_cnt, dv=-0.1,v=75, ott='linear', itt='linear')
#        
#        cmds.setDrivenKeyframe( '%s.rotateZ'%self.jaw, cd='%s.translateX'%self.jaw_cnt, dv=0,v=0, ott='linear', itt='linear')
#        cmds.setDrivenKeyframe( '%s.rotateZ'%self.jaw, cd='%s.translateX'%self.jaw_cnt, dv=0.1,v=-10, ott='linear', itt='linear')
#        cmds.setDrivenKeyframe( '%s.rotateZ'%self.jaw, cd='%s.translateX'%self.jaw_cnt, dv=-0.1,v=10, ott='linear', itt='linear')
#        
#        # Jaw translation up/down
#        jaw_ty_val = cmds.getAttr('%s.translateY'%self.jaw)
#        cmds.setDrivenKeyframe( '%s.translateY'%self.jaw, cd='%s.translateY'%self.jaw_cnt, dv=0,v=jaw_ty_val, ott='linear', itt='linear')
#        cmds.setDrivenKeyframe( '%s.translateY'%self.jaw, cd='%s.translateY'%self.jaw_cnt, dv=-0.1,v=jaw_ty_val-0.05, ott='linear', itt='linear')
#        cmds.setDrivenKeyframe( '%s.translateY'%self.jaw, cd='%s.translateY'%self.jaw_cnt, dv=0.1,v=jaw_ty_val+0.08, ott='linear', itt='linear')
#        
#        # Jaw translation forward/back
#        jaw_tz_val = cmds.getAttr('%s.translateZ'%self.jaw)
#        cmds.setDrivenKeyframe( '%s.translateZ'%self.jaw, cd='%s.translateY'%self.jaw_cnt, dv=0,v=jaw_tz_val, ott='linear', itt='linear')
#        cmds.setDrivenKeyframe( '%s.translateZ'%self.jaw, cd='%s.translateY'%self.jaw_cnt, dv=0.1,v=jaw_tz_val+0.05, ott='linear', itt='linear')
#        cmds.setDrivenKeyframe( '%s.translateZ'%self.jaw, cd='%s.translateY'%self.jaw_cnt, dv=-0.1,v=jaw_tz_val-0.08, ott='linear', itt='linear')

        #--- Brows
        cmds.pointConstraint( self.l_brow_01_cnt, self.l_brow_01,mo=True )
        cmds.pointConstraint( self.l_brow_02_cnt, self.l_brow_02,mo=True )
        cmds.pointConstraint( self.l_brow_03_cnt, self.l_brow_03,mo=True )
        cmds.pointConstraint( self.r_brow_01_cnt, self.r_brow_01,mo=True )
        cmds.pointConstraint( self.r_brow_02_cnt, self.r_brow_02,mo=True )
        cmds.pointConstraint( self.r_brow_03_cnt, self.r_brow_03,mo=True )
        cmds.pointConstraint( self.mid_brow_cnt, self.mid_brow,mo=True )
        
        # Rotation SDKs
        cmds.connectAttr( '%s.rotate'%self.l_brow_01_cnt, '%s.rotate'%self.l_brow_01,f=True )
        cmds.connectAttr( '%s.rotate'%self.l_brow_02_cnt, '%s.rotate'%self.l_brow_02,f=True )
        cmds.connectAttr( '%s.rotate'%self.l_brow_03_cnt, '%s.rotate'%self.l_brow_03,f=True )
        cmds.connectAttr( '%s.rotate'%self.r_brow_01_cnt, '%s.rotate'%self.r_brow_01,f=True )
        cmds.connectAttr( '%s.rotate'%self.r_brow_02_cnt, '%s.rotate'%self.r_brow_02,f=True )
        cmds.connectAttr( '%s.rotate'%self.r_brow_03_cnt, '%s.rotate'%self.r_brow_03,f=True )
        cmds.connectAttr( '%s.rotate'%self.mid_brow_cnt, '%s.rotate'%self.mid_brow,f=True )
        
        #--- Mouth
        # Top lip
        cmds.pointConstraint( self.l_top_lip_cnt, self.l_top_lip,mo=True )
        cmds.pointConstraint( self.r_top_lip_cnt, self.r_top_lip,mo=True )
        cmds.pointConstraint( self.mid_top_lip_cnt, self.mid_top_lip,mo=True )
        
        cmds.connectAttr( '%s.rotate'%self.l_top_lip_cnt, '%s.rotate'%self.l_top_lip,f=True )
        cmds.connectAttr( '%s.rotate'%self.r_top_lip_cnt, '%s.rotate'%self.r_top_lip,f=True )
        cmds.connectAttr( '%s.rotate'%self.mid_top_lip_cnt, '%s.rotate'%self.mid_top_lip,f=True )
        
        # Bottom lip: Direct connect buffer groups to controls
        cmds.connectAttr(self.l_btm_lip_cnt+'.t', self.l_btm_lip + '_buffer_grp.t',f=True)
        cmds.connectAttr(self.l_btm_lip_cnt+'.r', self.l_btm_lip + '_buffer_grp.r',f=True)
        
        cmds.connectAttr(self.mid_btm_lip_cnt+'.t', self.mid_btm_lip + '_buffer_grp.t',f=True)
        cmds.connectAttr(self.mid_btm_lip_cnt+'.r', self.mid_btm_lip + '_buffer_grp.r',f=True)
        
        cmds.connectAttr(self.r_btm_lip_cnt+'.t', self.r_btm_lip + '_buffer_grp.t',f=True)
        cmds.connectAttr(self.r_btm_lip_cnt+'.r', self.r_btm_lip + '_buffer_grp.r',f=True)
        
        # Parent constrain top node of btm lip controls to jaw jnt
        cmds.parentConstraint( self.jaw,'btm_lip_jnts_grp', mo=True )
        
        # Corner: Point constraint to bottom, lower lip controls, weight favoring the upper controls
        #cmds.pointConstraint( self.jaw, self.sNames.headJoints['head'], 'mouth_corner_jnts_grp', mo=True, w=0.5 )
        
        # Direct connect the corner buffers to the cnts
        cmds.connectAttr(self.l_mouth_crnr_cnt+'.t', self.l_mouth_crnr + '_buffer_grp.t',f=True)
        cmds.connectAttr(self.l_mouth_crnr_cnt+'.r', self.l_mouth_crnr + '_buffer_grp.r',f=True)
        
        cmds.connectAttr(self.r_mouth_crnr_cnt+'.t', self.r_mouth_crnr + '_buffer_grp.t',f=True)
        cmds.connectAttr(self.r_mouth_crnr_cnt+'.r', self.r_mouth_crnr + '_buffer_grp.r',f=True)
        
        #--- Cheeks
        cmds.pointConstraint( self.l_cheek_cnt, self.l_cheek,mo=True )
        cmds.pointConstraint( self.r_cheek_cnt, self.r_cheek,mo=True )
        
        cmds.connectAttr( '%s.rotate'%self.l_cheek_cnt, '%s.rotate'%self.l_cheek,f=True )
        cmds.connectAttr( '%s.rotate'%self.r_cheek_cnt, '%s.rotate'%self.r_cheek,f=True )
        
        #--- Nose
        cmds.pointConstraint(self.nose_cnt, self.nose,mo=True )
        cmds.connectAttr( '%s.rotate'%self.nose_cnt, '%s.rotate'%self.nose,f=True )
        
        #--- Ears
        cmds.pointConstraint( self.l_ear_cnt, self.l_ear,mo=True )
        cmds.pointConstraint( self.r_ear_cnt, self.r_ear,mo=True )
        cmds.connectAttr( '%s.rotate'%self.l_ear_cnt, '%s.rotate'%self.l_ear,f=True )
        cmds.connectAttr( '%s.rotate'%self.r_ear_cnt, '%s.rotate'%self.r_ear,f=True )
        
        