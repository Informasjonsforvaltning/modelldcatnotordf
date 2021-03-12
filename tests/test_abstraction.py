"""Test cases for the abstraction module."""

import pytest
from pytest_mock import MockFixture
from rdflib import Graph

from modelldcatnotordf.modelldcatno import Abstraction, ObjectType
from tests import testutils
from tests.testutils import assert_isomorphic, skolemization

"""
A test class for testing the class Abstraction.

"""


def test_instantiate_abstraction() -> None:
    """It does not raise an exception."""
    try:
        _ = Abstraction()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_blank_skolemization(mocker: MockFixture) -> None:
    """It returns a abstraction graph as blank node isomorphic to spec."""
    abstraction = Abstraction()

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
         a modelldcatno:Abstraction  .

        """
    g1 = Graph().parse(data=abstraction.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    abstraction = Abstraction()
    abstraction.identifier = "http://example.com/abstractions/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/abstractions/1> a modelldcatno:Abstraction .

        """
    g1 = Graph().parse(data=abstraction.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_is_abstraction_of_both_identifiers() -> None:
    """It returns a is_abstraction_of graph isomorphic to spec."""
    abstraction = Abstraction()
    abstraction.identifier = "http://example.com/abstractions/1"

    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    abstraction.is_abstraction_of = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/abstractions/1> a modelldcatno:Abstraction ;
            modelldcatno:isAbstractionOf <http://example.com/modelelements/1> .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType ;

        .
        """
    g1 = Graph().parse(data=abstraction.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_is_abstr_blank_node_abstr_identifier() -> None:
    """It returns a is_abstraction_of graph isomorphic to spec."""
    abstraction = Abstraction()
    abstraction.identifier = "http://example.com/abstractions/1"

    modelelement = ObjectType()
    abstraction.is_abstraction_of = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/abstractions/1> a modelldcatno:Abstraction ;
            modelldcatno:isAbstractionOf [ a modelldcatno:ObjectType ] .

        """
    g1 = Graph().parse(data=abstraction.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_is_abstr_of_skolemization_modelelement_id(
    mocker: MockFixture,
) -> None:
    """It returns a is_abstraction_of graph isomorphic to spec."""
    abstraction = Abstraction()

    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    abstraction.is_abstraction_of = modelelement

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
         a modelldcatno:Abstraction ;
            modelldcatno:isAbstractionOf <http://example.com/modelelements/1>
         .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType .

        """
    g1 = Graph().parse(data=abstraction.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_is_abstraction_of_both_skolemized(
    mocker: MockFixture,
) -> None:
    """It returns a is_abstraction_of graph isomorphic to spec."""
    abstraction = Abstraction()

    modelelement = ObjectType()
    abstraction.is_abstraction_of = modelelement

    skolemutils = testutils.SkolemUtils()

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        side_effect=skolemutils.get_skolemization,
    )

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a modelldcatno:Abstraction ;
            modelldcatno:isAbstractionOf [ a modelldcatno:ObjectType ]
         .
        """
    g1 = Graph().parse(data=abstraction.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_is_abstraction_as_uri() -> None:
    """It returns a is_abstraction_of graph isomorphic to spec."""
    abstraction = Abstraction()
    abstraction.identifier = "http://example.com/abstractions/1"

    modelelement = "http://example.com/modelelements/1"
    abstraction.is_abstraction_of = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/abstractions/1> a modelldcatno:Abstraction ;
            modelldcatno:isAbstractionOf <http://example.com/modelelements/1> .

        """
    g1 = Graph().parse(data=abstraction.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
