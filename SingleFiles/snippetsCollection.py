"""
Collection of useful snipettes
"""


'''
Grab multiple meshes to select their influences, and skin the last selected item to them.
Used for combine geo task
'''
import pymel.core as pm

def getInfs(obj=None):
    infs = []
    sc = mel.eval('findRelatedSkinCluster("%s");'%obj.name())
    if sc:
        infs.append(cmds.skinCluster(sc,q=True,inf=True))
    return infs

sel = pm.ls(sl=1, type='transform')
infs = []
for obj in sel[:-1]:
    pm.select(clear=1)
    temp = []
    temp = getInfs(obj=obj)
    for inf in temp:	
        infs.append(inf)

pm.select(infs, r=1)
pm.select(sel[-1], add=1)
pm.skinCluster(tsb=1)

# Select vertex from one mesh, toggle select the same one on target mesh.
import pymel.core as pm
targetMesh = 'lf_shldrTwistBack_neg_x90_inverted'
sel = pm.ls(sl=1)
pm.select(clear=1)
for each in sel:
    pm.select(targetMesh + "." + each.split('.')[1], add=True)


# Print all edges connected to selected rivets
sel = pm.ls(sl=1)
for each in sel:
    for edge in each.inputs()[0].inputs()[0].inputs():
        print '"%s"' % edge

# Order selected. Selected must have common parent node
import sys
import pymel.core as pm

sel = pm.ls(sl=1)
sel.sort()
for each in sel:
    prnt = pm.listRelatives(each, parent=1)[0]
    pm.parent(each,w=1)
    pm.parent(each, prnt)

# Creat SDK and FK joint at selected objects
import sys
import pymel.core as pm

sel = pm.ls(sl=1)
name = 'lf_Fang'
n = 1
for each in sel:
    pm.select(clear=1)
    jntSDK = pm.joint(n=name+'_sdkJnt_%s' % n)
    pm.delete(pm.pointConstraint(each, jntSDK, mo=0))
    jnt = pm.joint(n=name+'_fkJnt_%s' % n)
    n += 1


# Create joint/constrain to selected vertices
import pymel.core as pm
verts = pm.ls(sl=1,fl=1)
prefix = 'GillJnt'
n = 1
for vert in verts:
    loc = pm.spaceLocator()
    pm.select(clear=1)
    p = []
    p=pm.xform(vert,q=1,ws=1,t=1)
    jnt = pm.joint(name=prefix+'_%s' % n, p=p)
    loc.translate.set(p)
    pm.delete(pm.pointConstraint(loc,jnt,mo=0))
    pm.select(vert, jnt, r=1)
    pm.mel.eval('doCreatePointOnPolyConstraintArgList 2 {   "0" ,"0" ,"0" ,"1" ,"" ,"1" ,"0" ,"0" ,"0" ,"0" };')
    pm.delete(loc)
    n += 1

# Get edges for selected rivets
sel = pm.ls(sl=1)
count = 0
for each in sel:
    print '[',
    for edgeNode in each.inputs()[0].inputs()[0].inputs():
        pm.select(edgeNode, r=1)
        edge =  pm.getAttr(edgeNode.edgeIndex[0])
        print '"body.e[%s]",' % edge,
        count += 1
    if not count % 2:
        print '],'


# Make a controller for each selected
path = '/Users/mauricio/GoogleDrive/MayaTools'
import sys
import pymel.core as pm
if path not in sys.path:
    sys.path.append(path)
from MakeController import MakeController

sel = pm.ls(sl=1)
name = 'Fang'
n = 1
for each in sel:
    MakeController.make(jnt=each,
                        name=name+'_%s_' % n,
                        offsets=2,
                        hi=True,
                        suffix='_ctrl')
    n += 1

# Select two end joints,
# Creates mid joint.
# Constrains mid joint to follow and aim at second end joint.
# Adjust move direction as needed

import pymel.core as pm

sel = pm.ls(sl=1)

a = sel[0]
b = sel[1]
pm.select(clear=1)
# Create joint
jnt = pm.joint(n=a.name()+'_btween_jnt')
pm.delete(pm.parentConstraint(a, b, jnt, mo=0))

# Setup up locator
loc = pm.spaceLocator(name='%s_upLoc' % a)
pm.delete(pm.pointConstraint(b, loc, mo=0))
# Adjust placement of Up object here
pm.move(20, loc, moveY=1)
pm.parent(loc, b)

# Constrain joint
pm.pointConstraint(a, b, jnt, mo=1)
pm.aimConstraint(b, jnt, wut='object', wuo=loc.name(), mo=1)


#----------------------------------------------------------------
# Sum two attrs and connect result to attribute
import pymel.core as pm

def sumAttr(sumCtrl=None,
            ctrlAttrA=None, ctrlAttrB=None,
            ctrlAttrResult=None,
            scaleA=None, scaleB=None):

    pmaNode = pm.shadingNode('plusMinusAverage',n='%s_Sum'%sumCtrl, asUtility=1)
    if scaleA:
        scaleA_node = pm.shadingNode('multiplyDivide',n='%s_ScaleA'%sumCtrl, asUtility=1)
        pm.setAttr('%s.input1X'%scaleA_node,scaleA)
        pm.connectAttr(ctrlAttrA,'%s.input2X'%scaleA_node,f=1)
        pm.connectAttr('%s.outputX'%scaleA_node,'%s.input1D[0]'%pmaNode,f=1)
    else:
        pm.connectAttr(ctrlAttrA,'%s.input1D[0]'%pmaNode,f=1)

    if scaleB:
        scaleB_node = pm.shadingNode('multiplyDivide',n='%s_ScaleB'%sumCtrl, asUtility=1)
        pm.setAttr('%s.input1X'%scaleB_node,scaleB)
        pm.connectAttr(ctrlAttrB,'%s.input2X'%scaleB_node,f=1)
        pm.connectAttr('%s.outputX'%scaleB_node,'%s.input1D[1]'%pmaNode,f=1)
    else:
        pm.connectAttr(ctrlAttrB,'%s.input1D[1]'%pmaNode,f=1)

    try:
        pm.addAttr(sumCtrl, ln=ctrlAttrResult.split('.')[1], k=1)
    except Exception, e:
        raise( e )

    pm.connectAttr('%s.output1D'%pmaNode, ctrlAttrResult, f=1)

sumCtrl = 'FaceGui'
cntrl = 'JawSyncDistLoc'
attrA = 'JawSyncDistA.distance'
attrB = 'JawSyncDistB.distance'
sumAttrName = 'JawSync_L_Wide_Sum'
sumAttr(sumCtrl=sumCtrl,
        ctrlAttrA='%s' % (attrA),
        ctrlAttrB='%s' % (attrB),
        ctrlAttrResult='%s.%s' % (sumCtrl, sumAttrName),
        scaleA=None, scaleB=None)

#------------------------------------
# Give BS's and controls, create attributes that drive each blendshape on control.
import pymel.core as pm

shapes = ['MouthAndSacShapes', 'NoseShapes']
controls = ['mouthShapes_ctrl', 'noseShapes_ctrl']

index = 0
for shape in shapes:
    pm.select(shape,r=1)
    bs = pm.ls(sl=1)[0]

    temp = pm.aliasAttr(bs,q=1)
    temp.sort()
    targets = []
    for each in temp:
        if each.startswith('weight'): continue
        targets.append(each)

    for tgt in targets:
        try:
            pm.addAttr(controls[index],ln=tgt,k=1, min=0, max=1)
            pm.connectAttr('%s.%s'%(controls[index], tgt),'%s.%s'%(bs, tgt),f=1)
        except Exception,e:
            print e
            pm.warning('%s failed to create / connect'%tgt)
    index += 1

#-----------------------------------------------------------------
# Set all blendshape target weights to 0



