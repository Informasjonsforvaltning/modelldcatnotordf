"""Test cases for the property module."""
from typing import List, Union

from concepttordf import Concept
from datacatalogtordf import URI
import pytest
from pytest_mock import MockFixture
from rdflib import Graph
from skolemizer.testutils import skolemization, SkolemUtils

from modelldcatnotordf.modelldcatno import (
    ModelElement,
    ModelProperty,
    Module,
    ObjectType,
    Role,
)
from tests.testutils import assert_isomorphic

"""
A test class for testing the class Property.

"""


def test_instantiate_resource_should_fail_with_typeerror() -> None:
    """It returns a TypeErro exception."""
    with pytest.raises(TypeError):
        _ = ModelProperty()  # type: ignore


def test_to_graph_should_return_skolemization(mocker: MockFixture) -> None:
    """It returns a property graph as blank node isomorphic to spec."""
    property = Role()

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
            a modelldcatno:Role .

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

    has_types: List[Union[ModelElement, URI]] = [modelelement]
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


def test_to_graph_should_return_has_type_skolemization_property_id(
    mocker: MockFixture,
) -> None:
    """It returns a has_type graph isomorphic to spec."""
    property = Role()
    property.identifier = "http://example.com/properties/1"

    modelelement = ObjectType()
    property.has_type.append(modelelement)

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/properties/1> a modelldcatno:Role ;
        modelldcatno:hasType
        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>

        .

        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
             a modelldcatno:ObjectType .

        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_type_skolemization_modelelement_id(
    mocker: MockFixture,
) -> None:
    """It returns a has_type graph isomorphic to spec."""
    property = Role()

    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    property.has_type.append(modelelement)

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
            a modelldcatno:Role ;
                modelldcatno:hasType <http://example.com/modelelements/1>
        .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType .

        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_type_both_skolemizations(
    mocker: MockFixture,
) -> None:
    """It returns a has_type graph isomorphic to spec."""
    property = Role()

    modelelement = ObjectType()
    property.has_type.append(modelelement)

    skolemutils = SkolemUtils()

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        side_effect=skolemutils.get_skolemization,
    )

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
    a modelldcatno:Role ; modelldcatno:hasType
    <http://example.com/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce> .

        <http://example.com/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce>
                 a modelldcatno:ObjectType .
    """

    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_min_occurs() -> None:
    """It returns a min_occurs graph isomorphic to spec."""
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
    """It returns a max_occurs graph isomorphic to spec."""
    property = Role()
    property.identifier = "http://example.com/properties/1"
    property.max_occurs = "1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/properties/1> a modelldcatno:Role ;
            xsd:maxOccurs "1"^^xsd:nonNegativeInteger .

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


def test_to_graph_should_return_description() -> None:
    """It returns a description graph isomorphic to spec."""
    """It returns an identifier graph isomorphic to spec."""
    modelproperty = Role()
    modelproperty.identifier = "http://example.com/modelpropertys/1"
    modelproperty.description = {"nb": "Beskrivelse", "en": "Description"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .


    <http://example.com/modelpropertys/1> a modelldcatno:Role ;
            dct:description   "Description"@en, "Beskrivelse"@nb ;
    .
    """
    g1 = Graph().parse(data=modelproperty.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_belongs_to_module_str(
    mocker: MockFixture,
) -> None:
    """It returns a belongs_to_module graph isomorphic to spec."""
    modelproperty = Role()
    modelproperty.identifier = "http://example.com/properties/1"
    module = "http://www.example.org/core"
    belongs_to_module: List[Union[Module, str]] = [module]
    modelproperty.belongs_to_module = belongs_to_module

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .


    <http://example.com/properties/1>    a modelldcatno:Role ;
        modelldcatno:belongsToModule
            <http://www.example.org/core>
    .

    """
    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=modelproperty.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_belongs_to_module_as_graph(mocker: MockFixture) -> None:
    """It returns a belongs_to_module graph isomorphic to spec."""
    modelproperty = Role()
    modelproperty.identifier = "http://example.com/properties/1"
    module = Module()
    module.title = {None: "core"}

    modelproperty.belongs_to_module = [module]

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/properties/1>    a modelldcatno:Role ;
         modelldcatno:belongsToModule
          <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
    .
    <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:Module ;
            dct:title "core"
    .
    """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )
    g1 = Graph().parse(data=modelproperty.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_forms_symmetry_with() -> None:
    """It returns an identifier graph isomorphic to spec."""
    modelproperty1 = Role()
    modelproperty1.identifier = "http://example.com/properties/1"

    modelproperty2 = Role()
    modelproperty2.identifier = "http://example.com/properties/2"

    modelproperty1.forms_symmetry_with = modelproperty2

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix xkos: <http://rdf-vocabulary.ddialliance.org/xkos#> .


        <http://example.com/properties/1>
                a modelldcatno:Role;
                    modelldcatno:formsSymmetryWith <http://example.com/properties/2> .

        <http://example.com/properties/2>
            a modelldcatno:Role .

        """
    g1 = Graph().parse(data=modelproperty1.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_forms_symmetry_with_skolemization(
    mocker: MockFixture,
) -> None:
    """It returns an identifier graph isomorphic to spec."""
    modelproperty1 = Role()
    modelproperty1.identifier = "http://example.com/properties/1"

    modelproperty2 = Role()
    modelproperty2.title = {"ru": "заглавие", "nb": "Tittel", "en": "Title"}

    modelproperty1.forms_symmetry_with = modelproperty2

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix xkos: <http://rdf-vocabulary.ddialliance.org/xkos#> .

    <http://example.com/properties/1> a modelldcatno:Role;
        modelldcatno:formsSymmetryWith
        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
    .

    <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:Role ;
            dct:title
                "заглавие"@ru,
                "Title"@en,
                "Tittel"@nb
    .

    """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )
    g1 = Graph().parse(data=modelproperty1.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_relation_property_label() -> None:
    """It returns a relation_property_label graph isomorphic to spec."""
    """It returns an identifier graph isomorphic to spec."""
    modelproperty = Role()
    modelproperty.identifier = "http://example.com/modelpropertys/1"
    modelproperty.relation_property_label = {
        "nb": "Navn på relasjon mellom to egenskaper.",
        "en": "A relation property label",
    }

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .


    <http://example.com/modelpropertys/1> a modelldcatno:Role ;
            modelldcatno:relationPropertyLabel
                            "A relation property label"@en,
                            "Navn på relasjon mellom to egenskaper."@nb ;
    .
    """
    g1 = Graph().parse(data=modelproperty.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_sequence_number() -> None:
    """It returns a sequence_number graph isomorphic to spec."""
    property = Role()
    property.identifier = "http://example.com/properties/1"
    property.sequence_number = 1

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/properties/1> a modelldcatno:Role ;
            modelldcatno:sequenceNumber "1"^^xsd:positiveInteger .

        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_type_as_uri() -> None:
    """It returns a has_type graph isomorphic to spec."""
    property = Role()
    property.identifier = "http://example.com/properties/1"

    modelelement = "http://example.com/modelelements/1"

    has_types: List[Union[ModelElement, URI]] = [modelelement]
    property.has_type = has_types

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/properties/1> a modelldcatno:Role ;
        modelldcatno:hasType <http://example.com/modelelements/1> .

        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_subject_as_uri() -> None:
    """It returns a subject graph isomorphic to spec."""
    modelproperty = Role()
    modelproperty.identifier = "http://example.com/properties/1"
    subject = "https://example.com/subjects/1"
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
    """
    g1 = Graph().parse(data=modelproperty.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_forms_symmetry_with_as_uri() -> None:
    """It returns an identifier graph isomorphic to spec."""
    modelproperty1 = Role()
    modelproperty1.identifier = "http://example.com/properties/1"

    modelproperty2 = "http://example.com/properties/2"

    modelproperty1.forms_symmetry_with = modelproperty2

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix xkos: <http://rdf-vocabulary.ddialliance.org/xkos#> .


        <http://example.com/properties/1>
                a modelldcatno:Role;
                    modelldcatno:formsSymmetryWith <http://example.com/properties/2> .

        """
    g1 = Graph().parse(data=modelproperty1.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_navigable() -> None:
    """It returns an navigable graph isomorphic to spec."""
    modelproperty = Role()
    modelproperty.identifier = "http://example.com/properties/1"

    modelproperty.navigable = True

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix xkos: <http://rdf-vocabulary.ddialliance.org/xkos#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .



        <http://example.com/properties/1>
                a modelldcatno:Role;
                    modelldcatno:navigable "true"^^xsd:boolean .
    """

    g1 = Graph().parse(data=modelproperty.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_max_occurs_asterisk() -> None:
    """It returns a max_occurs graph isomorphic to spec."""
    property = Role()
    property.identifier = "http://example.com/properties/1"
    property.max_occurs = "*"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/properties/1> a modelldcatno:Role ;
            xsd:maxOccurs "*" .

        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_min_occurs_0(mocker: MockFixture) -> None:
    """It returns a role graph isomorphic to spec."""
    role = Role()
    role.min_occurs = 0

    src = """
      @prefix dct: <http://purl.org/dc/terms/> .
      @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
      @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
      @prefix dcat: <http://www.w3.org/ns/dcat#> .
      @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
      @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

      <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
          a modelldcatno:Role ;
            xsd:minOccurs 0
        .
      """

    skolemutils = SkolemUtils()

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        side_effect=skolemutils.get_skolemization,
    )

    g1 = Graph().parse(data=role.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_sequence_number_0(mocker: MockFixture) -> None:
    """It returns a role graph isomorphic to spec."""
    role = Role()
    role.sequence_number = 0

    src = """
      @prefix dct: <http://purl.org/dc/terms/> .
      @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
      @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
      @prefix dcat: <http://www.w3.org/ns/dcat#> .
      @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
      @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

      <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
          a modelldcatno:Role ;
            modelldcatno:sequenceNumber "0"^^xsd:positiveInteger
        .
      """

    skolemutils = SkolemUtils()

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        side_effect=skolemutils.get_skolemization,
    )

    g1 = Graph().parse(data=role.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_max_occurs_0(mocker: MockFixture) -> None:
    """It returns a role graph isomorphic to spec."""
    role = Role()
    role.max_occurs = 0

    src = """
      @prefix dct: <http://purl.org/dc/terms/> .
      @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
      @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
      @prefix dcat: <http://www.w3.org/ns/dcat#> .
      @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
      @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

      <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
          a modelldcatno:Role ;
            xsd:maxOccurs "0"^^xsd:nonNegativeInteger
        .
      """

    skolemutils = SkolemUtils()

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        side_effect=skolemutils.get_skolemization,
    )

    g1 = Graph().parse(data=role.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
