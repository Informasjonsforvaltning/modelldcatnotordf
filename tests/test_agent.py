"""Test cases for the foaf:agent module."""

from datacatalogtordf import Agent, Catalog, Dataset
import pytest
from rdflib import Graph

from tests.testutils import assert_isomorphic

"""
A test class for testing the class Agent.
"""


def test_instantiate_agent() -> None:
    """It does not raise an exception."""
    try:
        _ = Agent()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_agent() -> None:
    """It returns a agent graph isomorphic to spec."""
    agent = Agent()
    agent.identifier = "http://example.com/agents/1"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf:  <http://xmlns.com/foaf/0.1/> .

    <http://example.com/agents/1> a foaf:Agent ;

    .
    """
    g1 = Graph().parse(data=agent.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_name() -> None:
    """It returns a agent graph isomorphic to spec."""
    """It returns an name graph isomorphic to spec."""
    agent = Agent()
    agent.identifier = "http://example.com/agents/1"
    agent.name = {"nb": "Et navn"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf:  <http://xmlns.com/foaf/0.1/> .

    <http://example.com/agents/1> a foaf:Agent ;
            foaf:name   "Et navn"@nb ;

    .
    """
    g1 = Graph().parse(data=agent.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_orgnr_() -> None:
    """It returns a agent graph isomorphic to spec."""
    """It returns an orgnr graph isomorphic to spec."""
    agent = Agent()
    agent.identifier = "http://example.com/agents/1"
    agent.organization_id = "123456789"

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

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_publisher_as_bnode() -> None:
    """It returns a name graph isomorphic to spec."""
    dataset = Dataset()
    dataset.identifier = "http://example.com/datasets/1"
    agent = Agent()
    agent.name = {"en": "James Bond", "nb": "Djeims Bånd", "nn": "Jonas Bonde"}
    dataset.publisher = agent

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf: <http://xmlns.com/foaf/0.1/> .

    <http://example.com/datasets/1> a dcat:Dataset;
    dct:publisher   [a foaf:Agent ;
                       foaf:name "James Bond"@en, "Djeims Bånd"@nb, "Jonas Bonde"@nn ;
                    ] ;
    .
    """
    g1 = Graph().parse(data=dataset.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_publisher_as_bnode_with_catalog() -> None:
    """It returns a name graph isomorphic to spec."""
    catalog = Catalog()
    catalog.identifier = "http://example.com/catalogs/1"
    agent = Agent()
    agent.name = {"en": "James Bond", "nb": "Djeims Bånd"}
    catalog.publisher = agent

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf: <http://xmlns.com/foaf/0.1/> .

    <http://example.com/catalogs/1> a dcat:Catalog;
    dct:publisher   [a foaf:Agent ;
                       foaf:name "James Bond"@en, "Djeims Bånd"@nb ;
                    ] ;
    .
    """
    g1 = Graph().parse(data=catalog.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_sameas() -> None:
    """It returns a agent graph isomorphic to spec."""
    """It returns an sameAs graph isomorphic to spec."""
    agent = Agent()
    agent.identifier = "http://example.com/agents/1"
    agent.same_as = "http://example.com/agents/2"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
    @prefix owl: <http://www.w3.org/2002/07/owl#> .
    <http://example.com/agents/1> a foaf:Agent ;
        owl:sameAs <http://example.com/agents/2> ;
        .
        """
    g1 = Graph().parse(data=agent.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


# ---------------------------------------------------------------------- #
