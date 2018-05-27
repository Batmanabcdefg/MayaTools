import unittest

from tests import test_snapshot
from tests import test_implement_snapshot
from tests import test_diff_snapshot

suites = []
suites.append(test_snapshot.suite())
suites.append(test_implement_snapshot.suite())
suites.append(test_diff_snapshot.suite())

alltests = unittest.TestSuite(suites)

unittest.TextTestRunner(verbosity=5).run(alltests)
