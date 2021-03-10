"""Test cases for the model element module."""
from typing import List, Union

from concepttordf import Concept
from datacatalogtordf import URI
import pytest
from pytest_mock import MockFixture
from rdflib import Graph

from modelldcatnotordf.modelldcatno import ModelElement, ModelProperty, ObjectType, Role
from tests.testutils import assert_isomorphic, skolemization

"""
A test class for testing the class ModelElement.

"""


def test_instantiate_resource_should_fail_with_typeerror() -> None:
    """It returns a TypeErro exception."""
    with pytest.raises(TypeError):
        _ = ModelElement()  # type: ignore


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


def test_to_graph_should_return_title_and_skolemization(mocker: MockFixture) -> None:
    """It returns a title graph isomorphic to spec."""
    modelelement = ObjectType()
    modelelement.title = {"nb": "Tittel 1", "en": "Title 1"}

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:ObjectType ;
            dct:title  "Title 1"@en, "Tittel 1"@nb ;
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

    modelproperty = Role()
    modelproperty.identifier = "http://example.com/properties/1"

    has_properties: List[Union[ModelProperty, URI]] = [modelproperty]
    modelelement.has_property = has_properties

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType ;
        modelldcatno:hasProperty <http://example.com/properties/1> .

        <http://example.com/properties/1> a modelldcatno:Role ;

        .
        """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_property_bnode_modelelement_id() -> None:
    """It returns a has_property graph isomorphic to spec."""
    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"

    modelproperty = Role()
    modelelement.has_property.append(modelproperty)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType ;
            modelldcatno:hasProperty [ a modelldcatno:Role ] .

        """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_property_skolemization_property_id(
    mocker: MockFixture,
) -> None:
    """It returns a has_property graph isomorphic to spec."""
    modelelement = ObjectType()

    modelproperty = Role()
    modelproperty.identifier = "http://example.com/properties/1"
    modelelement.has_property.append(modelproperty)

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a modelldcatno:ObjectType ;
            modelldcatno:hasProperty <http://example.com/properties/1>
         .

        <http://example.com/properties/1> a modelldcatno:Role .

        """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_property_both_skolemizations(
    mocker: MockFixture,
) -> None:
    """It returns a has_property graph isomorphic to spec."""
    modelelement = ObjectType()

    modelproperty = Role()
    modelelement.has_property.append(modelproperty)

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a modelldcatno:ObjectType ;
            modelldcatno:hasProperty [ a modelldcatno:Role ]
         .
        """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_belongs_to_module_as_graph() -> None:
    """It returns a belongs_to_module graph isomorphic to spec."""
    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    modelelement.belongs_to_module = ["core"]

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/modelelements/1>    a modelldcatno:ObjectType ;
        modelldcatno:belongsToModule "core";
    .
    """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_description() -> None:
    """It returns a description graph isomorphic to spec."""
    """It returns an identifier graph isomorphic to spec."""
    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    modelelement.description = {"nb": "Beskrivelse", "en": "Description"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .


    <http://example.com/modelelements/1> a modelldcatno:ObjectType ;
            dct:description   "Description"@en, "Beskrivelse"@nb ;
    .
    """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_belongs_to_module_any_uri_graph() -> None:
    """It returns a belongs_to_module graph isomorphic to spec."""
    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    belongs_to_module = "http://www.example.org/core"
    modelelement.belongs_to_module = [belongs_to_module]

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .


    <http://example.com/modelelements/1>    a modelldcatno:ObjectType ;
        modelldcatno:belongsToModule "http://www.example.org/core"^^xsd:anyURI ;
    .
    """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_property_as_uri() -> None:
    """It returns a has_property graph isomorphic to spec."""
    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"

    modelproperty = "http://example.com/properties/1"

    has_properties: List[Union[ModelProperty, URI]] = [modelproperty]
    modelelement.has_property = has_properties

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType ;
        modelldcatno:hasProperty <http://example.com/properties/1>

        .
        """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_subject_as_uri() -> None:
    """It returns a subject graph isomorphic to spec."""
    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    subject = "https://example.com/subjects/1"
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
    """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
