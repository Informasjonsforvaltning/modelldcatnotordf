"""Test cases for the skos:ConceptScheme module."""

import pytest
from pytest_mock import MockFixture
from rdflib import Graph
from skolemizer.testutils import skolemization

from modelldcatnotordf.conceptscheme import ConceptScheme
from tests.testutils import assert_isomorphic

"""
A test class for testing the class Concept Scheme.
"""


def test_instantiate_conceptscheme() -> None:
    """It does not raise an exception."""
    try:
        _ = ConceptScheme()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_identifier_set_at_constructor() -> None:
    """It returns a concept scheme graph isomorphic to spec."""
    conceptscheme = ConceptScheme("http://example.com/conceptschemes/1")

    src = """
        @prefix skos: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

        <http://example.com/conceptschemes/1>
            a skos:ConceptScheme
        .
        """

    g1 = Graph().parse(data=conceptscheme.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_identifier() -> None:
    """It returns a concept scheme graph isomorphic to spec."""
    conceptscheme = ConceptScheme()
    conceptscheme.identifier = "http://example.com/conceptschemes/1"

    src = """
        @prefix skos: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

        <http://example.com/conceptschemes/1>
            a skos:ConceptScheme
        .
        """

    g1 = Graph().parse(data=conceptscheme.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_concept_scheme_skolemization(
    mocker: MockFixture,
) -> None:
    """It returns a concept scheme graph isomorphic to spec."""
    conceptscheme = ConceptScheme()

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization", return_value=skolemization,
    )

    src = """
        @prefix skos: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
           a skos:ConceptScheme
        .
      """

    g1 = Graph().parse(data=conceptscheme.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
