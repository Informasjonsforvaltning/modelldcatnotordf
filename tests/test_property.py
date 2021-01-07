"""Test cases for the property module."""
from typing import List

from concepttordf import Concept
import pytest
from rdflib import Graph

from modelldcatnotordf.modelldcatno import ModelElement, ObjectType, Role
from tests.testutils import assert_isomorphic

"""
A test class for testing the class Property.

"""


def test_instantiate_property() -> None:
    """It does not raise an exception."""
    try:
        _ = Role()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_blank_node() -> None:
    """It returns a property graph as blank node isomorphic to spec."""
    property = Role()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Role ] .

        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    property = Role()
    property.identifier = "http://example.com/properties/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/properties/1> a modelldcatno:Role .

        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_type_both_identifiers() -> None:
    """It returns a has_type graph isomorphic to spec."""
    property = Role()
    property.identifier = "http://example.com/properties/1"

    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"

    has_types: List[ModelElement] = [modelelement]
    property.has_type = has_types

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/properties/1> a modelldcatno:Role ;
        modelldcatno:hasType <http://example.com/modelelements/1> .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType ;

        .
        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_type_blank_node_property_identifier() -> None:
    """It returns a has_type graph isomorphic to spec."""
    property = Role()
    property.identifier = "http://example.com/properties/1"

    modelelement = ObjectType()
    property.has_type.append(modelelement)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/properties/1> a modelldcatno:Role ;
            modelldcatno:hasType [ a modelldcatno:ObjectType ] .

        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_type_blank_node_modelelement_identifier() -> None:
    """It returns a has_type graph isomorphic to spec."""
    property = Role()

    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    property.has_type.append(modelelement)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Role ;
            modelldcatno:hasType <http://example.com/modelelements/1>
        ] .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType .

        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_type_blank_nodes() -> None:
    """It returns a has_type graph isomorphic to spec."""
    property = Role()

    modelelement = ObjectType()
    property.has_type.append(modelelement)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Role ;
            modelldcatno:hasType [ a modelldcatno:ObjectType ]
        ] .
        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_min_occurs() -> None:
    """It returns a has_type graph isomorphic to spec."""
    property = Role()
    property.identifier = "http://example.com/properties/1"
    property.min_occurs = 1

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/properties/1> a modelldcatno:Role ;
            xsd:minOccurs 1 .

        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_max_occurs() -> None:
    """It returns a has_type graph isomorphic to spec."""
    property = Role()
    property.identifier = "http://example.com/properties/1"
    property.max_occurs = 1

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/properties/1> a modelldcatno:Role ;
            xsd:maxOccurs 1 .

        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_title_and_identifier() -> None:
    """It returns a title graph isomorphic to spec."""
    """It returns an identifier graph isomorphic to spec."""

    modelproperty = Role()
    modelproperty.identifier = "http://example.com/properties/1"
    modelproperty.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/properties/1> a modelldcatno:Role;
                dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
        """
    g1 = Graph().parse(data=modelproperty.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_subject() -> None:
    """It returns a subject graph isomorphic to spec."""
    modelproperty = Role()
    modelproperty.identifier = "http://example.com/properties/1"
    subject = Concept()
    subject.identifier = "https://example.com/subjects/1"
    modelproperty.subject = subject

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/properties/1> a modelldcatno:Role ;
        dct:subject <https://example.com/subjects/1> ;
    .
     <https://example.com/subjects/1> a skos:Concept .

    """
    g1 = Graph().parse(data=modelproperty.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
