"""Modelldcatno module for mapping a Modelldcatno model to rdf.

This module contains methods for mapping to rdf
according to the modelldcat-ap-no specification._

Refer to sub-class for typical usage examples.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
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
XKOS = Namespace("http://rdf-vocabulary.ddialliance.org/xkos#")


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
        """Set for informationmodelidentifier."""
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
        """Set for license."""
        self._licensedocument = licensedocument

    @property
    def title(self) -> dict:
        """Get for title."""
        return self._title

    @title.setter
    def title(self, value: dict) -> None:
        """Set for title."""
        self._title = value

    @property
    def description(self) -> dict:
        """Get for description."""
        return self._description

    @description.setter
    def description(self, value: dict) -> None:
        """Set for description."""
        self._description = value

    @property
    def theme(self) -> List[str]:
        """Get for theme."""
        return self._theme

    @theme.setter
    def theme(self, value: List[str]) -> None:
        """Set for theme."""
        self._theme = value

    @property
    def publisher(self: InformationModel) -> Agent:
        """Get for publisher."""
        return self._publisher

    @publisher.setter
    def publisher(self: InformationModel, publisher: Agent) -> None:
        """Set for publisher."""
        self._publisher = publisher

    @property
    def subject(self: InformationModel) -> List[Concept]:
        """Get for subject."""
        return self._subject

    @subject.setter
    def subject(self: InformationModel, subject: List[Concept]) -> None:
        """Set for subject."""
        self._subject = subject

    @property
    def modelelements(self: InformationModel) -> List[ModelElement]:
        """Get for modelelements."""
        return self._modelelements

    @modelelements.setter
    def modelelements(
        self: InformationModel, modelelements: List[ModelElement]
    ) -> None:
        """Set for modelelements."""
        self._modelelements = modelelements

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

                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCT.subject,
                        _subject,
                    )
                )

    def _modelelements_to_graph(self: InformationModel) -> None:

        if getattr(self, "modelelements", None):

            for modelelement in self._modelelements:

                if getattr(modelelement, "identifier", None):
                    _modelelement = URIRef(modelelement.identifier)
                else:
                    _modelelement = BNode()

                for _s, p, o in modelelement._to_graph().triples((None, None, None)):
                    self._g.add(
                        (_modelelement, p, o)
                        if isinstance(_modelelement, BNode)
                        else (_s, p, o)
                    )

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
                self._g.add(
                    (_licensedocument, p, o)
                    if isinstance(_licensedocument, BNode)
                    else (_s, p, o)
                )

            self._g.add((URIRef(self.identifier), DCT.license, _licensedocument))


class ModelElement(ABC):
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
    _has_property: List[ModelProperty]
    _subject: Concept

    @abstractmethod
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
        """Set for identifier."""
        self._identifier = URI(identifier)

    @property
    def dct_identifier(self) -> str:
        """Get for dct_identifier."""
        return self._dct_identifier

    @dct_identifier.setter
    def dct_identifier(self, dct_identifier: str) -> None:
        """Set for dct_identifier."""
        self._dct_identifier = dct_identifier

    @property
    def title(self) -> dict:
        """Get for Title attribute."""
        return self._title

    @title.setter
    def title(self, title: dict) -> None:
        """Set for Title attribute."""
        self._title = title

    @property
    def subject(self) -> Concept:
        """Get for subject."""
        return self._subject

    @subject.setter
    def subject(self, subject: Concept) -> None:
        """Set for subject."""
        self._subject = subject

    @property
    def has_property(self) -> List[ModelProperty]:
        """Get for has_property."""
        return self._has_property

    @has_property.setter
    def has_property(self, has_property: List[ModelProperty]) -> None:
        """Set for has_property."""
        self._has_property = has_property

    @abstractmethod
    def to_rdf(self, format: str = "turtle", encoding: Optional[str] = "utf-8") -> str:
        """Maps the modelelement to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        """

    def _to_graph(
        self, type: str = MODELLDCATNO.ModelElement, selfobject: Any = None
    ) -> Graph:
        """Returns the modelelement as graph.

         Args:
            type: type for identifying class. Default: MODELLDCATNO.ModelElement
            selfobject: a bnode or URI passed from a subclass Default: None

        Returns:
            the modelelement graph
        """
        # Set up graph and namespaces:
        self._g = Graph()
        self._g.bind("modelldcatno", MODELLDCATNO)
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)
        self._g.bind("skos", SKOS)
        self._g.bind("xsd", XSD)

        self._g.add((selfobject, RDF.type, type))

        if getattr(self, "title", None):
            for key in self.title:
                self._g.add(
                    (
                        selfobject,
                        DCT.title,
                        Literal(self.title[key], lang=key),
                    )
                )

        if getattr(self, "dct_identifier", None):
            self._g.add((selfobject, DCT.identifier, Literal(self._dct_identifier)))

        if getattr(self, "subject", None):

            _subject = URIRef(self.subject.identifier)

            for _s, p, o in self.subject._to_graph().triples((None, None, None)):
                self._g.add((_subject, p, o))

            self._g.add((selfobject, DCT.subject, _subject))

        if getattr(self, "has_property", None):
            self._has_property_to_graph(selfobject)

        return self._g

    def _has_property_to_graph(self, _self: Any) -> None:
        if getattr(self, "has_property", None):
            for has_property in self._has_property:

                if getattr(has_property, "identifier", None):
                    _has_property = URIRef(has_property.identifier)
                else:
                    _has_property = BNode()

                for _s, p, o in has_property._to_graph().triples((None, None, None)):
                    self._g.add(
                        (_has_property, p, o)
                        if isinstance(_has_property, BNode)
                        else (_s, p, o)
                    )

                self._g.add(
                    (
                        _self,
                        MODELLDCATNO.hasProperty,
                        _has_property,
                    )
                )


class ModelProperty(ABC):
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

    @abstractmethod
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
        """Set for subject."""
        self._subject = subject

    @property
    def title(self) -> dict:
        """Get for title attribute."""
        return self._title

    @title.setter
    def title(self, title: dict) -> None:
        """Set for title attribute."""
        self._title = title

    @property
    def has_type(self) -> List[ModelElement]:
        """Get for has_type."""
        return self._has_type

    @has_type.setter
    def has_type(self, has_type: List[ModelElement]) -> None:
        """Set for has_type."""
        self._has_type = has_type

    @property
    def identifier(self) -> str:
        """Get for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str) -> None:
        """Set for identifier."""
        self._identifier = URI(identifier)

    @property
    def min_occurs(self) -> int:
        """Get for min_occurs."""
        return self._min_occurs

    @min_occurs.setter
    def min_occurs(self, min_occurs: int) -> None:
        """Set for min_occurs."""
        self._min_occurs = min_occurs

    @property
    def max_occurs(self) -> int:
        """Get for max_occurs."""
        return self._max_occurs

    @max_occurs.setter
    def max_occurs(self, max_occurs: int) -> None:
        """Set for max_occurs."""
        self._max_occurs = max_occurs

    @abstractmethod
    def to_rdf(self, format: str = "turtle", encoding: Optional[str] = "utf-8") -> str:
        """Maps the property to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into
        """

    def _to_graph(
        self, type: str = MODELLDCATNO.Property, selfobject: Any = None
    ) -> Graph:
        """Returns the property as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Property
            selfobject: a bnode or URI passed from a subclass Default: None

        Returns:
            the property graph
        """
        # Set up graph and namespaces:
        self._g = Graph()
        self._g.bind("modelldcatno", MODELLDCATNO)
        self._g.bind("dct", DCT)
        self._g.bind("skos", SKOS)

        self._g.add((selfobject, RDF.type, type))

        self._has_type_to_graph(selfobject)

        if getattr(self, "min_occurs", None):
            self._g.add((selfobject, XSD.minOccurs, Literal(self.min_occurs)))

        if getattr(self, "max_occurs", None):
            self._g.add((selfobject, XSD.maxOccurs, Literal(self.max_occurs)))

        if getattr(self, "title", None):
            for key in self.title:
                self._g.add(
                    (
                        selfobject,
                        DCT.title,
                        Literal(self.title[key], lang=key),
                    )
                )

        if getattr(self, "subject", None):

            _subject = URIRef(self.subject.identifier)

            for _s, p, o in self.subject._to_graph().triples((None, None, None)):
                self._g.add((_subject, p, o))

            self._g.add((selfobject, DCT.subject, _subject))

        return self._g

    def _has_type_to_graph(self, _self: Any) -> None:
        if getattr(self, "has_type", None):

            for has_type in self._has_type:

                if getattr(has_type, "identifier", None):
                    _has_type = URIRef(has_type.identifier)
                else:
                    _has_type = BNode()

                for _s, p, o in has_type._to_graph().triples((None, None, None)):
                    self._g.add(
                        (_has_type, p, o)
                        if isinstance(_has_type, BNode)
                        else (_s, p, o)
                    )

                self._g.add(
                    (
                        _self,
                        MODELLDCATNO.hasType,
                        _has_type,
                    )
                )


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
        """Set for has_object_type."""
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
            selfobject: a bnode or URI passed from a subclass Default: None

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
                self._g.add(
                    (_has_object_type, p, o)
                    if isinstance(_has_object_type, BNode)
                    else (_s, p, o)
                )

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

    def _to_graph(
        self: ObjectType, type: str = MODELLDCATNO.ObjectType, selfobject: Any = None
    ) -> Graph:
        """Returns the object type as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.ObjectType
            selfobject: a bnode or URI passed from a subclass Default: None

        Returns:
            the object type graph
        """
        if getattr(self, "identifier", None):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        super(ObjectType, self)._to_graph(MODELLDCATNO.ObjectType, _self)

        return self._g


