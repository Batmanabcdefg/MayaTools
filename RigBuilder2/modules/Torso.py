import os,sys
import pymel.core as pm
import logging
import maya.cmds as cmds

#--- Add cwd and lib
cwd = os.path.dirname(os.path.abspath(__file__))
lib = cwd.replace('modules','library')
if cwd not in sys.path:
    sys.path.append(cwd)
if lib not in sys.path:
    sys.path.append(lib)
    
import Names
reload( Names )
import Control
reload( Control )
import RegisterControl
reload( RegisterControl )

#--- Logging
from pymel.tools import loggingControl
loggingControl.initMenu()
from pymel.internal.plogging import pymelLogger
pymelLogger.setLevel(logging.DEBUG)

def build():
    pymelLogger.debug('Starting: build()...') 
    
    # createJnts
    jntList = createJnts( Names.joints_torso_ww )
    
    
    # CreateIKSpline
    
    ikSObjList = createIKSpline( jntList ) #[ikHandleTorso(pm), drvStart, drvEnd ]
 
    ikHandleTorso = ikSObjList[0]
    drvStart = ikSObjList[1]
    drvEnd = ikSObjList[2]
    
    
    # StretchyBack
    stryBackObjList = stretchyBack( ikHandleTorso, jntList ) # [curveInfoNodeBack,MDCurveBack]
    curveInfoNodeBack = stryBackObjList[0]
    MDCurveBack = stryBackObjList[1]
    
    # Volume Conservation
    vcExprList = volumeConservation(ikHandleTorso, curveInfoNodeBack, jntList, 1)# [expr, expressionNode]
    expr = vcExprList[0]
    expressionNode = vcExprList[1]
    
    # Advanced Twist
    advancedTwist( ikHandleTorso, drvStart, drvEnd )
    
    # Hip Shouders Controls
    scOBjList = createHipShoudersControls( drvStart, drvEnd, Names.joints_torso_ww )  # [hips_cnt, shoulder_cnt]
    hips_cnt = scOBjList[0]
    shoulder_cnt = scOBjList[1]
     
    # createFKControls( jntList )
    fkJnts = createFKControls( Names.joints_torso_ww )
   
    # body Ctrl SetUp 
    body_cnt_offset = bodyCtrlSetUp( fkJnts, hips_cnt, shoulder_cnt, drvStart ) # body_cnt_offset
   
    # Clean Outliner
    characterNode = cleanOutliner( jntList, drvStart, drvEnd, body_cnt_offset, ikHandleTorso) 
    
    # complete stretchy setup (global scale)
    completeStretchySetup( expr, expressionNode, characterNode, curveInfoNodeBack ) 

    # parentToControlsGrp
    parentToControlsGrp( characterNode )
    
    # connecting to single hierarchy
    spines = jntList[1:-1]
    source_jnts = []
    source_jnts.append(Names.joints_torso_ww[0] + '_' + Names.suffixes['control'])
    for sp in spines:
        source_jnts.append(sp)
    source_jnts.append(drvEnd)

    connectToSH( source_jnts, Names.joints_torso_ww )
    
    # deselect selected to make sure that following module does not break
    pm.select(clear=1)
    
    pymelLogger.debug('End: build()...')

def connectToSH( source_jnts, torso_jnts  ):
    
    pymelLogger.debug('Starting: connectToSH()...')
    
    for jntS,jntT in zip(source_jnts,torso_jnts):
        try: pm.parentConstraint( jntS, jntT, mo=1 )
        except: print 'Could not constraint: ' + jntS,jntT
        
    pymelLogger.debug('End: connectToSH()...')
        
    
       
    
def setRotateOrder(object, value=2):
    pm.setAttr(object + '.rotateOrder', value)
        
def hideLockAttr(object, values=[]):
    for val in values:
        pm.setAttr(object + val, lock = True, keyable = False, channelBox = False)

# use this as constants
lockHideTRSV = ['.tx','.ty','.tz','.rx','.ry','.rz','.sx','.sy','.sz','.v']
lockHideTSV = ['.tx','.ty','.tz','.sx','.sy','.sz','.v']
lockHideSV = ['.sx','.sy','.sz','.v']
lockHideS = ['.sx','.sy','.sz']
lockHideXZ = ['.sx','.sz'] 
      
