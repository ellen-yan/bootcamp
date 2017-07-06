# File for testing function in test-driven_dev
import test_driven_dev
import pytest

def test_n_neg():
    """Perform unit tests on test-driven_dev.n_neg."""

    assert test_driven_dev.n_neg('E') == 1
    assert test_driven_dev.n_neg('D') == 1
    assert test_driven_dev.n_neg('') == 0
    assert test_driven_dev.n_neg('ACKLWTTAE') == 1
    assert test_driven_dev.n_neg('DDDDEEEE') == 8
    assert test_driven_dev.n_neg('acklwttae') == 1

# There's no need to pass arguments to pytest, which is useful
# for testing a large number of tests. Now we can organize tests
# into more meaningful functional units
def test_n_neg_for_single_E_or_D():
    """Perform unit tests on n_neg."""

    assert test_driven_dev.n_neg('E') == 1
    assert test_driven_dev.n_neg('D') == 1

def test_n_neg_for_empty_sequence():
    assert test_driven_dev.n_neg('') == 0

def test_n_neg_for_longer_sequences():
    assert test_driven_dev.n_neg('ACKLWTTAE') == 1
    assert test_driven_dev.n_neg('DDDDEEEE') == 8

def test_n_neg_for_lower_case_sequences():
    assert test_driven_dev.n_neg('acklwttae') == 1

# If we want to test that the function does not accept improper
# input and that the function should throw an exception, we
# use pytest.raises()
# In general: raise exceptions when you are checking inputs to your
# function, use assertions to make sure the function operates
# as expected for given input
def test_n_neg_for_invalid_amino_acid():
    with pytest.raises(RuntimeError) as excinfo:
        test_driven_dev.n_neg('Z')
    excinfo.match("Z is not a valid amino acid")
