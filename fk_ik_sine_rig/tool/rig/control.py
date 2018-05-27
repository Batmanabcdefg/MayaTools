import os.path
import pymel.core as pm
from ..data import data
from ..maya_testing import general
from ..errors import errors


general.logSetup('debug', 'control')

colors = {
    'black': 1,
    'dark_grey': 2,
    'light_grey': 3,
    'bergundy': 4,
    'navy_blue': 5,
    'light_blue': 6,
    'dark_green': 7,
    'dark_purple': 8,
    'pink': 9,
    'light_brown': 10,
    'dark_brown': 11,
    'dark_red': 12,
    'light_red': 13,
    'light_green': 14,
    'dark_blue': 15,
    'white': 16,
    'yellow': 17,
    'teal': 18,
    'mint': 19,
    'light_pink': 20,
    'light_tan': 21,
    'light_yellow': 22,
    'dark_mint': 23,
    'tan': 24,
    'dark_mustard': 25,
    'pastel_green': 26,
    'pastel_mint': 27,
    'pastel_blue': 28,
    'pastel_blue': 29,
    'pastel_purple': 30,
    'fuschia': 31}


types = ['circle', 'square', 'cube', 'pointed_circle']


def match_object(a=None, b=None):  # None
    '''Match object a orientations to b

    Attributes:
        a -- Object to be moved
        b -- Object to match to
    '''
    general.check_type(a, 'a', [pm.nt.Transform, pm.nt.Joint])
    general.check_type(b, 'b', [pm.nt.Transform, pm.nt.Joint])

    pm.delete(pm.parentConstraint(b, a, mo=0))


def create_heirarchy(name=None, obj=None, num=None):  # grps[]
    '''Given a pm.nt.Transform, create a heirarchy above it, below it's parent

    Attributes:
        name -- Prefix name for nodes
        obj -- Object to create heirarchy for
        num -- Number of nodes to make
    '''
    general.check_type(name, 'name', [str])
    general.check_type(obj, 'obj', [pm.nt.Transform])
    general.check_type(num, 'num', [int])

    prnt = None
    if obj.getParent():
        prnt = obj.getParent()

    # Create the nodes
    pm.select(clear=True)
    grps = []
    for i in range(num):
        if i == 0:
            grp = pm.group(name='%s_top_node' % name, empty=True)
        elif i == (num-1):
            grp = pm.group(name='%s_btm_node' % name, empty=True)
            pm.parent(grp, grps[i-1])
        else:
            grp = pm.group(name='%s_node%s' % (name, num), empty=True)
            pm.parent(grp, grps[i-1])
        grps.append(grp)

    pm.select(clear=True)
    if prnt:
        pm.parent(grps[0], prnt)

    # Position and zero the nodes
    count = 0
    for g in grps:
        pm.delete(pm.parentConstraint(obj, g, mo=0))
        if count > 0:
            pm.makeIdentity(g, a=1, r=1, s=1, t=1)
        count += 1

    # Insert obj into the heirarchy
    pm.parent(obj, grps[-1])
    try:
        pm.makeIdentity(obj, a=1, r=1, s=1, t=1)
    except:
        pass
    return grps


# reg_node, cnt
def create_curve(name=None, typ=None, scale=None,
                 color=None, reg_node=None):
    '''Create a control curve

    Attributes:
        name -- PRefix name to be used
        typ -- Type of control: circle, pointed_circle, square, cube. Str
        scale -- Float
        color -- Name of color to use
        reg_node -- Reg node to use instead of creating one
    '''
    general.check_type(name, 'name', [str])
    general.check_type(typ, 'typ', [str])
    general.check_type(scale, 'scale', [float])
    general.check_type(color, 'color', [str])
    if reg_node:
        general.check_type(reg_node, 'reg_node', [pm.nt.Transform])

    if typ not in types:
        errors.InputError('typ', typ, [types])

    if color not in colors.keys():
        errors.InputError('color', color, colors.keys())

    try:
        f = os.path.dirname(__file__) +\
            os.path.sep + 'maya_files' + os.path.sep + '%s.ma' % typ
        pm.importFile(f, defaultNamespace=True)
    except:
        raise errors.BuildError('create_curve', 'Failed to open: %s' % f)

    try:
        pm.select('%s' % typ, r=True)
        cnt = pm.ls(sl=1)[0]
    except:
        raise errors.BuildError('create_curve', 'Failed to select control')

    for s in cnt.getShapes():
        s.overrideEnabled.set(1)
        s.overrideColor.set(colors[color])
    cnt.scale.set([scale, scale, scale])
    cnt.rename(name)

    if not reg_node:
        try:
            pm.select('%s_reg_node' % name, r=1)
            reg_node = pm.ls(sl=1)[0]
        except:
            reg_node = create_register_node(name)

    register_object(reg_node, name, cnt)

    return reg_node, cnt


def create_register_node(name=None):  # reg_node
    '''Create a TRansform to be used as a registraion node

    Attributes:
        name -- Name for the node. Str
    '''
    general.check_type(name, 'name', [str])

    node = pm.createNode('transform', name=name + '_reg_node')
    node.addAttr('reg_node', dt='string')
    node.addAttr('version', dt='string')
    node.version.set(data.version)
    node.reg_node.set('True')

    return node


# None
def register_object(reg_node=None, attr_name=None,
                    obj=None, log=False):
    '''Register an object to a reg_node

    Attributes:
        reg_node -- Registration node. pm.nt.Transform
        attr_name -- Name for attr to be created on reg_node. Str
        obj -- Object to connect message attr to reg_node.attr. pm.nt.Transform
    '''
    general.check_type(reg_node, 'reg_node', [pm.nt.Transform])
    general.check_type(attr_name, 'attr_name', [str])
    general.check_type(obj, 'obj', [pm.nt.Transform])

    for attr in ['version', 'reg_node']:
        if not hasattr(reg_node, attr):
            raise errors.ObjectError(reg_node, 'Attr: %s' % attr, None)

    reg_node.addAttr(attr_name, at='message')
    pm.connectAttr('%s.message' % obj,
                   '%s.%s' % (reg_node, attr_name), f=1)

    if log:
        str_1 = 'Connected: %s.%s >> %s.message' % (reg_node,
                                                    attr_name,
                                                    obj)
        general.logging.debug(str_1)
