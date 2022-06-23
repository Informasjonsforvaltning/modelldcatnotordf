"""Test cases for the simple type module."""

from concepttordf import Concept
import pytest
from pytest_mock import MockFixture
from rdflib import Graph
from skolemizer.testutils import skolemization

from modelldcatnotordf.modelldcatno import SimpleType
from tests.testutils import assert_isomorphic

"""
A test class for testing the class SimpleType.

"""


def test_instantiate_simpletype() -> None:
    """It does not raise an exception."""
    try:
        _ = SimpleType()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_identifier_set_at_constructor() -> None:
    """It returns an identifier graph isomorphic to spec."""
    simpletype = SimpleType("http://example.com/simpletypes/1")

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType;
        .
        """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_title_and_identifier() -> None:
    """It returns a title graph isomorphic to spec."""
    """It returns an identifier graph isomorphic to spec."""

    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    simpletype.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType;
                dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
        """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_title_and_no_identifier(mocker: MockFixture) -> None:
    """It returns a title graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a modelldcatno:SimpleType ;
            dct:title   "Title 1"@en, "Tittel 1"@nb ;
        .
        """

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_dct_identifier_as_graph() -> None:
    """It returns a dct_identifier graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    simpletype.dct_identifier = "123456789"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/simpletypes/1>    a modelldcatno:SimpleType ;
        dct:identifier "123456789";
    .
    """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_subject() -> None:
    """It returns a subject graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    subject = Concept()
    subject.identifier = "https://example.com/subjects/1"
    simpletype.subject = subject

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;
        dct:subject <https://example.com/subjects/1> ;
    .
     <https://example.com/subjects/1> a skos:Concept .

    """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_min_length() -> None:
    """It returns a min_length graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    simpletype.min_length = 1

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;
            xsd:minLength 1 .

        """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_max_length() -> None:
    """It returns a max_length graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    simpletype.max_length = 1

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;
            xsd:maxLength 1 .

        """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_fraction_digits() -> None:
    """It returns a fraction_digits graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    simpletype.fraction_digits = 1

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;
            xsd:fractionDigits 1 .

        """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_length() -> None:
    """It returns a length graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    simpletype.length = 1

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;
            xsd:length 1 .

        """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_total_digits() -> None:
    """It returns a total_digits graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    simpletype.total_digits = 1

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;
            xsd:totalDigits 1 .

        """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_max_inclusive() -> None:
    """It returns a max_inclusive graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    simpletype.max_inclusive = float("1.05")

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;
            xsd:maxInclusive 1.05e+00 .

        """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_min_inclusive() -> None:
    """It returns a min_inclusive graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    simpletype.min_inclusive = float("1.05")

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;
            xsd:minInclusive 1.05e+00 .

        """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_type_definition_referance() -> None:
    """It returns a min_inclusive graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    simpletype.type_definition_reference = "http://example.com/typedefinitions/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;
            modelldcatno:typeDefinitionReference <http://example.com/typedefinitions/1>.

        """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_pattern() -> None:
    """It returns a pattern graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    simpletype.pattern = "\b(a*ha+h[ha]*|o?l+o+l+[ol]*)\b"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;
            xsd:pattern "\b(a*ha+h[ha]*|o?l+o+l+[ol]*)\b" .

        """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_min_exclusive() -> None:
    """It returns a min_exclusive graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    simpletype.min_exclusive = float("1.05")

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;
            xsd:minExclusive 1.05e+00 .

        """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_max_exclusive() -> None:
    """It returns a max_exclusive graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    simpletype.max_exclusive = float("1.05")

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;
            xsd:maxExclusive 1.05e+00 .

        """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_min_length_0() -> None:
    """It returns a min_length graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    simpletype.min_length = 0

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;
            xsd:minLength 0 .

        """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_max_length_0() -> None:
    """It returns a max_length graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    simpletype.max_length = 0

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;
            xsd:maxLength 0 .

        """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_fraction_digits_0() -> None:
    """It returns a fraction_digits graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    simpletype.fraction_digits = 0

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;
            xsd:fractionDigits 0 .

        """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_length_0() -> None:
    """It returns a length graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    simpletype.length = 0

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;
            xsd:length 0 .

        """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_total_digits_0() -> None:
    """It returns a total_digits graph isomorphic to spec."""
    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    simpletype.total_digits = 0

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;
            xsd:totalDigits 0 .

        """
    g1 = Graph().parse(data=simpletype.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