class SimpleType(ModelElement):
    """A class representing a modelldcatno:SimpleType."""

    __slots__ = (
        "_min_length",
        "_max_length",
        "_fraction_digits",
        "_length",
        "_total_digits",
        "_max_inclusive",
        "_min_inclusive",
        "_type_definition_reference",
        "_pattern",
    )

    _identifier: URI
    _dct_identifier: str
    _g: Graph
    _min_length: int
    _max_length: int
    _fraction_digits: int
    _length: int
    _total_digits: int
    _max_inclusive: float
    _min_inclusive: float
    _type_definition_reference: URI
    _pattern: str

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()

    @property
    def min_length(self) -> int:
        """Get for min_length."""
        return self._min_length

    @min_length.setter
    def min_length(self, min_length: int) -> None:
        """Set for min_length."""
        self._min_length = min_length

    @property
    def max_length(self) -> int:
        """Get for max_length."""
        return self._max_length

    @max_length.setter
    def max_length(self, max_length: int) -> None:
        """Set for max_length."""
        self._max_length = max_length

    @property
    def fraction_digits(self) -> int:
        """Get for fraction_digits."""
        return self._fraction_digits

    @fraction_digits.setter
    def fraction_digits(self, fraction_digits: int) -> None:
        """Set for fraction_digits."""
        self._fraction_digits = fraction_digits

    @property
    def length(self) -> int:
        """Get for length."""
        return self._length

    @length.setter
    def length(self, length: int) -> None:
        """Set for length."""
        self._length = length

    @property
    def total_digits(self) -> int:
        """Get for total_digits."""
        return self._total_digits

    @total_digits.setter
    def total_digits(self, total_digits: int) -> None:
        """Set for total_digits."""
        self._total_digits = total_digits

    @property
    def max_inclusive(self) -> float:
        """Get for max_inclusive."""
        return self._max_inclusive

    @max_inclusive.setter
    def max_inclusive(self, max_inclusive: float) -> None:
        """Set for max_inclusive."""
        self._max_inclusive = max_inclusive

    @property
    def min_inclusive(self) -> float:
        """Get for min_inclusive."""
        return self._min_inclusive

    @min_inclusive.setter
    def min_inclusive(self, min_inclusive: float) -> None:
        """Set for min_inclusive."""
        self._min_inclusive = min_inclusive

    @property
    def type_definition_reference(self) -> str:
        """Get for type_definition_reference."""
        return self._type_definition_reference

    @type_definition_reference.setter
    def type_definition_reference(self, type_definition_reference: str) -> None:
        """Set for type_definition_reference."""
        self._type_definition_reference = URI(type_definition_reference)

    @property
    def pattern(self) -> str:
        """Get for pattern."""
        return self._pattern

    @pattern.setter
    def pattern(self, pattern: str) -> None:
        """Set for pattern."""
        self._pattern = pattern

    def to_rdf(
        self: SimpleType, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> str:
        """Maps the object type to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: SimpleType, type: str = MODELLDCATNO.SimpleType, selfobject: Any = None
    ) -> Graph:
        """Returns the object type as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.SimpleType
            selfobject: a bnode or URI passed from a subclass Default: None

        Returns:
            the object type graph
        """
        if getattr(self, "identifier", None):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        super(SimpleType, self)._to_graph(MODELLDCATNO.SimpleType, _self)

        self._add_properties(_self)

        return self._g

    def _add_properties(self, _self: Any) -> None:

        if getattr(self, "min_length", None):
            self._g.add((_self, XSD.minLength, Literal(self.min_length)))

        if getattr(self, "max_length", None):
            self._g.add((_self, XSD.maxLength, Literal(self.max_length)))

        if getattr(self, "fraction_digits", None):
            self._g.add((_self, XSD.fractionDigits, Literal(self.fraction_digits)))

        if getattr(self, "length", None):
            self._g.add((_self, XSD.length, Literal(self.length)))

        if getattr(self, "total_digits", None):
            self._g.add((_self, XSD.totalDigits, Literal(self.total_digits)))

        if getattr(self, "max_inclusive", None):
            self._g.add((_self, XSD.maxInclusive, Literal(self.max_inclusive)))

        if getattr(self, "min_inclusive", None):
            self._g.add((_self, XSD.minInclusive, Literal(self.min_inclusive)))

        if getattr(self, "type_definition_reference", None):
            self._g.add(
                (_self, XSD.anyURI, URIRef(self.type_definition_reference)),
            )

        if getattr(self, "pattern", None):
            self._g.add((_self, XSD.pattern, Literal(self.pattern)))


class Composition(ModelProperty):
    """A class representing a modelldcatno:Composition."""

    __slots__ = "_contains"

    _contains: ModelElement
    _identifier: URI
    _g: Graph

    @property
    def contains(self: Composition) -> ModelElement:
        """Get for contains."""
        return self._contains

    @contains.setter
    def contains(self: Composition, contains: ModelElement) -> None:
        """Set for contains."""
        self._contains = contains

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()

    def to_rdf(
        self: Composition, format: str = "turtle", encoding: Optional[str] = "utf-8"
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
        self: Composition, type: str = MODELLDCATNO.Composition, selfobject: Any = None
    ) -> Graph:
        """Returns the role as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Composition
            selfobject: a bnode or URI passed from a subclass Default: None

        Returns:
            the role graph
        """
        if getattr(self, "identifier", None):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        super(Composition, self)._to_graph(MODELLDCATNO.Composition, _self)

        self._contains_to_graph(_self)

        return self._g

    def _contains_to_graph(self, _self: Any) -> None:

        if getattr(self, "contains", None):

            if getattr(self._contains, "identifier", None):
                _contains = URIRef(self._contains.identifier)
            else:
                _contains = BNode()

            for _s, p, o in self._contains._to_graph().triples((None, None, None)):
                self._g.add(
                    (_contains, p, o) if isinstance(_contains, BNode) else (_s, p, o)
                )

            self._g.add((_self, MODELLDCATNO.contains, _contains))


class Collection(ModelProperty):
    """A class representing a modelldcatno:Collection."""

    __slots__ = "_has_member"

    _has_member: ModelElement
    _identifier: URI
    _g: Graph

    @property
    def has_member(self: Collection) -> ModelElement:
        """Get for has_member."""
        return self._has_member

    @has_member.setter
    def has_member(self: Collection, has_member: ModelElement) -> None:
        """Set for has_member."""
        self._has_member = has_member

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()

    def to_rdf(
        self: Collection, format: str = "turtle", encoding: Optional[str] = "utf-8"
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
        self: Collection, type: str = MODELLDCATNO.Collection, selfobject: Any = None
    ) -> Graph:
        """Returns the role as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Collection
            selfobject: a bnode or URI passed from a subclass Default: None

        Returns:
            the role graph
        """
        if getattr(self, "identifier", None):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        super(Collection, self)._to_graph(MODELLDCATNO.Collection, _self)

        self._has_member_to_graph(_self)

        return self._g

    def _has_member_to_graph(self, _self: Any) -> None:

        if getattr(self, "has_member", None):

            if getattr(self._has_member, "identifier", None):
                _has_member = URIRef(self._has_member.identifier)
            else:
                _has_member = BNode()

            for _s, p, o in self._has_member._to_graph().triples((None, None, None)):
                self._g.add(
                    (_has_member, p, o)
                    if isinstance(_has_member, BNode)
                    else (_s, p, o)
                )

            self._g.add((_self, MODELLDCATNO.hasMember, _has_member))


class Association(ModelProperty):
    """A class representing a modelldcatno:Association."""

    __slots__ = "_refers_to"

    _refers_to: ModelElement
    _identifier: URI
    _g: Graph

    @property
    def refers_to(self: Association) -> ModelElement:
        """Get for refers_to."""
        return self._refers_to

    @refers_to.setter
    def refers_to(self: Association, refers_to: ModelElement) -> None:
        """Set for refers_to."""
        self._refers_to = refers_to

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()

    def to_rdf(
        self: Association, format: str = "turtle", encoding: Optional[str] = "utf-8"
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
        self: Association, type: str = MODELLDCATNO.Association, selfobject: Any = None
    ) -> Graph:
        """Returns the association as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Association
            selfobject: a bnode or URI passed from a subclass Default: None

        Returns:
            the association graph
        """
        if getattr(self, "identifier", None):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        super(Association, self)._to_graph(MODELLDCATNO.Association, _self)

        self._refers_to_to_graph(_self)

        return self._g

    def _refers_to_to_graph(self, _self: Any) -> None:

        if getattr(self, "refers_to", None):

            if getattr(self._refers_to, "identifier", None):
                _refers_to = URIRef(self._refers_to.identifier)
            else:
                _refers_to = BNode()

            for _s, p, o in self._refers_to._to_graph().triples((None, None, None)):
                self._g.add(
                    (_refers_to, p, o) if isinstance(_refers_to, BNode) else (_s, p, o)
                )

            self._g.add((_self, MODELLDCATNO.refersTo, _refers_to))

        return self._g


class Choice(ModelProperty):
    """A class representing a modelldcatno:Choice."""

    __slots__ = "_has_some"

    _has_some: List[ModelElement]
    _identifier: URI
    _g: Graph

    @property
    def has_some(self: Choice) -> List[ModelElement]:
        """Get for has_some."""
        return self._has_some

    @has_some.setter
    def has_some(self: Choice, has_some: List[ModelElement]) -> None:
        """Set for has_some."""
        self._has_some = has_some

    def __init__(self) -> None:
        """Inits Choice object with default values."""
        super().__init__()
        self._has_some = []

    def to_rdf(
        self: Choice, format: str = "turtle", encoding: Optional[str] = "utf-8"
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
        self: Choice, type: str = MODELLDCATNO.Choice, selfobject: Any = None
    ) -> Graph:
        """Returns the role as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Choice
            selfobject: a bnode or URI passed from a subclass Default: None

        Returns:
            the role graph
        """
        if getattr(self, "identifier", None):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        super(Choice, self)._to_graph(MODELLDCATNO.Choice, _self)

        self._has_some_to_graph(_self)

        return self._g

    def _has_some_to_graph(self, _self: Any) -> None:

        if getattr(self, "has_some", None):

            for has_some in self._has_some:

                if getattr(has_some, "identifier", None):
                    _has_some = URIRef(has_some.identifier)
                else:
                    _has_some = BNode()

                for _s, p, o in has_some._to_graph().triples((None, None, None)):
                    self._g.add(
                        (_has_some, p, o)
                        if isinstance(_has_some, BNode)
                        else (_s, p, o)
                    )

                self._g.add((_self, MODELLDCATNO.hasSome, _has_some))


class Attribute(ModelProperty):
    """A class representing a modelldcatno:Attribute."""

    __slots__ = (
        "_identifier",
        "_contains_object_type",
        "_has_simple_type",
        "_has_data_type",
        "_has_value_from",
    )

    _identifier: URI
    _contains_object_type: ObjectType
    _g: Graph
    _has_simple_type: SimpleType
    _has_data_type: DataType
    _has_value_from: CodeList

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()

    @property
    def contains_object_type(self: Attribute) -> ObjectType:
        """Get for contains_object_type."""
        return self._contains_object_type

    @contains_object_type.setter
    def contains_object_type(self: Attribute, contains_object_type: ObjectType) -> None:
        """Set for contains_object_type."""
        self._contains_object_type = contains_object_type

    @property
    def has_simple_type(self: Attribute) -> SimpleType:
        """Get for has_simple_type."""
        return self._has_simple_type

    @has_simple_type.setter
    def has_simple_type(self: Attribute, has_simple_type: SimpleType) -> None:
        """Set for has_simple_type."""
        self._has_simple_type = has_simple_type

    @property
    def has_data_type(self: Attribute) -> DataType:
        """Get for has_data_type."""
        return self._has_data_type

    @has_data_type.setter
    def has_data_type(self: Attribute, has_data_type: DataType) -> None:
        """Set for has_data_type."""
        self._has_data_type = has_data_type

    @property
    def has_value_from(self: Attribute) -> CodeList:
        """Get for has_value_from."""
        return self._has_value_from

    @has_value_from.setter
    def has_value_from(self: Attribute, has_value_from: CodeList) -> None:
        """Set for has_value_from."""
        self._has_value_from = has_value_from

    def to_rdf(
        self: Attribute, format: str = "turtle", encoding: Optional[str] = "utf-8"
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
        self: Attribute, type: str = MODELLDCATNO.Attribute, selfobject: Any = None
    ) -> Graph:
        """Returns the role as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Attribute
            selfobject: a bnode or URI passed from a subclass Default: None

        Returns:
            the role graph
        """
        if getattr(self, "identifier", None):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        super(Attribute, self)._to_graph(MODELLDCATNO.Attribute, _self)

        self._contains_object_type_to_graph(_self)
        self._has_simple_type_to_graph(_self)
        self._has_data_type_to_graph(_self)
        self._has_value_from_to_graph(_self)

        return self._g

    def _contains_object_type_to_graph(self, _self: Any) -> None:

        if getattr(self, "contains_object_type", None):

            if getattr(self._contains_object_type, "identifier", None):
                _contains_object_type = URIRef(self._contains_object_type.identifier)
            else:
                _contains_object_type = BNode()

            for _s, p, o in self._contains_object_type._to_graph().triples(
                (None, None, None)
            ):
                self._g.add(
                    (_contains_object_type, p, o)
                    if isinstance(_contains_object_type, BNode)
                    else (_s, p, o)
                )

            self._g.add((_self, MODELLDCATNO.containsObjectType, _contains_object_type))

    def _has_simple_type_to_graph(self, _self: Any) -> None:

        if getattr(self, "has_simple_type", None):

            if getattr(self._has_simple_type, "identifier", None):
                _has_simple_type = URIRef(self._has_simple_type.identifier)
            else:
                _has_simple_type = BNode()

            for _s, p, o in self._has_simple_type._to_graph().triples(
                (None, None, None)
            ):
                self._g.add(
                    (_has_simple_type, p, o)
                    if isinstance(_has_simple_type, BNode)
                    else (_s, p, o)
                )

            self._g.add((_self, MODELLDCATNO.hasSimpleType, _has_simple_type))

    def _has_data_type_to_graph(self, _self: Any) -> None:

        if getattr(self, "has_data_type", None):

            if getattr(self._has_data_type, "identifier", None):
                _has_data_type = URIRef(self._has_data_type.identifier)
            else:
                _has_data_type = BNode()

            for _s, p, o in self._has_data_type._to_graph().triples((None, None, None)):
                self._g.add(
                    (_has_data_type, p, o)
                    if isinstance(_has_data_type, BNode)
                    else (_s, p, o)
                )

            self._g.add((_self, MODELLDCATNO.hasDataType, _has_data_type))

    def _has_value_from_to_graph(self, _self: Any) -> None:

        if getattr(self, "has_value_from", None):

            _has_value_from = (
                URIRef(self._has_value_from.identifier)
                if getattr(self._has_value_from, "identifier", None)
                else BNode()
            )

            for _s, p, o in self._has_value_from._to_graph().triples(
                (None, None, None)
            ):
                self._g.add(
                    (_has_value_from, p, o)
                    if isinstance(_has_value_from, BNode)
                    else (_s, p, o)
                )

            self._g.add((_self, MODELLDCATNO.hasValueFrom, _has_value_from))


class Specialization(ModelProperty):
    """A class representing a modelldcatno:Specialization."""

    __slots__ = "_has_general_concept"

    _has_general_concept: ModelElement
    _identifier: URI
    _g: Graph

    @property
    def has_general_concept(self: Specialization) -> ModelElement:
        """Get for has_general_concept."""
        return self._has_general_concept

    @has_general_concept.setter
    def has_general_concept(
        self: Specialization, has_general_concept: ModelElement
    ) -> None:
        """Set for has_general_concept."""
        self._has_general_concept = has_general_concept

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()

    def to_rdf(
        self: Specialization, format: str = "turtle", encoding: Optional[str] = "utf-8"
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
        self: Specialization,
        type: str = MODELLDCATNO.Specialization,
        selfobject: Any = None,
    ) -> Graph:
        """Returns the role as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Association
            selfobject: a bnode or URI passed from a subclass Default: None

        Returns:
            the role graph
        """
        if getattr(self, "identifier", None):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        super(Specialization, self)._to_graph(MODELLDCATNO.Specialization, _self)

        self._has_general_concept_to_graph(_self)

        return self._g

    def _has_general_concept_to_graph(self, _self: Any) -> None:

        if getattr(self, "has_general_concept", None):

            if getattr(self._has_general_concept, "identifier", None):
                _has_general_concept = URIRef(self.has_general_concept.identifier)
            else:
                _has_general_concept = BNode()

            for _s, p, o in self._has_general_concept._to_graph().triples(
                (None, None, None)
            ):
                self._g.add(
                    (_has_general_concept, p, o)
                    if isinstance(_has_general_concept, BNode)
                    else (_s, p, o)
                )

            self._g.add((_self, MODELLDCATNO.hasGeneralConcept, _has_general_concept))


class Realization(ModelProperty):
    """A class representing a modelldcatno:Realization."""

    __slots__ = "_has_supplier"

    _has_supplier: ModelElement
    _identifier: URI
    _g: Graph

    @property
    def has_supplier(self: Realization) -> ModelElement:
        """Get for has_supplier."""
        return self._has_supplier

    @has_supplier.setter
    def has_supplier(self: Realization, has_supplier: ModelElement) -> None:
        """Set for has_supplier."""
        self._has_supplier = has_supplier

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()

    def to_rdf(
        self: Realization, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> str:
        """Maps the realization to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: Realization, type: str = MODELLDCATNO.Realization, selfobject: Any = None
    ) -> Graph:
        """Returns the realization as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Association
            selfobject: a bnode or URI passed from a subclass Default: None

        Returns:
            the assocation graph
        """
        if getattr(self, "identifier", None):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        super(Realization, self)._to_graph(MODELLDCATNO.Realization, _self)

        self._has_supplier_to_graph(_self)

        return self._g

    def _has_supplier_to_graph(self, _self: Any) -> None:

        if getattr(self, "has_supplier", None):

            if getattr(self._has_supplier, "identifier", None):
                _has_supplier = URIRef(self._has_supplier.identifier)
            else:
                _has_supplier = BNode()

            for _s, p, o in self._has_supplier._to_graph().triples((None, None, None)):
                self._g.add(
                    (_has_supplier, p, o)
                    if isinstance(_has_supplier, BNode)
                    else (_s, p, o)
                )

            self._g.add((_self, MODELLDCATNO.hasSupplier, _has_supplier))


