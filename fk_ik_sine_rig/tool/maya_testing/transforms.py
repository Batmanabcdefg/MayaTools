import pymel.core as pm
import general as general
from tool.errors import errors
'''
Test methods for transforms in Maya
'''


general.logSetup('debug', 'Transforms')


def assertAimingAt(a=None, b=None, axis=None, log=False):
    '''Assert a aims at b along axis

    Attributes:
        a -- Object a. [pm.nt.Transform, pm.nt.Joint]
        b -- Object b. [pm.nt.Transform, pm.nt.Joint]
        axis -- axis aiming at b. 'x' 'y' or 'z'
    '''
    general.check_type(a, 'a', [pm.nt.Transform, pm.nt.Joint])
    general.check_type(b, 'b', [pm.nt.Transform, pm.nt.Joint])
    general.check_type(axis, 'axis', [str])

    if axis not in ['x', 'y', 'z']:
        raise errors.InputError(axis, 'axis', ['x', 'y', 'z'])

    pos_a = pm.dt.Vector(pm.xform(a, q=1, ws=1, rp=1))
    pos_b = pm.dt.Vector(pm.xform(b, q=1, ws=1, rp=1))
    vec = pos_b - pos_a

    if not vec.length() > 0:
        raise errors.ObjectError(a, 'Different position than b',
                                 'Same position as b')

    loc = pm.spaceLocator()
    pm.parent(loc, a)
    loc.setTranslation(0)
    loc.setRotation([0, 0, 0])
    if axis == 'x':
        loc.tx.set(vec.length())
    elif axis == 'y':
        loc.ty.set(vec.length())
    elif axis == 'z':
        loc.tz.set(vec.length())

    pos_loc = pm.dt.Vector(pm.xform(loc, q=1, ws=1, rp=1))
    pm.delete(loc)

    if log:
        str_1 = 'pos_a: ', pos_a
        str_2 = 'pos_b: ', pos_b
        str_3 = 'pos_loc: ', pos_loc
        general.logging.debug(str_1)
        general.logging.debug(str_2)
        general.logging.debug(str_3)

    return general.assertAlmostEquals(pos_loc, pos_b, 3)


def assertOrientationMatches(a=None, b=None):
    '''Check that axises and position match for a and b

    Attributes:
        a -- Object to check against b. [pm.nt.Transform, pm.nt.Joint]
        a -- Object to check against a. [pm.nt.Transform, pm.nt.Joint]

    '''

    def makeLoc(obj=None):
        # Place locator as child to jnt and zero it
        loc = pm.spaceLocator()
        pm.parent(loc, obj)
        loc.setTranslation(0)
        loc.setRotation([0, 0, 0])
        return loc

    def moveLoc(loc=None, axis=None, amount=None):
        # Move loc along axis by amount, return position
        if axis == 'x':
            loc.tx.set(amount)
        if axis == 'y':
            loc.ty.set(amount)
        if axis == 'z':
            loc.tz.set(amount)
        return pm.xform(loc, q=1, ws=1, rp=1)

    general.check_type(a, 'a', [pm.nt.Transform, pm.nt.Joint])
    general.check_type(b, 'b', [pm.nt.Transform, pm.nt.Joint])

    a_pos = []
    b_pos = []
    for axis in ['x', 'y', 'z']:
        # Make locators
        loc_a = makeLoc(a)
        loc_b = makeLoc(b)

        a_pos.append(moveLoc(loc_a, axis, 5))
        b_pos.append(moveLoc(loc_b, axis, 5))

        pm.delete(loc_a)
        pm.delete(loc_b)

    return general.assertAlmostEquals(a_pos, b_pos)


def assertLocationsMatch(a=None, b=None):
    '''Assert a and b locations match

    Attributes:
        a -- Object a. [pm.nt.Transform, pm.nt.Joint]
        b -- Object b. [pm.nt.Transform, pm.nt.Joint
    '''
    general.check_type(a, 'a', [pm.nt.Transform, pm.nt.Joint])
    general.check_type(b, 'b', [pm.nt.Transform, pm.nt.Joint])

    pos_a = pm.xform(a, q=1, ws=1, rp=1)
    pos_b = pm.xform(b, q=1, ws=1, rp=1)

    return general.assertAlmostEquals(pos_a, pos_b, 2)


def assertParentIs(obj=None, prnt=None):
    '''Assert prnt is the paprent of obj

    Attributes:
        obj -- Object that is to be checked
        prnt -- Expected parent  of obj
    '''
    general.check_type(obj, 'obj', [pm.nt.Transform, pm.nt.Joint])
    general.check_type(prnt, 'prnt', [pm.nt.Transform, pm.nt.Joint])

    if obj.getParent() == prnt:
        return True
    return False


def assertLocationIs(obj=None, pos=None):
    '''Assert obj is located at position pos

    Attributes:
        obj -- Object to check. (pm.nt.Transform, pm.nt.Joint)
        pos -- pm.dt.Point=(x, y, z)
    '''
    general.check_type(obj, 'obj', [pm.nt.Transform])
    general.check_type(pos, 'pos', [pm.dt.Point])

    return general.assertAlmostEquals(pm.dt.Point(pm.xform(obj,
                                                           q=1,
                                                           ws=1,
                                                           t=1)), pos, 3)


def assertAllZero(obj=None):
    '''Assert obj has zero translations/rotations/scale

    Attributes:
        obj -- Object to check. dt.Transform
    '''
    general.check_type(obj, 'obj', [pm.nt.Transform])

    expected = pm.dt.TransformationMatrix([[1.0, 0.0, 0.0, 0.0],
                                           [0.0, 1.0, 0.0, 0.0],
                                           [0.0, 0.0, 1.0, 0.0],
                                           [0.0, 0.0, 0.0, 1.0]])

    if obj.getTransformation() != expected:
        return False

    return True


def assertZeroTrans(obj=None):
    '''Assert obj has zero translations

    Attributes:
        obj -- Object to check. dt.Transform
    '''
    general.check_type(obj, 'obj', [pm.nt.Transform])

    return obj.getTranslation() == pm.dt.Vector([0, 0, 0])


def assertZeroRots(obj=None):
    '''Assert obj has zero rotations

    Attributes:
        obj -- Object to check. dt.Transform
    '''
    general.check_type(obj, 'obj', [pm.nt.Transform])

    return obj.getRotation() == pm.dt.EulerRotation([0, 0, 0])


def assertDefaultScale(obj=None):
    '''Assert obj has default scale of 1

    Attributes:
        obj -- Object to check. dt.Transform
    '''
    general.check_type(obj, 'obj', [pm.nt.Transform])

    return obj.getScale() == [1, 1, 1]
