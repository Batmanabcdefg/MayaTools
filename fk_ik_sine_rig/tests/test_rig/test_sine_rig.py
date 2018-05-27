import unittest
import pymel.core as pm
from tool.errors import errors
from tool.rig import sine_rig


class Test_sine_rig(unittest.TestCase):
    def test_sine_rig_build_errors(self):
        self.assertRaises(errors.InputError, sine_rig.build)
        self.assertRaises(errors.InputError, sine_rig.build,
                          'temp', 'plane', 'reg_node')

    def test_sine_rig_build(self):
        name = 'temp'
        crv = pm.circle()[0]
        reg_node = pm.nt.Transform()
        cnt = pm.circle()[0]
        reg_node.addAttr('temp1_ik_cnt', at='message')
        reg_node.addAttr('version', at='message')
        reg_node.addAttr('reg_node', at='message')
        cnt.message >> reg_node.temp1_ik_cnt

        reg_node = sine_rig.build(name, crv, reg_node)

        for a in ['wavelength', 'amplitude', 'sineOffOn',
                  'offset', 'direction']:
            self.assertTrue(hasattr(cnt, a))

        self.assertTrue(hasattr(reg_node, 'sine_handle'))
        self.assertTrue(pm.PyNode('%s_sineDeformer' % name).objExists())


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Test_sine_rig)

if __name__ == "__main__":
    unittest.__main__()
