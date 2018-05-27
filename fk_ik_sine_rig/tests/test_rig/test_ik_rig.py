import unittest
import pymel.core as pm

from tool.errors import errors
from tool.rig import ik_rig
from tool.maya_testing import transforms


class Test_ik_rig(unittest.TestCase):
    def setUp(self):
        pm.newFile(force=True)

    def test_ik_rig_build_errors(self):
        self.assertRaises(errors.InputError,
                          ik_rig.build)
        self.assertRaises(errors.InputError,
                          ik_rig.build,
                          'curve', 'loc', 'num')

        pos = [(0, y, 0) for y in range(15)]
        crv = pm.curve(p=pos)
        loc = pm.spaceLocator()

        self.assertRaises(errors.InputError,
                          ik_rig.build,
                          crv, 'loc', 'num_jnts', 'num_cnts')
        self.assertRaises(errors.InputError,
                          ik_rig.build,
                          crv, loc, 'num_jnts', 'num_cnts')
        self.assertRaises(errors.InputError,
                          ik_rig.build,
                          crv, 'loc', 5, 'num_cnts')
        self.assertRaises(errors.InputError,
                          ik_rig.build,
                          crv, loc, 5, 1, 'xyz')
        self.assertRaises(errors.InputError,
                          ik_rig.build,
                          crv, 'loc', 5, 2, 'xyz')
        self.assertRaises(errors.InputError,
                          ik_rig.build,
                          crv, loc, 5, 2, 'xya')

    def test_ik_rig_build(self):
        pos = [(0, y, 0) for y in range(15)]
        crv = pm.curve(p=pos)
        loc = pm.spaceLocator(p=(0, 0, -1))

        reg_node = ik_rig.build('temp', crv, loc, 10, 4, 'xyz')

        # Check controls connected to reg_node
        cnts = [pm.PyNode('temp%s_ik_cnt' % (x+1)) for x in range(3)]

        for c in cnts:
            attr = getattr(reg_node, c.name())
            self.assertEqual(attr.listConnections()[0].name(), c)

        # Confirm ik joint chain root connected to reg_node
        self.assertEqual(reg_node.temp_chain_root.listConnections()[0].
                         name(), 'temp_Jnt_1')

        # Confirm heirarchy
        tn = pm.PyNode('temp_ik_rig_grp')
        cnts_grp = pm.PyNode('temp_cnts_grp')
        jnts_grp = pm.PyNode('temp_ik_skin_jnts_grp')
        dont_move = pm.PyNode('temp_dont_move_grp')
        fol_grp = pm.PyNode('temp_follicle_grp')
        self.assertTrue(pm.PyNode(tn).objExists())
        self.assertTrue(
            transforms.assertParentIs(cnts_grp, tn))
        self.assertTrue(
            transforms.assertParentIs(jnts_grp, tn))
        self.assertTrue(
            transforms.assertParentIs(dont_move, tn))
        self.assertTrue(
            transforms.assertParentIs(fol_grp, tn))


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Test_ik_rig)

if __name__ == "__main__":
    unittest.__main__()
