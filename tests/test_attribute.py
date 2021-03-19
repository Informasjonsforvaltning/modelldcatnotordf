"""Test cases for the attribute module."""
import pytest
from pytest_mock import MockFixture
from rdflib import Graph

from modelldcatnotordf.modelldcatno import (
    Attribute,
    CodeList,
    DataType,
    ObjectType,
    SimpleType,
)
from tests import testutils
from tests.testutils import assert_isomorphic, skolemization

"""
A test class for testing the class Attribute.

"""


def test_instantiate_attribute() -> None:
    """It does not raise an exception."""
    try:
        _ = Attribute()
    except Exception:
        pytest.fail("Unexpected Exception ..")


def test_to_graph_should_return_skolemization(mocker: MockFixture) -> None:
    """It returns a attribute graph as blank node isomorphic to spec."""
    attribute = Attribute()

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
         a modelldcatno:Attribute  .

        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_identifier() -> None:
    """It returns an identifier graph isomorphic to spec."""
    attribute = Attribute()
    attribute.identifier = "http://example.com/attributes/1"

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/attributes/1> a modelldcatno:Attribute .

        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_contains_object_type_both_identifiers() -> None:
    """It returns a contains_object_type graph isomorphic to spec."""
    attribute = Attribute()
    attribute.identifier = "http://example.com/attributes/1"

    objecttype = ObjectType()
    objecttype.identifier = "http://example.com/objecttypes/1"
    attribute.contains_object_type = objecttype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/attributes/1> a modelldcatno:Attribute ;
            modelldcatno:containsObjectType <http://example.com/objecttypes/1> .

        <http://example.com/objecttypes/1> a modelldcatno:ObjectType ;

        .
        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_contains_object_type_skolemization_attribute_id(
    mocker: MockFixture,
) -> None:
    """It returns a contains_object_type graph isomorphic to spec."""
    attribute = Attribute()
    attribute.identifier = "http://example.com/attributes/1"

    objecttype = ObjectType()
    attribute.contains_object_type = objecttype

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://example.com/attributes/1> a modelldcatno:Attribute ;
        modelldcatno:containsObjectType
        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
    .
    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
    a modelldcatno:ObjectType .
    """

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_contains_object_type_objecttype_id(
    mocker: MockFixture,
) -> None:
    """It returns a contains_object_type graph isomorphic to spec."""
    attribute = Attribute()

    objecttype = ObjectType()
    objecttype.identifier = "http://example.com/objecttypes/1"
    attribute.contains_object_type = objecttype

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
         a modelldcatno:Attribute ;
            modelldcatno:containsObjectType <http://example.com/objecttypes/1>
         .

        <http://example.com/objecttypes/1> a modelldcatno:ObjectType .

        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_contains_object_type_both_skolemizations(
    mocker: MockFixture,
) -> None:
    """It returns a contains_object_type graph isomorphic to spec."""
    attribute = Attribute()

    objecttype = ObjectType()
    attribute.contains_object_type = objecttype

    skolemutils = testutils.SkolemUtils()

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        side_effect=skolemutils.get_skolemization,
    )

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:Attribute ; modelldcatno:containsObjectType
        <http://wwww.digdir.no/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce>
    .
    <http://wwww.digdir.no/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce>
        a modelldcatno:ObjectType
    .
    """

    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_simple_type_both_identifiers() -> None:
    """It returns a has_simple_type graph isomorphic to spec."""
    attribute = Attribute()
    attribute.identifier = "http://example.com/attributes/1"

    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    attribute.has_simple_type = simpletype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/attributes/1> a modelldcatno:Attribute ;
            modelldcatno:hasSimpleType <http://example.com/simpletypes/1> .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType ;

        .
        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_simple_type_bnode_attribute_id() -> None:
    """It returns a has_simple_type graph isomorphic to spec."""
    attribute = Attribute()
    attribute.identifier = "http://example.com/attributes/1"

    simpletype = SimpleType()
    attribute.has_simple_type = simpletype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/attributes/1> a modelldcatno:Attribute ;
            modelldcatno:hasSimpleType [ a modelldcatno:SimpleType ] .

        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_simple_type_skolemization_simpletype(
    mocker: MockFixture,
) -> None:
    """It returns a has_simple_type graph isomorphic to spec."""
    attribute = Attribute()

    simpletype = SimpleType()
    simpletype.identifier = "http://example.com/simpletypes/1"
    attribute.has_simple_type = simpletype

    skolemutils = testutils.SkolemUtils()

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        side_effect=skolemutils.get_skolemization,
    )

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a modelldcatno:Attribute ;
            modelldcatno:hasSimpleType <http://example.com/simpletypes/1>
         .

        <http://example.com/simpletypes/1> a modelldcatno:SimpleType .

        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_simple_type_both_skolemized(
    mocker: MockFixture,
) -> None:
    """It returns a has_simple_type graph isomorphic to spec."""
    attribute = Attribute()

    simpletype = SimpleType()
    attribute.has_simple_type = simpletype

    skolemutils = testutils.SkolemUtils()

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        side_effect=skolemutils.get_skolemization,
    )

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a modelldcatno:Attribute ;
            modelldcatno:hasSimpleType [ a modelldcatno:SimpleType ]
         .
        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_data_type_both_identifiers() -> None:
    """It returns a has_data_type graph isomorphic to spec."""
    attribute = Attribute()
    attribute.identifier = "http://example.com/attributes/1"

    datatype = DataType()
    datatype.identifier = "http://example.com/datatypes/1"
    attribute.has_data_type = datatype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/attributes/1> a modelldcatno:Attribute ;
            modelldcatno:hasDataType <http://example.com/datatypes/1> .

        <http://example.com/datatypes/1> a modelldcatno:DataType ;

        .
        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_data_type_bnode_attribute_id(
    mocker: MockFixture,
) -> None:
    """It returns a has_data_type graph isomorphic to spec."""
    attribute = Attribute()
    attribute.identifier = "http://example.com/attributes/1"

    datatype = DataType()
    attribute.has_data_type = datatype

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

    <http://example.com/attributes/1> a modelldcatno:Attribute ;
        modelldcatno:hasDataType
    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94> .

    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:DataType  .

    """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_data_type_skolemization_datatype(
    mocker: MockFixture,
) -> None:
    """It returns a has_data_type graph isomorphic to spec."""
    attribute = Attribute()

    datatype = DataType()
    datatype.identifier = "http://example.com/datatypes/1"
    attribute.has_data_type = datatype

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
         a modelldcatno:Attribute ;
            modelldcatno:hasDataType <http://example.com/datatypes/1>
         .

        <http://example.com/datatypes/1> a modelldcatno:DataType .

        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_data_type_both_skolemized(
    mocker: MockFixture,
) -> None:
    """It returns a has_data_type graph isomorphic to spec."""
    attribute = Attribute()

    datatype = DataType()
    attribute.has_data_type = datatype

    skolemutils = testutils.SkolemUtils()

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        side_effect=skolemutils.get_skolemization,
    )

    src = """
    @prefix dct: <http://purl.org/dc/terms/> .
    @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
    @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
    @prefix dcat: <http://www.w3.org/ns/dcat#> .
    @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

    <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
        a modelldcatno:Attribute ; modelldcatno:hasDataType
        <http://wwww.digdir.no/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce>
    .

    <http://wwww.digdir.no/.well-known/skolem/21043186-80ce-11eb-9829-cf7c8fc855ce>
        a modelldcatno:DataType
         .
        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_value_from_both_identifiers() -> None:
    """It returns a has_value_from graph isomorphic to spec."""
    attribute = Attribute()
    attribute.identifier = "http://example.com/attributes/1"

    codelist = CodeList()
    codelist.identifier = "http://example.com/codelists/1"
    attribute.has_value_from = codelist

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/attributes/1> a modelldcatno:Attribute ;
            modelldcatno:hasValueFrom <http://example.com/codelists/1> .

        <http://example.com/codelists/1> a modelldcatno:CodeList ;

        .
        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_value_from_bnode_attribute_id() -> None:
    """It returns a has_value_from graph isomorphic to spec."""
    attribute = Attribute()
    attribute.identifier = "http://example.com/attributes/1"

    codelist = CodeList()
    attribute.has_value_from = codelist

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/attributes/1> a modelldcatno:Attribute ;
            modelldcatno:hasValueFrom [ a modelldcatno:CodeList ] .

        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_value_from_skolemization_codelist(
    mocker: MockFixture,
) -> None:
    """It returns a has_value_from graph isomorphic to spec."""
    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        return_value=skolemization,
    )

    attribute = Attribute()

    codelist = CodeList()
    codelist.identifier = "http://example.com/codelists/1"
    attribute.has_value_from = codelist

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a modelldcatno:Attribute ;
            modelldcatno:hasValueFrom <http://example.com/codelists/1>
         .

        <http://example.com/codelists/1> a modelldcatno:CodeList .

        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_value_from_both_skolemized(
    mocker: MockFixture,
) -> None:
    """It returns a has_value_from graph isomorphic to spec."""
    attribute = Attribute()

    codelist = CodeList()
    attribute.has_value_from = codelist

    skolemutils = testutils.SkolemUtils()

    mocker.patch(
        "modelldcatnotordf.skolemizer.Skolemizer.add_skolemization",
        side_effect=skolemutils.get_skolemization,
    )

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://wwww.digdir.no/.well-known/skolem/284db4d2-80c2-11eb-82c3-83e80baa2f94>
         a modelldcatno:Attribute ;
            modelldcatno:hasValueFrom [ a modelldcatno:CodeList ]
         .
        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_contains_object_type_as_uri() -> None:
    """It returns a contains_object_type graph isomorphic to spec."""
    attribute = Attribute()
    attribute.identifier = "http://example.com/attributes/1"

    objecttype = "http://example.com/objecttypes/1"
    attribute.contains_object_type = objecttype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/attributes/1> a modelldcatno:Attribute ;
            modelldcatno:containsObjectType <http://example.com/objecttypes/1> .


        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_simple_type_as_uri() -> None:
    """It returns a has_simple_type graph isomorphic to spec."""
    attribute = Attribute()
    attribute.identifier = "http://example.com/attributes/1"

    simpletype = "http://example.com/simpletypes/1"
    attribute.has_simple_type = simpletype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/attributes/1> a modelldcatno:Attribute ;
            modelldcatno:hasSimpleType <http://example.com/simpletypes/1> .

        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_data_type_as_uri() -> None:
    """It returns a has_data_type graph isomorphic to spec."""
    attribute = Attribute()
    attribute.identifier = "http://example.com/attributes/1"

    datatype = "http://example.com/datatypes/1"
    attribute.has_data_type = datatype

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/attributes/1> a modelldcatno:Attribute ;
            modelldcatno:hasDataType <http://example.com/datatypes/1> .


        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)


def test_to_graph_should_return_has_value_from_as_uri() -> None:
    """It returns a has_value_from graph isomorphic to spec."""
    attribute = Attribute()
    attribute.identifier = "http://example.com/attributes/1"

    codelist = "http://example.com/codelists/1"
    attribute.has_value_from = codelist

    src = """
        @prefix dct: <http://purl.org/dc/terms/> .
        @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
        @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
        @prefix dcat: <http://www.w3.org/ns/dcat#> .
        @prefix modelldcatno: <https://data.norge.no/vocabulary/modelldcatno#> .

        <http://example.com/attributes/1> a modelldcatno:Attribute ;
            modelldcatno:hasValueFrom <http://example.com/codelists/1> .

        """
    g1 = Graph().parse(data=attribute.to_rdf(), format="turtle")
    g2 = Graph().parse(data=src, format="turtle")

    assert_isomorphic(g1, g2)
