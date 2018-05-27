import unittest

from tests.test_errors import test_errors

from tests.test_maya_testing import test_joints
from tests.test_maya_testing import test_transforms
from tests.test_maya_testing import test_general
from tests.test_rig import test_combine_rig
from tests.test_rig import test_fk_rig
from tests.test_rig import test_ik_rig
from tests.test_rig import test_sine_rig
from tests.test_rig import test_control
from tests.test_rig import test_utils

suites = []
suites.append(test_general.suite())
suites.append(test_errors.suite())
suites.append(test_joints.suite())
suites.append(test_transforms.suite())
suites.append(test_combine_rig.suite())
suites.append(test_fk_rig.suite())
suites.append(test_utils.suite())
suites.append(test_ik_rig.suite())
suites.append(test_sine_rig.suite())
suites.append(test_control.suite())

alltests = unittest.TestSuite(suites)

unittest.TextTestRunner(verbosity=2).run(alltests)
