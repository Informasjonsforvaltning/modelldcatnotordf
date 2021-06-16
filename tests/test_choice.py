"""Test cases for the choice module."""
from typing import List, Union

from datacatalogtordf import URI
import pytest
from pytest_mock import MockFixture
from rdflib import Graph
from skolemizer.testutils import skolemization, SkolemUtils

from modelldcatnotordf.modelldcatno import (
    Choice,
    ModelElement,
    ModelProperty,
    ObjectType,
    Role,
)
from tests.testutils import assert_isomorphic

"""
A test class for testing the class Choice.

"""


def test_instantiate_choice() -> None:
    """It does not raise an exception."""
    try:
        _ = Choice()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_identifier_set_at_constructor() -> None:
    """It returns an identifier graph isomorphic to spec."""
    choice = Choice("http://example.com/choices/1")

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/choices/1> a modelldcatno:Choice .

        """
    g1 = Graph().parse(data=choice.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_skolemization(mocker: MockFixture) -> None:
    """It returns a choice graph as blank node isomorphic to spec."""
    choice = Choice()

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization", return_value=skolemization,
    )

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a modelldcatno:Choice  .

        """
    g1 = Graph().parse(data=choice.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    choice = Choice()
    choice.identifier = "http://example.com/choices/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/choices/1> a modelldcatno:Choice .

        """
    g1 = Graph().parse(data=choice.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_some_both_identifiers(mocker: MockFixture) -> None:
    """It returns a has_some graph isomorphic to spec."""
    choice = Choice()
    choice.identifier = "http://example.com/choices/1"

    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"

    role = Role()

    has_somes: List[Union[ModelElement, ModelProperty]] = [modelelement, role]
    choice.has_some = has_somes

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/choices/1>
        a modelldcatno:Choice ;
        modelldcatno:hasSome <http://example.com/modelelements/1> ;
        modelldcatno:hasSome
        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        .
        <http://example.com/modelelements/1> a modelldcatno:ObjectType .
        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
            a modelldcatno:Role .

        """
    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization", return_value=skolemization,
    )

    g1 = Graph().parse(data=choice.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_some_skolemization_choice_identifier(
    mocker: MockFixture,
) -> None:
    """It returns a has_some graph isomorphic to spec."""
    choice = Choice()
    choice.identifier = "http://example.com/choices/1"

    modelelement = ObjectType()
    choice.has_some.append(modelelement)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/choices/1> a modelldcatno:Choice ;
    modelldcatno:hasSome
    <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
    .
    <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
    a modelldcatno:ObjectType .
    """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization", return_value=skolemization,
    )

    g1 = Graph().parse(data=choice.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_some_blank_node_modelelement_identifier(
    mocker: MockFixture,
) -> None:
    """It returns a has_some graph isomorphic to spec."""
    choice = Choice()

    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    choice.has_some.append(modelelement)

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization", return_value=skolemization,
    )

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a modelldcatno:Choice ;
            modelldcatno:hasSome <http://example.com/modelelements/1>
         .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType .

        """
    g1 = Graph().parse(data=choice.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_some_both_skolemized(mocker: MockFixture) -> None:
    """It returns a has_some graph isomorphic to spec."""
    choice = Choice()

    modelelement = ObjectType()
    choice.has_some.append(modelelement)

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:Choice ;
        modelldcatno:hasSome
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
    g1 = Graph().parse(data=choice.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_some_as_uri() -> None:
    """It returns a has_some graph isomorphic to spec."""
    choice = Choice()
    choice.identifier = "http://example.com/choices/1"

    modelelement1 = ObjectType()
    modelelement1.identifier = "http://example.com/modelelements/1"

    modelelement2 = "http://example.com/modelelements/2"

    has_somes: List[Union[ModelElement, URI]] = [modelelement1, modelelement2]
    choice.has_some = has_somes

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/choices/1>
            a modelldcatno:Choice ;
            modelldcatno:hasSome <http://example.com/modelelements/1> ;
            modelldcatno:hasSome <http://example.com/modelelements/2> ;

        .
        <http://example.com/modelelements/1> a modelldcatno:ObjectType .

        """
    g1 = Graph().parse(data=choice.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
