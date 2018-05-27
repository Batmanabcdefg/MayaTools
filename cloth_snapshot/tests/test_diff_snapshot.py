import unittest
import tempfile

import tool.diff_snapshot as ds


class Test_diff_snapshot(unittest.TestCase):
    def setUp(self):
        self.temp1 = tempfile.NamedTemporaryFile()
        self.temp1.writelines(['a:3:int', 'b:4.5:float', 'c:5:int'])
        self.temp2 = tempfile.NamedTemporaryFile()
        self.temp2.writelines(['a:5:int', 'b:4.7:float', 'c:5:int'])

    def tearDown(self):
        self.temp1.close()
        self.temp2.close()

    def test_get_diff(self):
        expected = {'a': [3, 5],
                    'b': [4.5, 4.7]}

        result = ds.get_diff(self.temp1.name, self.temp2.name)

        e_sorted = expected.keys()
        r_sorted = result.keys()
        e_sorted.sort()
        r_sorted.sort()

        for e, r in zip(e_sorted, r_sorted):
            self.assertEqual(e, r)
            self.assertEqual(expected[e], result[r])


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Test_diff_snapshot)

if __name__ == '__main__':
    unittest.__main__()
