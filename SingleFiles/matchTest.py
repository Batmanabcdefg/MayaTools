"""
   Author:     $Author: mauricio $
   Revised on: 	$Date: 2011-08-06 19:23:09 -0700 (Sat, 06 Aug 2011) $
   SVN Ver:    $Revision: 131 $
   File:       $HeadURL: file:///Users/mauricio/SVN_Repos/Maya_Tools/trunk/Tools/Rigging/General/matchTest.py $

    FK to the IK:
        Get IK chain rotations, set FK to those values
        
    IK to the FK:
        Get FK wrist worldSpace
        Get IK wrist worldSpace at zero (Offset)
        translateWrist = FKworldSpace - IK_Offset
    
        Get FK elbow worldSpace
        Get IK pv_cnt worldSPace at zero (Offset)
        translatePV = FKworldSpace - IK_Offset
"""

obj = mc.ls(sl=True,fl=True)
print obj

if 'l_' in obj[0]:
    state = mc.getAttr('l_hand_cnt.FK_IK')

    if state:
        # Left arm FK matching IK
        shoulder_ik_rotateX = mc.getAttr('l_arm_shldrJnt_ik.rotateX')
        shoulder_ik_rotateY = mc.getAttr('l_arm_shldrJnt_ik.rotateY')
        shoulder_ik_rotateZ = mc.getAttr('l_arm_shldrJnt_ik.rotateZ')

        elbow_ik_rotateX = mc.getAttr('l_arm_elbow1Jnt_ik.rotateX')
        elbow_ik_rotateY = mc.getAttr('l_arm_elbow1Jnt_ik.rotateY')
        elbow_ik_rotateZ = mc.getAttr('l_arm_elbow1Jnt_ik.rotateZ')

        wrist_ik_rotateX = mc.getAttr('l_arm_wristJnt_ik.rotateX')
        wrist_ik_rotateY = mc.getAttr('l_arm_wristJnt_ik.rotateY')
        wrist_ik_rotateZ = mc.getAttr('l_arm_wristJnt_ik.rotateZ')

        mc.setAttr('l_arm_shldrJnt_fk.rotateX',shoulder_ik_rotateX)
        mc.setAttr('l_arm_shldrJnt_fk.rotateY',shoulder_ik_rotateY)
        mc.setAttr('l_arm_shldrJnt_fk.rotateZ',shoulder_ik_rotateZ)

        mc.setAttr('l_arm_elbow1Jnt_fk.rotateX',elbow_ik_rotateX)
        mc.setAttr('l_arm_elbow1Jnt_fk.rotateY',elbow_ik_rotateY)
        mc.setAttr('l_arm_elbow1Jnt_fk.rotateZ',elbow_ik_rotateZ)

        mc.setAttr('l_arm_wristJnt_fk.rotateX',wrist_ik_rotateX)
        mc.setAttr('l_arm_wristJnt_fk.rotateY',wrist_ik_rotateY)
        mc.setAttr('l_arm_wristJnt_fk.rotateZ',wrist_ik_rotateZ)

        mc.setAttr('l_hand_cnt.FK_IK',0)

    else:
        #Left arm IK matching FK
        #Get wrist translates/rotates
        wristFK_translates = mc.xform('l_arm_wristJnt_fk',q=True, ws=True, t=True)

        wristFK_rotateX = mc.getAttr('l_arm_wristJnt_fk.rotateX')
        wristFK_rotateY = mc.getAttr('l_arm_wristJnt_fk.rotateY')
        wristFK_rotateZ = mc.getAttr('l_arm_wristJnt_fk.rotateZ')

        #Get elbow translates/rotates
        elbowFK_translates = mc.xform('l_arm_elbow1Jnt_fk',q=True, ws=True, t=True)

        #Snap wrist controller to fk wrist values l_arm_ikCnt
        mc.setAttr('l_arm_ikCnt.translateX',(wristFK_translates[0] - 56.77) )
        mc.setAttr('l_arm_ikCnt.translateY',(wristFK_translates[1] - 109.13) )
        mc.setAttr('l_arm_ikCnt.translateZ',(wristFK_translates[2] - 2.52) )

        mc.setAttr('l_arm_ikCnt.rotateX',wristFK_rotateX)
        mc.setAttr('l_arm_ikCnt.rotateY',wristFK_rotateY)
        mc.setAttr('l_arm_ikCnt.rotateZ',wristFK_rotateZ)

        #Snap ik pole vector to fk elbow
        mc.setAttr('l_arm_pv_cnt.translateX',elbowFK_translates[0])
        mc.setAttr('l_arm_pv_cnt.translateY',elbowFK_translates[1])
        mc.setAttr('l_arm_pv_cnt.translateZ',elbowFK_translates[2])

        mc.setAttr('l_hand_cnt.FK_IK',1)

