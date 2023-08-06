import unittest

from b2.tests.test_selection_loop import TestSelections
from b2.tests.test_linking import TestLinking


if __name__ == '__main__':
    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner()
    suite = unittest.TestSuite(map(loader.loadTestsFromTestCase, [TestLinking, TestSelections]))
    runner.run(suite)
