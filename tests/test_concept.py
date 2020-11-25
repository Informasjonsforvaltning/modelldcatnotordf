"""Test cases for the skos:concept module."""

from concepttordf import Concept
import pytest


"""
A test class for testing the class Concept.
"""


def test_instantiate_concept() -> None:
    """It returns a TypeErro exception."""
    try:
        _ = Concept()
    except Exception:
        pytest.fail("Unexpected Exception ..")
