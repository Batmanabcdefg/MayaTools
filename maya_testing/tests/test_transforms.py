import unittest
import pymel.core as pm

from lib import transforms
from lib import errors


class TestTransforms(unittest.TestCase):
    def setUp(self):
        pm.newFile(force=True)
        self.joints = []
        self.joints.append(pm.joint(p=(0, 0, 0)))
        self.joints.append(pm.joint(p=(0, 1, 0)))
        self.joints.append(pm.joint(p=(0, 2, 0)))

    def test_assertAimingAt_errors(self):
        self.assertRaises(errors.InputError,
                          transforms.assertAimingAt)
        self.assertRaises(errors.InputError,
                          transforms.assertAimingAt, 'foo')
        self.assertRaises(errors.InputError,
                          transforms.assertAimingAt, 'foo', 'bar')
        g = pm.group(empty=1)
        self.assertRaises(errors.InputError,
                          transforms.assertAimingAt, g, g, 3)
        self.assertRaises(errors.InputError,
                          transforms.assertAimingAt, g, g, 'a')

    def test_assertAimingAt(self):
        a = pm.group(empty=1)
        b = pm.group(empty=1)
        pm.move(3, 3, 3, b, a=1)

        self.assertFalse(transforms.assertAimingAt(a, b, 'x'))
        pm.aimConstraint(b, a)
        self.assertFalse(transforms.assertAimingAt(a, b, 'y'))
        self.assertFalse(transforms.assertAimingAt(a, b, 'z'))

        self.assertTrue(transforms.assertAimingAt(a, b, 'x'))

    def test_assertOrientationMatches_errors(self):
        self.assertRaises(errors.InputError,
                          transforms.assertOrientationMatches)
        self.assertRaises(errors.InputError,
                          transforms.assertOrientationMatches, 'foo')
        self.assertRaises(errors.InputError,
                          transforms.assertOrientationMatches, 'foo', 'bar')
        g = pm.group(empty=1)
        self.assertRaises(errors.InputError,
                          transforms.assertOrientationMatches, g, 'foo')

    def test_assertOrientationMatches(self):
        a = pm.circle()[0]
        b = pm.circle()[0]
        self.assertTrue(transforms.assertOrientationMatches(a, b))
        b.rx.set(90)
        self.assertFalse(transforms.assertOrientationMatches(a, b))

    def test_assertLocationsMatch_errors(self):
        self.assertRaises(errors.InputError,
                          transforms.assertLocationsMatch)
        self.assertRaises(errors.InputError,
                          transforms.assertLocationsMatch,
                          'obj1', 'obj2')

    def test_assertLocationsMatch(self):
        self.assertTrue(transforms.assertLocationsMatch(self.joints[0],
                                                        self.joints[0]))
        self.assertFalse(transforms.assertLocationsMatch(self.joints[0],
                                                         self.joints[1]))

    def test_assertParentIs_errors(self):
        self.assertRaises(errors.InputError,
                          transforms.assertParentIs,
                          'foo', 'x')
        self.assertRaises(errors.InputError,
                          transforms.assertParentIs,
                          self.joints[0], 'x')
        self.assertRaises(errors.InputError,
                          transforms.assertParentIs,
                          'foo', self.joints[0])

    def test_assertParentIs(self):
        self.assertFalse(transforms.assertParentIs(self.joints[0],
                                                   self.joints[1]))
        self.assertFalse(transforms.assertParentIs(self.joints[0],
                                                   self.joints[0]))
        self.assertTrue(transforms.assertParentIs(self.joints[1],
                                                  self.joints[0]))
        self.assertTrue(transforms.assertParentIs(self.joints[2],
                                                  self.joints[1]))

    def test_assertLocationIs_errors(self):
        self.assertRaises(errors.InputError,
                          transforms.assertLocationIs,
                          'foo', 'bar')
        self.assertRaises(errors.InputError,
                          transforms.assertLocationIs,
                          self.joints[0], 'bar')
        self.assertRaises(errors.InputError,
                          transforms.assertLocationIs,
                          self.joints[0], [0, 0, 0])

    def test_assertLocationIs(self):
        self.assertFalse(transforms.assertLocationIs(self.joints[0],
                                                     pm.dt.Point(0, 1, 0)))
        self.assertFalse(transforms.assertLocationIs(self.joints[1],
                                                     pm.dt.Point(0, 3, 0)))
        self.assertFalse(transforms.assertLocationIs(self.joints[0],
                                                     pm.dt.Point(0, 1, 0)))

        self.assertTrue(transforms.assertLocationIs(self.joints[0],
                                                    pm.dt.Point(0, 0, 0)))
        self.assertTrue(transforms.assertLocationIs(self.joints[1],
                                                    pm.dt.Point(0, 1.0001, 0)))
        self.assertTrue(transforms.assertLocationIs(self.joints[2],
                                                    pm.dt.Point(0, 2, 0)))

    def test_assertAllZero_errors(self):
        self.assertRaises(errors.InputError, transforms.assertAllZero)
        self.assertRaises(errors.InputError, transforms.assertAllZero, 'foo')

    def test_assertAllZero(self):
        self.assertTrue(transforms.assertAllZero(self.joints[0]))
        self.joints[0].rx.set(5)
        self.assertFalse(transforms.assertAllZero(self.joints[0]))
        self.joints[0].rx.set(0)
        self.joints[0].sx.set(5)
        self.assertFalse(transforms.assertAllZero(self.joints[0]))
        self.assertFalse(transforms.assertAllZero(self.joints[1]))

    def test_assertZeroTrans_errors(self):
        self.assertRaises(errors.InputError, transforms.assertZeroTrans)
        self.assertRaises(errors.InputError, transforms.assertZeroTrans,
                          'foo')

    def test_assertZeroTrans(self):
        self.assertTrue(transforms.assertZeroTrans(self.joints[0]))
        self.assertFalse(transforms.assertZeroTrans(self.joints[1]))

    def test_assertZeroRots_errors(self):
        self.assertRaises(errors.InputError, transforms.assertZeroRots)
        self.assertRaises(errors.InputError, transforms.assertZeroRots, 'foo')

    def test_assertZeroRots(self):
        self.assertTrue(transforms.assertZeroRots(self.joints[0]))
        self.joints[0].rx.set(5)
        self.assertFalse(transforms.assertZeroRots(self.joints[0]))

    def test_assertDefaultScale_errors(self):
        self.assertRaises(errors.InputError, transforms.assertDefaultScale)
        self.assertRaises(errors.InputError, transforms.assertDefaultScale,
                          'foo')

    def test_assertDefaultScale(self):
        self.assertTrue(transforms.assertDefaultScale(self.joints[0]))
        self.joints[0].sx.set(2)
        self.assertFalse(transforms.assertDefaultScale(self.joints[0]))
        self.joints[0].sx.set(1)
        self.joints[0].sy.set(2)
        self.assertFalse(transforms.assertDefaultScale(self.joints[0]))
        self.joints[0].sy.set(1)
        self.joints[0].sz.set(2)
        self.assertFalse(transforms.assertDefaultScale(self.joints[0]))


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestTransforms)

if __name__ == "__main__":
    unittest.__main__()
