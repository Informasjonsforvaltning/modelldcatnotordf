"""Test cases for the property module."""

import pytest
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic

from modelldcatnotordf.modelldcatno import ModelElement
from modelldcatnotordf.modelldcatno import ModelProperty

"""
A test class for testing the class Property.

"""


def test_instantiate_property() -> None:
    """It returns a TypeErro exception."""
    try:
        _ = ModelProperty()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_blank_node() -> None:
    """It returns a property graph as blank node isomorphic to spec."""
    property = ModelProperty()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Property ] .

        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    property = ModelProperty()
    property.identifier = "http://example.com/properties/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/properties/1> a modelldcatno:Property .

        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_type_both_identifiers() -> None:
    """It returns a has_type graph isomorphic to spec."""
    property = ModelProperty()
    property.identifier = "http://example.com/properties/1"

    modelelement = ModelElement()
    modelelement.identifier = "http://example.com/modelelements/1"
    property.has_type.append(modelelement)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/properties/1> a modelldcatno:Property ;
        modelldcatno:hasType <http://example.com/modelelements/1> .

        <http://example.com/modelelements/1> a modelldcatno:ModelElement ;

        .
        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_type_blank_node_property_identifier() -> None:
    """It returns a has_type graph isomorphic to spec."""
    property = ModelProperty()
    property.identifier = "http://example.com/properties/1"

    modelelement = ModelElement()
    property.has_type.append(modelelement)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/properties/1> a modelldcatno:Property ;
            modelldcatno:hasType [ a modelldcatno:ModelElement ] .

        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_type_blank_node_modelelement_identifier() -> None:
    """It returns a has_type graph isomorphic to spec."""
    property = ModelProperty()

    modelelement = ModelElement()
    modelelement.identifier = "http://example.com/modelelements/1"
    property.has_type.append(modelelement)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Property ;
            modelldcatno:hasType <http://example.com/modelelements/1>
        ] .

        <http://example.com/modelelements/1> a modelldcatno:ModelElement .

        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_type_blank_nodes() -> None:
    """It returns a has_type graph isomorphic to spec."""
    property = ModelProperty()

    modelelement = ModelElement()
    property.has_type.append(modelelement)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Property ;
            modelldcatno:hasType [ a modelldcatno:ModelElement ]
        ] .
        """
    g1 = Graph().parse(data=property.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


# ---------------------------------------------------------------------- #
# Utils for displaying debug information


def _dump_diff(g1: Graph, g2: Graph) -> None:
    in_both, in_first, in_second = graph_diff(g1, g2)
    print("\nin both:")
    _dump_turtle(in_both)
    print("\nin first:")
    _dump_turtle(in_first)
    print("\nin second:")
    _dump_turtle(in_second)


def _dump_turtle(g: Graph) -> None:
    for _l in g.serialize(format="turtle").splitlines():
        if _l:
            print(_l.decode())
