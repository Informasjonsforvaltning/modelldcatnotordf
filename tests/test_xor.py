"""Test cases for the modelldcatno:Xor module."""

import pytest
from pytest_mock import MockFixture
from rdflib import Graph
from skolemizer.testutils import skolemization

from modelldcatnotordf.modelldcatno import Xor
from tests.testutils import assert_isomorphic

"""
A test class for testing the class Xor.

"""


def test_instantiate_or() -> None:
    """It does not raise an exception."""
    try:
        _ = Xor()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_identifier_set_at_constructor() -> None:
    """It returns an identifier graph isomorphic to spec."""
    modelldcatno_xor = Xor("http://example.com/modelldcatno_xors/1")

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/modelldcatno_xors/1> a modelldcatno:Xor .

        """
    g1 = Graph().parse(data=modelldcatno_xor.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_skolemization(mocker: MockFixture) -> None:
    """It returns a modelldcatno:Xor graph with skolemization isomorphic to spec."""
    modelldcatno_xor = Xor()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a modelldcatno:Xor .

        """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization", return_value=skolemization,
    )

    g1 = Graph().parse(data=modelldcatno_xor.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    modelldcatno_xor = Xor()
    modelldcatno_xor.identifier = "http://example.com/modelldcatno_xors/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/modelldcatno_xors/1> a modelldcatno:Xor .

        """

    g1 = Graph().parse(data=modelldcatno_xor.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
