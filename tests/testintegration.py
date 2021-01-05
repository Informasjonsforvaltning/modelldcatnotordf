"""Test cases for larger scale integration across classes."""

from rdflib import Graph

from modelldcatnotordf.modelldcatno import InformationModel, ObjectType
from modelldcatnotordf.modelldcatno import ModelProperty
from tests.testutils import assert_isomorphic

"""
Test cases for larger scale integration across classes.

"""


def test_title_should_be_set_on_correct_element() -> None:
    """It returns a information model graph isomorphic to spec."""
    element = ObjectType()
    element.identifier = "http://example.com/element"
    element.title = {"nb": "element"}

    prop0 = ModelProperty()
    prop0.identifier = "http://example.com/egenskap0"
    prop0.title = {"nb": "egenskap0"}
    element.has_property.append(prop0)

    prop1 = ModelProperty()
    prop1.identifier = "http://example.com/egenskap1"
    prop1.title = {"nb": "egenskap1"}
    element.has_property.append(prop1)

    prop2 = ModelProperty()
    prop2.identifier = "http://example.com/egenskap2"
    prop2.title = {"nb": "egenskap2"}
    element.has_property.append(prop2)

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
                modelldcatno:containsModelelement <http://example.com/element> .

        <http://example.com/egenskap0> a modelldcatno:Property ;
                dct:title "egenskap0"@nb .

        <http://example.com/egenskap1> a modelldcatno:Property ;
                dct:title "egenskap1"@nb .

        <http://example.com/egenskap2> a modelldcatno:Property ;
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
