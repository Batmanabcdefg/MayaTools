import unittest
import pymel.core as pm
from tool.maya_testing import joints
from tool.maya_testing import transforms

from tool.errors import errors
from tool.rig import utils


class Test_utils_build_plane(unittest.TestCase):
    def setUp(self):
        pm.newFile(f=True)
        positions = [(0, x, 0) for x in range(14)]
        self.crv = pm.curve(p=positions, d=3)

    def test_build_plane_errors(self):
        # Bad inputs
        self.assertRaises(errors.InputError, utils.build_plane)
        self.assertRaises(errors.InputError, utils.build_plane, 'temp')

    def test_build_plane_errors_2(self):
        self.assertRaises(errors.InputError, utils.build_plane,
                          'temp', self.crv, 5, 'u', 'a')

    def test_build_plane_errors_3(self):
        self.assertRaises(errors.InputError, utils.build_plane,
                          'temp', self.crv, 5, 'a', 'x')

    def test_build_plane1(self):
        p = utils.build_plane(name='temp',
                              crv=self.crv,
                              spans=5,
                              direction='u',
                              width_axis='x',
                              width=1)

        self.assertEqual(p.boundingBox().center(),
                         self.crv.boundingBox().center())
        self.assertEqual(p.boundingBox().height(),
                         self.crv.boundingBox().height())
        self.assertEqual(p.getShape().numSpansInU(), 5)
        self.assertEqual(p.getShape().numSpansInV(), 2)

    def test_build_plane2(self):
        p = utils.build_plane(name='temp',
                              crv=self.crv,
                              spans=5,
                              direction='v',
                              width_axis='x',
                              width=1)

        self.assertEqual(p.boundingBox().center(),
                         self.crv.boundingBox().center())
        self.assertEqual(p.boundingBox().height(),
                         self.crv.boundingBox().height())
        self.assertEqual(p.getShape().numSpansInU(), 2)
        self.assertEqual(p.getShape().numSpansInV(), 5)


class Test_utils_build_joint_chain(unittest.TestCase):
    def setUp(self):
        pm.newFile(force=True)
        self.loc = pm.spaceLocator(p=(0, 0, -1))
        pm.move(0, 0, -1, self.loc)
        self.positions = [(0, y, 0) for y in range(11)]
        self.crv = pm.curve(p=self.positions, d=1)

    def test_build_joint_chain_errors(self):
        self.assertRaises(errors.InputError,
                          utils.build_joint_chain)
        self.assertRaises(errors.InputError,
                          utils.build_joint_chain,
                          'temp', 'foo', 'xyz', 10)
        self.assertRaises(errors.InputError,
                          utils.build_joint_chain,
                          'temp', self.crv, 'a', 10)
        self.assertRaises(errors.InputError,
                          utils.build_joint_chain,
                          'temp', self.crv, 'xyz', '10')

    def test_build_joint_chain(self):
        reg_node, chain = utils.build_joint_chain(name='temp',
                                                  crv=self.crv,
                                                  order='xyz',
                                                  num=10,
                                                  loc=self.loc)

        # Confirm right number of joints
        self.assertEqual(len(chain), 10)

        # Confirm expected names
        self.assertEqual([x.name() for x in chain],
                         ['temp_Jnt_%s' % (x+1) for x in range(10)])

        # Check positions match input curves'
        for jnt, pos in zip(chain, self.positions):
            self.assertTrue(transforms.assertLocationIs(jnt, pm.dt.Point(pos)))

        # Check aim axis is x
        for jnt in chain[:-1]:
            self.assertTrue(joints.assertAimAxis(jnt, 'x'))

        # Check for reg_node connection
        self.assertEqual(reg_node.temp_chain_root.listConnections()[0],
                         chain[0])

        # Check y axis pointing backwards (x, y, -1)
        for jnt in chain:
            loc = pm.spaceLocator()
            pm.delete(pm.parentConstraint(jnt, loc, mo=0))
            pm.move(loc, 0, 0, -1, r=1)
            pos = pm.xform(loc, q=1, ws=1, rp=1)
            self.assertAlmostEqual(pos[-1], -1)
            pm.delete(loc)


def suite():
    suites = unittest.TestLoader().\
        loadTestsFromTestCase(Test_utils_build_plane)
    suites.addTests(unittest.TestLoader().
                    loadTestsFromTestCase(Test_utils_build_joint_chain))
    return suites

if __name__ == "__main__":
    unittest.__main__()
