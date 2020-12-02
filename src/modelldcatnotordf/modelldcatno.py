"""Modelldcatno module for mapping a Modelldcatno model to rdf.

This module contains methods for mapping to rdf
according to the modelldcat-ap-no specification._

Refer to sub-class for typical usage examples.
"""
from __future__ import annotations

from typing import Any, List, Optional

from concepttordf import Concept
from datacatalogtordf import Agent, Resource, URI
from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef

from modelldcatnotordf.licensedocument import LicenseDocument

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
PROV = Namespace("http://www.w3.org/ns/prov#")
MODELLDCATNO = Namespace("https://data.norge.no/vocabulary/modelldcatno#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")


class InformationModel(Resource):
    """A class representing a modelldatno:InformationModel."""

    __slots__ = (
        "_title",
        "_type",
        "_description",
        "_theme",
        "_publisher",
        "_subject",
        "_modelelements",
        "_informationmodelidentifier",
        "_licensedocument",
    )

    _title: dict
    _publisher: Agent
    _subject: List[Concept]
    _modelelements: List[ModelElement]
    _informationmodelidentifier: str
    _licensedocument: LicenseDocument

    def __init__(self) -> None:
        """Inits InformationModel object with default values."""
        super().__init__()
        self._type = MODELLDCATNO.InformationModel
        self._subject = []
        self._modelelements = []

    @property
    def informationmodelidentifier(self) -> str:
        """Get for informationmodelidentifier."""
        return self._informationmodelidentifier

    @informationmodelidentifier.setter
    def informationmodelidentifier(self, informationmodelidentifier: str) -> None:
        self._informationmodelidentifier = informationmodelidentifier

    @property
    def type(self) -> str:
        """Get for type."""
        return self._type

    @property
    def licensedocument(self) -> LicenseDocument:
        """Get for license."""
        return self._licensedocument

    @licensedocument.setter
    def licensedocument(self, licensedocument: LicenseDocument) -> None:
        self._licensedocument = licensedocument

    @property
    def title(self) -> dict:
        """Get for title."""
        return self._title

    @title.setter
    def title(self, value: dict) -> None:
        self._title = value

    @property
    def description(self) -> dict:
        """Get for description."""
        return self._description

    @description.setter
    def description(self, value: dict) -> None:
        self._description = value

    @property
    def theme(self) -> List[str]:
        """Get for theme."""
        return self._theme

    @theme.setter
    def theme(self, value: List[str]) -> None:
        self._theme = value

    @property
    def publisher(self: InformationModel) -> Agent:
        """Get for publisher."""
        return self._publisher

    @publisher.setter
    def publisher(self: InformationModel, publisher: Agent) -> None:
        self._publisher = publisher

    @property
    def subject(self: InformationModel) -> List[Concept]:
        """Get for subject."""
        return self._subject

    @property
    def modelelements(self: InformationModel) -> List[ModelElement]:
        """Get for modelelements."""
        return self._modelelements

    def to_rdf(
        self: InformationModel,
        format: str = "turtle",
        encoding: Optional[str] = "utf-8",
    ) -> str:
        """Maps the information model to rdf.

        Available formats:
         - turtle (default)
         - xml
         - json-ld

        Args:
            format (str): a valid format.
            encoding (str): the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    # -

    def _to_graph(self: InformationModel) -> Graph:

        super(InformationModel, self)._to_graph()

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        self._publisher_to_graph()
        self._subject_to_graph()
        self._modelelements_to_graph()
        self._licensedocument_to_graph()

        if getattr(self, "informationmodelidentifier", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    MODELLDCATNO.informationModelIdentifier,
                    Literal(self._informationmodelidentifier),
                )
            )

        return self._g

    def _subject_to_graph(self: InformationModel) -> None:
        if getattr(self, "subject", None):

            for subject in self._subject:

                _subject = URIRef(subject.identifier)

                for _s, p, o in subject._to_graph().triples((None, None, None)):
                    self._g.add((_subject, p, o))

                self._g.add((URIRef(self.identifier), DCT.subject, _subject,))

    def _modelelements_to_graph(self: InformationModel) -> None:

        if getattr(self, "modelelements", None):

            for modelelement in self._modelelements:

                if getattr(modelelement, "identifier", None):
                    _modelelement = URIRef(modelelement.identifier)
                else:
                    _modelelement = BNode()

                for _s, p, o in modelelement._to_graph().triples((None, None, None)):
                    self._g.add((_modelelement, p, o))

                self._g.add(
                    (
                        URIRef(self.identifier),
                        MODELLDCATNO.containsModelelement,
                        _modelelement,
                    )
                )

    def _licensedocument_to_graph(self: InformationModel) -> None:

        if getattr(self, "licensedocument", None):

            if getattr(self.licensedocument, "identifier", None):
                _licensedocument = URIRef(self.licensedocument.identifier)

            else:
                _licensedocument = BNode()

            for _s, p, o in self.licensedocument._to_graph().triples(
                (None, None, None)
            ):
                self._g.add((_licensedocument, p, o))

            self._g.add((URIRef(self.identifier), DCT.license, _licensedocument))


class ModelElement:
    """A class representing a modelldcatno:ModelElement."""

    __slots__ = (
        "_type",
        "_g",
        "_title",
        "_identifier",
        "_has_property",
        "_dct_identifier",
        "_subject",
    )

    _g: Graph
    _title: dict
    _identifier: URI
    _dct_identifier: str
    _has_property: List[Any]
    _subject: Concept

    def __init__(self) -> None:
        """Inits an object with default values."""
        self._type = MODELLDCATNO.ModelElement
        self._has_property = []

    @property
    def identifier(self) -> str:
        """Get for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str) -> None:
        self._identifier = URI(identifier)

    @property
    def dct_identifier(self) -> str:
        """Get for dct_identifier."""
        return self._dct_identifier

    @dct_identifier.setter
    def dct_identifier(self, dct_identifier: str) -> None:
        self._dct_identifier = dct_identifier

    @property
    def title(self) -> dict:
        """Title attribute."""
        return self._title

    @title.setter
    def title(self, title: dict) -> None:
        self._title = title

    @property
    def subject(self) -> Concept:
        """Get for subject."""
        return self._subject

    @subject.setter
    def subject(self, subject: Concept) -> None:
        self._subject = subject

    @property
    def has_property(self) -> List[Any]:
        """Get for has_type."""
        return self._has_property

    def to_rdf(self, format: str = "turtle", encoding: Optional[str] = "utf-8") -> str:
        """Maps the modelelement to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(self, type: str = MODELLDCATNO.ModelElement) -> Graph:
        """Returns the modelelement as graph.

         Args:
            type: type for identifying class. Default: MODELLDCATNO.ModelElement

        Returns:
            the modelelement graph
        """
        # Set up graph and namespaces:
        self._g = Graph()
        self._g.bind("modelldcatno", MODELLDCATNO)
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)
        self._g.bind("skos", SKOS)

        if getattr(self, "identifier", None):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        self._g.add((_self, RDF.type, type))

        if getattr(self, "title", None):
            for key in self.title:
                self._g.add((_self, DCT.title, Literal(self.title[key], lang=key),))

        if getattr(self, "dct_identifier", None):
            self._g.add((_self, DCT.identifier, Literal(self._dct_identifier)))

        if getattr(self, "subject", None):

            _subject = URIRef(self.subject.identifier)

            for _s, p, o in self.subject._to_graph().triples((None, None, None)):
                self._g.add((_subject, p, o))

            self._g.add((_self, DCT.subject, _subject))

        if getattr(self, "has_property", None):
            self._has_property_to_graph(_self)

        return self._g

    def _has_property_to_graph(self, _self: Any) -> None:
        if getattr(self, "has_property", None):
            for has_property in self._has_property:

                if getattr(has_property, "identifier", None):
                    _has_property = URIRef(has_property.identifier)
                else:
                    _has_property = BNode()

                for _s, p, o in has_property._to_graph().triples((None, None, None)):
                    self._g.add((_has_property, p, o))

                self._g.add((_self, MODELLDCATNO.hasProperty, _has_property,))


class ModelProperty:
    """A class representing a modelldcatno:Property."""

    __slots__ = (
        "_type",
        "_g",
        "_title",
        "_identifier",
        "_has_type",
        "_min_occurs",
        "_max_occurs",
        "_title",
        "_subject",
    )

    _g: Graph
    _identifier: URI
    _has_type: List[ModelElement]
    _min_occurs: int
    _max_occurs: int
    _title: dict
    _subject: Concept

    def __init__(self) -> None:
        """Inits an object with default values."""
        self._type = MODELLDCATNO.Property
        self._has_type = []

    @property
    def subject(self) -> Concept:
        """Get for subject."""
        return self._subject

    @subject.setter
    def subject(self, subject: Concept) -> None:
        self._subject = subject

    @property
    def title(self) -> dict:
        """Title attribute."""
        return self._title

    @title.setter
    def title(self, title: dict) -> None:
        self._title = title

    @property
    def has_type(self) -> List[ModelElement]:
        """Get for has_type."""
        return self._has_type

    @property
    def identifier(self) -> str:
        """Get for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str) -> None:
        self._identifier = URI(identifier)

    @property
    def min_occurs(self) -> int:
        """Get for min_occurs."""
        return self._min_occurs

    @min_occurs.setter
    def min_occurs(self, min_occurs: int) -> None:
        self._min_occurs = min_occurs

    @property
    def max_occurs(self) -> int:
        """Get for max_occurs."""
        return self._max_occurs

    @max_occurs.setter
    def max_occurs(self, max_occurs: int) -> None:
        self._max_occurs = max_occurs

    def to_rdf(self, format: str = "turtle", encoding: Optional[str] = "utf-8") -> str:
        """Maps the property to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self, type: str = MODELLDCATNO.Property, selfobject: Any = None
    ) -> Graph:
        """Returns the property as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Property
            selfobject: a bnode or URI passed from an subclass Default: None

        Returns:
            the property graph
        """
        # Set up graph and namespaces:
        self._g = Graph()
        self._g.bind("modelldcatno", MODELLDCATNO)
        self._g.bind("dct", DCT)
        self._g.bind("skos", SKOS)

        if selfobject:
            _self = selfobject

        elif getattr(self, "identifier", None):
            _self = URIRef(self.identifier)

        else:
            _self = BNode()

        self._g.add((_self, RDF.type, type))

        self._has_type_to_graph(_self)

        if getattr(self, "min_occurs", None):
            self._g.add((_self, XSD.minOccurs, Literal(self.min_occurs)))

        if getattr(self, "max_occurs", None):
            self._g.add((_self, XSD.maxOccurs, Literal(self.max_occurs)))

        if getattr(self, "title", None):
            for key in self.title:
                self._g.add((_self, DCT.title, Literal(self.title[key], lang=key),))

        if getattr(self, "subject", None):

            _subject = URIRef(self.subject.identifier)

            for _s, p, o in self.subject._to_graph().triples((None, None, None)):
                self._g.add((_subject, p, o))

            self._g.add((_self, DCT.subject, _subject))

        return self._g

    def _has_type_to_graph(self, _self: Any) -> None:
        if getattr(self, "has_type", None):

            for has_type in self._has_type:

                if getattr(has_type, "identifier", None):
                    _has_type = URIRef(has_type.identifier)
                else:
                    _has_type = BNode()

                for _s, p, o in has_type._to_graph().triples((None, None, None)):
                    self._g.add((_has_type, p, o))

                self._g.add((_self, MODELLDCATNO.hasType, _has_type,))


class Role(ModelProperty):
    """A class representing a modelldcatno:Role."""

    __slots__ = (
        "_identifier",
        "_has_object_type",
    )

    _identifier: URI
    _has_object_type: ObjectType
    _g: Graph

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()

    @property
    def has_object_type(self: Role) -> ObjectType:
        """Get for has_object_type."""
        return self._has_object_type

    @has_object_type.setter
    def has_object_type(self: Role, has_object_type: Any) -> None:
        self._has_object_type = has_object_type

    def to_rdf(
        self: Role, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> str:
        """Maps the role to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: Role, type: str = MODELLDCATNO.Role, selfobject: Any = None
    ) -> Graph:
        """Returns the role as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Role
            selfobject: a bnode or URI passed from an subclass Default: None

        Returns:
            the role graph
        """
        if getattr(self, "identifier", None):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        super(Role, self)._to_graph(MODELLDCATNO.Role, _self)

        self._has_object_type_to_graph(_self)

        return self._g

    def _has_object_type_to_graph(self, _self: Any) -> None:

        if getattr(self, "has_object_type", None):

            if getattr(self._has_object_type, "identifier", None):
                _has_object_type = URIRef(self._has_object_type.identifier)
            else:
                _has_object_type = BNode()

            for _s, p, o in self._has_object_type._to_graph().triples(
                (None, None, None)
            ):
                self._g.add((_has_object_type, p, o))

            self._g.add((_self, MODELLDCATNO.hasObjectType, _has_object_type))


class ObjectType(ModelElement):
    """A class representing a modelldcatno:ObjectType."""

    _identifier: URI
    _dct_identifier: str
    _g: Graph

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()

    def to_rdf(
        self: ObjectType, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> str:
        """Maps the object type to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(self: ObjectType, type: str = MODELLDCATNO.ObjectType) -> Graph:
        """Returns the object type as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.ObjectType

        Returns:
            the object type graph
        """
        super(ObjectType, self)._to_graph(MODELLDCATNO.ObjectType)

        return self._g