def createJnts( torso_jnts ):
    pymelLogger.debug('Starting: createJnts()...') 

    listJnts = []
    for jnt in torso_jnts:
        pm.select(clear=1)
        newJnt = pm.duplicate(jnt,rr=True,po=True, name=jnt+'_'+Names.suffixes['ik'])[0]
        newJnt.setParent(world=1)
        listJnts.append(newJnt)
       
    listJnts.reverse()
    index = 0
    for jnt in listJnts:
        if index+1 == len(listJnts): break
        jnt.setParent(listJnts[index+1])
        index = index + 1
        
    listJnts.reverse()

    pymelLogger.debug('End: createJnts()...') 
    return listJnts
     
    
def createIKSpline( jntList ):
    pymelLogger.debug('Starting: createIKSpline()...') 
    # Make IK Spline
    ikHandleTorso = pm.ikHandle( startJoint=jntList[0], endEffector=jntList[-1], solver = 'ikSplineSolver', numSpans = 4, name = jntList[-1]+'_'+Names.suffixes['ikhandle'])
    # we should probably rename the object created to know names ......    
    # CAREFULL // inherits Transform OFF, to avoid double transformation when grouped later on
    pm.setAttr(ikHandleTorso[2] + '.inheritsTransform', 0)
    
    # Duplicate last and first joint to use as Drivers of the spine Ik curve
    print jntList
    drvStart = pm.duplicate(jntList[0], parentOnly=True, name = Names.prefixes['driver']+'_'+ jntList[0] +'_'+Names.suffixes['start'])
    drvEnd = pm.duplicate(jntList[-1], parentOnly=True, name = Names.prefixes['driver']+'_'+ jntList[-1] +'_'+Names.suffixes['end'])
    pm.parent(drvEnd, w=1)
    
    # Make radius bigger
    pm.joint(drvStart, edit = True, radius = 1)
    pm.joint(drvEnd, edit = True, radius = 1)
    
    # Skin hip/shldr jnt's to back curve
    pm.skinCluster(drvStart,drvEnd,ikHandleTorso[2],dr=4)
    
    # return nedded elements
    rList = [ikHandleTorso, drvStart, drvEnd ]
    
    pymelLogger.debug('End: createIKSpline()...') 
    return rList
    

def stretchyBack( ikHandleTorso, jntList ):
    pymelLogger.debug('Starting: stretchyBack()...')     
    #Stretchy process
    # ArcLen to create curveInfo
    curveInfoNodeBack = pm.arclen( ikHandleTorso[2], ch=True )
    # add attr to curveinfo Node (normalizedScale)
    # this will have a value coming from a multiply divide node that will be 
    # dividing the current length by the initial length of the curve
    # this will be used later to scale the joints
    pm.addAttr(curveInfoNodeBack, longName='normalizedScale', attributeType='double')
    # get initial length of the curve
    iniLen = pm.getAttr( curveInfoNodeBack + '.arcLength' )
    
    # create a node multiplydivide, operation set to division
    MDCurveBack = pm.shadingNode( 'multiplyDivide', asUtility=True )
    pm.setAttr( MDCurveBack+'.operation', 2 ) # divide
    
    # Connect curve arcLength to input1X
    pm.connectAttr( curveInfoNodeBack + '.arcLength', MDCurveBack + '.input1X', force=True )
    # Set input2X to initial length of the curve
    pm.setAttr(MDCurveBack+'.input2X', iniLen)
    # connect outpux x from multiplydivide to normalized scale of the curve info
    pm.connectAttr(MDCurveBack + '.outputX', curveInfoNodeBack + '.normalizedScale', force=True)
    
    returnList = [curveInfoNodeBack,MDCurveBack]
    
    
    pymelLogger.debug('End: stretchyBack()...')   
    return returnList
    

