"""Test cases for the specialization module."""

import pytest
from rdflib import Graph

from modelldcatnotordf.modelldcatno import ObjectType, Specialization
from tests.testutils import assert_isomorphic

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

    assert_isomorphic(g1, g2)


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

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_general_concept_both_identifiers() -> None:
    """It returns a has_general_concept graph isomorphic to spec."""
    specialization = Specialization()
    specialization.identifier = "http://example.com/specializations/1"

    modelelement = ObjectType()
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

        <http://example.com/modelelements/1> a modelldcatno:ObjectType ;

        .
        """
    g1 = Graph().parse(data=specialization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_general_concept_bnode_specialization_id() -> None:
    """It returns a has_general_concept graph isomorphic to spec."""
    specialization = Specialization()
    specialization.identifier = "http://example.com/specializations/1"

    modelelement = ObjectType()
    specialization.has_general_concept = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/specializations/1> a modelldcatno:Specialization ;
            modelldcatno:hasGeneralConcept [ a modelldcatno:ObjectType ] .

        """
    g1 = Graph().parse(data=specialization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_general_concept_bnode_modelelement_id() -> None:
    """It returns a has_general_concept graph isomorphic to spec."""
    specialization = Specialization()

    modelelement = ObjectType()
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

        <http://example.com/modelelements/1> a modelldcatno:ObjectType .

        """
    g1 = Graph().parse(data=specialization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_general_concept_blank_nodes() -> None:
    """It returns a has_general_concept graph isomorphic to spec."""
    specialization = Specialization()

    modelelement = ObjectType()
    specialization.has_general_concept = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Specialization ;
            modelldcatno:hasGeneralConcept [ a modelldcatno:ObjectType ]
        ] .
        """
    g1 = Graph().parse(data=specialization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
