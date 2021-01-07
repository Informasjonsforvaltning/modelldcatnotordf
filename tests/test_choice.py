"""Test cases for the choice module."""
from typing import List

import pytest
from rdflib import Graph

from modelldcatnotordf.modelldcatno import Choice, ModelElement, ObjectType
from tests.testutils import assert_isomorphic

"""
A test class for testing the class Choice.

"""


def test_instantiate_choice() -> None:
    """It does not raise an exception."""
    try:
        _ = Choice()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_blank_node() -> None:
    """It returns a choice graph as blank node isomorphic to spec."""
    choice = Choice()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Choice ] .

        """
    g1 = Graph().parse(data=choice.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    choice = Choice()
    choice.identifier = "http://example.com/choices/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/choices/1> a modelldcatno:Choice .

        """
    g1 = Graph().parse(data=choice.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_some_both_identifiers() -> None:
    """It returns a has_some graph isomorphic to spec."""
    choice = Choice()
    choice.identifier = "http://example.com/choices/1"

    modelelement1 = ObjectType()
    modelelement1.identifier = "http://example.com/modelelements/1"

    modelelement2 = ObjectType()
    modelelement2.identifier = "http://example.com/modelelements/2"

    has_somes: List[ModelElement] = [modelelement1, modelelement2]
    choice.has_some = has_somes

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/choices/1>
            a modelldcatno:Choice ;
            modelldcatno:hasSome <http://example.com/modelelements/1> ;
            modelldcatno:hasSome <http://example.com/modelelements/2> ;

        .
        <http://example.com/modelelements/1> a modelldcatno:ObjectType .
        <http://example.com/modelelements/2> a modelldcatno:ObjectType .

        """
    g1 = Graph().parse(data=choice.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_some_blank_node_choice_identifier() -> None:
    """It returns a has_some graph isomorphic to spec."""
    choice = Choice()
    choice.identifier = "http://example.com/choices/1"

    modelelement = ObjectType()
    choice.has_some.append(modelelement)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/choices/1> a modelldcatno:Choice ;
            modelldcatno:hasSome [ a modelldcatno:ObjectType ] .

        """
    g1 = Graph().parse(data=choice.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_some_blank_node_modelelement_identifier() -> None:
    """It returns a has_some graph isomorphic to spec."""
    choice = Choice()

    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    choice.has_some.append(modelelement)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Choice ;
            modelldcatno:hasSome <http://example.com/modelelements/1>
        ] .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType .

        """
    g1 = Graph().parse(data=choice.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_some_blank_nodes() -> None:
    """It returns a has_some graph isomorphic to spec."""
    choice = Choice()

    modelelement = ObjectType()
    choice.has_some.append(modelelement)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Choice ;
            modelldcatno:hasSome [ a modelldcatno:ObjectType ]
        ] .
        """
    g1 = Graph().parse(data=choice.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