def volumeConservation( ikHandleTorso, curveInfoNodeBack, jntList, opt = 1 ):
    pymelLogger.debug('Starting: volumeConservation()...')   
    # for now volumeConservation inclues yes and no
    # List with all joints
    endJnt = len(jntList)-1
    jntToScale = jntList[:-1]

    
    if opt == 0:
        # Connect output x of the multiplydivide node to the x scale of the joint 
        # (or the axis that goes down the joint)
        # Do not connect the end joint  
        for jnt in jntToScale:
            pm.connectAttr( curveInfoNodeBack + '.normalizedScale', jnt + '.scaleX')
            
    else: # if volume  
        # following jasons techniques
        # we will create a anim curve that will be used to determine
        # the scaling power of the joints
        
        # Add Attr to curve (scalePower) this will let us control the curve
        pm.addAttr(ikHandleTorso[2], longName='scalePower', attributeType='double')
        # Make it keyable
        pm.setAttr(ikHandleTorso[2] + '.scalePower', keyable = True)
        
        # Get total number of joints to scale
        # this will be the range we will have to keyframe
        # we will put keyframe on 1 and another at X (depending on how many joints are created)
        numOfJnts = len(jntToScale)
        # Set the two keyframes
        
        pm.setKeyframe(ikHandleTorso[2], attribute = 'scalePower', time = 1, value = 0)
        pm.setKeyframe(ikHandleTorso[2], attribute = 'scalePower', time = numOfJnts, value = 0)
        # We configure the shape of the animation curve
        # weightingtangents and setting an out and in angle
        pm.keyTangent(ikHandleTorso[2], weightedTangents=True, weightLock = False, attribute = 'scalePower') 
        pm.keyTangent(ikHandleTorso[2], edit=True, absolute = True, time=(1,numOfJnts), outAngle=50, attribute = 'scalePower')
        pm.keyTangent(ikHandleTorso[2], edit=True, absolute = True, time=(numOfJnts,numOfJnts), inAngle=-50, attribute = 'scalePower')
        
        
        # Creating a frameCache for each joint to be scaled
        # Connecting scalePower to each frameCache Stream
        fCount = 1
        for jnt in jntToScale:
            
            frameC = pm.createNode('frameCache', name = jnt + '_'+Names.suffixes['frameCache']) 
            
            pm.connectAttr(ikHandleTorso[2] + '.scalePower', frameC + '.stream')
            
            # set frame number
            pm.setAttr(frameC+'.vt', fCount)
            fCount += 1
            
            # Create Attr Pow for each joint
            powJnt = pm.addAttr(jnt, longName='pow', attributeType='double')
           
            pm.setAttr(jnt + '.pow', keyable = True)
            
            # Connect Attr varying to jnt.pow
            pm.connectAttr(frameC + '.v', jnt + '.pow', force=True)
        
      
        
        # Writing the expression to apply the scale
        expr = '$scale = ' + curveInfoNodeBack + '.normalizedScale;\n'
        # inv scale
        expr += '$sqrt =  1/sqrt($scale);\n'
        for jnt in jntToScale:
            # x joint scale
            expr += jnt+'.scaleX = $scale;\n'
            expr += jnt+'.scaleY = pow($sqrt,'+jnt+'.pow);\n'
            expr += jnt+'.scaleZ = pow($sqrt,'+jnt+'.pow);\n'
        
        # Create expression
        expressionNode = pm.expression(string=expr, name=ikHandleTorso[2]+'_'+Names.suffixes['expression'])
    
    rList = [expr, expressionNode]
    return rList
    pymelLogger.debug('End: volumeConservation()...')   
               
   

def advancedTwist( ikHandleTorso, drvStart, drvEnd ):  
    
    pymelLogger.debug('Starting: advancedTwist()...')   
    
    # Enable Twist Controls
    pm.setAttr(ikHandleTorso[0] + '.dTwistControlEnable',1)
    # Set World Up Type to Object Rotation Up(Start/End) 
    pm.setAttr(ikHandleTorso[0] + '.dWorldUpType',4)
    # Set Up Axis to Positive Y (This will depend on the bones orientation)
    pm.setAttr(ikHandleTorso[0] + '.dWorldUpAxis',0)
    # Set Up Vector to 0 1 0  (Y) changing to Z evaluate behaviour
    pm.setAttr(ikHandleTorso[0] + '.dWorldUpVectorZ',1)
    pm.setAttr(ikHandleTorso[0] + '.dWorldUpVectorY',0)
    # Set Up Vector 2 to 0 1 0  (Y) changing to Z evaluate behaviour
    pm.setAttr(ikHandleTorso[0] + '.dWorldUpVectorEndZ',1)
    pm.setAttr(ikHandleTorso[0] + '.dWorldUpVectorEndY',0)
    # Set World Up Object (Start/Root)
    pm.connectAttr( drvStart[0] + '.worldMatrix[0]', ikHandleTorso[0] + '.dWorldUpMatrix')
    # Set World Up Object 2 (End)
    pm.connectAttr(drvEnd[0] + '.worldMatrix[0]', ikHandleTorso[0] + '.dWorldUpMatrixEnd' )

    pymelLogger.debug('End: advancedTwist()...')
   
    
