# Stable IK chain spine
# Select SH joints, this creates alternate/stable joints
import pymel.core as pm

sel = pm.ls(sl=1)

pm.select(clear=1)
jnts = []
count = 0
for sh in sel:
    pm.select(clear=1)
    upLoc = pm.spaceLocator(n='%s_upLoc' % sh)
    pm.delete(pm.parentConstraint(sh, upLoc, mo=0))
    pm.parent(upLoc, sh)
    pm.move(0, 0, 5, upLoc, r=1)
    if count > 0:
        pm.parent(upLoc, jnts[count-1])
    
    pm.select(clear=1)
    jnts.append(pm.joint(n='%s_SH' % sh))
    pm.delete(pm.parentConstraint(sh, jnts[count], mo=0))
    pm.pointConstraint(sh, jnts[count], mo=0)
    pm.scaleConstraint(sh, jnts[count])
    if count > 0:
        pm.aimConstraint(jnts[count-1], jnts[count],
                        wut='object', wuo=upLoc)
    count += 1
    
    
#--- Preserve seletectd positions with named locators
# Select objects to make locators for
import pymel.core as pm

sel = pm.ls(sl=1)
mainGrp = pm.group(em=1, name='PositionLocators_grp')
for each in sel:
    grp = pm.group(name=each+'_posGrp', em=1)
    pm.delete(pm.parentConstraint(each, grp, mo=0))
    pm.parent(grp, mainGrp)
    
# Restore positions based on named locators
# Select position locators
sel = pm.ls(sl=1)
for grp in sel:
    obj = grp[:-7]
    obj = pm.PyNode(obj)
    attrs = pm.listAttr(obj, k=1)
    
    try:
        pm.delete(pm.parentConstraint(grp, obj, mo=0))
        print 'Snapped: ' + obj
        continue
    except:
        pass
    try:
        pm.delete(pm.pointConstraint(grp, obj, mo=0))
        print 'Snapped: ' + obj
        continue
    except:
        pass
    try:
        pm.delete(pm.orientConstraint(grp, obj, mo=0))
        print 'Snapped: ' + obj
        continue
    except:
        pass
        
    for attr in attrs:
        if 'translate' in attr:
            for skip in [('y', 'z'), ('x', 'z'), ('y', 'x')]:
                try:
                    pm.select(grp, obj, r=1)
                    pm.delete(
                        pm.mel.eval('pointConstraint -offset 0 0 0 ' +\
                        '-skip %s -skip %s -weight 1;' %\
                        (skip[0], skip[1])))
                    print 'Snapped: ' + obj + '.' + attr
                    break
                except Exception, e:
                    print e
                    break
        if 'rotate' in attr:
            for skip in [('y', 'z'), ('x', 'z'), ('y', 'x')]:
                try:
                    pm.select(grp, obj, r=1)
                    pm.delete(
                        pm.mel.eval('pointConstraint -offset 0 0 0 ' +\
                        '-skip %s -skip %s -weight 1;' %\
                        (skip[0], skip[1])))
                    print 'Snapped: ' + obj + '.' + attr
                    break
                except Exception, e:
                    print e
                    break

#--- Select two edges and RR control.
# Constrains controls' parent to rivet
import pymel.core as pm

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
                
# Select two edges and control
sel = pm.ls(sl=1, fl=1)
pm.select(sel[2], r=1)
cnt = pm.ls(sl=1)[0]

# Create rivet
pm.select(sel[0], sel[1], r=1)
riv = pm.mel.eval('rivet')
pm.select(riv, r=1)
riv = pm.ls(sl=1)[0]
riv.rename('%s_riv' % sel[2])

# Unlock control parent
prnt = cnt.getParent()
unlock(prnt)

# Delete contraints
children = pm.listRelatives(prnt)
for child in children:
    if 'Constraint' in child:
        pm.delete(child)

# Contrain prnt to rivet
pm.parentConstraint(riv, prnt, mo=1)
pm.select(clear=1)

#--- Select transform and RR control.
# Constrains controls' parent to transform
import pymel.core as pm

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
                
# Select transform and  rr control
sel = pm.ls(sl=1)
obj = pm.PyNode(sel[0])
cnt = pm.PyNode(sel[1])

# Unlock control parent
prnt = cnt.getParent()
unlock(prnt)

# Delete contraints
children = pm.listRelatives(prnt)
for child in children:
    if 'Constraint' in child:
        pm.delete(child)

# Contrain prnt to obj
pm.parentConstraint(obj, prnt, mo=1)
pm.select(clear=1)

#--- SDK on RR FK Control
def rrFkCntSDK(cnt=None, attr=None,
               driver=None, v=[], dv=[]):
    '''
    Given selected rr fk control, 
    create SDK on parent group.
    '''
    pm.select(cnt, r=1)
    cnt = pm.ls(sl=1)[0]
    prnt = cnt.getParent()
    unlock(obj=prnt)
    for val, dval in zip(v, dv):
        pm.setDrivenKeyframe(prnt, cd=driver,
                             dv=dval, v=val,
                             at=attr)

