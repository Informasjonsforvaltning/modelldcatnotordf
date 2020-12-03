"""Test cases for the composition module."""

import pytest
from rdflib import Graph
from rdflib.compare import isomorphic

from modelldcatnotordf.modelldcatno import Composition, ModelElement
from tests.testutils import _dump_diff

"""
A test class for testing the class Composition.

"""


def test_instantiate_composition() -> None:
    """It returns a TypeErro exception."""
    try:
        _ = Composition()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_blank_node() -> None:
    """It returns a composition graph as blank node isomorphic to spec."""
    composition = Composition()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Composition ] .

        """
    g1 = Graph().parse(data=composition.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    composition = Composition()
    composition.identifier = "http://example.com/compositions/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/compositions/1> a modelldcatno:Composition .

        """
    g1 = Graph().parse(data=composition.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_contains_both_identifiers() -> None:
    """It returns a contains graph isomorphic to spec."""
    composition = Composition()
    composition.identifier = "http://example.com/compositions/1"

    modelelement = ModelElement()
    modelelement.identifier = "http://example.com/modelelements/1"
    composition.contains = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/compositions/1> a modelldcatno:Composition ;
        modelldcatno:contains <http://example.com/modelelements/1> .

        <http://example.com/modelelements/1> a modelldcatno:ModelElement ;

        .
        """
    g1 = Graph().parse(data=composition.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_contains_blank_node_composition_identifier() -> None:
    """It returns a contains graph isomorphic to spec."""
    composition = Composition()
    composition.identifier = "http://example.com/compositions/1"

    modelelement = ModelElement()
    composition.contains = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/compositions/1> a modelldcatno:Composition ;
            modelldcatno:contains [ a modelldcatno:ModelElement ] .

        """
    g1 = Graph().parse(data=composition.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_contains_blank_node_modelelement_identifier() -> None:
    """It returns a contains graph isomorphic to spec."""
    composition = Composition()

    modelelement = ModelElement()
    modelelement.identifier = "http://example.com/modelelements/1"
    composition.contains = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Composition ;
            modelldcatno:contains <http://example.com/modelelements/1>
        ] .

        <http://example.com/modelelements/1> a modelldcatno:ModelElement .

        """
    g1 = Graph().parse(data=composition.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_contains_blank_nodes() -> None:
    """It returns a contains graph isomorphic to spec."""
    composition = Composition()

    modelelement = ModelElement()
    composition.contains = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Composition ;
            modelldcatno:contains [ a modelldcatno:ModelElement ]
        ] .
        """
    g1 = Graph().parse(data=composition.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic
