"""Test cases for the constraint rule module."""
from typing import List, Union

import pytest
from pytest_mock import MockFixture
from rdflib import Graph
from skolemizer.testutils import skolemization

from modelldcatnotordf.modelldcatno import (
    ConstraintRule,
    ModelElement,
    ModelProperty,
    ObjectType,
    Role,
)
from tests.testutils import assert_isomorphic

"""
A test class for testing the class ConstraintRule.

"""


def test_instantiate_constraint_rule() -> None:
    """It does not raise an exception."""
    try:
        _ = ConstraintRule()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_identifier_set_at_constructor() -> None:
    """It returns an identifier graph isomorphic to spec."""
    constraint_rule = ConstraintRule("http://example.com/constraint_rules/1")

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/constraint_rules/1> a modelldcatno:ConstraintRule .

        """
    g1 = Graph().parse(data=constraint_rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_skolemization(mocker: MockFixture) -> None:
    """It returns a constraint_rule graph as blank node isomorphic to spec."""
    constraint_rule = ConstraintRule()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a modelldcatno:ConstraintRule  .

        """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization", return_value=skolemization,
    )

    g1 = Graph().parse(data=constraint_rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    constraint_rule = ConstraintRule()
    constraint_rule.identifier = "http://example.com/constraint_rules/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/constraint_rules/1> a modelldcatno:ConstraintRule .

        """

    g1 = Graph().parse(data=constraint_rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_constrains_modelelement() -> None:
    """It returns an constrains graph isomorphic to spec."""
    constraint_rule = ConstraintRule()
    constraint_rule.identifier = "http://example.com/constraint_rules/1"

    modelelement = ObjectType("http://example.com/modelelements/1")

    constrains: List[Union[ModelElement, ModelProperty]] = [modelelement]
    constraint_rule.constrains = constrains

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/constraint_rules/1> a modelldcatno:ConstraintRule ;
        modelldcatno:constrains <http://example.com/modelelements/1> .


    <http://example.com/modelelements/1> a modelldcatno:ObjectType .

    """

    g1 = Graph().parse(data=constraint_rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_constrains_property() -> None:
    """It returns an constrains graph isomorphic to spec."""
    constraint_rule = ConstraintRule()
    constraint_rule.identifier = "http://example.com/constraint_rules/1"

    modelproperty = Role("http://example.com/properties/1")

    constrains: List[Union[ModelElement, ModelProperty]] = [modelproperty]
    constraint_rule.constrains = constrains

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/constraint_rules/1> a modelldcatno:ConstraintRule ;
        modelldcatno:constrains <http://example.com/properties/1> .

    <http://example.com/properties/1> a modelldcatno:Role .

    """

    g1 = Graph().parse(data=constraint_rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_constrains_modelelement_skolemized(
    mocker: MockFixture,
) -> None:
    """It returns an constrains graph isomorphic to spec."""
    constraint_rule = ConstraintRule()
    constraint_rule.identifier = "http://example.com/constraint_rules/1"

    modelelement = ObjectType()

    constrains: List[Union[ModelElement, ModelProperty]] = [modelelement]
    constraint_rule.constrains = constrains

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/constraint_rules/1> a modelldcatno:ConstraintRule ;
        modelldcatno:constrains
        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
    .
    <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:ObjectType .

    """
    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization", return_value=skolemization,
    )

    g1 = Graph().parse(data=constraint_rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_constrains_property_skolemized(
    mocker: MockFixture,
) -> None:
    """It returns an constrains graph isomorphic to spec."""
    constraint_rule = ConstraintRule()
    constraint_rule.identifier = "http://example.com/constraint_rules/1"

    modelproperty = Role()

    constrains: List[Union[ModelElement, ModelProperty]] = [modelproperty]
    constraint_rule.constrains = constrains

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/constraint_rules/1> a modelldcatno:ConstraintRule ;
        modelldcatno:constrains
            <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
    .

    <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:Role
    .
    """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization", return_value=skolemization,
    )

    g1 = Graph().parse(data=constraint_rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_constrains_link() -> None:
    """It returns an constrains graph isomorphic to spec."""
    constraint_rule = ConstraintRule()
    constraint_rule.identifier = "http://example.com/constraint_rules/1"

    modelelement = "http://example.com/modelelements/1"

    constrains: List[Union[ModelElement, ModelProperty, str]] = [modelelement]
    constraint_rule.constrains = constrains

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/constraint_rules/1> a modelldcatno:ConstraintRule ;
        modelldcatno:constrains <http://example.com/modelelements/1> .

    """

    g1 = Graph().parse(data=constraint_rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_constraint_expression() -> None:
    """It returns a constraint_expression graph isomorphic to spec."""
    constraint_rule = ConstraintRule()
    constraint_rule.identifier = "http://example.com/constraint_rules/1"
    constraint_rule.constraint_expression = {
        "nb": "Begrensningsregeluttrykk",
        "en": "A constraint expression",
    }

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/constraint_rules/1> a modelldcatno:ConstraintRule;
                modelldcatno:constraintExpression
                    "A constraint expression"@en, "Begrensningsregeluttrykk"@nb ;
        .
        """
    g1 = Graph().parse(data=constraint_rule.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
