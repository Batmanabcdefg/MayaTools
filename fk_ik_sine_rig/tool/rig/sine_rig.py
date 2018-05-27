import pymel.core as pm
from ..errors import errors
from ..maya_testing import general
import control


# reg_node
def build(name=None, crv=None, reg_node=None, log=False):
    '''Create ine node deformer and attributes on given plane, and
    IK control connected to the reg_node.

    name -- Prefix name. Str
    crv -- Curve to add deformer to. nt.Transform
    reg_node -- registration node. nt.Transform
    '''
    general.check_type(name, 'name', [str])
    general.check_type(crv, 'crv', [pm.nt.Transform])
    general.check_type(reg_node, 'reg_node', [pm.nt.Transform])

    cnt_attr = '%s1_ik_cnt' % name
    if not hasattr(reg_node, cnt_attr):
        raise errors.InputError('reg_node',
                                reg_node,
                                'Missing attr: %s' % cnt_attr)

    attr = getattr(reg_node, cnt_attr)
    cnt = attr.listConnections()[0]

    if log:
        str_1 = 'Cnt: ', cnt
        general.logging.debug(str_1)

    crv2 = crv.duplicate()
    sineDef, sineHndl = pm.nonLinear(crv2,
                                     typ='sine',
                                     name='%s_sineDeformer' % name)
    bs = pm.blendShape(crv2, crv, foc=True,
                       name='%s_sineBlendShape' % name)[0]

    attr = getattr(bs, crv2[0].name())
    attr.set(1)

    sineDef.rename('%s_sineDeformer' % name)
    sineHndl.rename('%s_sineDeformerHandle' % name)

    attrs = {'sineOffOn': [1, 0, 1],
             'amplitude': 0.3,
             'wavelength': 2,
             'offset': 0,
             'direction': 0}

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
    cnt.direction >> sineHndl.rotateY

    # Setup the handle
    hndl_grp = pm.group(name='%s_hndlGrp' % name, em=1)
    pm.parent(sineHndl, hndl_grp)
    sineHndl.rz.set(180)
    sineDef.dropoff.set(1)
    sineDef.lowBound.set(0)
    sineDef.highBound.set(2)

    control.register_object(reg_node, 'sine_handle', sineHndl)

    return reg_node
