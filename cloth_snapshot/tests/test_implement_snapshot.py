import unittest
from mock import MagicMock
from mock import patch
import pymel.core as pm
from pymel.core.runtime import nClothCreate

import tool.implement_snapshot as ims


class Test_implement_snapshot(unittest.TestCase):
    @patch('os.path.exists')
    @patch('__builtin__.open')
    def test_get_dict(self, open_mock, os_mock):
        file_mock = MagicMock('file_mock')
        file_mock.readlines =\
            MagicMock(return_value=
                        ["bounce:3.0:<type 'float'>\n",
                         "evaluationOrder:1:<type 'int'>\n",
                         "planeNormal:(0.0, 1.0, 0.0):<type 'tuple'>"])
        file_mock.close = MagicMock()
        open_mock.return_value = file_mock

        f = '/path/to/foo.txt'
        expected = {'bounce': 3.0,
                    'evaluationOrder': 1,
                    'planeNormal': (0.0, 1.0, 0.0)}

        result = ims.get_dict(f)

        self.assertTrue(file_mock.close.called)
        self.assertTrue(os_mock.called)
        open_mock.assert_called_with(f, 'r')
        self.assertTrue(file_mock.readlines.called)
        self.assertEqual(expected, result)

    def test_apply_dict(self):
        # New scene
        pm.newFile(f=True)

        # Create plane and ncloth
        self.plane = pm.polyPlane()[0]
        pm.select(self.plane, r=1)

        nClothCreate()

        self.ncloth = pm.PyNode('nCloth1')
        self.nucleus = pm.PyNode('nucleus1')

        d = {'bounce': 3.0,
             'evaluationOrder': 1}

        ims.apply_dict(self.ncloth, d)

        self.assertEqual(self.ncloth.getShape().
                         bounce.get(), 3.0)
        self.assertEqual(self.ncloth.getShape().
                         evaluationOrder.get(), 1)

        d = {'planeNormal': (0.0, 0.0, 1.0)}

        ims.apply_dict(self.nucleus, d)

        self.assertEqual(self.nucleus.planeNormal.get(), (0.0, 0.0, 1.0))


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Test_implement_snapshot)

if __name__ == '__main__':
    unittest.__main__()
