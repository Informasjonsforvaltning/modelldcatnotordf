"""Test cases for the specialization module."""

import pytest
from rdflib import Graph
from rdflib.compare import isomorphic

from modelldcatnotordf.modelldcatno import ModelElement, Specialization
from tests.testutils import _dump_diff

"""
A test class for testing the class Specialization.

"""


def test_instantiate_specialization() -> None:
    """It returns a TypeErro exception."""
    try:
        _ = Specialization()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_blank_node() -> None:
    """It returns a specialization graph as blank node isomorphic to spec."""
    specialization = Specialization()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Specialization ] .

        """
    g1 = Graph().parse(data=specialization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    specialization = Specialization()
    specialization.identifier = "http://example.com/specializations/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/specializations/1> a modelldcatno:Specialization .

        """
    g1 = Graph().parse(data=specialization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_general_concept_both_identifiers() -> None:
    """It returns a has_general_concept graph isomorphic to spec."""
    specialization = Specialization()
    specialization.identifier = "http://example.com/specializations/1"

    modelelement = ModelElement()
    modelelement.identifier = "http://example.com/modelelements/1"
    specialization.has_general_concept = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/specializations/1> a modelldcatno:Specialization ;
            modelldcatno:hasGeneralConcept <http://example.com/modelelements/1> .

        <http://example.com/modelelements/1> a modelldcatno:ModelElement ;

        .
        """
    g1 = Graph().parse(data=specialization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_general_concept_bnode_specialization_id() -> None:
    """It returns a has_general_concept graph isomorphic to spec."""
    specialization = Specialization()
    specialization.identifier = "http://example.com/specializations/1"

    modelelement = ModelElement()
    specialization.has_general_concept = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/specializations/1> a modelldcatno:Specialization ;
            modelldcatno:hasGeneralConcept [ a modelldcatno:ModelElement ] .

        """
    g1 = Graph().parse(data=specialization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_general_concept_bnode_modelelement_id() -> None:
    """It returns a has_general_concept graph isomorphic to spec."""
    specialization = Specialization()

    modelelement = ModelElement()
    modelelement.identifier = "http://example.com/modelelements/1"
    specialization.has_general_concept = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Specialization ;
            modelldcatno:hasGeneralConcept <http://example.com/modelelements/1>
        ] .

        <http://example.com/modelelements/1> a modelldcatno:ModelElement .

        """
    g1 = Graph().parse(data=specialization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_general_concept_blank_nodes() -> None:
    """It returns a has_general_concept graph isomorphic to spec."""
    specialization = Specialization()

    modelelement = ModelElement()
    specialization.has_general_concept = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Specialization ;
            modelldcatno:hasGeneralConcept [ a modelldcatno:ModelElement ]
        ] .
        """
    g1 = Graph().parse(data=specialization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic
