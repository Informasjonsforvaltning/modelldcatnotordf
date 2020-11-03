"""Test cases for the informationmodel module."""

import pytest
from rdflib import Graph
from rdflib.compare import graph_diff

from modelldcatnotordf.modelelement import ModelElement

"""
A test class for testing the class InformationModel.

"""


def test_instantiate_modelelement() -> None:
    """It returns a TypeErro exception."""
    try:
        _ = ModelElement()
    except Exception:
        pytest.fail("Unexpected Exception ..")


# ---------------------------------------------------------------------- #
# Utils for displaying debug information


def _dump_diff(g1: Graph, g2: Graph) -> None:
    in_both, in_first, in_second = graph_diff(g1, g2)
    print("\nin both:")
    _dump_turtle(in_both)
    print("\nin first:")
    _dump_turtle(in_first)
    print("\nin second:")
    _dump_turtle(in_second)


def _dump_turtle(g: Graph) -> None:
    for _l in g.serialize(format="turtle").splitlines():
        if _l:
            print(_l.decode())