#------------------------------------
import sys
import os
path = '/Users/mauricioptkvp/Development/maya/python'
if path not in sys.path:
    sys.path.insert(0,path)

from MakeController import MakeController
reload( MakeController )

jnts = pm.ls(sl=1,type='joint')
for jnt in jnts:
    MakeController.make(jnt=jnt,name=None)


#------------------------------------------
# Constrain bind joints to controls
import pymel.core as pm

jnts = pm.ls(sl=1,type='joint')
for jnt in jnts:
    pm.parentConstraint(jnt.name()+'_ctrl',jnt,mo=1)
    pm.scaleConstraint(jnt.name()+'_ctrl',jnt,mo=1)


#------------------------------------------
# Print out { "Selected joint names" : [] } in Maya script editor
jnts = pm.ls(sl=1, type='joint')
count = 0
for jnt in jnts:
    if count == 0:
        print "{"
    if not count % 5:
        print ""
    print '"%s":[],'%jnt,
    count += 1
print "}"

#-------------------------------------------
# Name proxy geo: Select: joint, geo
sel = pm.ls(sl=1)
pm.rename(sel[1],sel[0]+'_proxy')

#-------------------------------------------
# Add rotations to orients
jnt = pm.ls(sl=1)[0]
rotations = [0,0,0]
rotations[0]=pm.getAttr('%s.rotateX'%jnt.name())
rotations[1]=pm.getAttr('%s.rotateY'%jnt.name())
rotations[2]=pm.getAttr('%s.rotateZ'%jnt.name())
orients = [0,0,0]
orients[0]=pm.getAttr('%s.jointOrientX'%jnt.name())
orients[1]=pm.getAttr('%s.jointOrientY'%jnt.name())
orients[2]=pm.getAttr('%s.jointOrientZ'%jnt.name())

sum = [rotations[0]+orients[0],
       rotations[1]+orients[1],
       rotations[2]+orients[2]]

jnt.setRotation([0,0,0])
pm.setAttr('%s.jointOrientX'%jnt.name(),sum[0])
pm.setAttr('%s.jointOrientY'%jnt.name(),sum[1])
pm.setAttr('%s.jointOrientZ'%jnt.name(),sum[2])

#-------------------------------------------
# Import export weights
if (!`pluginInfo -q -l "transferSkinCluster.py"`) loadPlugin( "transferSkinCluster.py" );

# Export
sel = pm.ls(sl=1)
for each in sel:
    try:
        pm.mel.eval('icTransferSkinCluster 0 0;')
    except Exception, e:
        print e

# Import
icTransferSkinCluster 1 0;

#--------------------------------------------
# Create bind joints from selected groups
import pymel.core as pm

groups = pm.ls(sl=1)
for grp in groups:
    jnt = pm.joint(name = grp.replace('ROT','JNT'))
    pm.delete( pm.parentConstraint(grp,jnt,mo=False) )


#--------------------------------------------
# Connect bind joint to ik jnt/fk ctrl
jnts = pm.ls(sl=1,type='joint')

for jnt in jnts:
    fkJnt = jnt.name() + '_ctrl'
    ikJnt = jnt.name() + '_ik'
    revNode = pm.createNode('reverse',name=jnt.name()+'_revNode')

    # Parent constraint
    pc = pm.parentConstraint(fkJnt, ikJnt, jnt, mo=True)

    # Make connections
    pm.connectAttr("ikFkSwitches_ctrl.RightArmFKIK",'%s.input.inputX'%revNode.name(),f=True)
    pm.connectAttr('%s.output.outputX'%revNode.name(), '%s.%sW0'%(pc,fkJnt), f=1)
    pm.connectAttr("ikFkSwitches_ctrl.RightArmFKIK", '%s.%sW1'%(pc,ikJnt), f=1)

