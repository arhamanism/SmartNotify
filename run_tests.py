# run_tests.py
"""
Run all unit tests for the Smart Notification System.

Usage:
    python run_tests.py           # run all tests
    python run_tests.py -v        # verbose output
"""

import sys
import os
import unittest

# Ensure root is on the path so all imports resolve
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tests.test_singleton   import TestSingletonPattern
from tests.test_factory     import TestFactoryPattern
from tests.test_strategy    import TestStrategyPattern
from tests.test_observer    import TestObserverPattern
from tests.test_integration import TestIntegration


def run_all_tests():
    loader = unittest.TestLoader()
    suite  = unittest.TestSuite()

    test_classes = [
        TestSingletonPattern,
        TestFactoryPattern,
        TestStrategyPattern,
        TestObserverPattern,
        TestIntegration,
    ]

    for cls in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(cls))

    print("=" * 70)
    print("  Smart Notification System — Test Suite")
    print("=" * 70)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 70)
    if result.wasSuccessful():
        print(f"  ALL {result.testsRun} TESTS PASSED ✓")
    else:
        print(f"  {len(result.failures)} failure(s), "
              f"{len(result.errors)} error(s) out of {result.testsRun} tests")
    print("=" * 70)

    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    run_all_tests()
