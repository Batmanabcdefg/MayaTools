import unittest
import pymel.core as pm

from lib import joints
from lib import errors


class TestJoints(unittest.TestCase):
    def setUp(self):
        pm.newFile(force=True)
        self.joints = []
        self.joints.append(pm.joint(p=(0, 0, 0)))
        self.joints.append(pm.joint(p=(0, 1, 0)))
        self.joints.append(pm.joint(p=(0, 2, 0)))

    def test_assertAimAxis_errors(self):
        self.assertRaises(errors.InputError, joints.assertAimAxis)
        self.assertRaises(errors.InputError, joints.assertAimAxis, 'foo', 'x')
        self.assertRaises(errors.InputError, joints.assertAimAxis,
                          self.joints[0], 'a')
        self.assertRaises(errors.ObjectError, joints.assertAimAxis,
                          self.joints[-1], 'x')

    def test_assertAimAxis(self):
        pm.joint(self.joints[0], e=1, oj='yzx')
        self.assertFalse(joints.assertAimAxis(self.joints[0], 'x'))
        pm.joint(self.joints[0], e=1, oj='xyz')
        self.assertFalse(joints.assertAimAxis(self.joints[0], 'y'))
        pm.joint(self.joints[0], e=1, oj='xyz')
        self.assertFalse(joints.assertAimAxis(self.joints[0], 'z'))

        pm.joint(self.joints[0], e=1, oj='xyz')
        self.assertTrue(joints.assertAimAxis(self.joints[0], 'x'))
        pm.joint(self.joints[0], e=1, oj='yxz')
        self.assertTrue(joints.assertAimAxis(self.joints[0], 'y'))
        pm.joint(self.joints[0], e=1, oj='zyx')
        self.assertTrue(joints.assertAimAxis(self.joints[0], 'z'))


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestJoints)

if __name__ == "__main__":
    unittest.__main__()
