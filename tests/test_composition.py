"""Test cases for the composition module."""

import pytest
from pytest_mock import MockFixture
from rdflib import Graph
from skolemizer.testutils import skolemization, SkolemUtils

from modelldcatnotordf.modelldcatno import Composition, ObjectType
from tests.testutils import assert_isomorphic

"""
A test class for testing the class Composition.

"""


def test_instantiate_composition() -> None:
    """It does not raise an exception."""
    try:
        _ = Composition()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_identifier_set_at_constructor() -> None:
    """It returns an identifier graph isomorphic to spec."""
    composition = Composition("http://example.com/compositions/1")

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/compositions/1> a modelldcatno:Composition .

        """
    g1 = Graph().parse(data=composition.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_skolemization(mocker: MockFixture) -> None:
    """It returns a composition graph as blank node isomorphic to spec."""
    composition = Composition()

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
         a modelldcatno:Composition  .

        """
    g1 = Graph().parse(data=composition.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    composition = Composition()
    composition.identifier = "http://example.com/compositions/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/compositions/1> a modelldcatno:Composition .

        """
    g1 = Graph().parse(data=composition.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_contains_both_identifiers() -> None:
    """It returns a contains graph isomorphic to spec."""
    composition = Composition()
    composition.identifier = "http://example.com/compositions/1"

    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    composition.contains = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/compositions/1> a modelldcatno:Composition ;
            modelldcatno:contains <http://example.com/modelelements/1> .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType ;

        .
        """
    g1 = Graph().parse(data=composition.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_contains_skolemization_composition_identifier(
    mocker: MockFixture,
) -> None:
    """It returns a contains graph isomorphic to spec."""
    composition = Composition()
    composition.identifier = "http://example.com/compositions/1"

    modelelement = ObjectType()
    composition.contains = modelelement

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/compositions/1> a modelldcatno:Composition ;
        modelldcatno:contains
         <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
    .

    <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:ObjectType  .

    """
    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=composition.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_contains_blank_node_modelelement_identifier(
    mocker: MockFixture,
) -> None:
    """It returns a contains graph isomorphic to spec."""
    composition = Composition()

    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    composition.contains = modelelement

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
         a modelldcatno:Composition ;
            modelldcatno:contains <http://example.com/modelelements/1>
         .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType .

        """
    g1 = Graph().parse(data=composition.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_contains_both_skolemized(mocker: MockFixture) -> None:
    """It returns a contains graph isomorphic to spec."""
    composition = Composition()

    modelelement = ObjectType()
    composition.contains = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:Composition ; modelldcatno:contains
        <http://example.com/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce>
        .

        <http://example.com/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce>
         a modelldcatno:ObjectType
         .
        """

    skolemutils = SkolemUtils()
    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        side_effect=skolemutils.get_skolemization,
    )
    g1 = Graph().parse(data=composition.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_contains_as_uri() -> None:
    """It returns a contains graph isomorphic to spec."""
    composition = Composition()
    composition.identifier = "http://example.com/compositions/1"

    modelelement = "http://example.com/modelelements/1"
    composition.contains = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/compositions/1> a modelldcatno:Composition ;
            modelldcatno:contains <http://example.com/modelelements/1> .

        """
    g1 = Graph().parse(data=composition.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
