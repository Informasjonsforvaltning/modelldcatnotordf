"""Test cases for the note module."""

import pytest
from pytest_mock import MockFixture
from rdflib import Graph

from modelldcatnotordf.modelldcatno import Note
from tests.testutils import assert_isomorphic, skolemization

"""
A test class for testing the class Note.

"""


def test_instantiate_note() -> None:
    """It does not raise an exception."""
    try:
        _ = Note()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_skolemization(mocker: MockFixture) -> None:
    """It returns a note graph as blank node isomorphic to spec."""
    note = Note()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a modelldcatno:Note  .

        """

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )
    g1 = Graph().parse(data=note.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    note = Note()
    note.identifier = "http://example.com/notes/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/notes/1> a modelldcatno:Note .

        """
    g1 = Graph().parse(data=note.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_property_note() -> None:
    """It returns a property_note graph isomorphic to spec."""
    note = Note()
    note.identifier = "http://example.com/notes/1"
    note.property_note = {
        "en": "A property note",
        "nb": "En kommentar i form av en fritekst.",
    }

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix xkos: <http://rdf-vocabulary.ddialliance.org/xkos#> .


    <http://example.com/notes/1> a modelldcatno:Note ;
        modelldcatno:propertyNote "A property note"@en,
                            "En kommentar i form av en fritekst."@nb
    .
    """
    g1 = Graph().parse(data=note.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
