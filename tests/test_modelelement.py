"""Test cases for the model element module."""

from concepttordf import Concept
import pytest
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic

from modelldcatnotordf.modelldcatno import ModelElement
from modelldcatnotordf.modelldcatno import ModelProperty


"""
A test class for testing the class ModelElement.

"""


def test_instantiate_modelelement() -> None:
    """It returns a TypeErro exception."""
    try:
        _ = ModelElement()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_title_and_identifier() -> None:
    """It returns a title graph isomorphic to spec."""
    """It returns an identifier graph isomorphic to spec."""

    modelelement = ModelElement()
    modelelement.identifier = "http://example.com/modelelements/1"
    modelelement.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/modelelements/1> a modelldcatno:ModelElement;
                dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
        """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_title_and_no_identifier() -> None:
    """It returns a title graph isomorphic to spec."""
    modelelement = ModelElement()
    modelelement.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:ModelElement ;
            dct:title   "Title 1"@en, "Tittel 1"@nb ;
        ]
        .
        """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_dct_identifier_as_graph() -> None:
    """It returns a dct_identifier graph isomorphic to spec."""
    modelelement = ModelElement()
    modelelement.identifier = "http://example.com/modelelements/1"
    modelelement.dct_identifier = "123456789"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/modelelements/1>    a modelldcatno:ModelElement ;
        dct:identifier "123456789";
    .
    """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_subject() -> None:
    """It returns a subject graph isomorphic to spec."""
    modelelement = ModelElement()
    modelelement.identifier = "http://example.com/modelelements/1"
    subject = Concept()
    subject.identifier = "https://example.com/subjects/1"
    modelelement.subject = subject

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/modelelements/1> a modelldcatno:ModelElement ;
        dct:subject <https://example.com/subjects/1> ;
    .
     <https://example.com/subjects/1> a skos:Concept .

    """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_property_both_identifiers() -> None:
    """It returns a has_property graph isomorphic to spec."""
    modelelement = ModelElement()
    modelelement.identifier = "http://example.com/modelelements/1"

    modelproperty = ModelProperty()
    modelproperty.identifier = "http://example.com/properties/1"
    modelelement.has_property.append(modelproperty)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/modelelements/1> a modelldcatno:ModelElement ;
        modelldcatno:hasProperty <http://example.com/properties/1> .

        <http://example.com/properties/1> a modelldcatno:Property ;

        .
        """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_property_bnode_modelelement_id() -> None:
    """It returns a has_property graph isomorphic to spec."""
    modelelement = ModelElement()
    modelelement.identifier = "http://example.com/modelelements/1"

    modelproperty = ModelProperty()
    modelelement.has_property.append(modelproperty)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/modelelements/1> a modelldcatno:ModelElement ;
            modelldcatno:hasProperty [ a modelldcatno:Property ] .

        """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_property_bnode_modelproperty_id() -> None:
    """It returns a has_property graph isomorphic to spec."""
    modelelement = ModelElement()

    modelproperty = ModelProperty()
    modelproperty.identifier = "http://example.com/properties/1"
    modelelement.has_property.append(modelproperty)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:ModelElement ;
            modelldcatno:hasProperty <http://example.com/properties/1>
        ] .

        <http://example.com/properties/1> a modelldcatno:Property .

        """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_has_property_blank_nodes() -> None:
    """It returns a has_property graph isomorphic to spec."""
    modelelement = ModelElement()

    modelproperty = ModelProperty()
    modelelement.has_property.append(modelproperty)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:ModelElement ;
            modelldcatno:hasProperty [ a modelldcatno:Property ]
        ] .
        """
    g1 = Graph().parse(data=modelelement.to_rdf(), format="turtle")
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