def createHipShoudersControls( drvStart, drvEnd, jntList ):    
   
    pymelLogger.debug('Starting: createHipShoudersControls()...')
    
    # Get drvStart Position
    drvS_pos = pm.xform(drvStart[0], query = True, translation = True)
    # Get drvEnd Position
    drvE_pos = pm.xform(drvEnd[0], query = True, translation = True)
    
    # Create Hip Control
    
    ctrl = jntList[0] + '_' + Names.suffixes['control']
    rot = pm.xform(drvStart[0],q=1,ws=1,ro=1)
    rot = [-90,0,90]

    hips_cnt = Control.create( name= ctrl  , offsets=2, shape='cube', 
                    size=[1,1,1], color='cyan', 
                    pos=drvS_pos, rot=rot, parent=None, typ='body' )
 
    # Create Shoulder Ctrl
    #shoulder_cnt = Control.create()
    ######## fix this !!! top spine ctrl shoud b called SpineX_ctrl
    ctrl = jntList[-1]+ '_' + Names.suffixes['control']
    rot = pm.xform(jntList[-1],ws=1,q=1,ro=1)

    shoulder_cnt = Control.create( name=ctrl, offsets=2, shape='circle_01', 
                    size=2, color='red', 
                    pos=drvE_pos,rot=rot, parent=None, typ='body' ) 

    # Connect CC to Drv Jnts
    pm.parentConstraint(hips_cnt.listRelatives(ad=1)[0].getParent(), drvStart, maintainOffset = True)
    pm.parentConstraint(shoulder_cnt.listRelatives(ad=1)[0].getParent(), drvEnd, maintainOffset = True)

    # Clean Ctrls Attributes (Lock and Hide Scale and Visibility)

    hideLockAttr(hips_cnt, lockHideSV)
    hideLockAttr(shoulder_cnt, lockHideSV)
    hideLockAttr(drvStart[0], lockHideS)
    hideLockAttr(drvEnd[0], lockHideS)  
    
    rList = [hips_cnt, shoulder_cnt]
    
    pymelLogger.debug('End: createHipShoudersControls()...')
    return rList

def createFKControls( jntList ):
    
    pymelLogger.debug('Starting: createFKControls()...')
    
    # for now creating based on current spline and same number
    # will not be oriented to the joint but world (analyze this!!)


    listJnts = []
    for jnt in jntList:
        pm.select(clear=1)
        newJnt = pm.duplicate(jnt,rr=True,po=True, name=jnt+'_'+Names.suffixes['fk'])[0]
        try:
            newJnt.setParent(world=1)
        except: pass 
        listJnts.append(newJnt)
       
    listJnts.reverse()
    index = 0
    for jnt in listJnts:
        if index+1 == len(listJnts): break
        jnt.setParent(listJnts[index+1])
        index = index + 1
        
    listJnts.reverse()

    # Create controls for the fk spines
    fkSpines = listJnts[1:-1]
    # parent shape to joint
    #cc_torso01 = jcControl.circleControl('cc_'+torso01)
    offsetList = []
    for fkJnt in fkSpines:
  
        jPos = pm.xform(fkJnt, query = True, translation = True, ws=1)
        rot = pm.xform(fkJnt, query = True, ro = True, ws=1)

        cName = fkJnt.split('_')[0] + '_' + Names.suffixes['control']
        #rot = pm.xform(fkJnt.replace( '_' + Names.suffixes['fk'], '' ),ws=1,q=1,ro=1)
        offsetGrp = Control.create( name=cName, offsets=2, shape='circle_01', 
                        size=1.8, color='yellow', 
                        pos=jPos, parent=None,rot=rot, typ='body' ) 
     
        offsetList.append(offsetGrp)
        
        # parent constraint
        print offsetGrp.listRelatives(ad=1)[0].getParent()
        pm.parentConstraint( offsetGrp.listRelatives(ad=1)[0].getParent(), fkJnt, mo=1 )
        

    # parent offset grps
    topGrp = offsetList[0]
    if not len(offsetList) == 0:
        # parent groups
        offsetList.reverse()
        last = ''
        for offsetgrp in offsetList:
            if last:
                last.setParent(offsetgrp.listRelatives(ad=1)[0].getParent())
            last = offsetgrp 
        # parent top to hips_fk jnt
        topGrp.setParent(listJnts[0])
    
   
    
    # hide chain
    """
    for fkjnt in fkJntList:
        pm.hide(fkjnt)
    """
    
    
    pymelLogger.debug('End: createFKControls()...')
    return listJnts
    
    
    
  
