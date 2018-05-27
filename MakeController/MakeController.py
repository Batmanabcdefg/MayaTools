'''
Make a controller, given oriented joint(s)
- hi=True : Maintain parent / child relation ship of joints by parenting
the created controls.
'''
import pymel.core as pm

def make(jnt=None,name=None,offsets=2,hi=True,suffix='_ctrl'):
    if name:
        name=name
    else:
        name = jnt + suffix
        
    ctrl = pm.circle(n=name)[0]
    pm.delete(pm.parentConstraint(jnt,ctrl,mo=0))
    
    oGrps = []
    z = [0,0,0]
    
    pos = ctrl.getTranslation(space='world')
    rot = ctrl.getRotation(space='world')    
    oGrps.append(pm.group(ctrl, n=name+'_offsetA'))
    oGrps.append(pm.group(oGrps[0], n=name+'_offsetB'))
    oGrps.append(pm.group(oGrps[1], n=name+'_offsetC'))

    ctrl.setTranslation(z)
    ctrl.setRotation(z)
    
    for each in oGrps:
        each.centerPivots()    
        
    oGrps[-1].setTranslation(((oGrps[-1].getTranslation()[0]+pos[0]),
                              (oGrps[-1].getTranslation()[1]+pos[1]),
                              (oGrps[-1].getTranslation()[2]+pos[2])))
    oGrps[-1].setRotation(((oGrps[-1].getRotation()[0]+rot[0]),
                              (oGrps[-1].getRotation()[1]+rot[1]),
                              (oGrps[-1].getRotation()[2]+rot[2])))
    
    # If selected joint has parent, attempt to parent to a control with the expected parent name.
    if hi:
        p = jnt.getParent()
        if p:
            if p.type() == 'joint':
                try:
                    pm.parent(oGrps[-1],p+suffix)  
                except:
                    pass


