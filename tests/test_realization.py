"""Test cases for the realization module."""

import pytest
from rdflib import Graph
from rdflib.compare import isomorphic

from modelldcatnotordf.modelldcatno import ModelElement, Realization
from tests.testutils import _dump_diff

"""
A test class for testing the class Realization.

"""


def test_instantiate_realization() -> None:
    """It returns a TypeErro exception."""
    try:
        _ = Realization()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_blank_node() -> None:
    """It returns a realization graph as blank node isomorphic to spec."""
    realization = Realization()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Realization ] .

        """
    g1 = Graph().parse(data=realization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    realization = Realization()
    realization.identifier = "http://example.com/realizations/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/realizations/1> a modelldcatno:Realization .

        """
    g1 = Graph().parse(data=realization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_supplier_both_identifiers() -> None:
    """It returns a has_supplier graph isomorphic to spec."""
    realization = Realization()
    realization.identifier = "http://example.com/realizations/1"

    modelelement = ModelElement()
    modelelement.identifier = "http://example.com/modelelements/1"
    realization.has_supplier = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/realizations/1> a modelldcatno:Realization ;
            modelldcatno:hasSupplier <http://example.com/modelelements/1> .

        <http://example.com/modelelements/1> a modelldcatno:ModelElement ;

        .
        """
    g1 = Graph().parse(data=realization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_supplier_bnode_realization_id() -> None:
    """It returns a has_supplier graph isomorphic to spec."""
    realization = Realization()
    realization.identifier = "http://example.com/realizations/1"

    modelelement = ModelElement()
    realization.has_supplier = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/realizations/1> a modelldcatno:Realization ;
            modelldcatno:hasSupplier [ a modelldcatno:ModelElement ] .

        """
    g1 = Graph().parse(data=realization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_supplier_bnode_modelelement_id() -> None:
    """It returns a has_supplier graph isomorphic to spec."""
    realization = Realization()

    modelelement = ModelElement()
    modelelement.identifier = "http://example.com/modelelements/1"
    realization.has_supplier = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Realization ;
            modelldcatno:hasSupplier <http://example.com/modelelements/1>
        ] .

        <http://example.com/modelelements/1> a modelldcatno:ModelElement .

        """
    g1 = Graph().parse(data=realization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_supplier_blank_nodes() -> None:
    """It returns a has_supplier graph isomorphic to spec."""
    realization = Realization()

    modelelement = ModelElement()
    realization.has_supplier = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Realization ;
            modelldcatno:hasSupplier [ a modelldcatno:ModelElement ]
        ] .
        """
    g1 = Graph().parse(data=realization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic
