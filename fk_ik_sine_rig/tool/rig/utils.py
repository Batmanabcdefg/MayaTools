import pymel.core as pm
from ..errors import errors
from ..maya_testing import general
import control


# plane
def build_plane(name=None, crv=None, spans=None,
                direction='u', width_axis=None,
                width=1, log=True):
    '''Given a valid curve, build nurbs plane

    Attributes:
        name -- Prefix name for plane. Str
        crv -- Curve to use as build guide. nt.Transform
        spans -- Spans for the plane. Int
        direction -- Build direction. 'u' or 'v'
        width_axis -- Plane width axis. 'x', 'y' or 'z'
        width -- Width of plane. Float
    '''
    general.check_type(name, 'name', [str])
    general.check_type(crv, 'crv', [pm.nt.Transform])
    general.check_type(spans, 'spans', [int])
    general.check_type(direction, 'direction', [str])
    general.check_type(width_axis, 'width_axis', [str])
    general.check_type(width, 'width', [float, int])

    if direction not in ['u', 'v']:
        raise errors.InputError('direction', direction, "'u' or 'v'")

    if width_axis not in ['x', 'y', 'z']:
        raise errors.InputError('width_axis', width_axis, "'x', 'y' or 'z'")

    d1 = crv.duplicate()
    d2 = crv.duplicate()

    move_amt = []
    if width_axis == 'x':
        move_amt = [width, 0, 0]
    elif width_axis == 'y':
        move_amt = [0, width, 0]
    elif width_axis == 'z':
        move_amt = [0, 0, width]
    if log:
        str_1 = 'move_amt: ', move_amt
        general.logging.debug(str_1)

    pm.move(move_amt[0],
            move_amt[1],
            move_amt[2],
            d1, r=1)

    pm.move(-move_amt[0],
            -move_amt[1],
            -move_amt[2],
            d2, r=1)

    p = pm.loft(d1, d2, n=name+'_plane', ch=0)[0]

    if direction == 'u':
        pm.rebuildSurface(p, dir=2, su=spans, sv=2)
    if direction == 'v':
        pm.rebuildSurface(p, dir=2, sv=spans, su=2)

    pm.delete(d1)
    pm.delete(d2)

    return p


# reg_node, chain[]
def build_joint_chain(name=None, crv=None,
                      order=None, num=None,
                      loc=None, reg_node=None, log=False):
    '''Given a valid curve, build joint chain along curve, num joints long

    Attributes:
        name -- Prefix name for plane. Str
        crv -- Curve to use as build guide. pm.nt.Transform
        order -- ['xyz','xzy','yxz','yzx','zxy','zyx']
        num -- Number of joints. 3 - 50, Int
        loc -- Used to set aim of secondary axis nt.Transform
        reg_node -- Registratioin node. nt.Transform
        log -- Output logging messages. Bool
    '''
    general.check_type(name, 'name', [str])
    general.check_type(crv, 'crv', [pm.nt.Transform])
    general.check_type(order, 'order', [str])
    general.check_type(num, 'num', [int])
    general.check_type(loc, 'loc', [pm.nt.Transform])

    orders = ['xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx']
    if order not in orders:
        raise errors.InputError('order', order, orders)
    if num < 3 or num > 50:
        raise errors.InputError('num', num, 'Range: 3 - 50')

    loc = loc.duplicate()[0]
    chain = []
    loc_v = None
    incr = float(1.0/num)
    if log:
        str_1 = 'Curve Length: ', pm.arclen(crv)
        str_2 = 'Increment: ', incr
        general.logging.debug(str_1)
        general.logging.debug(str_2)
    param = 0
    pm.select(clear=1)
    for i in range(num):
        pos = pm.pointOnCurve(crv, pr=param, p=True, top=True)
        if i == 0:  # Get vector to locator
            pos_v = pm.dt.Vector(pos)
            loc_pos = pm.dt.Vector(pm.xform(loc, q=1, ws=1, rp=1))
            loc_v = loc_pos - pos_v
            if log:
                str_1 = 'Jnt Pos: ', pos_v
                str_2 = 'Loc Pos: ', loc_pos
                str_3 = 'Loc Vec: ', loc_v
                general.logging.debug(str_1)
                general.logging.debug(str_2)
                general.logging.debug(str_3)
        j = pm.joint(p=pos, name='%s_Jnt_%s' % (name, (i+1)))
        chain.append(j)
        if log:
            str_1 = 'Created Joint: ', j
            str_2 = 'Parameter: ', param
            str_3 = 'Pos: ', pos
            str_4 = 'Curve: ', crv
            general.logging.debug(str_1)
            general.logging.debug(str_2)
            general.logging.debug(str_3)
            general.logging.debug(str_4)
        param += incr

    if log:
        str_1 = 'Chain: ', str(chain)
        general.logging.debug(str_1)

    # aim vector
    aim_v = []
    if order[0].lower() == 'x':
        aim_v = [1, 0, 0]
    if order[0].lower() == 'y':
        aim_v = [0, 1, 0]
    if order[0].lower() == 'z':
        aim_v = [0, 0, 1]

    # up vector
    up_v = []
    if order[1].lower() == 'x':
        up_v = [1, 0, 0]
    if order[1].lower() == 'y':
        up_v = [0, 1, 0]
    if order[1].lower() == 'z':
        up_v = [0, 0, 1]

    for jnt in chain[:-1]:
        # Snap/parent locator to jnt
        pm.parent(loc, jnt)
        loc.setTranslation(0)
        loc.setRotation([0, 0, 0])

        # move by loc_v
        pm.move(loc_v[0],
                loc_v[1],
                loc_v[2],
                loc, r=1)
        pm.parent(loc, w=1)

        # Remove joint from hierarchy
        p = jnt.getParent()
        c = jnt.getChildren()
        try:
            pm.parent(jnt, w=1)
        except:
            pass
        pm.parent(c, w=1)

        # Aim to child
        pm.delete(pm.aimConstraint(c,
                                   jnt,
                                   aim=aim_v,
                                   wu=up_v,
                                   wut='object',
                                   wuo=loc,
                                   mo=0))

        # Reinsert to heirarchy
        if c:
            pm.parent(c, jnt)
        if p:
            pm.parent(jnt, p)

    # Oreint last joint to none
    pm.joint(chain[-1], e=1, oj='none', zso=True)

    if not reg_node:
        reg_node = control.create_register_node(name)

    control.register_object(reg_node,
                            '%s_chain_root' % name,
                            chain[0])

    pm.select(clear=1)
    pm.delete(loc)
    return reg_node, chain