class Abstraction(ModelProperty):
    """A class representing a modelldcatno:Abstraction."""

    __slots__ = "_is_abstraction_of"

    _is_abstraction_of: ModelElement
    _identifier: URI
    _g: Graph

    @property
    def is_abstraction_of(self: Abstraction) -> ModelElement:
        """Get for is_abstraction_of."""
        return self._is_abstraction_of

    @is_abstraction_of.setter
    def is_abstraction_of(self: Abstraction, is_abstraction_of: ModelElement) -> None:
        """Set for is_abstraction_of."""
        self._is_abstraction_of = is_abstraction_of

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()

    def to_rdf(
        self: Abstraction, format: str = "turtle", encoding: Optional[str] = "utf-8"
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
        self: Abstraction, type: str = MODELLDCATNO.Abstraction, selfobject: Any = None
    ) -> Graph:
        """Returns the role as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Abstraction
            selfobject: a bnode or URI passed from a subclass Default: None

        Returns:
            the role graph
        """
        if getattr(self, "identifier", None):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        super(Abstraction, self)._to_graph(MODELLDCATNO.Abstraction, _self)

        self._is_abstraction_of_to_graph(_self)

        return self._g

    def _is_abstraction_of_to_graph(self, _self: Any) -> None:

        if getattr(self, "is_abstraction_of", None):

            if getattr(self._is_abstraction_of, "identifier", None):
                _is_abstraction_of = URIRef(self._is_abstraction_of.identifier)
            else:
                _is_abstraction_of = BNode()

            for _s, p, o in self._is_abstraction_of._to_graph().triples(
                (None, None, None)
            ):
                self._g.add(
                    (_is_abstraction_of, p, o)
                    if isinstance(_is_abstraction_of, BNode)
                    else (_s, p, o)
                )

            self._g.add((_self, MODELLDCATNO.isAbstractionOf, _is_abstraction_of))


