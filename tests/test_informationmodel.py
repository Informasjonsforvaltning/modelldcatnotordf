"""Test cases for the informationmodel module."""

import pytest

from modelldcatnotordf import InformationModel

"""
A test class for testing the _abstract_ class Resource.
Using Dataset class in order to instantiate Resource.
"""


def test_instantiate_InformationModel() -> None:
    """It returns a TypeErro exception."""
    try:
        _ = InformationModel()
    except Exception:
        pytest.fail("Unexpected Exception ..")
