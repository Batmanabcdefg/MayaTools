import pymel.core as pm
import unittest

from tool.errors import errors
from tool.rig import fk_rig
from tool.maya_testing import transforms


class Test_make_control(unittest.TestCase):
    def setUp(self):
        pm.newFile(force=True)
        self.positions = [(0, y, 0) for y in range(5)]
        self.jnts = []
        for pos in self.positions:
            self.jnts.append(pm.joint(p=pos))

    def test_make_control_errors(self):
        self.assertRaises(errors.InputError,
                          fk_rig.make_control)
        self.assertRaises(errors.InputError,
                          fk_rig.make_control, 'foo')

    def test_make_control(self):
        controls = []
        reg_node = None
        for i in range(5):
            if i == 0:
                reg_node, control = fk_rig.make_control(name='temp%s' %
                                                        str(i+1),
                                                        obj=self.jnts[i],
                                                        buffers=2,
                                                        color='light_blue',
                                                        scale=3.0,
                                                        typ='cube')
            else:
                reg_node, control = fk_rig.make_control(name='temp%s' %
                                                        str(i+1),
                                                        obj=self.jnts[i],
                                                        buffers=2,
                                                        color='light_blue',
                                                        scale=3.0,
                                                        typ='cube',
                                                        reg_node=reg_node)
            controls.append(control)

        self.assertEqual(len(controls), 5)

        count = 0
        for cnt, jnt in zip(controls, self.jnts):
            name = 'temp%s' % (count+1)
            for s in cnt.getShapes():
                self.assertEqual(s.overrideColor.get(), 6)
            self.assertTrue(transforms.assertOrientationMatches(cnt, jnt))
            attr = getattr(reg_node, cnt.name())
            self.assertEqual(attr.listConnections()[0], cnt)
            self.assertEqual(cnt.name().split('_')[0], name)
            self.assertTrue(transforms.assertLocationsMatch(cnt, jnt))
            self.assertTrue(transforms.assertAllZero(cnt))

            # Check that joint is under curve
            pm.select(cnt, hi=True, r=True)
            sel = pm.ls(sl=1)
            self.assertIn(jnt, sel)
            pm.select(clear=True)

            # Check heirarchy
            try:
                p1 = cnt.getParent()
                p2 = p1.getParent()
                if count > 0:
                    prnt = p2.getParent()
                    self.assertEqual(prnt, self.jnts[count-1])
                self.assertTrue(transforms.assertAllZero(p1))
                self.assertEqual(p1.name(), '%s_btm_node' % name)
                self.assertEqual(p2.name(), '%s_top_node' % name)
            except Exception as e:
                str_1 = 'Heirarchy check failed: Error: ', str(e)
                self.fail(str_1)
            count += 1


class Test_build(unittest.TestCase):
    def test_build_errors(self):
        self.assertRaises(errors.InputError, fk_rig.build)
        self.assertRaises(errors.InputError, fk_rig.build,
                          name=2, crv=1, loc=1, order='a',
                          num='a', buffers='a', color=1,
                          scale='a', typ=1, reg_node=1)

        self.assertRaises(errors.InputError, fk_rig.build,
                          name='temp', crv=1, loc=1, order='a',
                          num='a', buffers='a', color=1,
                          scale='a', typ=1, reg_node=1)

    def test_build(self):
        crv = pm.curve(p=[(0, 0, 0),
                          (0, 1, 0),
                          (0, 2, 0),
                          (0, 3, 0)])
        loc = pm.spaceLocator(p=(0, 0, -2))
        reg_node = fk_rig.build(name='temp', crv=crv, loc=loc, order='xyz',
                                num=5, buffers=3, color='yellow',
                                scale=0.5, typ='circle')

        cnts = ['temp_%s' % (x+1) for x in range(5)]
        jnts = ['temp_Jnt_%s' % (x+1) for x in range(5)]
        for c, j in zip(cnts, jnts):
            self.assertTrue(pm.PyNode(c).objExists())
            self.assertTrue(pm.PyNode(j).objExists())

        self.assertTrue(hasattr(reg_node, 'fk_top_node'))


def suite():
    suites = unittest.TestLoader().loadTestsFromTestCase(Test_make_control)
    suites.addTests(unittest.TestLoader().
                    loadTestsFromTestCase(Test_build))
    return suites

if __name__ == "__main__":
    unittest.__main__()
