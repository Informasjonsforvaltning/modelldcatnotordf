"""Test cases for the code list module."""

from concepttordf import Concept
import pytest
from rdflib import Graph

from modelldcatnotordf.modelldcatno import CodeList
from tests.testutils import assert_isomorphic

"""
A test class for testing the class CodeList.

"""


def test_instantiate_codelist() -> None:
    """It does not raise an exception."""
    try:
        _ = CodeList()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_title_and_identifier() -> None:
    """It returns a title graph isomorphic to spec."""
    """It returns an identifier graph isomorphic to spec."""

    codelist = CodeList()
    codelist.identifier = "http://example.com/codelists/1"
    codelist.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/codelists/1> a modelldcatno:CodeList;
                dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
        """
    g1 = Graph().parse(data=codelist.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_title_and_no_identifier() -> None:
    """It returns a title graph isomorphic to spec."""
    codelist = CodeList()
    codelist.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:CodeList ;
            dct:title   "Title 1"@en, "Tittel 1"@nb ;
        ]
        .
        """
    g1 = Graph().parse(data=codelist.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_dct_identifier_as_graph() -> None:
    """It returns a dct_identifier graph isomorphic to spec."""
    codelist = CodeList()
    codelist.identifier = "http://example.com/codelists/1"
    codelist.dct_identifier = "123456789"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/codelists/1>    a modelldcatno:CodeList ;
        dct:identifier "123456789";
    .
    """
    g1 = Graph().parse(data=codelist.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_subject() -> None:
    """It returns a subject graph isomorphic to spec."""
    codelist = CodeList()
    codelist.identifier = "http://example.com/codelists/1"
    subject = Concept()
    subject.identifier = "https://example.com/subjects/1"
    codelist.subject = subject

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/codelists/1> a modelldcatno:CodeList ;
        dct:subject <https://example.com/subjects/1> ;
    .
     <https://example.com/subjects/1> a skos:Concept .

    """
    g1 = Graph().parse(data=codelist.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_code_list_reference() -> None:
    """It returns an identifier graph isomorphic to spec."""
    codelist1 = CodeList()
    codelist1.identifier = "http://example.com/codelists/1"

    codelist2 = CodeList()
    codelist2.identifier = "http://example.com/codelists/2"

    codelist1.code_list_reference = codelist2

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix xkos: <http://rdf-vocabulary.ddialliance.org/xkos#> .


        <http://example.com/codelists/1>
                a modelldcatno:CodeList;
                    modelldcatno:codeListReference <http://example.com/codelists/2> .

        <http://example.com/codelists/2> a modelldcatno:CodeList .

        """
    g1 = Graph().parse(data=codelist1.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_code_list_reference_bnode() -> None:
    """It returns an identifier graph isomorphic to spec."""
    codelist1 = CodeList()
    codelist1.identifier = "http://example.com/codelists/1"

    codelist2 = CodeList()

    codelist1.code_list_reference = codelist2

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix xkos: <http://rdf-vocabulary.ddialliance.org/xkos#> .

        <http://example.com/codelists/1>
                a modelldcatno:CodeList;
                    modelldcatno:codeListReference [ a modelldcatno:CodeList ]  .

        """
    g1 = Graph().parse(data=codelist1.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
