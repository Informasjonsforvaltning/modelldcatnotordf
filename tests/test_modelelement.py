"""Test cases for the model element module."""
from typing import List

from concepttordf import Concept
from rdflib import Graph

from modelldcatnotordf.modelldcatno import ModelProperty, ObjectType
from tests.testutils import assert_isomorphic

"""
A test class for testing the class ModelElement.

"""


def test_to_graph_should_return_title_and_identifier() -> None:
    """It returns a title graph isomorphic to spec."""
    """It returns an identifier graph isomorphic to spec."""

    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    modelelement.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType;
                dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
        """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_title_and_no_identifier() -> None:
    """It returns a title graph isomorphic to spec."""
    modelelement = ObjectType()
    modelelement.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:ObjectType ;
            dct:title   "Title 1"@en, "Tittel 1"@nb ;
        ]
        .
        """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_dct_identifier_as_graph() -> None:
    """It returns a dct_identifier graph isomorphic to spec."""
    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    modelelement.dct_identifier = "123456789"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/modelelements/1>    a modelldcatno:ObjectType ;
        dct:identifier "123456789";
    .
    """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_subject() -> None:
    """It returns a subject graph isomorphic to spec."""
    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    subject = Concept()
    subject.identifier = "https://example.com/subjects/1"
    modelelement.subject = subject

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/modelelements/1> a modelldcatno:ObjectType ;
        dct:subject <https://example.com/subjects/1> ;
    .
     <https://example.com/subjects/1> a skos:Concept .

    """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_property_both_identifiers() -> None:
    """It returns a has_property graph isomorphic to spec."""
    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"

    modelproperty = ModelProperty()
    modelproperty.identifier = "http://example.com/properties/1"

    has_properties: List[ModelProperty] = []
    has_properties.append(modelproperty)
    modelelement.has_property = has_properties

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType ;
        modelldcatno:hasProperty <http://example.com/properties/1> .

        <http://example.com/properties/1> a modelldcatno:Property ;

        .
        """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_property_bnode_modelelement_id() -> None:
    """It returns a has_property graph isomorphic to spec."""
    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"

    modelproperty = ModelProperty()
    modelelement.has_property.append(modelproperty)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType ;
            modelldcatno:hasProperty [ a modelldcatno:Property ] .

        """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_property_bnode_modelproperty_id() -> None:
    """It returns a has_property graph isomorphic to spec."""
    modelelement = ObjectType()

    modelproperty = ModelProperty()
    modelproperty.identifier = "http://example.com/properties/1"
    modelelement.has_property.append(modelproperty)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:ObjectType ;
            modelldcatno:hasProperty <http://example.com/properties/1>
        ] .

        <http://example.com/properties/1> a modelldcatno:Property .

        """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_property_blank_nodes() -> None:
    """It returns a has_property graph isomorphic to spec."""
    modelelement = ObjectType()

    modelproperty = ModelProperty()
    modelelement.has_property.append(modelproperty)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:ObjectType ;
            modelldcatno:hasProperty [ a modelldcatno:Property ]
        ] .
        """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
