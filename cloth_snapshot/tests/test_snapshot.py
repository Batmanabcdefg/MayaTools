import tempfile
import unittest
from datetime import datetime
import os
import pymel.core as pm
from pymel.core.runtime import nClothCreate
from mock import patch

import tool.snapshot as ss


class Test_snapshot(unittest.TestCase):
    def setUp(self):
        # New scene
        pm.newFile(f=True)

        # Get ncloth attributes from file
        self.ncloth_attrs = []
        self.ncloth_attrsFile = os.path.dirname(__file__).\
            replace('tests', 'tool')
        self.ncloth_attrsFile = self.ncloth_attrsFile + \
            os.sep + 'ncloth_attrs.txt'

        if not os.path.exists(self.ncloth_attrsFile):
            msg = 'File not found: ', self.ncloth_attrsFile
            raise Exception(msg)

        f = open(self.ncloth_attrsFile, 'r')
        self.ncloth_attrs = f.readlines()
        f.close()

        # Get nucleus attributes from file
        self.nucleus_attrs = []
        self.nucleus_attrsFile = os.path.dirname(__file__).\
            replace('tests', 'tool')
        self.nucleus_attrsFile = self.nucleus_attrsFile + \
            os.sep + 'nucleus_attrs.txt'

        if not os.path.exists(self.nucleus_attrsFile):
            msg = 'File not found: ', self.nucleus_attrsFile
            raise Exception(msg)

        f = open(self.nucleus_attrsFile, 'r')
        self.nucleus_attrs = f.readlines()
        f.close()

        # Create plane and ncloth
        self.plane = pm.polyPlane()[0]
        pm.select(self.plane, r=1)

        nClothCreate()

        self.ncloth = pm.PyNode('nCloth1')
        self.nucleus = pm.PyNode('nucleus1')

        # Create expected name
        now = datetime.now()
        self.name = self.ncloth.name() + '_' + \
            str(now.year) + '-' + str(now.month) + '-' + \
            str(now.day) + '_' + \
            str(now.hour) + '-' + str(now.minute)

    def test_make_dict_ncloth(self):
        d = ss.make_dict(node=self.ncloth, typ='ncloth')
        self.assertEqual(len(d.keys()), len(self.ncloth_attrs))
        keys = d.keys()
        keys.sort()
        self.ncloth_attrs.sort()

        for k, a in zip(keys, self.ncloth_attrs):
            self.assertEqual(k, a.strip())

    def test_make_dict_nucleus(self):
        d = ss.make_dict(node=self.nucleus, typ='nucleus')
        self.assertEqual(len(d.keys()), len(self.nucleus_attrs))
        keys = d.keys()
        keys.sort()
        self.nucleus_attrs.sort()

        for k, a in zip(keys, self.nucleus_attrs):
            self.assertEqual(k, a.strip())

    def test_gen_filename(self):
        name = ss.gen_filename(node=self.ncloth)
        self.assertEqual(name, (self.name + '.txt'))

    def test_make_file(self):
        tempPath = tempfile.mkdtemp()
        d = {'a': 1, 'b': 'z'}
        name = str(tempPath + os.sep + self.name + '.txt')
        expected = ['a:1:int', 'b:z:str', '}']

        ss.make_file(name=name, data=d)

        self.assertTrue(os.path.exists(name))

        f = open(name, 'r')
        written = f.readlines()
        f.close()

        self.assertTrue(written, expected)

    @patch('tool.snapshot.make_file')
    @patch('tool.snapshot.gen_filename')
    @patch('tool.snapshot.make_dict')
    def test_take_snapshot(self,
                           dict_mock,
                           gen_mock,
                           file_mock):
        path = '/foo/bar'
        d = {'attr': 1}
        dict_mock.return_value = d
        gen_mock.return_value = 'biz'

        pm.select(self.ncloth, self.nucleus, r=1)
        results = ss.take_snapshot(path=path)

        expected = ['Created: /foo/bar/biz',
                    'Created: /foo/bar/biz']

        self.assertEquals(expected, results)

        dict_mock.assert_any_call(self.ncloth, 'ncloth')
        gen_mock.assert_any_call(self.ncloth)
        file_mock.assert_any_call('/foo/bar/biz', d)

        dict_mock.assert_any_call(self.nucleus, 'nucleus')
        gen_mock.assert_any_call(self.nucleus)
        file_mock.assert_any_call('/foo/bar/biz', d)


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(Test_snapshot)

if __name__ == '__main__':
    unittest.__main__()
