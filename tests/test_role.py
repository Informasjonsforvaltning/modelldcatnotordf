"""Test cases for the role module."""

from concepttordf import Concept
import pytest
from rdflib import Graph

from modelldcatnotordf.modelldcatno import ObjectType, Role
from tests.testutils import assert_isomorphic

"""
A test class for testing the class Role.

"""


def test_instantiate_role() -> None:
    """It returns a TypeErro exception."""
    try:
        _ = Role()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_blank_node() -> None:
    """It returns a role graph as blank node isomorphic to spec."""
    role = Role()

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Role ] .

        """
    g1 = Graph().parse(data=role.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    role = Role()
    role.identifier = "http://example.com/roles/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/roles/1> a modelldcatno:Role .

        """
    g1 = Graph().parse(data=role.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_object_type_both_identifiers() -> None:
    """It returns a has_object_type graph isomorphic to spec."""
    role = Role()
    role.identifier = "http://example.com/roles/1"

    objecttype = ObjectType()
    objecttype.identifier = "http://example.com/objecttypes/1"
    role.has_object_type = objecttype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/roles/1> a modelldcatno:Role ;
            modelldcatno:hasObjectType <http://example.com/objecttypes/1> .

        <http://example.com/objecttypes/1> a modelldcatno:ObjectType ;

        .
        """
    g1 = Graph().parse(data=role.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_object_type_blank_node_role_identifier() -> None:
    """It returns a has_object_type graph isomorphic to spec."""
    role = Role()
    role.identifier = "http://example.com/roles/1"

    objecttype = ObjectType()
    role.has_object_type = objecttype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/roles/1> a modelldcatno:Role ;
            modelldcatno:hasObjectType [ a modelldcatno:ObjectType ] .

        """
    g1 = Graph().parse(data=role.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_object_type_blank_node_objecttype() -> None:
    """It returns a has_object_type graph isomorphic to spec."""
    role = Role()

    objecttype = ObjectType()
    objecttype.identifier = "http://example.com/objecttypes/1"
    role.has_object_type = objecttype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Role ;
            modelldcatno:hasObjectType <http://example.com/objecttypes/1>
        ] .

        <http://example.com/objecttypes/1> a modelldcatno:ObjectType .

        """
    g1 = Graph().parse(data=role.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_object_type_blank_nodes() -> None:
    """It returns a has_object_type graph isomorphic to spec."""
    role = Role()

    objecttype = ObjectType()
    role.has_object_type = objecttype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        [ a modelldcatno:Role ;
            modelldcatno:hasObjectType [ a modelldcatno:ObjectType ]
        ] .
        """
    g1 = Graph().parse(data=role.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_min_occurs() -> None:
    """It returns a min_occurs graph isomorphic to spec."""
    role = Role()
    role.identifier = "http://example.com/roles/1"
    role.min_occurs = 1

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/roles/1> a modelldcatno:Role ;
            xsd:minOccurs 1 .

        """
    g1 = Graph().parse(data=role.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_max_occurs() -> None:
    """It returns a max_occurs graph isomorphic to spec."""
    role = Role()
    role.identifier = "http://example.com/roles/1"
    role.max_occurs = 1

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/roles/1> a modelldcatno:Role ;
            xsd:maxOccurs 1 .

        """
    g1 = Graph().parse(data=role.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_title() -> None:
    """It returns a title graph isomorphic to spec."""
    """It returns an identifier graph isomorphic to spec."""

    role = Role()
    role.identifier = "http://example.com/roles/1"
    role.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/roles/1> a modelldcatno:Role;
                dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
        """
    g1 = Graph().parse(data=role.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_subject() -> None:
    """It returns a subject graph isomorphic to spec."""
    role = Role()
    role.identifier = "http://example.com/roles/1"
    subject = Concept()
    subject.identifier = "https://example.com/subjects/1"
    role.subject = subject

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/roles/1> a modelldcatno:Role ;
        dct:subject <https://example.com/subjects/1> ;
    .
     <https://example.com/subjects/1> a skos:Concept .

    """
    g1 = Graph().parse(data=role.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