if 'r_' in obj[0]:
    state = mc.getAttr('r_hand_cnt.FK_IK')

    if state:
        # Left arm FK matching IK
        shoulder_ik_rotateX = mc.getAttr('r_arm_shldrJnt_ik.rotateX')
        shoulder_ik_rotateY = mc.getAttr('r_arm_shldrJnt_ik.rotateY')
        shoulder_ik_rotateZ = mc.getAttr('r_arm_shldrJnt_ik.rotateZ')

        elbow_ik_rotateX = mc.getAttr('r_arm_elbow1Jnt_ik.rotateX')
        elbow_ik_rotateY = mc.getAttr('r_arm_elbow1Jnt_ik.rotateY')
        elbow_ik_rotateZ = mc.getAttr('r_arm_elbow1Jnt_ik.rotateZ')

        wrist_ik_rotateX = mc.getAttr('r_arm_wristJnt_ik.rotateX')
        wrist_ik_rotateY = mc.getAttr('r_arm_wristJnt_ik.rotateY')
        wrist_ik_rotateZ = mc.getAttr('r_arm_wristJnt_ik.rotateZ')

        mc.setAttr('r_arm_shldrJnt_fk.rotateX',shoulder_ik_rotateX)
        mc.setAttr('r_arm_shldrJnt_fk.rotateY',shoulder_ik_rotateY)
        mc.setAttr('r_arm_shldrJnt_fk.rotateZ',shoulder_ik_rotateZ)

        mc.setAttr('r_arm_elbow1Jnt_fk.rotateX',elbow_ik_rotateX)
        mc.setAttr('r_arm_elbow1Jnt_fk.rotateY',elbow_ik_rotateY)
        mc.setAttr('r_arm_elbow1Jnt_fk.rotateZ',elbow_ik_rotateZ)

        mc.setAttr('r_arm_wristJnt_fk.rotateX',wrist_ik_rotateX)
        mc.setAttr('r_arm_wristJnt_fk.rotateY',wrist_ik_rotateY)
        mc.setAttr('r_arm_wristJnt_fk.rotateZ',wrist_ik_rotateZ)

        mc.setAttr('r_hand_cnt.FK_IK',0)

    else:
        #Left arm IK matching FK
        #Get wrist translates/rotates
        wristFK_translates = mc.xform('r_arm_wristJnt_fk',q=True, ws=True, t=True)

        wristFK_rotateX = mc.getAttr('r_arm_wristJnt_fk.rotateX')
        wristFK_rotateY = mc.getAttr('r_arm_wristJnt_fk.rotateY')
        wristFK_rotateZ = mc.getAttr('r_arm_wristJnt_fk.rotateZ')

        #Get elbow translates/rotates
        elbowFK_translates = mc.xform('r_arm_elbow1Jnt_fk',q=True, ws=True, t=True)

        #Snap wrist controller to fk wrist values r_arm_ikCnt
        mc.setAttr('r_arm_ikCnt.translateX',(wristFK_translates[0] + 56.77) )
        mc.setAttr('r_arm_ikCnt.translateY',(wristFK_translates[1] - 109.13) )
        mc.setAttr('r_arm_ikCnt.translateZ',(wristFK_translates[2] - 2.52) )

        mc.setAttr('r_arm_ikCnt.rotateX',wristFK_rotateX)
        mc.setAttr('r_arm_ikCnt.rotateY',wristFK_rotateY)
        mc.setAttr('r_arm_ikCnt.rotateZ',wristFK_rotateZ)

        #Snap ik pole vector to fk elbow
        mc.setAttr('r_arm_pv_cnt.translateX',elbowFK_translates[0])
        mc.setAttr('r_arm_pv_cnt.translateY',elbowFK_translates[1])
        mc.setAttr('r_arm_pv_cnt.translateZ',elbowFK_translates[2])

        mc.setAttr('r_hand_cnt.FK_IK',1)