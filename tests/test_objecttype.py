"""Test cases for the object type module."""

from concepttordf import Concept
import pytest
from pytest_mock import MockFixture
from rdflib import Graph

from modelldcatnotordf.modelldcatno import ObjectType
from tests.testutils import assert_isomorphic, skolemization

"""
A test class for testing the class ObjectType.

"""


def test_instantiate_objectype() -> None:
    """It does not raise an exception."""
    try:
        _ = ObjectType()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_title_and_identifier() -> None:
    """It returns a title graph isomorphic to spec."""
    """It returns an identifier graph isomorphic to spec."""

    objectype = ObjectType()
    objectype.identifier = "http://example.com/objectypes/1"
    objectype.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/objectypes/1> a modelldcatno:ObjectType;
                dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
        """
    g1 = Graph().parse(data=objectype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_title_and_skolemization(mocker: MockFixture) -> None:
    """It returns a title graph isomorphic to spec."""
    objectype = ObjectType()
    objectype.title = {"nb": "Tittel 1", "en": "Title 1"}

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
            dct:title   "Title 1"@en, "Tittel 1"@nb ;

        .
        """
    g1 = Graph().parse(data=objectype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_dct_identifier_as_graph() -> None:
    """It returns a dct_identifier graph isomorphic to spec."""
    objectype = ObjectType()
    objectype.identifier = "http://example.com/objectypes/1"
    objectype.dct_identifier = "123456789"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/objectypes/1>    a modelldcatno:ObjectType ;
        dct:identifier "123456789";
    .
    """
    g1 = Graph().parse(data=objectype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_subject() -> None:
    """It returns a subject graph isomorphic to spec."""
    objectype = ObjectType()
    objectype.identifier = "http://example.com/objectypes/1"
    subject = Concept()
    subject.identifier = "https://example.com/subjects/1"
    objectype.subject = subject

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/objectypes/1> a modelldcatno:ObjectType ;
        dct:subject <https://example.com/subjects/1> ;
    .
     <https://example.com/subjects/1> a skos:Concept .

    """
    g1 = Graph().parse(data=objectype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