def bodyCtrlSetUp( fkJnts, hips_cnt, shoulder_cnt, drvStart ): 
    
    pymelLogger.debug('Starting: bodyCtrlSetUp()...')  
    
    # Body control 

    
    pos = pm.xform(hips_cnt, q=1, ws=1,rp=1)
    body_cnt_offset = Control.create( name= Names.controls_torso_cog , offsets=1, shape='circle_2_arrow', 
                size=[1,1,1], color='darkBlue', 
                pos=pos, parent=None, typ='body' )
                
    body_cnt = body_cnt_offset.listRelatives(ad=1)[0].getParent()
    
    # position and freeze 
    #rootPos = pm.xform(drvStart[0], query = True, translation = True)
    #body_cnt.setTranslation(rootPos)
    #pm.makeIdentity(body_cnt, apply=True)
    # Change rotation order cc_body
    #setRotateOrder(body_cnt, 2)
    # Lock and Hide Scale - Vis
    hideLockAttr(body_cnt, lockHideSV)
    
    
    # Parent torso_baseJnt to cc_body (CAREFUL!!!  If no FKControls created this will not work now!!!!)
    pm.parent(fkJnts[0], body_cnt)

    # Group cc_jc_hip and parent it to torso_baseJnt (We group it first to keep de cc zeroed out)
    grp_cc_hip = pm.group(hips_cnt, name= Names.torso_hips_grp )
    pm.parent(grp_cc_hip, fkJnts[0])
    
    # Group cc_jc_shoulder and parent it to torso_endJnt (We group it first to keep de cc zeroed out)
    grp_cc_shoulder = pm.group(shoulder_cnt, name=Names.torso_shoulders_grp )
    pm.parent(grp_cc_shoulder, fkJnts[-1])
    
    # Lock and Hide Attr groups created
    hideLockAttr(grp_cc_hip, lockHideTRSV)
    hideLockAttr(grp_cc_shoulder, lockHideTRSV)
    
    pymelLogger.debug('End: bodyCtrlSetUp()...')  
    
    return body_cnt_offset
        
def cleanOutliner( jntList,drvStart,drvEnd, body_cnt_offset, ikHandleTorso ):
    
    
    pymelLogger.debug('Starting: cleanOutliner()...')  
    # Clean Outline, grouping things ...
    # Grup cc_body (this has all the controls the animator will use)
    grp_cc_body_anim = pm.group(em=True, name = Names.torso_anim_controls)
    pm.parent(body_cnt_offset, grp_cc_body_anim)
    
    # Group Driver Joints, back joints (the one used for the IK), ikHandle, backCurve
    # first backIK joint jntList[0], drvStart, drvEnd, ikHandleBack, ikCurveBack
    noTouchGrp = pm.group(em=True, name = Names.torso_notouch)
    pm.parent(jntList[0],drvStart[0],drvEnd[0],ikHandleTorso[0],ikHandleTorso[2],noTouchGrp)
    #pm.group(jntList[0],drvStart,drvEnd,ikHandleBack[0],ikCurveBack, relative=True)


    # Create group for grp_cc_body_anim and noTouchGrp
    characterNode = pm.group(em=True, name = Names.torso_module)
    pm.parent(grp_cc_body_anim, characterNode)
    pm.parent(noTouchGrp, characterNode)   
    
    pymelLogger.debug('End: cleanOutliner()...') 
    return characterNode
    
def completeStretchySetup( expr, expressionNode, characterNode, curveInfoNodeBack ):
    
    pymelLogger.debug('Starting: completeStretchySetup()...') 
    # if stretchy back is selected
    # When scaling characterNode character breaks
    # because the backcurve is also scaling
    # applying two time scale
    # we need to edit ikcurve expression and change the scale to
    # $scale = (curveinfoName).normalizedScale/(characterNode).scaleY;
    
    endFirstLineExpr = expr.find('\n')
    slicedExpr = expr[endFirstLineExpr:]

   
    # Edit first line and add the old expression sliced
    newExpr = '$scale = ' + curveInfoNodeBack + '.normalizedScale/' + characterNode + '.scaleY;\n'
    newExpr += slicedExpr
    pm.expression(expressionNode, edit = True, string=newExpr)
    
    
    
    # To avoid scaling uniformally in x and z 
    # the scale Y attr will drive X and Z
    pm.connectAttr(characterNode+'.scaleY', characterNode+'.scaleX')
    pm.connectAttr(characterNode+'.scaleY', characterNode+'.scaleZ')
    
    # Now we can lock and hide scale X and Z
    hideLockAttr(characterNode, lockHideXZ)
    
    # Change attr name of Scale Y to name = globalScale
    # it allows us to still use the scale manipulator
    # instead of adding a new attr for that
    pm.aliasAttr('globalScale', characterNode + '.scaleY')
    
    pymelLogger.debug('End: completeStretchySetup()...') 
    
def parentToControlsGrp( characterNode ): 
    pymelLogger.debug('Starting: parentToControlsGrp()...') 
    
    pm.parent( characterNode, Names.modules_grp ) 
    
    pymelLogger.debug('End: parentToControlsGrp()...') 
      