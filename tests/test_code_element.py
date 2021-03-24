"""A test class for testing the class CodeElement."""
from typing import List, Union

from concepttordf import Concept
from datacatalogtordf import URI
import pytest
from pytest_mock import MockFixture
from rdflib import Graph

from modelldcatnotordf.modelldcatno import CodeElement, CodeList
from tests import testutils
from tests.testutils import assert_isomorphic, skolemization


def test_instantiate_codeelement() -> None:
    """It does not raise an exception."""
    try:
        _ = CodeElement()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_codeelement(mocker: MockFixture) -> None:
    """It returns an codeelement graph isomorphic to spec."""
    codeelement = CodeElement()

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a modelldcatno:CodeElement
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


def test_to_graph_should_return_notation_as_graph() -> None:
    """It returns a notation graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"
    codeelement.notation = "str"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/codeelements/1>    a modelldcatno:CodeElement ;
        skos:notation "str";
    .
    """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_in_scheme_both_identifiers() -> None:
    """It returns a is_codeelement_of graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"

    codelist = CodeList()
    codelist.identifier = "http://example.com/codelists/1"

    inschemes: List[CodeList] = [codelist]

    codeelement.in_scheme = inschemes

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .


        <http://example.com/codeelements/1> a modelldcatno:CodeElement ;
            skos:inScheme <http://example.com/codelists/1> .

        <http://example.com/codelists/1> a modelldcatno:CodeList ;

        .
        """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_in_scheme_skolemization_codeelement_identifier(
    mocker: MockFixture,
) -> None:
    """It returns a is_codeelement_of graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"

    codelist = CodeList()

    inschemes: List[CodeList] = [codelist]

    codeelement.in_scheme = inschemes

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/codeelements/1> a modelldcatno:CodeElement ;
        skos:inScheme
        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>

    .
    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:CodeList .
    """

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_is_codeelement_of_both_skolemized(
    mocker: MockFixture,
) -> None:
    """It returns a is_codeelement_of graph isomorphic to spec."""
    codeelement = CodeElement()

    codelist = CodeList()

    inschemes: List[CodeList] = [codelist]

    codeelement.in_scheme = inschemes

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:CodeElement ;
        skos:inScheme
        <http://wwww.digdir.no/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce>
    .
    <http://wwww.digdir.no/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce>
        a modelldcatno:CodeList
    .
    """

    skolemutils = testutils.SkolemUtils()

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        side_effect=skolemutils.get_skolemization,
    )

    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_in_scheme_skolemization_codelist_id(
    mocker: MockFixture,
) -> None:
    """It returns a is_codeelement_of graph isomorphic to spec."""
    codeelement = CodeElement()

    codelist = CodeList()
    codelist.identifier = "http://example.com/codelists/1"

    inschemes: List[CodeList] = [codelist]

    codeelement.in_scheme = inschemes

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a modelldcatno:CodeElement ;
            skos:inScheme <http://example.com/codelists/1>
         .

        <http://example.com/codelists/1> a modelldcatno:CodeList .

        """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_top_concept_of_both_identifiers() -> None:
    """It returns a is_codeelement_of graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"

    codelist = CodeList()
    codelist.identifier = "http://example.com/codelists/1"

    inschemes: List[CodeList] = [codelist]

    codeelement.top_concept_of = inschemes

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .


        <http://example.com/codeelements/1> a modelldcatno:CodeElement ;
            skos:topConceptOf <http://example.com/codelists/1> .

        <http://example.com/codelists/1> a modelldcatno:CodeList ;

        .
        """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_top_concept_of_skolemization_codeelement_id(
    mocker: MockFixture,
) -> None:
    """It returns a is_codeelement_of graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"

    codelist = CodeList()

    inschemes: List[CodeList] = [codelist]

    codeelement.top_concept_of = inschemes

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .


    <http://example.com/codeelements/1> a modelldcatno:CodeElement ;
        skos:topConceptOf
        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
    .
    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:CodeList .
    """

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_top_concept_of_both_skolemized(
    mocker: MockFixture,
) -> None:
    """It returns a is_codeelement_of graph isomorphic to spec."""
    codeelement = CodeElement()

    codelist = CodeList()

    inschemes: List[CodeList] = [codelist]

    codeelement.top_concept_of = inschemes

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:CodeElement ; skos:topConceptOf
        <http://wwww.digdir.no/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce>
    .
    <http://wwww.digdir.no/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce>
        a modelldcatno:CodeList
    .
    """

    skolemutils = testutils.SkolemUtils()

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        side_effect=skolemutils.get_skolemization,
    )

    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_top_concept_of_skolemization_codelist_id(
    mocker: MockFixture,
) -> None:
    """It returns a is_codeelement_of graph isomorphic to spec."""
    codeelement = CodeElement()

    codelist = CodeList()
    codelist.identifier = "http://example.com/codelists/1"

    inschemes: List[CodeList] = [codelist]
    codeelement.top_concept_of = inschemes

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a modelldcatno:CodeElement ;
            skos:topConceptOf <http://example.com/codelists/1>
         .

        <http://example.com/codelists/1> a modelldcatno:CodeList .

        """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_altlabel() -> None:
    """It returns a altlabel graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"
    codeelement.altlabel = {"nb": "Samling", "en": "Collection"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/codeelements/1> a modelldcatno:CodeElement ;
        skos:altLabel "Collection"@en, "Samling"@nb
    .
    """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_definition() -> None:
    """It returns a definition graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"
    codeelement.definition = {
        "nb": "Ordnet mengde elementer",
        "en": "Ordered set of elements",
    }

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/codeelements/1> a modelldcatno:CodeElement ;
        skos:definition "Ordered set of elements"@en, "Ordnet mengde elementer"@nb
    .
    """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_example() -> None:
    """It returns a example graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"
    codeelement.example = ["An example", "Another example"]

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/codeelements/1> a modelldcatno:CodeElement ;
        skos:example "An example", "Another example"
    .
    """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_hiddenlabel() -> None:
    """It returns a hiddenlabel graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"
    codeelement.hiddenlabel = {"nb": "En uegnet betegnelse", "en": "A hidden label"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/codeelements/1> a modelldcatno:CodeElement ;
        skos:hiddenLabel "A hidden label"@en, "En uegnet betegnelse"@nb
    .
    """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_note() -> None:
    """It returns a note graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"
    codeelement.note = {"en": "A note", "nb": "En merknad"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/codeelements/1> a modelldcatno:CodeElement ;
        skos:note "A note"@en, "En merknad"@nb
    .
    """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_scopenote() -> None:
    """It returns a scopenote graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"
    codeelement.scopenote = {
        "en": "A scope note",
        "nb": "En merknad ang. bruken av kodeelementet",
    }

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

    <http://example.com/codeelements/1> a modelldcatno:CodeElement ;
        skos:scopeNote "A scope note"@en, "En merknad ang. bruken av kodeelementet"@nb
    .
    """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_exclusion_note() -> None:
    """It returns a exclusion_note graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"
    codeelement.exclusion_note = {
        "en": "An exclusion note",
        "nb": "En merknad ang. ekskluderte elementer",
    }

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix xkos: <http://rdf-vocabulary.ddialliance.org/xkos#> .


    <http://example.com/codeelements/1> a modelldcatno:CodeElement ;
        xkos:exclusionNote "An exclusion note"@en,
                            "En merknad ang. ekskluderte elementer"@nb
    .
    """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_inclusion_note() -> None:
    """It returns a inclusion_note graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"
    codeelement.inclusion_note = {
        "en": "An inclusion note",
        "nb": "En merknad om hva som er inkludert i kodeelementet",
    }

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix xkos: <http://rdf-vocabulary.ddialliance.org/xkos#> .


    <http://example.com/codeelements/1> a modelldcatno:CodeElement ;
        xkos:inclusionNote "An inclusion note"@en,
                            "En merknad om hva som er inkludert i kodeelementet"@nb
    .
    """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_next() -> None:
    """It returns an identifier graph isomorphic to spec."""
    codeelement1 = CodeElement()
    codeelement1.identifier = "http://example.com/codeelements/1"

    codeelement2 = CodeElement()
    codeelement2.identifier = "http://example.com/codeelements/2"

    codeelement1.next_element = codeelement2

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix xkos: <http://rdf-vocabulary.ddialliance.org/xkos#> .


        <http://example.com/codeelements/1>
                a modelldcatno:CodeElement;
                    xkos:next <http://example.com/codeelements/2> .

        <http://example.com/codeelements/2> a modelldcatno:CodeElement .

        """
    g1 = Graph().parse(data=codeelement1.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_next_skolemization(mocker: MockFixture) -> None:
    """It returns an identifier graph isomorphic to spec."""
    codeelement1 = CodeElement()
    codeelement1.identifier = "http://example.com/codeelements/1"

    codeelement2 = CodeElement()

    codeelement1.next_element = codeelement2

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix xkos: <http://rdf-vocabulary.ddialliance.org/xkos#> .

    <http://example.com/codeelements/1>
        a modelldcatno:CodeElement; xkos:next
        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
    .
    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:CodeElement .
    """

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=codeelement1.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_previous() -> None:
    """It returns an identifier graph isomorphic to spec."""
    codeelement1 = CodeElement()
    codeelement1.identifier = "http://example.com/codeelements/1"

    codeelement2 = CodeElement()
    codeelement2.identifier = "http://example.com/codeelements/2"

    codeelement1.previous_element = codeelement2

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix xkos: <http://rdf-vocabulary.ddialliance.org/xkos#> .


        <http://example.com/codeelements/1>
                a modelldcatno:CodeElement;
                    xkos:previous <http://example.com/codeelements/2> .

        <http://example.com/codeelements/2> a modelldcatno:CodeElement .

        """
    g1 = Graph().parse(data=codeelement1.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_previous_bnode(mocker: MockFixture) -> None:
    """It returns an identifier graph isomorphic to spec."""
    codeelement1 = CodeElement()
    codeelement1.identifier = "http://example.com/codeelements/1"

    codeelement2 = CodeElement()

    codeelement1.previous_element = codeelement2

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix xkos: <http://rdf-vocabulary.ddialliance.org/xkos#> .

    <http://example.com/codeelements/1>
        a modelldcatno:CodeElement; xkos:previous
        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
    .
    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:CodeElement .
    """

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=codeelement1.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_subject_as_uri() -> None:
    """It returns a subject graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"
    subject = "https://example.com/subjects/1"
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

    """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_in_scheme_as_uri() -> None:
    """It returns a is_codeelement_of graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"

    codelist = "http://example.com/codelists/1"

    inschemes: List[Union[CodeList, URI]] = [codelist]

    codeelement.in_scheme = inschemes

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .


        <http://example.com/codeelements/1> a modelldcatno:CodeElement ;
            skos:inScheme <http://example.com/codelists/1> .

        """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_top_concept_of_as_uri() -> None:
    """It returns a is_codeelement_of graph isomorphic to spec."""
    codeelement = CodeElement()
    codeelement.identifier = "http://example.com/codeelements/1"

    codelist = "http://example.com/codelists/1"

    inschemes: List[Union[CodeList, URI]] = [codelist]

    codeelement.top_concept_of = inschemes

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .


        <http://example.com/codeelements/1> a modelldcatno:CodeElement ;
            skos:topConceptOf <http://example.com/codelists/1> .


        """
    g1 = Graph().parse(data=codeelement.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_next_as_uri() -> None:
    """It returns an identifier graph isomorphic to spec."""
    codeelement1 = CodeElement()
    codeelement1.identifier = "http://example.com/codeelements/1"

    codeelement2 = "http://example.com/codeelements/2"

    codeelement1.next_element = codeelement2

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix xkos: <http://rdf-vocabulary.ddialliance.org/xkos#> .


        <http://example.com/codeelements/1>
                a modelldcatno:CodeElement;
                    xkos:next <http://example.com/codeelements/2> .


        """
    g1 = Graph().parse(data=codeelement1.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_previous_as_uri() -> None:
    """It returns an identifier graph isomorphic to spec."""
    codeelement1 = CodeElement()
    codeelement1.identifier = "http://example.com/codeelements/1"

    codeelement2 = "http://example.com/codeelements/2"

    codeelement1.previous_element = codeelement2

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
        @prefix xkos: <http://rdf-vocabulary.ddialliance.org/xkos#> .


        <http://example.com/codeelements/1>
                a modelldcatno:CodeElement;
                    xkos:previous <http://example.com/codeelements/2> .

        """
    g1 = Graph().parse(data=codeelement1.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
