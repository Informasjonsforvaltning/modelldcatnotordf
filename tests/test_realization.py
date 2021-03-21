"""Test cases for the realization module."""

import pytest
from pytest_mock import MockFixture
from rdflib import Graph

from modelldcatnotordf.modelldcatno import ObjectType, Realization
from tests import testutils
from tests.testutils import assert_isomorphic, skolemization

"""
A test class for testing the class Realization.

"""


def test_instantiate_realization() -> None:
    """It does not raise an exception."""
    try:
        _ = Realization()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_skolemization(mocker: MockFixture) -> None:
    """It returns a realization graph as blank node isomorphic to spec."""
    realization = Realization()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a modelldcatno:Realization  .

        """
    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )
    g1 = Graph().parse(data=realization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    realization = Realization()
    realization.identifier = "http://example.com/realizations/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/realizations/1> a modelldcatno:Realization .

        """
    g1 = Graph().parse(data=realization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_supplier_both_identifiers() -> None:
    """It returns a has_supplier graph isomorphic to spec."""
    realization = Realization()
    realization.identifier = "http://example.com/realizations/1"

    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    realization.has_supplier = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/realizations/1> a modelldcatno:Realization ;
            modelldcatno:hasSupplier <http://example.com/modelelements/1> .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType ;

        .
        """
    g1 = Graph().parse(data=realization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_supplier_skolemization_realization_id(
    mocker: MockFixture,
) -> None:
    """It returns a has_supplier graph isomorphic to spec."""
    realization = Realization()
    realization.identifier = "http://example.com/realizations/1"

    modelelement = ObjectType()
    realization.has_supplier = modelelement

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/realizations/1> a modelldcatno:Realization ;
        modelldcatno:hasSupplier
        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
    .
    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:ObjectType .

    """

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=realization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_supplier_skolemization_modelelement_id(
    mocker: MockFixture,
) -> None:
    """It returns a has_supplier graph isomorphic to spec."""
    realization = Realization()

    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    realization.has_supplier = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a modelldcatno:Realization ;
            modelldcatno:hasSupplier <http://example.com/modelelements/1>
         .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType .

        """

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=realization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_supplier_both_skolemized(
    mocker: MockFixture,
) -> None:
    """It returns a has_supplier graph isomorphic to spec."""
    realization = Realization()

    modelelement = ObjectType()
    realization.has_supplier = modelelement

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:Realization ;
        modelldcatno:hasSupplier
        <http://wwww.digdir.no/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce>
    .
    <http://wwww.digdir.no/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce>
        a modelldcatno:ObjectType
    .
    """

    skolemutils = testutils.SkolemUtils()

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        side_effect=skolemutils.get_skolemization,
    )

    g1 = Graph().parse(data=realization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_supplier_as_uri() -> None:
    """It returns a has_supplier graph isomorphic to spec."""
    realization = Realization()
    realization.identifier = "http://example.com/realizations/1"

    modelelement = "http://example.com/modelelements/1"
    realization.has_supplier = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/realizations/1> a modelldcatno:Realization ;
            modelldcatno:hasSupplier <http://example.com/modelelements/1> .

        """
    g1 = Graph().parse(data=realization.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
