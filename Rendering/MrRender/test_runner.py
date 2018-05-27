import unittest

import test_mr_render

suites = []
suites.append(test_flatten_scene.suite())

alltests = unittest.TestSuite(suites)

unittest.TextTestRunner(verbosity=5).run(alltests)