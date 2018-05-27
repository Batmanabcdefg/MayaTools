import unittest
import pymel.core as pm
from tool.maya_testing import general
from tool.errors import errors


class TestGeneral(unittest.TestCase):

    def test_assertAlmostEquals_errors(self):
        self.assertRaises(errors.InputError,
                          general.assertAlmostEquals)
        self.assertRaises(errors.InputError,
                          general.assertAlmostEquals, [1], [1], 'a')

    def test_assertAlmostEquals(self):
        self.assertTrue(general.assertAlmostEquals([1.9991], [1.9995], 2))
        self.assertTrue(general.assertAlmostEquals([1, 2, 3],
                                                   [1, 2, 3]))
        self.assertTrue(general.assertAlmostEquals([1.0001, 2.0001, 2.9998],
                                                   [1.0005, 2.0007, 3.0007],
                                                   2))
        self.assertTrue(general.assertAlmostEquals([0.0, -1.110223e-16, 0.0],
                                                   [0, 0, 0]))
        self.assertTrue(general.assertAlmostEquals(['a', 'b', 'c'],
                                                   ['a', 'b', 'c']))
        self.assertTrue(general.assertAlmostEquals([[1, 2]], [[1, 2]], 4))

        self.assertFalse(general.assertAlmostEquals([1, 2, 3],
                                                    [2, 2, 3]))
        self.assertFalse(general.assertAlmostEquals(['a', 'b'],
                                                    ['a', 'c']))
        self.assertFalse(general.assertAlmostEquals(['a'],
                                                    ['a', 'b']))
        self.assertFalse(general.assertAlmostEquals([1], ['a']))

        v1 = pm.dt.Vector(0.013334, 2.34447, 3.22223)
        v2 = pm.dt.Vector(0.013335, 2.34446, 3.22226)
        self.assertTrue(general.assertAlmostEquals(v1, v2, 3))

    def test_check_type_errors(self):
        self.assertRaises(errors.InputError,
                          general.check_type)
        self.assertRaises(errors.InputError,
                          general.check_type, 'foo', 'bar')

    def test_check_type(self):
        for a in ['a', 1, ['a']]:
            self.assertTrue(general.check_type(a, 'a', [str, int, list]))
        self.assertRaises(errors.InputError,
                          general.check_type, 'a', 'a', [int])


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestGeneral)

if __name__ == "__main__":
    unittest.__main__()
