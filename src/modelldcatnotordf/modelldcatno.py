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
    _has_property: List[ModelProperty]
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
    def has_property(self) -> List[ModelProperty]:
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

        if selfobject:
            _self = selfobject

        elif getattr(self, "identifier", None):
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
            selfobject: a bnode or URI passed from a subclass Default: None

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
        self._min_length = min_length

    @property
    def max_length(self) -> int:
        """Get for max_length."""
        return self._max_length

    @max_length.setter
    def max_length(self, max_length: int) -> None:
        self._max_length = max_length

    @property
    def fraction_digits(self) -> int:
        """Get for fraction_digits."""
        return self._fraction_digits

    @fraction_digits.setter
    def fraction_digits(self, fraction_digits: int) -> None:
        self._fraction_digits = fraction_digits

    @property
    def length(self) -> int:
        """Get for length."""
        return self._length

    @length.setter
    def length(self, length: int) -> None:
        self._length = length

    @property
    def total_digits(self) -> int:
        """Get for total_digits."""
        return self._total_digits

    @total_digits.setter
    def total_digits(self, total_digits: int) -> None:
        self._total_digits = total_digits

    @property
    def max_inclusive(self) -> float:
        """Get for max_inclusive."""
        return self._max_inclusive

    @max_inclusive.setter
    def max_inclusive(self, max_inclusive: float) -> None:
        self._max_inclusive = max_inclusive

    @property
    def min_inclusive(self) -> float:
        """Get for min_inclusive."""
        return self._min_inclusive

    @min_inclusive.setter
    def min_inclusive(self, min_inclusive: float) -> None:
        self._min_inclusive = min_inclusive

    @property
    def type_definition_reference(self) -> str:
        """Get for type_definition_reference."""
        return self._type_definition_reference

    @type_definition_reference.setter
    def type_definition_reference(self, type_definition_reference: str) -> None:
        self._type_definition_reference = URI(type_definition_reference)

    @property
    def pattern(self) -> str:
        """Get for pattern."""
        return self._pattern

    @pattern.setter
    def pattern(self, pattern: str) -> None:
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
            self._g.add((_self, XSD.anyURI, URIRef(self.type_definition_reference)),)

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
        self._contains = contains

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
                self._g.add((_contains, p, o))

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
        self._has_member = has_member

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
                self._g.add((_has_member, p, o))

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
        self._refers_to = refers_to

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
                self._g.add((_refers_to, p, o))

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

    def __init__(self) -> None:
        """Inits Choice object with default values."""
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
                    self._g.add((_has_some, p, o))

                self._g.add((_self, MODELLDCATNO.hasSome, _has_some))


class Attribute(ModelProperty):
    """A class representing a modelldcatno:Attribute."""

    __slots__ = ("_identifier", "_contains_object_type", "_has_simple_type")

    _identifier: URI
    _contains_object_type: ObjectType
    _g: Graph
    _has_simple_type: SimpleType

    def __init__(self) -> None:
        """Inits an object with default values."""
        super().__init__()

    @property
    def contains_object_type(self: Attribute) -> ObjectType:
        """Get for contains_object_type."""
        return self._contains_object_type

    @contains_object_type.setter
    def contains_object_type(self: Attribute, contains_object_type: ObjectType) -> None:
        self._contains_object_type = contains_object_type

    @property
    def has_simple_type(self: Attribute) -> SimpleType:
        """Get for has_simple_type."""
        return self._has_simple_type

    @has_simple_type.setter
    def has_simple_type(self: Attribute, has_simple_type: SimpleType) -> None:
        self._has_simple_type = has_simple_type

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
                self._g.add((_contains_object_type, p, o))

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
                self._g.add((_has_simple_type, p, o))

            self._g.add((_self, MODELLDCATNO.hasSimpleType, _has_simple_type))


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
        self._has_general_concept = has_general_concept

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
                has_general_concept = URIRef(self.has_general_concept.identifier)
            else:
                has_general_concept = BNode()

            for _s, p, o in self._has_general_concept._to_graph().triples(
                (None, None, None)
            ):
                self._g.add((has_general_concept, p, o))

            self._g.add((_self, MODELLDCATNO.hasGeneralConcept, has_general_concept))


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
        self._has_supplier = has_supplier

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
                self._g.add((_has_supplier, p, o))

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
        self._is_abstraction_of = is_abstraction_of

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
                self._g.add((_is_abstraction_of, p, o))

            self._g.add((_self, MODELLDCATNO.isAbstractionOf, _is_abstraction_of))
