import pymel.core as pm
import pymel.core.datatypes as dt

'''
Given named curve:
- create fluid container
- create rig group (everything is created under this group)
- create emitters group
- create up locator
- translate up locator 3000 units along up_vec
- connect group to motion path
- create X emitters at start of curve
- along vector up_vec
- with s spacing
- parent rig group to container
'''

def create_emitter(container=None, name=None, pos=None): # PyNode
    em = pm.fluidEmitter( pos=pos, type='omni', der=1, r=100.0 )
    em.rename(name)
    pm.connectDynamic(container, em=em)
    return name

def create_fluid_container(name=None, prnt=None): # PyNode 
    cont = pm.nodetypes.FluidShape().create3D(10, 10, 10, 10, 10, 10,
            parent=prnt)
    cont.rename(name+'Shape')
    return cont

def get_pos(crv, param=0): # dt.Vector
    return dt.Vector(pm.pointOnCurve( crv, pr=param, p=True ))

def create_rig( crv=None, 
                emitters=10, 
                up_vec=(0,0,-1), 
                s=(0,0,-1),
                start=1,
                end=50):
    crv = pm.PyNode(crv)
    name = crv.name()
    cont_name = name + '_fluidContainer'
    emitter_name = name + '_emitter'
    rig_grp_name = name + '_rigGrp'
    up_loc_name = name + '_upLoc'

    up_vec = dt.Vector(up_vec)
    s = dt.Vector(s)
    pos = get_pos(crv=crv, param=0)

    rig_grp = pm.group(em=1, name=rig_grp_name)
    em_grp = pm.group(em=1, name=emitter_name+'Grp')
    pm.move(em_grp, pos)

    cont_grp = pm.group(em=1, name=cont_name)
    cont = create_fluid_container(name=cont_name, prnt=cont_grp)
    pm.move(cont_grp, pos)
    
    emittersList = []
    em_pos = pos
    for i in range(emitters):
        em = create_emitter(container=cont, name=(emitter_name+'_%s' % i),
                pos=em_pos)
        em_pos += s
        pm.parent(em, em_grp)
        emittersList.append(em)

    up_loc = pm.spaceLocator(p=pos, name=up_loc_name)
    pm.move(up_loc, (pos + up_vec*-3000))
    pm.parent(up_loc, rig_grp)

    pm.pathAnimation(   em_grp, 
                        stu=start, 
                        etu=end, 
                        c=crv,
                        wut='object',
                        wuo=up_loc)

    pm.parent(em_grp, rig_grp)
    pm.parent(rig_grp, cont)
    
create_rig(crv=pm.ls(sl=1)[0]) 
