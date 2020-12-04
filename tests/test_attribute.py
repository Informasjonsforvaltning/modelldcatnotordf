"""Test cases for the attribute module."""

import pytest
from rdflib import Graph
from rdflib.compare import isomorphic

from modelldcatnotordf.modelldcatno import Attribute, ObjectType, SimpleType
from tests.testutils import _dump_diff

"""
A test class for testing the class Attribute.

"""


def test_instantiate_attribute() -> None:
    """It returns a TypeErro exception."""
    try:
        _ = Attribute()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_blank_node() -> None:
    """It returns a attribute graph as blank node isomorphic to spec."""
    attribute = Attribute()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Attribute ] .

        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    attribute = Attribute()
    attribute.identifier = "http://example.com/attributes/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/attributes/1> a modelldcatno:Attribute .

        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_contains_object_type_both_identifiers() -> None:
    """It returns a contains_object_type graph isomorphic to spec."""
    attribute = Attribute()
    attribute.identifier = "http://example.com/attributes/1"

    objecttype = ObjectType()
    objecttype.identifier = "http://example.com/objecttypes/1"
    attribute.contains_object_type = objecttype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/attributes/1> a modelldcatno:Attribute ;
            modelldcatno:containsObjectType <http://example.com/objecttypes/1> .

        <http://example.com/objecttypes/1> a modelldcatno:ObjectType ;

        .
        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_contains_object_type_bnode_attribute_id() -> None:
    """It returns a contains_object_type graph isomorphic to spec."""
    attribute = Attribute()
    attribute.identifier = "http://example.com/attributes/1"

    objecttype = ObjectType()
    attribute.contains_object_type = objecttype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/attributes/1> a modelldcatno:Attribute ;
            modelldcatno:containsObjectType [ a modelldcatno:ObjectType ] .

        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_contains_object_type_blank_node_objecttype() -> None:
    """It returns a contains_object_type graph isomorphic to spec."""
    attribute = Attribute()

    objecttype = ObjectType()
    objecttype.identifier = "http://example.com/objecttypes/1"
    attribute.contains_object_type = objecttype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Attribute ;
            modelldcatno:containsObjectType <http://example.com/objecttypes/1>
        ] .

        <http://example.com/objecttypes/1> a modelldcatno:ObjectType .

        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_contains_object_type_blank_nodes() -> None:
    """It returns a contains_object_type graph isomorphic to spec."""
    attribute = Attribute()

    objecttype = ObjectType()
    attribute.contains_object_type = objecttype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Attribute ;
            modelldcatno:containsObjectType [ a modelldcatno:ObjectType ]
        ] .
        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_simple_type_both_identifiers() -> None:
    """It returns a has_simple_type graph isomorphic to spec."""
    attribute = Attribute()
    attribute.identifier = "http://example.com/attributes/1"

    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    attribute.has_simple_type = simpletype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/attributes/1> a modelldcatno:Attribute ;
            modelldcatno:hasSimpleType <http://example.com/simpletypes/1> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;

        .
        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_simple_type_bnode_attribute_id() -> None:
    """It returns a has_simple_type graph isomorphic to spec."""
    attribute = Attribute()
    attribute.identifier = "http://example.com/attributes/1"

    simpletype = SimpleType()
    attribute.has_simple_type = simpletype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/attributes/1> a modelldcatno:Attribute ;
            modelldcatno:hasSimpleType [ a modelldcatno:SimpleType ] .

        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_simple_type_blank_node_simpletype() -> None:
    """It returns a has_simple_type graph isomorphic to spec."""
    attribute = Attribute()

    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    attribute.has_simple_type = simpletype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Attribute ;
            modelldcatno:hasSimpleType <http://example.com/simpletypes/1>
        ] .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType .

        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_simple_type_blank_nodes() -> None:
    """It returns a has_simple_type graph isomorphic to spec."""
    attribute = Attribute()

    simpletype = SimpleType()
    attribute.has_simple_type = simpletype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Attribute ;
            modelldcatno:hasSimpleType [ a modelldcatno:SimpleType ]
        ] .
        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic
