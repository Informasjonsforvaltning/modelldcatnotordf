"""Test cases for the property module."""

import pytest

from modelldcatnotordf.property import Property

"""
A test class for testing the class Property.

"""


def test_instantiate_modelelement() -> None:
    """It returns a TypeErro exception."""
    try:
        _ = Property()
    except Exception:
        pytest.fail("Unexpected Exception ..")
