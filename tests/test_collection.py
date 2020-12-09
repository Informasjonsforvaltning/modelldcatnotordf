"""Test cases for the collection module."""

import pytest
from rdflib import Graph

from modelldcatnotordf.modelldcatno import Collection, ModelElement
from tests.testutils import assert_isomorphic

"""
A test class for testing the class Collection.

"""


def test_instantiate_collection() -> None:
    """It returns a TypeErro exception."""
    try:
        _ = Collection()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_blank_node() -> None:
    """It returns a collection graph as blank node isomorphic to spec."""
    collection = Collection()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Collection ] .

        """
    g1 = Graph().parse(data=collection.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    collection = Collection()
    collection.identifier = "http://example.com/collections/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/collections/1> a modelldcatno:Collection .

        """
    g1 = Graph().parse(data=collection.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_member_both_identifiers() -> None:
    """It returns a has_member graph isomorphic to spec."""
    collection = Collection()
    collection.identifier = "http://example.com/collections/1"

    modelelement = ModelElement()
    modelelement.identifier = "http://example.com/modelelements/1"
    collection.has_member = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/collections/1> a modelldcatno:Collection ;
            modelldcatno:hasMember <http://example.com/modelelements/1> .

        <http://example.com/modelelements/1> a modelldcatno:ModelElement ;

        .
        """
    g1 = Graph().parse(data=collection.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_member_blank_node_collection_identifier() -> None:
    """It returns a has_member graph isomorphic to spec."""
    collection = Collection()
    collection.identifier = "http://example.com/collections/1"

    modelelement = ModelElement()
    collection.has_member = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/collections/1> a modelldcatno:Collection ;
            modelldcatno:hasMember [ a modelldcatno:ModelElement ] .

        """
    g1 = Graph().parse(data=collection.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_member_blank_node_modelelement_identifier() -> None:
    """It returns a has_member graph isomorphic to spec."""
    collection = Collection()

    modelelement = ModelElement()
    modelelement.identifier = "http://example.com/modelelements/1"
    collection.has_member = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Collection ;
            modelldcatno:hasMember <http://example.com/modelelements/1>
        ] .

        <http://example.com/modelelements/1> a modelldcatno:ModelElement .

        """
    g1 = Graph().parse(data=collection.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_member_blank_nodes() -> None:
    """It returns a has_member graph isomorphic to spec."""
    collection = Collection()

    modelelement = ModelElement()
    collection.has_member = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Collection ;
            modelldcatno:hasMember [ a modelldcatno:ModelElement ]
        ] .
        """
    g1 = Graph().parse(data=collection.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
