"""Test cases for the association module."""

import pytest
from rdflib import Graph

from modelldcatnotordf.modelldcatno import Association, ObjectType
from tests.testutils import assert_isomorphic

"""
A test class for testing the class Association.

"""


def test_instantiate_association() -> None:
    """It does not raise an exception."""
    try:
        _ = Association()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_blank_node() -> None:
    """It returns a association graph as blank node isomorphic to spec."""
    association = Association()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Association ] .

        """
    g1 = Graph().parse(data=association.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    association = Association()
    association.identifier = "http://example.com/associations/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/associations/1> a modelldcatno:Association .

        """
    g1 = Graph().parse(data=association.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_refers_to_both_identifiers() -> None:
    """It returns a refers_to graph isomorphic to spec."""
    association = Association()
    association.identifier = "http://example.com/associations/1"

    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    association.refers_to = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/associations/1> a modelldcatno:Association ;
            modelldcatno:refersTo <http://example.com/modelelements/1> .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType ;

        .
        """
    g1 = Graph().parse(data=association.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_refers_to_blank_node_association_identifier() -> None:
    """It returns a refers_to graph isomorphic to spec."""
    association = Association()
    association.identifier = "http://example.com/associations/1"

    modelelement = ObjectType()
    association.refers_to = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/associations/1> a modelldcatno:Association ;
            modelldcatno:refersTo [ a modelldcatno:ObjectType ] .

        """
    g1 = Graph().parse(data=association.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_refers_to_blank_node_modelelement_identifier() -> None:
    """It returns a refers_to graph isomorphic to spec."""
    association = Association()

    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    association.refers_to = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Association ;
            modelldcatno:refersTo <http://example.com/modelelements/1>
        ] .

        <http://example.com/modelelements/1> a modelldcatno:ObjectType .

        """
    g1 = Graph().parse(data=association.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_refers_to_blank_nodes() -> None:
    """It returns a refers_to graph isomorphic to spec."""
    association = Association()

    modelelement = ObjectType()
    association.refers_to = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Association ;
            modelldcatno:refersTo [ a modelldcatno:ObjectType ]
        ] .
        """
    g1 = Graph().parse(data=association.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_refers_to_as_uri() -> None:
    """It returns a refers_to graph isomorphic to spec."""
    association = Association()
    association.identifier = "http://example.com/associations/1"

    modelelement = "http://example.com/modelelements/1"
    association.refers_to = modelelement

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/associations/1> a modelldcatno:Association ;
            modelldcatno:refersTo <http://example.com/modelelements/1> .


        """
    g1 = Graph().parse(data=association.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
