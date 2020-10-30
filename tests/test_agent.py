"""Test cases for the foaf:agent module."""

import pytest
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic

from modelldcatnotordf.agent import Agent

"""
A test class for testing the _abstract_ class Resource.
Using Dataset class in order to instantiate Resource.
"""


def test_instantiate_agent() -> None:
    """It returns a TypeErro exception."""
    try:
        _ = Agent()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_name_() -> None:
    """It returns a agent graph isomorphic to spec."""
    """It returns an name graph isomorphic to spec."""
    agent = Agent()
    agent.identifier = "http://example.com/agents/1"
    agent.name = "Etnavn"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf:  <http://xmlns.com/foaf/0.1/> .

    <http://example.com/agents/1> a foaf:Agent ;
            foaf:name   "Etnavn" ;

    .
    """
    g1 = Graph().parse(data=agent.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_orgnr_() -> None:
    """It returns a agent graph isomorphic to spec."""
    """It returns an name graph isomorphic to spec."""
    agent = Agent()
    agent.identifier = "http://example.com/agents/1"
    agent.orgnr = "123456789"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf:  <http://xmlns.com/foaf/0.1/> .

    <http://example.com/agents/1> a foaf:Agent ;
            dct:identifier "123456789" ;

    .
    """
    g1 = Graph().parse(data=agent.to_rdf(), format="turtle")
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
