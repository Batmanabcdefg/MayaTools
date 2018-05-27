import unittest

from tests import test_errors
from tests import test_general
from tests import test_transforms
from tests import test_joints

suites = []
suites.append(test_errors.suite())
suites.append(test_general.suite())
suites.append(test_transforms.suite())
suites.append(test_joints.suite())

alltests = unittest.TestSuite(suites)

unittest.TextTestRunner(verbosity=2).run(alltests)
