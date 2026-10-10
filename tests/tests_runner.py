import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
TEST_PATTERN = "test_*.py"


def run_all_tests():
    """Discover and run all unit, regression, and application tests."""
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir=str(TESTS_DIR), pattern=TEST_PATTERN, top_level_dir=str(TESTS_DIR.parent))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit code for CI systems (GitHub, etc.)
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    run_all_tests()
