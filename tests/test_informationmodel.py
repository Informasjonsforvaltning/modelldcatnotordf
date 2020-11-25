"""Test cases for the informationmodel module."""

from datacatalogtordf import Agent
import pytest
from rdflib import Graph, Namespace
from rdflib.compare import graph_diff, isomorphic

from modelldcatnotordf.modelldcatno import InformationModel
from modelldcatnotordf.modelldcatno import ModelElement

"""
A test class for testing the class InformationModel.

"""


def test_instantiate_informationmodel() -> None:
    """It returns a TypeErro exception."""
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

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


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

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


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

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


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

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_subject() -> None:
    """It returns a subject graph isomorphic to spec."""
    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"
    informationmodel.subject.append("http://example.com/subjects/1")
    informationmodel.subject.append("http://example.com/subjects/2")

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/informationmodels/1> a modelldcatno:InformationModel ;
        dct:Subject <http://example.com/subjects/1> ;
        dct:Subject <http://example.com/subjects/2> ;
    .
    """
    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_contains_model_element() -> None:
    """It returns a subject graph isomorphic to spec."""
    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"
    modelelement = ModelElement()
    modelelement.identifier = "http://example.com/modelelements/1"
    informationmodel.modelelements.append(modelelement)
    modelelement.title = {"nb": "Tittel 1", "en": "Title 1"}

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix skos: <http://www.w3.org/2004/02/skos/core#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/informationmodels/1> a modelldcatno:InformationModel ;
        modelldcatno:containsModelelement <http://example.com/modelelements/1> .

    <http://example.com/modelelements/1> a modelldcatno:ModelElement ;
        dct:title   "Title 1"@en, "Tittel 1"@nb
    .
    """
    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_modelelements_blank_node() -> None:
    """It returns a model element graph isomorphic to spec."""
    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"

    modelelement = ModelElement()
    informationmodel.modelelements.append(modelelement)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/informationmodels/1> a modelldcatno:InformationModel ;
            modelldcatno:containsModelelement [ a modelldcatno:ModelElement ] .

        """
    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


def test_to_graph_should_return_modelelements_blank_node_with_properties() -> None:
    """It returns a model element graph isomorphic to spec."""
    informationmodel = InformationModel()
    informationmodel.identifier = "http://example.com/informationmodels/1"

    modelelement = ModelElement()
    modelelement.title = {"nb": "Tittel 1", "en": "Title 1"}

    informationmodel.modelelements.append(modelelement)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/informationmodels/1> a modelldcatno:InformationModel ;
            modelldcatno:containsModelelement [ a modelldcatno:ModelElement ;
            dct:title   "Title 1"@en, "Tittel 1"@nb ] .

        """
    g1 = Graph().parse(data=informationmodel.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic


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
