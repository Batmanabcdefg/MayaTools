import pymel.core as pm
from ..errors import errors

'''
Test methods for joints in Maya
'''


def assertAimAxis(jnt=None, aim=None):
    '''Assert the given axis is the axis aiming at child nodes

    Attributes:
        jnt -- Joint in scene to check
        aim -- Character "x"|"y"|"z". Axis expected to aim at child
    '''
    if not isinstance(jnt, pm.nt.Joint):
        raise errors.InputError('jnt', jnt, pm.nt.Joint)

    if aim.lower() not in ['x', 'y', 'z']:
        raise errors.InputError('aim', aim, '"x", "y" or "z"')
    aim = aim.lower()

    children = jnt.getChildren()
    if not children:
        raise errors.ObjectError(jnt, 'Child nodes', children)

    if len(children) > 1:
        raise errors.ObjectError(jnt, 'One child', children)

    # Place locator as child to jnt and zero it
    loc = pm.spaceLocator()
    pm.parent(loc, jnt)
    loc.setTranslation(0)
    loc.setRotation([0, 0, 0])

    # Get magnitude of vector to child
    jnt_pos = pm.dt.Vector(pm.xform(jnt, q=1, ws=1, t=1))
    chld_pos = pm.dt.Vector(pm.xform(children[0], q=1, ws=1, t=1))
    vec = chld_pos - jnt_pos

    # Move it along expected axis
    if aim == 'x':
        loc.tx.set(vec.length())
    if aim == 'y':
        loc.ty.set(vec.length())
    if aim == 'z':
        loc.tz.set(vec.length())
    loc_pos = pm.xform(loc, q=1, ws=1, t=1)

    # Remove locator from the scene
    pm.delete(loc)

    for l, p in zip(loc_pos, chld_pos):
        if round(l, 6) != round(p, 6):
            return False
    return True
