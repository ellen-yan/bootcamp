# py.test gives the testing functionality
import pytest

import bioinfo_dicts

# TDD, paradigm of developing software. Idea: programmer thinks about
# a design specification for a bit of code, lays out what input and
# output should be, then writes a test for that code and updates code
# to pass the test. Do this incrementally.

# Use cases that we have not thought of might creep up. For everything
# that happens or a bug that's found, write another test that covers it.
# Importantly, any time you update your code, you need to run ALL of
# your tests

def n_neg(seq):
    """Number of negative residues in a protein sequence"""

    # Convert sequence to upper case
    seq = seq.upper()

    # Check for a valid sequence
    for aa in seq:
        if aa not in bioinfo_dicts.aa.keys():
            raise RuntimeError(aa + ' is not a valid amino acid.')

    # Count E's and D's, since these are the negative residues
    return seq.count('E') + seq.count('D')

# def test_n_neg():
#     """Perform unit tests on n_neg."""
#
#     assert n_neg('E') == 1
#     assert n_neg('D') == 1
#     assert n_neg('') == 0
#     assert n_neg('ACKLWTTAE') == 1
#     assert n_neg('DDDDEEEE') == 8
#     assert n_neg('acklwttae') == 1

# Run all the tests
# test_n_neg()

# pytest useful for feedback on tests; unittest from standard library
# and nose are two other major testing packages for Python
# Pytest can be run from the terminal and automatically looks for files
# starting with test_ or tests_ and ending with .py in the whole directory
# tree. Good idea to separate test

# PRINCIPLES OF TEST-DRIVEN DEVELOPMENT
# 1. Build your software out of small functions that do one specific thing
# 2. Build unit tests for all of your functions
# 3. Whenever you want to make any enhancements of adjustments to your code,
#    write tests for it first
# 4. Whenever you encounter a bug, write tests for it that reproduce the
#    behavior and then fix the code to make the entire test suite pass
