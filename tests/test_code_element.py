"""A test class for testing the class CodeElement."""

from concepttordf import Concept
import pytest
from rdflib import Graph

from modelldcatnotordf.modelldcatno import CodeElement
from tests.testutils import assert_isomorphic


def test_instantiate_codeelement() -> None:
    """It returns a TypeErro exception."""
    try:
        _ = CodeElement()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_codeelement() -> None:
    """It returns an identifier graph isomorphic to spec."""
    codeelement = CodeElement()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:CodeElement; ]
        .
        """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/codeelements/1> a modelldcatno:CodeElement;

        .
        """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_dct_identifier_as_graph() -> None:
    """It returns a dct_identifier graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"
    codeelement.dct_identifier = "123456789"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/codeelements/1>    a modelldcatno:CodeElement ;
        dct:identifier "123456789";
    .
    """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_subject() -> None:
    """It returns a subject graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"
    subject = Concept()
    subject.identifier = "https://example.com/subjects/1"
    codeelement.subject = subject

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/codeelements/1> a modelldcatno:CodeElement ;
        dct:subject <https://example.com/subjects/1> ;
    .
     <https://example.com/subjects/1> a skos:Concept .

    """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_preflabel() -> None:
    """It returns a preflabel graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"
    codeelement.preflabel = {"nb": "Liste", "en": "List"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/codeelements/1> a modelldcatno:CodeElement ;
        skos:prefLabel "List"@en, "Liste"@nb
    .
    """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
