import pymel.core as pm
import unittest

from tool.errors import errors
from tool.rig import control
from tool.maya_testing import transforms


class Test_control(unittest.TestCase):
    def setUp(self):
        pm.newFile(force=True)

    def test_create_curve_errors(self):
        self.assertRaises(errors.InputError,
                          control.create_curve)
        self.assertRaises(errors.InputError,
                          control.create_curve,
                          'temp')
        self.assertRaises(errors.InputError,
                          control.create_curve,
                          'temp', typ='circle', scale='a')

    def test_create_curve_new_reg_node(self):
        reg_node, cnt = control.create_curve(name='temp',
                                             typ='circle',
                                             scale=3.0,
                                             color='light_blue')
        for s in cnt.getShapes():
            self.assertEqual(s.overrideColor.get(), 6)
        self.assertEqual(reg_node.temp.listConnections()[0], cnt)
        self.assertTrue(isinstance(cnt, pm.nt.Transform))
        self.assertTrue(isinstance(cnt.getShape(), pm.nt.NurbsCurve))

    def test_create_curve_existing_reg_node(self):
        reg_node = pm.group(empty=1)
        reg_node.addAttr('version', dt="string")
        reg_node.addAttr('reg_node', dt="string")
        reg_node2, cnt = control.create_curve(name='temp',
                                              typ='circle',
                                              scale=3.0,
                                              color='light_blue',
                                              reg_node=reg_node)
        for s in cnt.getShapes():
            self.assertEqual(s.overrideColor.get(), 6)
        self.assertEqual(reg_node, reg_node2)
        self.assertEqual(reg_node.temp.listConnections()[0], cnt)
        self.assertTrue(isinstance(cnt, pm.nt.Transform))
        self.assertTrue(isinstance(cnt.getShape(), pm.nt.NurbsCurve))

    def test_create_heirarchy_errors(self):
        self.assertRaises(errors.InputError,
                          control.create_heirarchy)
        self.assertRaises(errors.InputError,
                          control.create_heirarchy,
                          'temp', 'obj1')

    def test_create_heirarchy(self):
        # Test on object with parent
        jnts = []
        jnts.append(pm.joint(p=(1, 1, 1)))
        jnts.append(pm.joint(p=(2, 2, 2)))
        crv = pm.circle()[0]
        pm.delete(pm.parentConstraint(jnts[-1], crv, mo=0))
        pm.parent(crv, jnts[-1])

        grps = control.create_heirarchy('temp', crv, 5)

        count = 0
        for g in grps:
            self.assertTrue(
                transforms.assertLocationsMatch(g, crv))
            self.assertTrue(
                transforms.assertDefaultScale(g))
            if count > 0:
                self.assertTrue(
                    transforms.assertAllZero(g))
                self.assertTrue(
                    transforms.assertParentIs(g, grps[count-1]))
            count += 1

        self.assertEqual(grps[0].name(), 'temp_top_node')
        self.assertEqual(grps[-1].name(), 'temp_btm_node')
        self.assertTrue(transforms.assertParentIs(crv,
                                                  grps[-1]))
        self.assertTrue(transforms.assertParentIs(grps[0],
                                                  jnts[-1]))
        self.assertTrue(transforms.assertAllZero(crv))
        self.assertTrue(transforms.assertDefaultScale(crv))

    def test_match_object_errors(self):
        self.assertRaises(errors.InputError,
                          control.match_object)
        self.assertRaises(errors.InputError,
                          control.match_object, 'foo')
        self.assertRaises(errors.InputError,
                          control.match_object, 'foo', 'bar')
        crv = pm.circle()[0]
        self.assertRaises(errors.InputError,
                          control.match_object, crv, 'bar')

    def test_match_object(self):
        a = pm.circle()[0]
        b = pm.circle()[0]

        b.rx.set(75)
        b.ry.set(75)
        b.rz.set(75)

        self.assertFalse(transforms.assertOrientationMatches(a, b))
        control.match_object(a, b)
        self.assertTrue(transforms.assertOrientationMatches(a, b))

    def testcreate_register_node_errors(self):
        self.assertRaises(errors.InputError,
                          control.create_register_node)

    def test_create_register_node(self):
        node = control.create_register_node(name='temp')
        self.assertTrue(isinstance(node, pm.nt.Transform))
        self.assertEqual(node.name(), 'temp_reg_node')
        for attr in ['reg_node', 'version']:
            self.assertTrue(hasattr(node, attr))
        self.assertEqual(node.getParent(), None)

    def test_register_object_errors(self):
        self.assertRaises(errors.InputError,
                          control.register_object)
        self.assertRaises(errors.InputError,
                          control.register_object, 'foo', 'bar')
        node = pm.group(empty=1)
        self.assertRaises(errors.InputError,
                          control.register_object, node, 'bar')

    def test_register_object(self):
        obj = pm.joint(n='jnt_1')
        node = control.create_register_node(name='temp')
        control.register_object(node, 'temp', obj)
        self.assertEqual(node.temp.listConnections()[0], obj)


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Test_control)

if __name__ == "__main__":
    unittest.__main__()