class DataType(ModelElement):
    """A class representing a modelldcatno:DataType."""

    _identifier: URI
    _dct_identifier: str
    _g: Graph

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()

    def to_rdf(
        self: DataType, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> str:
        """Maps the data type to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: DataType, type: str = MODELLDCATNO.DataType, selfobject: Any = None
    ) -> Graph:
        """Returns the data type as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.DataType
            selfobject: a bnode or URI passed from a subclass Default: None

        Returns:
            the object type graph
        """
        if getattr(self, "identifier", None):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        super(DataType, self)._to_graph(MODELLDCATNO.DataType, _self)

        return self._g


class RootObjectType(ModelElement):
    """A class representing a modelldcatno:RootObjectType."""

    _identifier: URI
    _dct_identifier: str
    _g: Graph

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()

    def to_rdf(
        self: RootObjectType, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> str:
        """Maps the data type to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: RootObjectType,
        type: str = MODELLDCATNO.RootObjectType,
        selfobject: Any = None,
    ) -> Graph:
        """Returns the root object type as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.RootObjectType
            selfobject: a bnode or URI passed from a subclass Default: None

        Returns:
            the root object type graph
        """
        if getattr(self, "identifier", None):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        super(RootObjectType, self)._to_graph(MODELLDCATNO.RootObjectType, _self)

        return self._g


