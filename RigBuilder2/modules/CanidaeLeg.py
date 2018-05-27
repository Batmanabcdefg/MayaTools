import os
import sys
import logging

import pymel.core as pm


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

#--- Logging
from pymel.tools import loggingControl
loggingControl.initMenu()
from pymel.internal.plogging import pymelLogger
pymelLogger.setLevel(logging.DEBUG)

def build( side=None ):
    pymelLogger.debug('Starting: build()...') 

    if side == None: raise Exception('Make sure side: %s is valid '%side) 

    if side == Names.prefixes['left']: LegJnts = Names.joints_leftLegNoRoll
    elif side == Names.prefixes['right']: LegJnts = Names.joints_rightLegNoRoll
    else: raise Exception('Make sure side: %s is valid '%side)

    listJnts = createJnts(LegJnts,side) # [listJnts]

    # create ik leg
    ikReturn = createIKLeg( listJnts, side ) # [pv_cnt, foot_cnt, ikh]
    pv_cnt = ikReturn[0]
    foot_cnt = ikReturn[1]
    ikh = ikReturn[2]
    
    # cleanUp
    cleanUp( listJnts, pv_cnt, foot_cnt )
    
    # connect to sh
    # list with the no rot toetoeBaseJnt = rList[0]
    #sourceJnts = listJnts[:-1]
    sourceJnts = listJnts
    #sourceJnts.append(toeBaseJnt[0])

    connectToSH( sourceJnts, LegJnts )
    
    # deselect selected to make sure that following module does not break
    pm.select(clear=1)
    
    pymelLogger.debug('End: build()...')

def connectToSH( listJnts, LegJnts ):
    
    pymelLogger.debug('Starting: connectToSH()...')
    
    for jntS,jntT in zip(listJnts,LegJnts):
        try: pm.parentConstraint( jntS, jntT, mo=1 )
        except: print 'Could not constraint: ' + jntS,jntT
        
    pymelLogger.debug('End: connectToSH()...')
    

def createJnts( LegJnts, side ):
   
    pymelLogger.debug('Starting: createJnts()...') 
    
    # duplicate joints
    listJnts = []
    print LegJnts
    for jnt in LegJnts:
        pm.select(clear=1)
        newJnt = pm.duplicate(jnt,rr=True,po=True, name=jnt+'_'+Names.suffixes['ik'])[0]
        try:
            newJnt.setParent(world=1)
        except: pass 
        listJnts.append(newJnt)
    print listJnts
    # parent joints  
    listJnts.reverse()
    index = 0
    for jnt in listJnts:
        if index+1 == len(listJnts): break
        jnt.setParent(listJnts[index+1])
        index = index + 1
        
    listJnts.reverse()

    # joints for inverse foot
    ankleFloorJnt = '%s%s' %(side,'AnkleFloor_if')
    # duplicate only joints ww for inverse foot
    pm.select(clear=1)
    toeBaseWW = listJnts[-3]
    invfootname = str(toeBaseWW).replace('_'+Names.suffixes['ik'], '_inversefoot')
    invfootjnt = pm.duplicate( toeBaseWW, name=invfootname )[0]
    invfootjnt.setParent(w=1)
    index = 1
    invjntlist = invfootjnt.listRelatives(ad=1)
    invjntlist.reverse()
    for jnt in invjntlist:
        jnt.rename(invfootname+str(index))
        jnt.setParent(w=1)
        index += 1
    invjntlist.reverse()
    invjntlist.append(invfootjnt)
    invjntlist.reverse()
    
    index = 0
    for jnt in invjntlist:
        if index+1 == len(invjntlist): break
        jnt.setParent(invjntlist[index+1])
        index = index + 1
        
    # make them child of the Ankle floor jnt
    invjntlist[-1].setParent(ankleFloorJnt)
    

    pm.select(clear=1)
    pymelLogger.debug('End: createJnts()...') 
    print listJnts
    return listJnts

def getSideColor(side=None):
    
    if side == Names.prefixes['left']: crv_color='red'
    elif side == Names.prefixes['right']: crv_color='midBlue'
    else: crv_color='white'
    return crv_color
        
    
