import unittest as unittest
import os
import re
import sys
import argparse

def compileRegExPattern(pattern):
    regex = None
    try:
        regex = re.compile(include_test_filename_pattern)
    except:
        etype, evalue, etb = sys.exc_info()
        print("RegEx error for pattern %s. Exception: %s, Error: %s." % (include_test_filename_pattern, etype, evalue))
        exit()
    return regex

if __name__ == "__main__":
    test_dir = os.path.dirname(os.path.realpath(__file__))
    parser = argparse.ArgumentParser()
    parser.add_argument("--include", help="Regex pattern to include select tests. Default: Test*.py")
    parser.add_argument("--exclude", help="Regex pattern to exclude select tests. Default: None")
    args = parser.parse_args()
    include_test_filename_pattern = 'Test*.py' if not args.include else args.include
    os.chdir(test_dir)
    all_tests = unittest.TestLoader().discover('.', pattern=include_test_filename_pattern)
    unittest.TextTestRunner(verbosity=2).run(all_tests)
