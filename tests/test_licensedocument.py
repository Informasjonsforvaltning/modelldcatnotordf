"""Test cases for the dct:LicenseDocument module."""

from concepttordf import Concept
import pytest
from pytest_mock import MockFixture
from rdflib import Graph
from skolemizer.testutils import skolemization

from modelldcatnotordf.licensedocument import LicenseDocument
from tests.testutils import assert_isomorphic

"""
A test class for testing the class License Document.
"""


def test_instantiate_licensedocument() -> None:
    """It does not raise an exception."""
    try:
        _ = LicenseDocument()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_identifier_set_at_constructor() -> None:
    """It returns a license document graph isomorphic to spec."""
    licensedocument = LicenseDocument("http://example.com/licensedocuments/1")

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

        <http://example.com/licensedocuments/1>
            a dct:LicenseDocument
        .
        """

    g1 = Graph().parse(data=licensedocument.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_type_and_identifier() -> None:
    """It returns a license document graph isomorphic to spec."""
    """It returns an type graph isomorphic to spec."""

    licensedocument = LicenseDocument()
    licensedocument.identifier = "http://example.com/licensedocuments/1"

    type1 = Concept()
    type1.identifier = "https://example.com/types/1"
    licensedocument.type.append(type1)

    type2 = Concept()
    type2.identifier = "https://example.com/types/2"
    licensedocument.type.append(type2)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

        <http://example.com/licensedocuments/1>
            a dct:LicenseDocument ;
            dct:type <https://example.com/types/1> ;
            dct:type <https://example.com/types/2> ;
        .
        <https://example.com/types/1> a skos:Concept .
        <https://example.com/types/2> a skos:Concept .

        """

    g1 = Graph().parse(data=licensedocument.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_license_document_skolemization_and_type(
    mocker: MockFixture,
) -> None:
    """It returns a license document graph isomorphic to spec."""
    """It returns an type graph isomorphic to spec."""

    licensedocument = LicenseDocument()

    type1 = Concept()
    type1.identifier = "https://example.com/types/1"
    licensedocument.type.append(type1)

    type2 = Concept()
    type2.identifier = "https://example.com/types/2"
    licensedocument.type.append(type2)

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
           a dct:LicenseDocument ;
            dct:type <https://example.com/types/1> ;
            dct:type <https://example.com/types/2> ;

        .
        <https://example.com/types/1> a skos:Concept .
        <https://example.com/types/2> a skos:Concept .
      """

    g1 = Graph().parse(data=licensedocument.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_type_as_uri() -> None:
    """It returns a license document graph isomorphic to spec."""
    """It returns an type graph isomorphic to spec."""

    licensedocument = LicenseDocument()
    licensedocument.identifier = "http://example.com/licensedocuments/1"

    type1 = Concept()
    type1.identifier = "https://example.com/types/1"
    licensedocument.type.append(type1)

    type2 = "https://example.com/types/2"
    licensedocument.type.append(type2)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

        <http://example.com/licensedocuments/1>
            a dct:LicenseDocument ;
            dct:type <https://example.com/types/1> ;
            dct:type <https://example.com/types/2> ;
        .
        <https://example.com/types/1> a skos:Concept .

        """

    g1 = Graph().parse(data=licensedocument.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
