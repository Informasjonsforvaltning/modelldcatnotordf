"""Test cases for the dct:LicenseDocument module."""

from concepttordf import Concept
import pytest
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic


from modelldcatnotordf.licensedocument import LicenseDocument

"""
A test class for testing the class License Document.
"""


def test_instantiate_licensedocument() -> None:
    """It returns a TypeErro exception."""
    try:
        _ = LicenseDocument()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_type_and_identifier() -> None:
    """It returns a license document graph isomorphic to spec."""
    """It returns an type graph isomorphic to spec."""

    licensedocument = LicenseDocument()
    licensedocument.identifier = "http://example.com/licensedocuments/1"

    type1 = Concept()
    type1.identifier = "https://example.com/types/1"
    licensedocument.type.append(type1)

    type2 = Concept()
    type2.identifier = "https://example.com/types/2"
    licensedocument.type.append(type2)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

        <http://example.com/licensedocuments/1>
            a dct:LicenseDocument ;
            dct:type <https://example.com/types/1> ;
            dct:type <https://example.com/types/2> ;
        .
        <https://example.com/types/1> a skos:Concept .
        <https://example.com/types/2> a skos:Concept .

        """

    g1 = Graph().parse(data=licensedocument.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_license_document_bnode_and_type() -> None:
    """It returns a license document graph isomorphic to spec."""
    """It returns an type graph isomorphic to spec."""

    licensedocument = LicenseDocument()

    type1 = Concept()
    type1.identifier = "https://example.com/types/1"
    licensedocument.type.append(type1)

    type2 = Concept()
    type2.identifier = "https://example.com/types/2"
    licensedocument.type.append(type2)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

        [   a dct:LicenseDocument ;
            dct:type <https://example.com/types/1> ;
            dct:type <https://example.com/types/2> ;
        ]
        .
        <https://example.com/types/1> a skos:Concept .
        <https://example.com/types/2> a skos:Concept .
      """

    g1 = Graph().parse(data=licensedocument.to_rdf(), format="turtle")
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
