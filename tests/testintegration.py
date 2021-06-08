"""Test cases for larger scale integration across classes."""
from pytest_mock import MockFixture
from rdflib import Graph
from skolemizer.testutils import SkolemUtils

from modelldcatnotordf.modelldcatno import (
    Attribute,
    DataType,
    InformationModel,
    ObjectType,
)
from modelldcatnotordf.modelldcatno import Role
from tests.testutils import assert_isomorphic

"""
Test cases for larger scale integration across classes.

"""


def test_title_should_be_set_on_correct_element() -> None:
    """It returns a information model graph isomorphic to spec."""
    element = ObjectType()
    element.identifier = "http://example.com/element"
    element.title = {"nb": "element"}

    modelproperty0 = Role()
    modelproperty0.identifier = "http://example.com/egenskap0"
    modelproperty0.title = {"nb": "egenskap0"}
    element.has_property.append(modelproperty0)

    modelproperty1 = Role()
    modelproperty1.identifier = "http://example.com/egenskap1"
    modelproperty1.title = {"nb": "egenskap1"}
    element.has_property.append(modelproperty1)

    modelproperty2 = Role()
    modelproperty2.identifier = "http://example.com/egenskap2"
    modelproperty2.title = {"nb": "egenskap2"}
    element.has_property.append(modelproperty2)

    model = InformationModel()
    model.identifier = "http://example.com/modell"
    model.modelelements.append(element)

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/modell> a modelldcatno:InformationModel ;
                modelldcatno:containsModelElement <http://example.com/element> .

        <http://example.com/egenskap0> a modelldcatno:Role ;
                dct:title "egenskap0"@nb .

        <http://example.com/egenskap1> a modelldcatno:Role ;
                dct:title "egenskap1"@nb .

        <http://example.com/egenskap2> a modelldcatno:Role ;
                dct:title "egenskap2"@nb .

        <http://example.com/element> a modelldcatno:ObjectType ;
                dct:title "element"@nb ;
                modelldcatno:hasProperty <http://example.com/egenskap0>,
                                        <http://example.com/egenskap1>,
                                        <http://example.com/egenskap2> .
          """

    g1 = Graph().parse(data=model.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_should_support_three_generations_of_nodes_without_identifier(
    mocker: MockFixture,
) -> None:
    """It returns a datatype graph isomorphic to spec."""
    datatype1 = DataType()
    attribute = Attribute()
    datatype2 = DataType()
    datatype1.has_property.append(attribute)
    attribute.has_data_type = datatype2
    datatype2.title = {"nb": "Tittel på datatype 2"}

    skolemutils = SkolemUtils()

    mocker.patch(
        "skolemizer.Skolemizer.add_skolemization",
        side_effect=skolemutils.get_skolemization,
    )

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:DataType ; modelldcatno:hasProperty
    <http://example.com/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce> .

    <http://example.com/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce>
        a modelldcatno:Attribute ; modelldcatno:hasDataType
    <http://example.com/.well-known/skolem/279b7540-80ce-11eb-ba1a-7fa81b1658fe> .

    <http://example.com/.well-known/skolem/279b7540-80ce-11eb-ba1a-7fa81b1658fe>
        a modelldcatno:DataType ;
        dct:title "Tittel på datatype 2"@nb .

    """

    g1 = Graph().parse(data=datatype1.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
