import unittest
import pymel.core as pm
from tool.errors import errors
from tool.rig import combine_rig
from tool.maya_testing import transforms


class Test_combine_rig(unittest.TestCase):
    def test_combine_rig_build_errors(self):
        self.assertRaises(errors.InputError,
                          combine_rig.build)

    def test_combine_rig_build(self):
        pos = [(0, y, 0) for y in range(15)]
        crv = pm.curve(p=pos)
        loc = pm.spaceLocator(p=(0, 0, -1))

        reg_node = combine_rig.build(name='temp',
                                     crv=crv,
                                     loc=loc,
                                     ik_jnts=10,
                                     ik_cnts=4,
                                     ik_order='xyz',
                                     fk_order='xyz',
                                     fk_num=5,
                                     fk_buffers=2,
                                     fk_color='light_blue',
                                     fk_scale=1.0,
                                     fk_typ='cube')
        # Test sine
        ik_cnt = reg_node.tempIK1_ik_cnt.listConnections()[0]
        for a in ['wavelength', 'amplitude', 'sineOffOn',
                  'offset', 'direction']:
            print '%s.%s' % (ik_cnt, a)
            self.assertTrue(hasattr(ik_cnt, a))

        self.assertTrue(pm.PyNode('tempIK_sineDeformer').objExists())

        # Test ik
        # Check controls connected to reg_node
        cnts = [pm.PyNode('tempIK%s_ik_cnt' % (x+1)) for x in range(3)]

        for c in cnts:
            attr = getattr(reg_node, c.name())
            self.assertEqual(attr.listConnections()[0].name(), c)

        # Confirm ik joint chain root connected to reg_node
        self.assertEqual(reg_node.tempIK_chain_root.
                         listConnections()[0].name(),
                         'tempIK_Jnt_1')

        # Test fk
        cnts = ['tempFK_%s' % (x+1) for x in range(5)]
        jnts = ['tempFK_Jnt_%s' % (x+1) for x in range(5)]
        for c, j in zip(cnts, jnts):
            self.assertTrue(pm.PyNode(c).objExists())
            self.assertTrue(pm.PyNode(j).objExists())

        # Check heirarchy
        sine = reg_node.sine_handle.listConnections()[0]
        ik_top = reg_node.ik_top_node.listConnections()[0]
        fk_top = reg_node.fk_top_node.listConnections()[0]
        rig_top = reg_node.rig_top_node.listConnections()[0]

        self.assertTrue(sine.objExists())
        self.assertTrue(ik_top.objExists())
        self.assertTrue(fk_top.objExists())
        self.assertTrue(rig_top.objExists())

        self.assertTrue(transforms.
                        assertParentIs(sine.getParent(), rig_top))
        self.assertTrue(transforms.assertParentIs(ik_top, rig_top))
        self.assertTrue(transforms.assertParentIs(fk_top, rig_top))


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Test_combine_rig)

if __name__ == "__main__":
    unittest.__main__()