class CodeList(ModelElement):
    """A class representing a modelldcatno:CodeList."""

    _identifier: URI
    _dct_identifier: str
    _g: Graph

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()

    def to_rdf(
        self: CodeList, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> str:
        """Maps the code list to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: CodeList,
        type: str = MODELLDCATNO.CodeList,
        selfobject: Any = None,
    ) -> Graph:
        """Returns the root object type as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.CodeList
            selfobject: a bnode or URI passed from a subclass Default: None

        Returns:
            the root object type graph
        """
        _self = (
            URIRef(self.identifier) if getattr(self, "identifier", None) else BNode()
        )

        super(CodeList, self)._to_graph(MODELLDCATNO.CodeList, _self)

        return self._g


class CodeElement:
    """A class representing a modelldcatno:CodeElement."""

    __slots__ = (
        "_identifier",
        "_dct_identifier",
        "_g",
        "_type",
        "_subject",
        "_preflabel",
        "_notation",
        "_in_scheme",
        "_top_concept_of",
        "_altlabel",
        "_definition",
    )

    _identifier: URI
    _dct_identifier: str
    _g: Graph
    _type: str
    _subject: Concept
    _preflabel: dict
    _notation: str
    _in_scheme: List[CodeList]
    _top_concept_of: List[CodeList]
    _altlabel: dict
    _definition: dict

    def __init__(self) -> None:
        """Inits an object with default values."""
        self._type = MODELLDCATNO.CodeElement

    @property
    def identifier(self: CodeElement) -> str:
        """Get for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self: CodeElement, identifier: str) -> None:
        """Set for identifier."""
        self._identifier = URI(identifier)

    @property
    def dct_identifier(self: CodeElement) -> str:
        """Get for dct_identifier."""
        return self._dct_identifier

    @dct_identifier.setter
    def dct_identifier(self: CodeElement, dct_identifier: str) -> None:
        """Set for dct_identifier."""
        self._dct_identifier = dct_identifier

    @property
    def subject(self: CodeElement) -> Concept:
        """Get for subject."""
        return self._subject

    @subject.setter
    def subject(self: CodeElement, subject: Concept) -> None:
        """Set for subject."""
        self._subject = subject

    @property
    def preflabel(self: CodeElement) -> dict:
        """Get for preflabel."""
        return self._preflabel

    @preflabel.setter
    def preflabel(self: CodeElement, preflabel: dict) -> None:
        """Set for preflabel."""
        self._preflabel = preflabel

    @property
    def notation(self: CodeElement) -> str:
        """Get for notation."""
        return self._notation

    @notation.setter
    def notation(self: CodeElement, notation: str) -> None:
        """Set for notation."""
        self._notation = notation

    @property
    def in_scheme(self: CodeElement) -> List[CodeList]:
        """Get for in_scheme."""
        return self._in_scheme

    @in_scheme.setter
    def in_scheme(self: CodeElement, in_scheme: List[CodeList]) -> None:
        """Set for in_scheme."""
        self._in_scheme = in_scheme

    @property
    def top_concept_of(self: CodeElement) -> List[CodeList]:
        """Get for top_concept_of."""
        return self._top_concept_of

    @top_concept_of.setter
    def top_concept_of(self: CodeElement, top_concept_of: List[CodeList]) -> None:
        """Set for top_concept_of."""
        self._top_concept_of = top_concept_of

    @property
    def altlabel(self: CodeElement) -> dict:
        """Get for altlabel."""
        return self._altlabel

    @altlabel.setter
    def altlabel(self: CodeElement, altlabel: dict) -> None:
        """Set for altlabel."""
        self._altlabel = altlabel

    @property
    def definition(self: CodeElement) -> dict:
        """Get for definition."""
        return self._definition

    @definition.setter
    def definition(self: CodeElement, definition: dict) -> None:
        """Set for definition."""
        self._definition = definition

    def to_rdf(
        self: CodeElement, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> str:
        """Maps the code element to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(self: CodeElement) -> Graph:
        """Returns the code element as graph.

        Returns:
            the code element graph
        """
        _self = (
            URIRef(self.identifier) if getattr(self, "identifier", None) else BNode()
        )

        # Set up graph and namespaces:
        self._g = Graph()
        self._g.bind("modelldcatno", MODELLDCATNO)
        self._g.bind("dct", DCT)
        self._g.bind("skos", SKOS)

        self._g.add((_self, RDF.type, self._type))

        if getattr(self, "dct_identifier", None):
            self._g.add((_self, DCT.identifier, Literal(self._dct_identifier)))

        if getattr(self, "notation", None):
            self._g.add((_self, SKOS.notation, Literal(self._notation)))

        self._preflabel_to_graph(_self)
        self._subject_to_graph(_self)
        self._in_scheme_to_graph(_self)
        self._top_concept_of_to_graph(_self)
        self._altlabel_to_graph(_self)
        self._definition_to_graph(_self)

        return self._g

    def _subject_to_graph(self, _self: Any) -> None:

        if getattr(self, "subject", None):

            _subject = URIRef(self.subject.identifier)

            for _s, p, o in self.subject._to_graph().triples((None, None, None)):
                self._g.add((_subject, p, o))

            self._g.add((_self, DCT.subject, _subject))

    def _preflabel_to_graph(self, _self: Any) -> None:

        if getattr(self, "preflabel", None):

            for key in self.preflabel:
                self._g.add(
                    (
                        _self,
                        SKOS.prefLabel,
                        Literal(self.preflabel[key], lang=key),
                    )
                )

    def _in_scheme_to_graph(self, _self: Any) -> None:

        if getattr(self, "in_scheme", None):

            for in_scheme in self._in_scheme:

                if getattr(in_scheme, "identifier", None):
                    _in_scheme = URIRef(in_scheme.identifier)
                else:
                    _in_scheme = BNode()

                for _s, p, o in in_scheme._to_graph().triples((None, None, None)):
                    self._g.add(
                        (_in_scheme, p, o)
                        if isinstance(_in_scheme, BNode)
                        else (_s, p, o)
                    )

                self._g.add((_self, SKOS.inScheme, _in_scheme))

    def _top_concept_of_to_graph(self, _self: Any) -> None:

        if getattr(self, "top_concept_of", None):

            for top_concept_of in self._top_concept_of:

                if getattr(top_concept_of, "identifier", None):
                    _top_concept_of = URIRef(top_concept_of.identifier)
                else:
                    _top_concept_of = BNode()

                for _s, p, o in top_concept_of._to_graph().triples((None, None, None)):
                    self._g.add(
                        (_top_concept_of, p, o)
                        if isinstance(_top_concept_of, BNode)
                        else (_s, p, o)
                    )

                self._g.add((_self, SKOS.topConceptOf, _top_concept_of))

    def _altlabel_to_graph(self, _self: Any) -> None:

        if getattr(self, "altlabel", None):

            for key in self.altlabel:
                self._g.add(
                    (
                        _self,
                        SKOS.altLabel,
                        Literal(self.altlabel[key], lang=key),
                    )
                )

    def _definition_to_graph(self, _self: Any) -> None:

        if getattr(self, "definition", None):

            for key in self.definition:
                self._g.add(
                    (
                        _self,
                        SKOS.definition,
                        Literal(self.definition[key], lang=key),
                    )
                )
