import pymel.core as pm
from ..maya_testing import general
import control
import utils

general.logSetup('debug', 'fk_rig')


# reg_node
def build(name=None, crv=None, loc=None, order=None,
          num=None, buffers=None, color=None, scale=None,
          typ=None, reg_node=None):
    '''Build fk joint chain with controls

    Attributes:
        name -- Prefixname used in rig. Str
        crv -- Curve used to build joint chain along. nt.Transform
        loc -- Locator used to determine up vector. nt.Transform
        order -- 'xyz' ... Str
        num -- Number of joints/controls. Int
        buffers -- Number of buffer groups to place above controls. Int
        color -- Color for controls. Str
        scale -- Scale for controls. Float
        typ -- control curve type. Str
        reg_node -- Registration node. nt.Transform
    '''
    general.check_type(name, 'name', [str])
    general.check_type(crv, 'crv', [pm.nt.Transform])
    general.check_type(loc, 'loc', [pm.nt.Transform])
    general.check_type(order, 'order', [str])
    general.check_type(num, 'num', [int])
    general.check_type(buffers, 'buffers', [int])
    general.check_type(color, 'color', [str])
    general.check_type(scale, 'scale', [float])
    general.check_type(typ, 'typ', [str])
    if reg_node:
        general.check_type(reg_node, 'reg_node', [pm.nt.Transform])

    reg_node, chain = utils.build_joint_chain(name, crv, order,
                                              num, loc, reg_node)

    count = 1
    for j in chain:
        make_control(name='%s_%s' % (name, count),
                     obj=j, buffers=buffers,
                     color=color,
                     scale=scale, typ=typ,
                     reg_node=reg_node)
        count += 1
    attr = getattr(reg_node, '%s_1' % (name))
    cnt = attr.listConnections()[0]

    prnt = cnt.getParent()
    for i in range(buffers-1):
        prnt = prnt.getParent()

    control.register_object(reg_node, 'fk_top_node', prnt)

    return reg_node


# reg_node, cnt
def make_control(name=None, obj=None, buffers=None, color=None,
                 scale=None, typ=None, reg_node=None):
    '''Given a pm.nt.Transform, create control at its
    location/orientation.

    Attributes:
        name -- Prefix name to be used for control
        obj -- Object control will be made for. [pm.nt.Transform, pm.nt.Joint]
        buffer -- Number of groups above the control. Int
        color -- Color for control. Str
        scale -- Scale for the control. Float
        typ -- Type of control curve. 'circle','pointed_circle','square','cube'
        reg_node -- reg_node to use
    '''
    general.check_type(name, 'name', [str])
    general.check_type(obj, 'obj', [pm.nt.Transform, pm.nt.Joint])
    general.check_type(buffers, 'buffers', [int])
    general.check_type(color, 'color', [str])
    general.check_type(scale, 'scale', [float])
    general.check_type(typ, 'typ', [str])
    if reg_node:
        general.check_type(reg_node, 'reg_node', [pm.nt.Transform])

    # Create curve
    reg_node, crv = control.create_curve(name=name,
                                         typ=typ,
                                         scale=scale,
                                         color=color,
                                         reg_node=reg_node)

    # Match curve to object
    control.match_object(crv, obj)

    # Setup heirarchy
    if obj.getParent():
        pm.parent(crv, obj.getParent())
    pm.parent(obj, crv)

    # Create heirarchy
    control.create_heirarchy(name=name, obj=crv, num=buffers)

    return reg_node, crv
