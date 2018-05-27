import pymel.core as pm
import control
import fk_rig
import ik_rig
import sine_rig
from ..maya_testing import general


def build(name=None,
          crv=None,
          loc=None,
          ik_jnts=None,
          ik_cnts=None,
          ik_order='xyz',
          fk_order='xyz',
          fk_num=None,
          fk_buffers=None,
          fk_color=None,
          fk_scale=None,
          fk_typ=None,
          log=False):
    ''' Create fk/ik/sine rig along provided curve

    Attributes:
          crv -- Curve to build rig along. nt.Transform
          loc -- Locator used to get up vector. nt.Transform
          ik_jnts -- Number of ik joints. Int
          ik_cnts -- Number of ik controls. Int
          ik_order -- IK joint order. Str. Default: 'xyz'
          fk_order -- FK joint order. Str. Default: 'xyz'
          fk_num -- Number of FK joints/Controls. Int
          fk_buffers -- Number of groups above controls. Int
          fk_color -- FK control color. Str
          fk_scale -- FK control scale. Float
          fk_typ -- FK control type. Str
          log -- Output logging messages. Bool
    '''
    general.check_type(name, 'name', [str])
    general.check_type(crv, 'crv', [pm.nt.Transform])
    general.check_type(loc, 'loc', [pm.nt.Transform])
    general.check_type(ik_jnts, 'ik_jnts', [int])
    general.check_type(ik_cnts, 'ik_cnts', [int])
    general.check_type(ik_order, 'ik_order', [str])
    general.check_type(fk_order, 'fk_order', [str])
    general.check_type(fk_num, 'fk_num', [int])
    general.check_type(fk_buffers, 'fk_buffers', [int])
    general.check_type(fk_color, 'fk_color', [str])
    general.check_type(fk_scale, 'fk_scale', [float])
    general.check_type(fk_typ, 'fk_typ', [str])
    general.check_type(log, 'log', [bool])

    reg_node = control.create_register_node(name=name)

    fk_rig.build(name=name+'FK', crv=crv, loc=loc, order=fk_order,
                 num=fk_num, buffers=fk_buffers, color=fk_color,
                 scale=fk_scale, typ=fk_typ, reg_node=reg_node)

    ik_rig.build(name+'IK', crv=crv, loc=loc,
                 num_jnts=ik_jnts, num_cnts=ik_cnts,
                 order=ik_order, reg_node=reg_node)

    crv = reg_node.ik_crv.listConnections()[0]
    sine_rig.build(name=name+'IK', crv=crv, reg_node=reg_node)

    sine = reg_node.sine_handle.listConnections()[0]
    ik_top = reg_node.ik_top_node.listConnections()[0]
    fk_top = reg_node.fk_top_node.listConnections()[0]

    rig_top = pm.group(name='%s_rig_top' % name, empty=1)

    pm.parent(sine.getParent(), rig_top)
    pm.parent(ik_top, rig_top)
    pm.parent(fk_top, rig_top)

    # Parent IK controls to fk
    fk_btm = pm.PyNode('%sFK_1' % name)
    fk_top = pm.PyNode('%sFK_%s' % (name, ik_cnts))
    ik_btm = pm.PyNode('%sIK_1_top_node' % name)
    ik_top = pm.PyNode('%sIK_%s_top_node' % (name, ik_cnts))

    pm.parent(ik_btm, fk_btm)
    pm.parent(ik_top, fk_top)

    control.register_object(reg_node, 'rig_top_node', rig_top)

    return reg_node