def createIKLeg( listJnts, side ):
    
    toeBaseJnt = listJnts[-3]

    # create ik handle
    ikh = pm.ikHandle( sj=listJnts[0], ee=toeBaseJnt, sol='ikRPsolver', name=toeBaseJnt + '_' +Names.suffixes['ikhandle'] )
    ikh[0].hide()
    
    # create ik sc solvers for foot and toe
    ikhfoot = pm.ikHandle( sj=toeBaseJnt, ee=listJnts[-2], sol='ikSCsolver', name=listJnts[-2] + '_' +Names.suffixes['ikhandle'] )
    ikhfoot[0].hide()
    ikhtoe = pm.ikHandle( sj=listJnts[-2], ee=listJnts[-1], sol='ikSCsolver', name=listJnts[-1] + '_' +Names.suffixes['ikhandle'] )
    ikhtoe[0].hide()
    
    # parent ik handles to inverse foot
    inverseFoot = str(toeBaseJnt.name()) 
    inverseFoot = pm.ls( inverseFoot.replace('_'+Names.suffixes['ik'], '_inversefoot'),r=1 )[0]
    
    inverseToe = pm.ls(str(inverseFoot.name())+'1',r=1)[0]
    inverseToeEnd = pm.ls(str(inverseFoot.name()+'2'),r=1)[0]

    # create offset for toe roll
    offsetGrp = pm.group(em=1,name=str(inverseToeEnd.name()) + '_offsetGrpA')
    offsetGrpB = pm.group(em=1,name=str(inverseToeEnd.name()) + '_offsetGrpB')
    offsetGrp.setParent( inverseToe )
    offsetGrp.setTranslation([0,0,0])
    offsetGrp.setRotation([0,0,0])
    offsetGrp.setParent(w=1)
    offsetGrpB.setParent(offsetGrp)
    offsetGrpB.setTranslation([0,0,0])
    offsetGrpB.setRotation([0,0,0])
    
    
    ikh[0].setParent(inverseFoot)
    ikhfoot[0].setParent(inverseToe)
    
    ikhtoe[0].setParent(offsetGrpB)
    offsetGrp.setParent(inverseToeEnd)
    
    
    
    # create curve for ik foot
    if side == Names.prefixes['left']: ctrl = Names.controls_leftLegIK
    elif side ==Names.prefixes['right']: ctrl = Names.controls_rightLegIK
    else: raise Exception('Make sure side: %s is valid '%side)
    
    
    posjnt = pm.xform(toeBaseJnt, query = True, translation = True, ws=1)
    rotjnt = pm.xform(toeBaseJnt, query = True, ro = True, ws=1)
 
    foot_cnt = Control.create( name=ctrl, offsets=1, shape='circle_01', 
                    size=1.5, color=getSideColor(side), 
                    pos=posjnt,rot=rotjnt, parent=None, typ='body' )
    
    
    ############ fix this! need to rotate 180 to make sure that ctrl behaves properly
    if side == Names.prefixes['right']:
        pm.rotate(foot_cnt,0,0,180,os=1, r=1)
       
    ankleFloorJnt = pm.ls('%s%s' %(side,'AnkleFloor_if'),r=1  )[0]
    foot_ctrl = foot_cnt.listRelatives(ad=1)[0].getParent()
    ankleFloorJnt.setParent( foot_ctrl )
    ankleFloorJnt.hide()
    
    # add attr to foot control
    pm.addAttr(foot_ctrl, longName='heel_roll',k=True)
    pm.addAttr(foot_ctrl, longName='toe_roll',k=True)
    pm.addAttr(foot_ctrl, longName='toeEnd_roll',k=True)
    pm.addAttr(foot_ctrl, longName='toe_up_down',k=True)
    
    # connect attrs
    pm.connectAttr( foot_ctrl + '.' + 'heel_roll', ankleFloorJnt + '.' + 'rotateZ' )
    pm.connectAttr( foot_ctrl + '.' + 'toe_roll', inverseToe + '.' + 'rotateZ' )
    pm.connectAttr( foot_ctrl + '.' + 'toeEnd_roll', inverseToeEnd + '.' + 'rotateZ' )
    pm.connectAttr( foot_ctrl + '.' + 'toe_up_down', offsetGrpB + '.' + 'rotateZ' )
    
    
    
    #####################
    # create pole vector
    if side == Names.prefixes['left']: ctrl = Names.controls_leftLegIKPV
    elif side ==Names.prefixes['right']: ctrl = Names.controls_rightLegIKPV
    else: raise Exception('Make sure side: %s is valid '%side)
    
    pv_cnt = Control.create( name=ctrl, offsets=1, shape='cube', 
                    size=0.4, color=getSideColor(side), 
                    pos=None, parent=None, typ='body' )
    
    # parent constraint w/o offsets to UpLeg, Leg
    cons = pm.parentConstraint( listJnts[0], listJnts[1],listJnts[2], pv_cnt, mo=0 )
    pm.delete(cons)
    # aim contraint to leg
    cons = pm.aimConstraint( listJnts[1], pv_cnt,mo=0 )
    pm.move( pv_cnt, 10,0,0, os=1,r=1)
    pm.delete(cons)
    
    # connect pole vector
    pm.poleVectorConstraint( pv_cnt.getChildren()[0], ikh[0] )
    ####################
    
    rList = [pv_cnt, foot_cnt, ikh]
    return rList

def cleanUp( listJnts, pv_cnt, foot_cnt ):
    
    cog_space = pm.ls('cog_ctrl_space',r=1)[0]
    cogPos = pm.xform(cog_space, q=1,ws=1,rp=1)
        
    # parent legs to legs group
    if not pm.objExists( Names.legs_grp ):
        legs_grp = pm.group( em=1, name=Names.legs_grp )
        legs_grp.setTranslation(cogPos)
        # contraint to hips # hard coded we should get it from  the character node
        pm.parentConstraint('Hips_ctrl', legs_grp, mo=1)
    else: legs_grp = pm.ls( Names.legs_grp )
    
    listJnts[0].setParent(legs_grp)
    
    # group other nodes
    if not pm.objExists( Names.legs_ikgrp ):
        other_grp = pm.group(em=1, name= Names.legs_ikgrp )
    else: other_grp = pm.ls( Names.legs_ikgrp )
    pv_cnt.setParent(other_grp)
    foot_cnt.setParent(other_grp)
    
    # parent all to module grp
    if not pm.objExists( Names.legs_module ):
        legs_mod = pm.group( em=1, name= Names.legs_module )
        
        #legs_mod.setTranslation(cogPos)
        pm.parent(other_grp,legs_mod)
        pm.parent(legs_grp,legs_mod)
        # parent to modules
        legs_mod.setParent( Names.modules_grp )
    
    
   
    
    

    
    
    
    
    
    
    
            
    
           