#--------------------------------------------
# Create / snap joint to selection
sel = pm.ls(sl=1)
pm.select(clear=1)
for each in sel:
    try:
        pm.delete( pm.parentConstraint(each, pm.joint(name=each+'_jnt'),mo=0))
        #pm.setAttr('%s.displayRotatePivot'%each,0)
    except Exception,e:
        print e


#--------------------------------------------
# Create n joint along selected curve
import pymel.core as pm
def jointsOnCurve(crv=None, num=None, name=None):
    if not crv: return
    if not num: return
    if not name: return
    if num < 1: return

    param_increment = 1.0/float(num)
    param = 0
    curveShape = pm.PyNode(crv).getShape()
    prnt = []
    for i in range(num):
        pm.select(clear=1)
        # Create joint
        jnt = pm.joint(n=name+'_'+str(i).zfill(2))
        # Attach to curve
        poci = pm.createNode('pointOnCurveInfo')
        pm.connectAttr('%s.ws'%curveShape,'%s.inputCurve'%poci,f=1)
        pm.connectAttr('%s.position'%poci,'%s.translate'%jnt,f=1)
        pm.setAttr('%s.parameter'%poci,param)
        pm.setAttr('%s.turnOnPercentage'%poci,1)

        pm.disconnectAttr('%s.position'%poci,'%s.translate'%jnt)
        pm.delete(poci)

        if len(prnt):
            pm.parent(jnt,prnt[-1])

        prnt.append(jnt)
        param += param_increment



class posLoc():
    """
    snapLoc: Snap locator via none-offset parentConstraint
               to selected object. Parent constraint is deleted.
    Why? To facilitate space switching. When switching
               parentConstraint weight values, objects pop
               to new relative space. By creating this locator
               you can snap popped position back to pre-pop position.
    Ideas: Make a script that automatically does this FK to IK snapping
    """
    def __init_(self):
        sel = mc.ls(sl=True,fl=True)
        loc = spaceLocator()
        pConst = mc.parentConstraint(sel,loc)
        mc.delete(pConst)
    #End: posLoc()



"""
Given: Nurbs plane + Locator, placed as needed,
Create + Connect + Geo Constraint setup for multi-axis driver, or
whatever.

Use: Select plane, then locator, then let the magic happen!
"""

sel = mc.ls(sl=True,fl=True)
plane = sel[0]
loc = sel[1]

pos = mc.createNode("closestPointOnSurface")

mc.addAttr(loc, ln='parameterU', at='double', min=0, max=1, dv=0.75)
mc.addAttr(loc, ln='parameterV', at='double', min=0, max=1, dv=0.75)
mc.setAttr('%s.parameterU'%loc,k=True)
mc.setAttr('%s.parameterV'%loc,k=True)

mc.geometryConstraint(plane,loc)

mc.connectAttr('%s.worldSpace'%plane, '%s.inputSurface'%pos, f=True)
mc.connectAttr('%s.translate'%loc, '%s.inPosition'%pos, f=True)
mc.connectAttr('%s.u'%pos, '%s.parameterU'%loc, f=True)
mc.connectAttr('%s.v'%pos, '%s.parameterV'%loc, f=True)


"""
given selected curve(s)
-Select all it's CVs
"""
sel = ls(sl=True)

select(clear=True)

for each in sel:
    spans = getAttr('%sShape.spans'%each)
    count = 0
    while count <= spans:
        select('%sShape.cv[%s]'%(each, count), add=True)
        count = count + 1

"""
given selected cv
-Select all shape CVs
"""
sel = ls(sl=True)

select(clear=True)
temp = sel[0].split('.')
shape = temp[0]

spans = getAttr('%s.spans'%shape)
count = 0
while count <= spans:
    select('%s.cv[%s]'%(shape, count), add=True)
    count = count + 1


"""
For selected, delete their constraints
"""
import pymel.core as pm


# Delete contraints
sel = pm.ls(sl=1)
for each in sel:
    try:
        children = pm.listRelatives(each)
    except:
        pass
    for child in children:
        if 'Constraint' in str(type(child)):
            try:
                pm.delete(child)
            except:
                pass

