"""Test cases for the informationmodel module."""
from typing import List

from concepttordf import Concept
from datacatalogtordf import Agent
import pytest
from rdflib import Graph, Namespace

from modelldcatnotordf.licensedocument import LicenseDocument
from modelldcatnotordf.modelldcatno import InformationModel, ModelElement, ObjectType
from tests.testutils import assert_isomorphic

"""
A test class for testing the class InformationModel.

"""


def test_instantiate_informationmodel() -> None:
    """It does not raise an exception."""
    try:
        _ = InformationModel()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_type_informationmodel() -> None:
    """It returns a the correct RDF-type."""
    modelldcatno = Namespace("https://data.norge.no/vocabulary/modelldcatno#")
    informationmodel = InformationModel()
    assert modelldcatno.InformationModel == informationmodel.type


def test_to_graph_should_return_title_and_identifier() -> None:
    """It returns a title graph isomorphic to spec."""
    """It returns an identifier graph isomorphic to spec."""
    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"
    informationmodel.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/informationmodels/1> a modelldcatno:InformationModel ;
            dct:title   "Title 1"@en, "Tittel 1"@nb ;
    .
    """
    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_description() -> None:
    """It returns a description graph isomorphic to spec."""
    """It returns an identifier graph isomorphic to spec."""
    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"
    informationmodel.description = {"nb": "Beskrivelse", "en": "Description"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .


    <http://example.com/informationmodels/1> a modelldcatno:InformationModel ;
            dct:description   "Description"@en, "Beskrivelse"@nb ;
    .
    """
    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_theme() -> None:
    """It returns a theme graph isomorphic to spec."""
    """It returns an identifier graph isomorphic to spec."""
    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"
    informationmodel.theme.append("http://example.com/themes/1")
    informationmodel.theme.append("http://example.com/themes/2")

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .


    <http://example.com/informationmodels/1> a modelldcatno:InformationModel ;
               dcat:theme   <http://example.com/themes/1> ,
                     <http://example.com/themes/2> ;
        .
    """
    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_publisher() -> None:
    """It returns a information model graph isomorphic to spec."""
    """It returns an agent graph isomorphic to spec."""

    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"

    agent = Agent()
    agent.organization_id = "123456789"
    agent.identifier = "https://example.com/organizations/1"
    informationmodel.publisher = agent
    informationmodel.title = {"nb": "CRD IV - Likviditet NSFR - konsolidert (KRT-1075)"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/informationmodels/1>
    a    modelldcatno:InformationModel ;
    dct:publisher    <https://example.com/organizations/1> ;
    dct:title    "CRD IV - Likviditet NSFR - konsolidert (KRT-1075)"@nb .

    <https://example.com/organizations/1> a <http://xmlns.com/foaf/0.1/Agent> ;
        dct:identifier "123456789" .

    """
    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_subject() -> None:
    """It returns a information model graph isomorphic to spec."""
    """It returns an subject graph isomorphic to spec."""

    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"

    subjects: List[Concept] = []

    subject1 = Concept()
    subject1.identifier = "https://example.com/subjects/1"
    subjects.append(subject1)

    subject2 = Concept()
    subject2.identifier = "https://example.com/subjects/2"
    subjects.append(subject2)

    informationmodel.subject = subjects

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

        <http://example.com/informationmodels/1>
            a modelldcatno:InformationModel ;
            dct:subject <https://example.com/subjects/1> ;
            dct:subject <https://example.com/subjects/2> ;
        .
        <https://example.com/subjects/1> a skos:Concept .
        <https://example.com/subjects/2> a skos:Concept .

        """

    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_contains_model_element() -> None:
    """It returns a subject graph isomorphic to spec."""
    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"
    modelelement = ObjectType()
    modelelement.identifier = "http://example.com/modelelements/1"
    modelelement.title = {"nb": "Tittel 1", "en": "Title 1"}

    modelelements: List[ModelElement] = [modelelement]
    informationmodel.modelelements = modelelements

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/informationmodels/1> a modelldcatno:InformationModel ;
        modelldcatno:containsModelElement <http://example.com/modelelements/1> .

    <http://example.com/modelelements/1> a modelldcatno:ObjectType ;
        dct:title   "Title 1"@en, "Tittel 1"@nb
    .
    """
    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_modelelements_blank_node() -> None:
    """It returns a model element graph isomorphic to spec."""
    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"

    modelelement = ObjectType()
    informationmodel.modelelements.append(modelelement)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/informationmodels/1> a modelldcatno:InformationModel ;
            modelldcatno:containsModelElement [ a modelldcatno:ObjectType ] .

        """
    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_modelelements_blank_node_with_properties() -> None:
    """It returns a model element graph isomorphic to spec."""
    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"

    modelelement = ObjectType()
    modelelement.title = {"nb": "Tittel 1", "en": "Title 1"}

    informationmodel.modelelements.append(modelelement)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/informationmodels/1> a modelldcatno:InformationModel ;
            modelldcatno:containsModelElement [ a modelldcatno:ObjectType ;
            dct:title   "Title 1"@en, "Tittel 1"@nb ] .

        """
    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_informationmodelidentifier() -> None:
    """It returns a information model identifier graph isomorphic to spec."""
    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"
    informationmodel.informationmodelidentifier = "8343e8b8-2e40-11eb-8192-f794be5d6ba1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/informationmodels/1> a modelldcatno:InformationModel ;
            modelldcatno:informationModelIdentifier
                "8343e8b8-2e40-11eb-8192-f794be5d6ba1" .

        """
    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_licensedocument() -> None:
    """It returns a license document graph isomorphic to spec."""
    licensedocument = LicenseDocument()
    licensedocument.identifier = "http://example.com/licensedocuments/1"

    informationmodel = InformationModel()
    informationmodel.identifier = "https://example.com/informationmodels/1"

    informationmodel.licensedocument = licensedocument

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

        <https://example.com/informationmodels/1> a modelldcatno:InformationModel ;
            dct:license <http://example.com/licensedocuments/1> .

        <http://example.com/licensedocuments/1> a dct:LicenseDocument .

        """

    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_license_document_bnode() -> None:
    """It returns a license document graph isomorphic to spec."""
    licensedocument = LicenseDocument()

    informationmodel = InformationModel()
    informationmodel.identifier = "https://example.com/informationmodels/1"
    informationmodel.licensedocument = licensedocument

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

        <https://example.com/informationmodels/1> a modelldcatno:InformationModel ;
            dct:license
                [   a dct:LicenseDocument  ]
        .
        """

    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_license_document_bnode_with_types() -> None:
    """It returns an information model graph isomorphic to spec."""
    """It returns a license document graph isomorphic to spec."""
    """It returns a type graph isomorphic to spec."""

    licensedocument = LicenseDocument()

    informationmodel = InformationModel()
    informationmodel.identifier = "https://example.com/informationmodels/1"
    informationmodel.licensedocument = licensedocument

    type1 = Concept()
    type1.identifier = "https://example.com/types/1"

    licensedocument.type.append(type1)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
        @prefix skos: <http://www.w3.org/2004/02/skos/core#> .

        <https://example.com/informationmodels/1> a modelldcatno:InformationModel ;
            dct:license
                [   a dct:LicenseDocument ;
                        a skos:Concept ;
                            dct:type  <https://example.com/types/1> ;
                ]
        .
        """

    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_replaces() -> None:
    """It returns a information model graph isomorphic to spec."""
    """It returns an replaces graph isomorphic to spec."""

    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"

    replaces: List[InformationModel] = []

    replaces1 = InformationModel()
    replaces1.identifier = "https://example.com/informationmodels/2"
    replaces.append(replaces1)

    replaces2 = InformationModel()
    replaces2.identifier = "https://example.com/informationmodels/3"
    replaces.append(replaces2)

    informationmodel.replaces = replaces

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .


        <http://example.com/informationmodels/1>
            a modelldcatno:InformationModel ;
            dct:replaces <https://example.com/informationmodels/2> ;
            dct:replaces <https://example.com/informationmodels/3> ;
        .
        <https://example.com/informationmodels/2> a modelldcatno:InformationModel .
        <https://example.com/informationmodels/3> a modelldcatno:InformationModel .

        """

    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_is_replaced_by() -> None:
    """It returns a information model graph isomorphic to spec."""
    """It returns an is_replaced_by graph isomorphic to spec."""

    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"

    is_replaced_by: List[InformationModel] = []

    is_replaced_by1 = InformationModel()
    is_replaced_by1.identifier = "https://example.com/informationmodels/2"
    is_replaced_by.append(is_replaced_by1)

    is_replaced_by2 = InformationModel()
    is_replaced_by2.identifier = "https://example.com/informationmodels/3"
    is_replaced_by.append(is_replaced_by2)

    informationmodel.is_replaced_by = is_replaced_by

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .


        <http://example.com/informationmodels/1>
            a modelldcatno:InformationModel ;
            dct:isReplacedBy <https://example.com/informationmodels/2> ;
            dct:isReplacedBy <https://example.com/informationmodels/3> ;
        .
        <https://example.com/informationmodels/2> a modelldcatno:InformationModel .
        <https://example.com/informationmodels/3> a modelldcatno:InformationModel .

        """

    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_part() -> None:
    """It returns a information model graph isomorphic to spec."""
    """It returns an has_part graph isomorphic to spec."""

    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"

    has_part: List[InformationModel] = []

    has_part1 = InformationModel()
    has_part1.identifier = "https://example.com/informationmodels/2"
    has_part.append(has_part1)

    has_part2 = InformationModel()
    has_part2.identifier = "https://example.com/informationmodels/3"
    has_part.append(has_part2)

    informationmodel.has_part = has_part

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .


        <http://example.com/informationmodels/1>
            a modelldcatno:InformationModel ;
            dct:hasPart <https://example.com/informationmodels/2> ;
            dct:hasPart <https://example.com/informationmodels/3> ;
        .
        <https://example.com/informationmodels/2> a modelldcatno:InformationModel .
        <https://example.com/informationmodels/3> a modelldcatno:InformationModel .

        """

    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_is_part_of() -> None:
    """It returns a information model graph isomorphic to spec."""
    """It returns an is_part_of graph isomorphic to spec."""

    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"

    is_part_of: List[InformationModel] = []

    is_part_of1 = InformationModel()
    is_part_of1.identifier = "https://example.com/informationmodels/2"
    is_part_of.append(is_part_of1)

    is_part_of2 = InformationModel()
    is_part_of2.identifier = "https://example.com/informationmodels/3"
    is_part_of.append(is_part_of2)

    informationmodel.is_part_of = is_part_of

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix foaf:  <http://xmlns.com/foaf/0.1/> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .


        <http://example.com/informationmodels/1>
            a modelldcatno:InformationModel ;
            dct:isPartOf <https://example.com/informationmodels/2> ;
            dct:isPartOf <https://example.com/informationmodels/3> ;
        .
        <https://example.com/informationmodels/2> a modelldcatno:InformationModel .
        <https://example.com/informationmodels/3> a modelldcatno:InformationModel .

        """

    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_language() -> None:
    """It returns a language graph isomorphic to spec."""
    """It returns an identifier graph isomorphic to spec."""
    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"

    informationmodel.language.append("http://id.loc.gov/vocabulary/iso639-1/en")
    informationmodel.language.append("http://id.loc.gov/vocabulary/iso639-1/nb")

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/informationmodels/1> a modelldcatno:InformationModel ;
                dct:language    <http://id.loc.gov/vocabulary/iso639-1/en> ,
                                <http://id.loc.gov/vocabulary/iso639-1/nb> ;
    .
    """
    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_homepage() -> None:
    """It returns a homepage graph isomorphic to spec."""
    infomationmodel = InformationModel()
    infomationmodel.identifier = "http://example.com/informationmodels/1"
    infomationmodel.homepage = "http://example.org/informationmodel"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix foaf:  <http://xmlns.com/foaf/0.1/> .

    <http://example.com/informationmodels/1> a modelldcatno:InformationModel ;
        foaf:homepage <http://example.org/informationmodel> ;
    .
    """
    g1 = Graph().parse(data=infomationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_keyword() -> None:
    """It returns a keyword graph isomorphic to spec."""
    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"
    _keyword = {"nb": "Etnøkkelord", "nn": "Eitnøkkelord", "en": "Akeyword"}
    informationmodel.keyword = _keyword

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcat: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix foaf:  <http://xmlns.com/foaf/0.1/> .

    <http://example.com/informationmodels/1> a modelldcat:InformationModel ;
        dcat:keyword   "Akeyword"@en, "Etnøkkelord"@nb, "Eitnøkkelord"@nn ;
        .
    """
    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_release_date() -> None:
    """It returns a issued graph isomorphic to spec."""
    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"
    informationmodel.release_date = "2020-03-24"

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcat: <https://data.norge.no/vocabulary/modelldcatno#> .
    @prefix foaf:  <http://xmlns.com/foaf/0.1/> .

    @prefix xsd:   <http://www.w3.org/2001/XMLSchema#> .

    <http://example.com/informationmodels/1> a modelldcat:InformationModel ;
        dct:issued   "2020-03-24"^^xsd:date ;
        .
    """

    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
