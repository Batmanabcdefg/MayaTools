import unittest

from lib import errors


class TestErrors(unittest.TestCase):
    def test_InputError(self):
        try:
            raise errors.InputError('arg1', '1', '0')
        except errors.InputError as e:
            self.assertEquals(str(e), 'arg1 passed 1. Expected 0.')

    def test_BuildError(self):
        try:
            raise errors.BuildError('func1', 'Failed because')
        except errors.BuildError as e:
            self.assertEqual(str(e), 'func1(): Failed because')

    def test_ObjectError(self):
        try:
            raise errors.ObjectError('obj1', 'a', 'b')
        except errors.ObjectError as e:
            self.assertEqual(str(e), 'Object: obj1 '
                                     'Expecting: a '
                                     'Got: b')


def suite():
    return unittest.TestLoader().loadTestsFromTestCase(TestErrors)

if __name__ == "__main__":
    unittest.__main__()