"""
Parent all selected to the first item selected
"""
sel = mc.ls(sl=True,fl=True)
x = 0
for each in sel:
    if x == 0: #Store and skip first item
        parent = each
        x = x + 1
        continue
    mc.parentConstraint(parent,each,mo=True)
    x = x + 1


"""
For selected, break connections on rotations
"""
import maya.cmds as mc
import maya.mel as mel

sel = mc.ls(sl=True)

for each in sel:
    mel.eval('CBdeleteConnection "%s.rx";'%each)
    mel.eval('CBdeleteConnection "%s.ry";'%each)
    mel.eval('CBdeleteConnection "%s.rz";'%each)

"""
Select only joints from all selected items
"""

sel = ls(sl=True)
select(clear=True)
for each in sel:
    type = nodeType(each)
    if "joint" in type:
        select(each,add=True)

#------------------------------------------------------
''' SDK locator on selected joints. '''
import pymel.core as pm
sel = pm.ls(sl=1)
for each in sel:
    prnt = pm.listRelatives(each,parent=1)
    loc = pm.spaceLocator(name='%s_loc' % each)
    pm.delete(pm.parentConstraint(each,loc,mo=0))
    pm.makeIdentity(loc,a=1)
    pm.setAttr('%s.localScaleX' % loc, .05)
    pm.setAttr('%s.localScaleY' % loc, .05)
    pm.setAttr('%s.localScaleZ' % loc, .05)
    pm.parent(each, loc)
    pm.parent(loc,prnt)


'''
Select sine handle / control to connect
'''
import pymel.core as pm

sel = pm.ls(sl=1)
sine = sel[0]
cnt = sel[1]
sineDef = sine.inputs()[0]

attrs = {'sineOffOn':[1, 0, 1],
         'amplitude':0.3,
         'wavelength':2,
         'offset':0,
         'direction':0}

for attr in attrs.keys():
    if isinstance(attrs[attr], list):
        pm.addAttr(cnt, ln=attr, 
                   dv=attrs[attr][0],
                   min=attrs[attr][1],
                   max=attrs[attr][2],
                   k=1)
    else:
        pm.addAttr(cnt, ln=attr, dv=attrs[attr], k=1)

cnt.sineOffOn >> sineDef.envelope
cnt.amplitude >> sineDef.amplitude
cnt.wavelength >> sineDef.wavelength
cnt.offset >> sineDef.offset
cnt.direction >> sine.rotateY

def unlock(obj=None, t=True, 
           r=True, s=False,
           axis = ['X','Y','Z']):
    '''
    Unlock and make keyable for selected
    '''
    pm.select(obj, r=1)
    obj = pm.ls(sl=1)[0]
    attrs = {}
    if t: attrs['t'] = 'translate'
    if r: attrs['r'] = 'rotate'
    if s: attrs['s'] = 'scale'

    for attr in attrs.keys():
        for a in axis:
            try:
                pm.setAttr('%s.%s%s' % (obj, attrs[attr], a), l=0, k=1)
            except Exception, e:
                print e

''' Rename skinCluster to mesh name '''
sel = pm.ls(sl=1)
for each in sel:
    try:
        sc = pm.PyNode(pm.mel.eval('findRelatedSkinCluster("%s")' % each))
        sc.rename('%s_sc' % each.split(':')[-1])
    except Exception,e:
        print e


"""
Given selected rivets, rename and create child joint
"""        
import pymel.core as pm

sel = pm.ls(sl=1)

count = 1
name = 'Buttons'
for each in sel:
    pm.select(clear=1)
    each.rename('%s_%s_rivet' % (name, count))
    aimConst = each.getChildren()[1]
    aimConst.rename('%s_%s_rivetAimConstraint' % (name, count))
    jnt = pm.joint(n='%s_%s_jnt' % (name, count))
    pm.delete(pm.parentConstraint(each, jnt, mo=0))
    pm.parent(jnt, each)
    count += 1