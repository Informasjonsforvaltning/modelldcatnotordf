"""Test cases for the informationmodel module."""

# import pytest
# from rdflib import Graph
# from rdflib.compare import graph_diff, isomorphic
#
# from modelldcatnotordf.agent import Agent
# from modelldcatnotordf.informationmodel import InformationModel

import pytest
from modelldcatnotordf.InformationModelDatacatalog import InformationModelDatacatalog

"""
A test class for testing the class InformationModelDatacatalog.

"""


def test_instantiate_informationmodeldatacatalog() -> None:
    """It returns a TypeErro exception."""
    try:
        _ = InformationModelDatacatalog()
    except Exception:
        pytest.fail("Unexpected Exception ..")

