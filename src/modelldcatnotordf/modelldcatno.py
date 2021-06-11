"""Modelldcatno module for mapping a Modelldcatno model to rdf.

This module contains methods for mapping to rdf
according to the modelldcat-ap-no specification._

Refer to sub-class for typical usage examples.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Union

from concepttordf import Concept, Contact
from datacatalogtordf import Agent, Location, Resource, URI
from datacatalogtordf.periodoftime import Date, PeriodOfTime
from rdflib import (
    BNode,
    DCTERMS,
    FOAF,
    Graph,
    Literal,
    Namespace,
    OWL,
    RDF,
    RDFS,
    SKOS,
    URIRef,
    XSD,
)
from skolemizer import Skolemizer
import validators

from modelldcatnotordf.document import FoafDocument
from modelldcatnotordf.licensedocument import LicenseDocument

DCAT = Namespace("http://www.w3.org/ns/dcat#")
ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
PROV = Namespace("http://www.w3.org/ns/prov#")
MODELLDCATNO = Namespace("https://data.norge.no/vocabulary/modelldcatno#")
XKOS = Namespace("http://rdf-vocabulary.ddialliance.org/xkos#")
ADMS = Namespace("http://www.w3.org/ns/adms#")


class Standard:
    """A class representing a dct:Standard."""

    _g: Graph
    _identifier: URI
    _title: dict
    _has_reference: str
    _has_version_number: str

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits InformationModel object with default values."""
        if identifier:
            self.identifier = identifier

    @property
    def identifier(self) -> str:
        """Get for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str) -> None:
        self._identifier = URI(identifier)

    @property
    def title(self) -> dict:
        """Get for title attribute."""
        return self._title

    @title.setter
    def title(self, title: dict) -> None:
        """Set for title attribute."""
        self._title = title

    @property
    def has_reference(self: Standard) -> str:
        """Get for has_reference."""
        return self._has_reference

    @has_reference.setter
    def has_reference(self: Standard, has_reference: str) -> None:
        """Set for has_reference."""
        self._has_reference = URI(has_reference)

    @property
    def has_version_number(self: Standard) -> str:
        """Get for has_version_number."""
        return self._has_version_number

    @has_version_number.setter
    def has_version_number(self: Standard, has_version_number: str) -> None:
        """Set for has_version_number."""
        self._has_version_number = has_version_number

    def to_rdf(
        self, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the standard to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format encoded as bytes.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(self) -> Graph:
        """Returns the standard as graph.

        Returns:
            the graph graph
        """
        self._g = Graph()
        self._g.bind("dct", DCTERMS)

        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        _self = URIRef(self.identifier)

        self._g.add((_self, RDF.type, DCTERMS.Standard))

        if getattr(self, "title", None):
            for key in self.title:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        DCTERMS.title,
                        Literal(self.title[key], lang=key),
                    )
                )

        if getattr(self, "has_reference", None):
            self._g.add(
                (URIRef(self.identifier), RDFS.seeAlso, URIRef(self.has_reference))
            )

        if getattr(self, "has_version_number", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    OWL.versionInfo,
                    Literal(self.has_version_number),
                )
            )

        return self._g


class InformationModel(Resource, Standard):
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
        "_replaces",
        "_is_replaced_by",
        "_has_part",
        "_is_part_of",
        "_homepage",
        "_contactpoints",
        "_locations",
        "_modified",
        "_dct_type",
        "_version_info",
        "_version_note",
        "_status",
        "_creator",
        "_has_format",
        "_temporal",
    )

    _title: dict
    _publisher: Union[Agent, URI]
    _subject: List[Union[Concept, URI]]
    _modelelements: List[Union[ModelElement, URI]]
    _informationmodelidentifier: str
    _licensedocument: Union[LicenseDocument, URI]
    _replaces: List[Union[InformationModel, URI]]
    _is_replaced_by: List[Union[InformationModel, URI]]
    _has_part: List[Union[InformationModel, URI]]
    _is_part_of: List[Union[InformationModel, URI]]
    _homepage: URI
    _contactpoints: List[Contact]
    _locations: List[Location]
    _modified: Date
    _dct_type: Union[Concept, URI]
    _version_info: str
    _version_note: dict
    _status: Union[Concept, URI]
    _creator: str
    _has_format: List[Union[FoafDocument, str]]
    _temporal: List[PeriodOfTime]

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits InformationModel object with default values."""
        if identifier:
            self.identifier = identifier

        super().__init__()
        self._type = MODELLDCATNO.InformationModel
        self._subject = []
        self._modelelements = []
        self._replaces = []
        self._is_replaced_by = []
        self._has_part = []
        self._is_part_of = []
        self._contactpoints = []
        self._locations = []
        self._has_format = []
        self._temporal = []

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
    def licensedocument(self) -> Union[LicenseDocument, URI]:
        """Get for license."""
        return self._licensedocument

    @licensedocument.setter
    def licensedocument(self, licensedocument: Union[LicenseDocument, URI]) -> None:
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
    def publisher(self: InformationModel) -> Union[Agent, URI]:
        """Get for publisher."""
        return self._publisher

    @publisher.setter
    def publisher(self: InformationModel, publisher: Union[Agent, URI]) -> None:
        """Set for publisher."""
        self._publisher = publisher

    @property
    def subject(self: InformationModel) -> List[Union[Concept, URI]]:
        """Get for subject."""
        return self._subject

    @subject.setter
    def subject(self: InformationModel, subject: List[Union[Concept, URI]]) -> None:
        """Set for subject."""
        self._subject = subject

    @property
    def modelelements(self: InformationModel) -> List[Union[ModelElement, URI]]:
        """Get for modelelements."""
        return self._modelelements

    @modelelements.setter
    def modelelements(
        self: InformationModel, modelelements: List[Union[ModelElement, URI]]
    ) -> None:
        """Set for modelelements."""
        self._modelelements = modelelements

    @property
    def replaces(self: InformationModel) -> List[Union[InformationModel, URI]]:
        """Get for replaces."""
        return self._replaces

    @replaces.setter
    def replaces(
        self: InformationModel, replaces: List[Union[InformationModel, URI]]
    ) -> None:
        """Set for replaces."""
        self._replaces = replaces

    @property
    def is_replaced_by(self: InformationModel) -> List[Union[InformationModel, URI]]:
        """Get for is_replaced_by."""
        return self._is_replaced_by

    @is_replaced_by.setter
    def is_replaced_by(
        self: InformationModel, is_replaced_by: List[Union[InformationModel, URI]]
    ) -> None:
        """Set for is_replaced_by."""
        self._is_replaced_by = is_replaced_by

    @property
    def has_part(self: InformationModel) -> List[Union[InformationModel, URI]]:
        """Get for has_part."""
        return self._has_part

    @has_part.setter
    def has_part(
        self: InformationModel, has_part: List[Union[InformationModel, URI]]
    ) -> None:
        """Set for has_part."""
        self._has_part = has_part

    @property
    def is_part_of(self: InformationModel) -> List[Union[InformationModel, URI]]:
        """Get for is_part_of."""
        return self._is_part_of

    @is_part_of.setter
    def is_part_of(
        self: InformationModel, is_part_of: List[Union[InformationModel, URI]]
    ) -> None:
        """Set for is_part_of."""
        self._is_part_of = is_part_of

    @property
    def homepage(self: InformationModel) -> str:
        """Get for homepage."""
        return self._homepage

    @homepage.setter
    def homepage(self: InformationModel, homepage: str) -> None:
        """Set for homepage."""
        self._homepage = URI(homepage)

    @property
    def contactpoints(self: InformationModel) -> List[Contact]:
        """Get for contactpoints."""
        return self._contactpoints

    @contactpoints.setter
    def contactpoints(self: InformationModel, contactpoints: List[Contact]) -> None:
        """Set for contactpoints."""
        self._contactpoints = contactpoints

    @property
    def locations(self: InformationModel) -> List[Location]:
        """Get for locations."""
        return self._locations

    @locations.setter
    def locations(self: InformationModel, locations: List[Location]) -> None:
        """Set for locations."""
        self._locations = locations

    @property
    def modified(self: InformationModel) -> str:
        """Get for modified."""
        return self._modified

    @modified.setter
    def modified(self: InformationModel, modified: str) -> None:
        """Set for modified."""
        self._modified = Date(modified)

    @property
    def dct_type(self: InformationModel) -> Union[Concept, URI]:
        """Get for dct_type."""
        return self._dct_type

    @dct_type.setter
    def dct_type(self: InformationModel, dct_type: Union[Concept, URI]) -> None:
        """Set for dct_type."""
        self._dct_type = dct_type

    @property
    def version_info(self: InformationModel) -> str:
        """Get for version_info."""
        return self._version_info

    @version_info.setter
    def version_info(self: InformationModel, version_info: str) -> None:
        """Set for version_info."""
        self._version_info = version_info

    @property
    def version_note(self) -> dict:
        """Get for version_note."""
        return self._version_note

    @version_note.setter
    def version_note(self, version_note: dict) -> None:
        """Set for version_note."""
        self._version_note = version_note

    @property
    def status(self) -> Union[Concept, URI]:
        """Get for status."""
        return self._status

    @status.setter
    def status(self, status: Union[Concept, URI]) -> None:
        """Set for status."""
        self._status = status

    @property
    def creator(self: InformationModel) -> str:
        """Get for creator."""
        return self._creator

    @creator.setter
    def creator(self: InformationModel, creator: str) -> None:
        """Set for creator."""
        self._creator = creator

    @property
    def has_format(self: InformationModel) -> List[Union[FoafDocument, str]]:
        """Get for has_format."""
        return self._has_format

    @has_format.setter
    def has_format(
        self: InformationModel, has_format: List[Union[FoafDocument, str]]
    ) -> None:
        """Set for has_format."""
        self._has_format = has_format

    @property
    def temporal(self: InformationModel) -> List[PeriodOfTime]:
        """Get for temporal."""
        return self._temporal

    @temporal.setter
    def temporal(self: InformationModel, temporal: List[PeriodOfTime]) -> None:
        """Set for temporal."""
        self._temporal = temporal

    def to_rdf(
        self: InformationModel,
        format: str = "turtle",
        encoding: Optional[str] = "utf-8",
    ) -> bytes:
        """Maps the information model to rdf.

        Available formats:
         - turtle (default)
         - xml
         - json-ld

        Args:
            format (str): a valid format.
            encoding (str): the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format encoded as bytes.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    # -

    def _to_graph(self: InformationModel) -> Graph:

        super(InformationModel, self)._to_graph()
        self._g.bind("modelldcatno", MODELLDCATNO)

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        self._publisher_to_graph()
        self._subject_to_graph()
        self._modelelements_to_graph()
        self._licensedocument_to_graph()
        self._replaces_to_graph()
        self._is_replaced_by_to_graph()
        self._has_part_to_graph()
        self._is_part_of_to_graph()
        self._homepage_to_graph()
        self._contactpoints_to_graph()
        self._locations_to_graph()
        self._modified_to_graph()
        self._dct_type_to_graph()
        self._version_note_to_graph()
        self._status_to_graph()
        self._has_formats_to_graph()
        self._temporals_to_graph()

        if getattr(self, "informationmodelidentifier", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    MODELLDCATNO.informationModelIdentifier,
                    Literal(self.informationmodelidentifier),
                )
            )

        if getattr(self, "version_info", None):
            self._g.add(
                (URIRef(self.identifier), OWL.versionInfo, Literal(self.version_info),)
            )

        return self._g

    def _subject_to_graph(self: InformationModel) -> None:
        if getattr(self, "subject", None):

            for subject in self._subject:

                _subject = (
                    URIRef(subject.identifier)
                    if isinstance(subject, Concept)
                    else URIRef(subject)
                )

                if isinstance(subject, Concept):
                    for _s, p, o in subject._to_graph().triples((None, None, None)):
                        self._g.add((_subject, p, o))

                self._g.add((URIRef(self.identifier), DCTERMS.subject, _subject,))

    def _modelelements_to_graph(self: InformationModel) -> None:

        if getattr(self, "modelelements", None):

            for modelelement in self._modelelements:

                if isinstance(modelelement, ModelElement):

                    if not getattr(modelelement, "identifier", None):
                        modelelement.identifier = Skolemizer.add_skolemization()

                    _modelelement = URIRef(modelelement.identifier)

                    for _s, p, o in modelelement._to_graph().triples(
                        (None, None, None)
                    ):
                        self._g.add((_s, p, o))

                elif isinstance(modelelement, str):
                    _modelelement = URIRef(modelelement)

                self._g.add(
                    (
                        URIRef(self.identifier),
                        MODELLDCATNO.containsModelElement,
                        _modelelement,
                    )
                )

    def _licensedocument_to_graph(self: InformationModel) -> None:

        if getattr(self, "licensedocument", None):

            if isinstance(self.licensedocument, LicenseDocument):

                if not getattr(self.licensedocument, "identifier", None):
                    self.licensedocument.identifier = Skolemizer.add_skolemization()

                _licensedocument = URIRef(self.licensedocument.identifier)

                for _s, p, o in self.licensedocument._to_graph().triples(
                    (None, None, None)
                ):
                    self._g.add((_s, p, o))

            elif isinstance(self.licensedocument, str):
                _licensedocument = URIRef(self.licensedocument)

            self._g.add((URIRef(self.identifier), DCTERMS.license, _licensedocument))

    def _replaces_to_graph(self: InformationModel) -> None:
        if getattr(self, "replaces", None):

            for replaces in self._replaces:

                if isinstance(replaces, InformationModel):
                    _replaces = URIRef(replaces.identifier)

                    for _s, p, o in replaces._to_graph().triples((None, None, None)):
                        self._g.add((_replaces, p, o))

                elif isinstance(replaces, str):
                    _replaces = URIRef(replaces)

                self._g.add((URIRef(self.identifier), DCTERMS.replaces, _replaces,))

    def _is_replaced_by_to_graph(self: InformationModel) -> None:
        if getattr(self, "is_replaced_by", None):

            for is_replaced_by in self._is_replaced_by:

                if isinstance(is_replaced_by, InformationModel):
                    _is_replaced_by = URIRef(is_replaced_by.identifier)

                    for _s, p, o in is_replaced_by._to_graph().triples(
                        (None, None, None)
                    ):
                        self._g.add((_is_replaced_by, p, o))

                elif isinstance(is_replaced_by, str):
                    _is_replaced_by = URIRef(is_replaced_by)

                self._g.add(
                    (URIRef(self.identifier), DCTERMS.isReplacedBy, _is_replaced_by,)
                )

    def _has_part_to_graph(self: InformationModel) -> None:
        if getattr(self, "has_part", None):

            for has_part in self._has_part:

                if isinstance(has_part, InformationModel):
                    _has_part = URIRef(has_part.identifier)

                    for _s, p, o in has_part._to_graph().triples((None, None, None)):
                        self._g.add((_has_part, p, o))

                elif isinstance(has_part, str):
                    _has_part = URIRef(has_part)

                self._g.add((URIRef(self.identifier), DCTERMS.hasPart, _has_part,))

    def _is_part_of_to_graph(self: InformationModel) -> None:
        if getattr(self, "is_part_of", None):

            for is_part_of in self._is_part_of:

                if isinstance(is_part_of, InformationModel):
                    _is_part_of = URIRef(is_part_of.identifier)

                    for _s, p, o in is_part_of._to_graph().triples((None, None, None)):
                        self._g.add((_is_part_of, p, o))

                elif isinstance(is_part_of, str):
                    _is_part_of = URIRef(is_part_of)

                self._g.add((URIRef(self.identifier), DCTERMS.isPartOf, _is_part_of,))

    def _homepage_to_graph(self: InformationModel) -> None:
        if getattr(self, "homepage", None):
            self._g.add((URIRef(self.identifier), FOAF.homepage, URIRef(self.homepage)))

    def _contactpoints_to_graph(self: InformationModel) -> None:
        if getattr(self, "contactpoints", None):

            for contactpoint in self._contactpoints:

                _contactpoint = BNode()

                for _s, p, o in contactpoint._to_graph().triples((None, None, None)):
                    self._g.add((_contactpoint, p, o))

                self._g.add(
                    (URIRef(self.identifier), DCAT.contactPoint, _contactpoint,)
                )

    def _locations_to_graph(self: InformationModel) -> None:
        if getattr(self, "locations", None):

            for location in self._locations:

                _location = BNode()

                for _s, p, o in location._to_graph().triples((None, None, None)):
                    self._g.add((_location, p, o))

                self._g.add((URIRef(self.identifier), DCTERMS.spatial, _location,))

    def _modified_to_graph(self: InformationModel) -> None:
        if getattr(self, "modified", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCTERMS.modified,
                    Literal(self.modified, datatype=XSD.date),
                )
            )

    def _dct_type_to_graph(self: InformationModel) -> None:
        if getattr(self, "dct_type", None):

            if isinstance(self.dct_type, Concept):
                _dct_type = URIRef(self.dct_type.identifier)

                for _s, p, o in self.dct_type._to_graph().triples((None, None, None)):
                    self._g.add((_dct_type, p, o))

            elif isinstance(self.dct_type, str):
                _dct_type = URIRef(self.dct_type)

            self._g.add((URIRef(self.identifier), DCTERMS.type, _dct_type,))

    def _version_note_to_graph(self: InformationModel) -> None:
        if getattr(self, "version_note", None):

            for key in self.version_note:
                self._g.add(
                    (
                        URIRef(self.identifier),
                        ADMS.versionNotes,
                        Literal(self.version_note[key], lang=key),
                    )
                )

    def _status_to_graph(self: InformationModel) -> None:

        if getattr(self, "status", None):

            if isinstance(self.status, Concept):
                _status = URIRef(self.status.identifier)

                for _s, p, o in self.status._to_graph().triples((None, None, None)):
                    self._g.add((_status, p, o))

            elif isinstance(self.status, str):
                _status = URIRef(self.status)

            self._g.add((URIRef(self.identifier), ADMS.status, _status))

    def _has_formats_to_graph(self: InformationModel) -> None:

        if getattr(self, "has_format", None):

            for has_format in self._has_format:

                if isinstance(has_format, FoafDocument):

                    if not getattr(has_format, "identifier", None):
                        has_format.identifier = Skolemizer.add_skolemization()

                    _has_format = URIRef(has_format.identifier)

                    for _s, p, o in has_format._to_graph().triples((None, None, None)):
                        self._g.add((_s, p, o))

                elif isinstance(has_format, str):
                    _has_format = URIRef(has_format)

                self._g.add((URIRef(self.identifier), DCTERMS.hasFormat, _has_format,))

    def _temporals_to_graph(self: InformationModel) -> None:
        if getattr(self, "temporal", None):

            for temporal in self._temporal:

                _temporal = BNode()

                for _s, p, o in temporal._to_graph().triples((None, None, None)):
                    self._g.add((_temporal, p, o))

                self._g.add((URIRef(self.identifier), DCTERMS.temporal, _temporal,))


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
        "_belongs_to_module",
        "_description",
    )

    _g: Graph
    _title: dict
    _identifier: URI
    _dct_identifier: str
    _has_property: List[Union[ModelProperty, URI]]
    _subject: Union[Concept, URI]
    _belongs_to_module: List[str]
    _description: dict

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
    def subject(self) -> Union[Concept, URI]:
        """Get for subject."""
        return self._subject

    @subject.setter
    def subject(self, subject: Union[Concept, URI]) -> None:
        """Set for subject."""
        self._subject = subject

    @property
    def has_property(self) -> List[Union[ModelProperty, URI]]:
        """Get for has_property."""
        return self._has_property

    @has_property.setter
    def has_property(self, has_property: List[Union[ModelProperty, URI]]) -> None:
        """Set for has_property."""
        self._has_property = has_property

    @property
    def belongs_to_module(self) -> List[str]:
        """Get for belongs_to_module."""
        return self._belongs_to_module

    @belongs_to_module.setter
    def belongs_to_module(self, belongs_to_module: List[str]) -> None:
        """Set for belongs_to_module."""
        self._belongs_to_module = belongs_to_module

    @property
    def description(self: ModelElement) -> dict:
        """Get for description."""
        return self._description

    @description.setter
    def description(self: ModelElement, description: dict) -> None:
        """Set for description."""
        self._description = description

    @abstractmethod
    def to_rdf(
        self, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the modelelement to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        """

    def _to_graph(
        self, type: str = MODELLDCATNO.ModelElement, selfobject: URIRef = None,
    ) -> Graph:
        """Returns the modelelement as graph.

         Args:
            type: type for identifying class. Default: MODELLDCATNO.ModelElement
            selfobject: a URIRef passed from a subclass Default: None

        Returns:
            the modelelement graph
        """
        # Set up graph and namespaces:
        self._g = Graph()
        self._g.bind("modelldcatno", MODELLDCATNO)
        self._g.bind("dct", DCTERMS)
        self._g.bind("dcat", DCAT)
        self._g.bind("skos", SKOS)
        self._g.bind("xsd", XSD)

        self._g.add((selfobject, RDF.type, type))

        if getattr(self, "title", None):
            for key in self.title:
                self._g.add(
                    (selfobject, DCTERMS.title, Literal(self.title[key], lang=key),)
                )

        if getattr(self, "dct_identifier", None):
            self._g.add((selfobject, DCTERMS.identifier, Literal(self.dct_identifier)))

        if getattr(self, "has_property", None):
            self._has_property_to_graph(selfobject)

        self._belongs_to_module_to_graph(selfobject)
        self._description_to_graph(selfobject)
        self._subjet_to_graph(selfobject)

        return self._g

    def _subjet_to_graph(self: ModelElement, selfobject: URIRef) -> None:

        if getattr(self, "subject", None):

            if isinstance(self.subject, Concept):
                _subject = URIRef(self.subject.identifier)

                for _s, p, o in self.subject._to_graph().triples((None, None, None)):
                    self._g.add((_subject, p, o))

            elif isinstance(self.subject, str):
                _subject = URIRef(self.subject)

            self._g.add((selfobject, DCTERMS.subject, _subject))

    def _belongs_to_module_to_graph(self: ModelElement, selfobject: URIRef) -> None:
        if getattr(self, "belongs_to_module", None):

            for belongs_to_module in self._belongs_to_module:
                _datatype = XSD.anyURI if validators.url(belongs_to_module) else None

                self._g.add(
                    (
                        selfobject,
                        MODELLDCATNO.belongsToModule,
                        Literal(belongs_to_module, datatype=_datatype),
                    )
                )

    def _description_to_graph(self: ModelElement, selfobject: URIRef) -> None:
        if getattr(self, "description", None):
            for key in self.description:
                self._g.add(
                    (
                        selfobject,
                        DCTERMS.description,
                        Literal(self.description[key], lang=key),
                    )
                )

    def _has_property_to_graph(self, _self: URIRef) -> None:
        if getattr(self, "has_property", None):
            for has_property in self._has_property:

                if isinstance(has_property, ModelProperty):

                    if not getattr(has_property, "identifier", None):
                        has_property.identifier = Skolemizer.add_skolemization()

                    _has_property = URIRef(has_property.identifier)

                    for _s, p, o in has_property._to_graph().triples(
                        (None, None, None)
                    ):
                        self._g.add((_s, p, o))

                elif isinstance(has_property, str):
                    _has_property = URIRef(has_property)

                self._g.add((_self, MODELLDCATNO.hasProperty, _has_property,))


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
        "_description",
        "_belongs_to_module",
        "_forms_symmetry_with",
        "_relation_property_label",
        "_sequence_number",
    )

    _g: Graph
    _identifier: URI
    _has_type: List[Union[ModelElement, URI]]
    _min_occurs: int
    _max_occurs: int
    _title: dict
    _subject: Union[Concept, URI]
    _description: dict
    _belongs_to_module: List[str]
    _forms_symmetry_with: Union[ModelProperty, URI]
    _relation_property_label: dict
    _sequence_number: int

    @abstractmethod
    def __init__(self) -> None:
        """Inits an object with default values."""
        self._type = MODELLDCATNO.Property
        self._has_type = []

    @property
    def subject(self) -> Union[Concept, URI]:
        """Get for subject."""
        return self._subject

    @subject.setter
    def subject(self, subject: Union[Concept, URI]) -> None:
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
    def has_type(self) -> List[Union[ModelElement, URI]]:
        """Get for has_type."""
        return self._has_type

    @has_type.setter
    def has_type(self, has_type: List[Union[ModelElement, URI]]) -> None:
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

    @property
    def description(self: ModelProperty) -> dict:
        """Get for description."""
        return self._description

    @description.setter
    def description(self: ModelProperty, description: dict) -> None:
        """Set for description."""
        self._description = description

    @property
    def belongs_to_module(self: ModelProperty) -> List[str]:
        """Get for belongs_to_module."""
        return self._belongs_to_module

    @belongs_to_module.setter
    def belongs_to_module(self: ModelProperty, belongs_to_module: List[str]) -> None:
        """Set for belongs_to_module."""
        self._belongs_to_module = belongs_to_module

    @property
    def forms_symmetry_with(self: ModelProperty) -> Union[ModelProperty, URI]:
        """Get for forms_symmetry_with."""
        return self._forms_symmetry_with

    @forms_symmetry_with.setter
    def forms_symmetry_with(
        self: ModelProperty, forms_symmetry_with: Union[ModelProperty, URI]
    ) -> None:
        """Set for forms_symmetry_with."""
        self._forms_symmetry_with = forms_symmetry_with

    @property
    def relation_property_label(self: ModelProperty) -> dict:
        """Get for relation_property_label."""
        return self._relation_property_label

    @relation_property_label.setter
    def relation_property_label(
        self: ModelProperty, relation_property_label: dict
    ) -> None:
        """Set for relation_property_label."""
        self._relation_property_label = relation_property_label

    @property
    def sequence_number(self: ModelProperty) -> int:
        """Get for sequence_number."""
        return self._sequence_number

    @sequence_number.setter
    def sequence_number(self: ModelProperty, sequence_number: int) -> None:
        """Set for sequence_number."""
        self._sequence_number = sequence_number

    @abstractmethod
    def to_rdf(
        self, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the property to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into
        """

    def _to_graph(
        self, type: str = MODELLDCATNO.Property, selfobject: URIRef = None,
    ) -> Graph:
        """Returns the property as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Property
            selfobject: a URIRef passed from a subclass Default: None

        Returns:
            the property graph
        """
        # Set up graph and namespaces:
        self._g = Graph()
        self._g.bind("modelldcatno", MODELLDCATNO)
        self._g.bind("dct", DCTERMS)
        self._g.bind("skos", SKOS)

        self._g.add((selfobject, RDF.type, type))

        self._has_type_to_graph(selfobject)

        if getattr(self, "sequence_number", None):
            self._g.add(
                (
                    selfobject,
                    MODELLDCATNO.sequenceNumber,
                    Literal(self.sequence_number, datatype=XSD.positiveInteger),
                )
            )

        if getattr(self, "min_occurs", None):
            self._g.add((selfobject, XSD.minOccurs, Literal(self.min_occurs)))

        if getattr(self, "max_occurs", None):
            self._g.add((selfobject, XSD.maxOccurs, Literal(self.max_occurs)))

        if getattr(self, "title", None):
            for key in self.title:
                self._g.add(
                    (selfobject, DCTERMS.title, Literal(self.title[key], lang=key),)
                )

        self._subject_to_graph(selfobject)
        self._description_to_graph(selfobject)
        self._belongs_to_module_to_graph(selfobject)
        self._forms_symmetry_with_to_graph(selfobject)
        self._relation_property_label_to_graph(selfobject)

        return self._g

    def _subject_to_graph(self: ModelProperty, selfobject: URIRef) -> None:

        if getattr(self, "subject", None):

            if isinstance(self.subject, Concept):
                _subject = URIRef(self.subject.identifier)

                for _s, p, o in self.subject._to_graph().triples((None, None, None)):
                    self._g.add((_subject, p, o))

            elif isinstance(self.subject, str):
                _subject = URIRef(self.subject)

            self._g.add((selfobject, DCTERMS.subject, _subject))

    def _has_type_to_graph(self, _self: URIRef) -> None:
        if getattr(self, "has_type", None):

            for has_type in self._has_type:

                if isinstance(has_type, ModelElement):

                    if not getattr(has_type, "identifier", None):
                        has_type.identifier = Skolemizer.add_skolemization()

                    _has_type = URIRef(has_type.identifier)

                    for _s, p, o in has_type._to_graph().triples((None, None, None)):
                        self._g.add((_s, p, o))

                elif isinstance(has_type, str):
                    _has_type = URIRef(has_type)

                self._g.add((_self, MODELLDCATNO.hasType, _has_type,))

    def _description_to_graph(self: ModelProperty, selfobject: URIRef) -> None:
        if getattr(self, "description", None):
            for key in self.description:
                self._g.add(
                    (
                        selfobject,
                        DCTERMS.description,
                        Literal(self.description[key], lang=key),
                    )
                )

    def _belongs_to_module_to_graph(self: ModelProperty, selfobject: URIRef) -> None:
        if getattr(self, "belongs_to_module", None):

            for belongs_to_module in self._belongs_to_module:
                _datatype = XSD.anyURI if validators.url(belongs_to_module) else None

                self._g.add(
                    (
                        selfobject,
                        MODELLDCATNO.belongsToModule,
                        Literal(belongs_to_module, datatype=_datatype),
                    )
                )

    def _forms_symmetry_with_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "forms_symmetry_with", None):

            if isinstance(self.forms_symmetry_with, ModelProperty):

                if not getattr(self.forms_symmetry_with, "identifier", None):
                    self.forms_symmetry_with.identifier = Skolemizer.add_skolemization()

                _forms_symmetry_with = URIRef(self.forms_symmetry_with.identifier)

                for _s, p, o in self.forms_symmetry_with._to_graph().triples(
                    (None, None, None)
                ):
                    self._g.add((_s, p, o))

            elif isinstance(self.forms_symmetry_with, str):
                _forms_symmetry_with = URIRef(self.forms_symmetry_with)

            self._g.add((_self, MODELLDCATNO.formsSymmetryWith, _forms_symmetry_with))

    def _relation_property_label_to_graph(
        self: ModelProperty, selfobject: URIRef
    ) -> None:
        if getattr(self, "relation_property_label", None):
            for key in self.relation_property_label:
                self._g.add(
                    (
                        selfobject,
                        MODELLDCATNO.relationPropertyLabel,
                        Literal(self.relation_property_label[key], lang=key),
                    )
                )


class Role(ModelProperty):
    """A class representing a modelldcatno:Role."""

    __slots__ = (
        "_identifier",
        "_has_object_type",
    )

    _identifier: URI
    _has_object_type: Union[ObjectType, URI]
    _g: Graph

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier
        super().__init__()

    @property
    def has_object_type(self: Role) -> Union[ObjectType, URI]:
        """Get for has_object_type."""
        return self._has_object_type

    @has_object_type.setter
    def has_object_type(self: Role, has_object_type: Union[ObjectType, URI]) -> None:
        """Set for has_object_type."""
        self._has_object_type = has_object_type

    def to_rdf(
        self: Role, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the role to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format encoded as bytes.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: Role, type: str = MODELLDCATNO.Role, selfobject: URIRef = None,
    ) -> Graph:
        """Returns the role as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Role
            selfobject: a URIRef passed from a subclass Default: None

        Returns:
            the role graph
        """
        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        _self = URIRef(self.identifier)

        super(Role, self)._to_graph(MODELLDCATNO.Role, _self)

        self._has_object_type_to_graph(_self)

        return self._g

    def _has_object_type_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "has_object_type", None):

            if isinstance(self.has_object_type, ObjectType):

                if not getattr(self.has_object_type, "identifier", None):
                    self._has_object_type.identifier = Skolemizer.add_skolemization()

                _has_object_type = URIRef(self.has_object_type.identifier)

                for _s, p, o in self._has_object_type._to_graph().triples(
                    (None, None, None)
                ):
                    self._g.add((_s, p, o))

            elif isinstance(self.has_object_type, str):
                _has_object_type = URIRef(self.has_object_type)

            self._g.add((_self, MODELLDCATNO.hasObjectType, _has_object_type))


class ObjectType(ModelElement):
    """A class representing a modelldcatno:ObjectType."""

    _identifier: URI
    _dct_identifier: str
    _g: Graph
    _belongs_to_module: List[str]

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier
        super().__init__()

    def to_rdf(
        self: ObjectType, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the object type to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format encoded as bytes.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: ObjectType,
        type: str = MODELLDCATNO.ObjectType,
        selfobject: URIRef = None,
    ) -> Graph:
        """Returns the object type as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.ObjectType
            selfobject: a URIRef passed from a subclass Default: None

        Returns:
            the object type graph
        """
        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()
        _self = URIRef(self.identifier)

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
    _belongs_to_module: List[str]

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier
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
    ) -> bytes:
        """Maps the simple type to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format encoded as bytes.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: SimpleType,
        type: str = MODELLDCATNO.SimpleType,
        selfobject: URIRef = None,
    ) -> Graph:
        """Returns the object type as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.SimpleType
            selfobject: a URIRef passed from a subclass Default: None

        Returns:
            the object type graph
        """
        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        _self = URIRef(self.identifier)

        super(SimpleType, self)._to_graph(MODELLDCATNO.SimpleType, _self)

        self._add_properties(_self)

        return self._g

    def _add_properties(self, _self: URIRef) -> None:

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
                (
                    _self,
                    MODELLDCATNO.typeDefinitionReference,
                    URIRef(self.type_definition_reference),
                ),
            )

        if getattr(self, "pattern", None):
            self._g.add((_self, XSD.pattern, Literal(self.pattern)))


class Composition(ModelProperty):
    """A class representing a modelldcatno:Composition."""

    __slots__ = "_contains"

    _contains: Union[ModelElement, URI]
    _identifier: URI
    _g: Graph

    @property
    def contains(self: Composition) -> Union[ModelElement, URI]:
        """Get for contains."""
        return self._contains

    @contains.setter
    def contains(self: Composition, contains: Union[ModelElement, URI]) -> None:
        """Set for contains."""
        self._contains = contains

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier
        super().__init__()

    def to_rdf(
        self: Composition, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the composition to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format encoded as bytes.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: Composition,
        type: str = MODELLDCATNO.Composition,
        selfobject: URIRef = None,
    ) -> Graph:
        """Returns the role as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Composition
            selfobject: a URIRef passed from a subclass Default: None

        Returns:
            the role graph
        """
        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        _self = URIRef(self.identifier)

        super(Composition, self)._to_graph(MODELLDCATNO.Composition, _self)

        self._contains_to_graph(_self)

        return self._g

    def _contains_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "contains", None):

            if isinstance(self.contains, ModelElement):

                if not getattr(self.contains, "identifier", None):
                    self.contains.identifier = Skolemizer.add_skolemization()

                _contains = URIRef(self.contains.identifier)

                for _s, p, o in self._contains._to_graph().triples((None, None, None)):
                    self._g.add((_s, p, o))

            elif isinstance(self.contains, str):
                _contains = URIRef(self.contains)

            self._g.add((_self, MODELLDCATNO.contains, _contains))


class Collection(ModelProperty):
    """A class representing a modelldcatno:Collection."""

    __slots__ = "_has_member"

    _has_member: Union[ModelElement, URI]
    _identifier: URI
    _g: Graph

    @property
    def has_member(self: Collection) -> Union[ModelElement, URI]:
        """Get for has_member."""
        return self._has_member

    @has_member.setter
    def has_member(self: Collection, has_member: Union[ModelElement, URI]) -> None:
        """Set for has_member."""
        self._has_member = has_member

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier
        super().__init__()

    def to_rdf(
        self: Collection, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the collection to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format encoded as bytes.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: Collection,
        type: str = MODELLDCATNO.Collection,
        selfobject: URIRef = None,
    ) -> Graph:
        """Returns the role as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Collection
            selfobject: a URIRef passed from a subclass Default: None

        Returns:
            the role graph
        """
        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        _self = URIRef(self.identifier)

        super(Collection, self)._to_graph(MODELLDCATNO.Collection, _self)

        self._has_member_to_graph(_self)

        return self._g

    def _has_member_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "has_member", None):

            if isinstance(self.has_member, ModelElement):

                if not getattr(self.has_member, "identifier", None):
                    self.has_member.identifier = Skolemizer.add_skolemization()

                _has_member = URIRef(self.has_member.identifier)

                for _s, p, o in self._has_member._to_graph().triples(
                    (None, None, None)
                ):
                    self._g.add((_s, p, o))

            elif isinstance(self.has_member, str):
                _has_member = URIRef(self.has_member)

            self._g.add((_self, MODELLDCATNO.hasMember, _has_member))


class Association(ModelProperty):
    """A class representing a modelldcatno:Association."""

    __slots__ = "_refers_to"

    _refers_to: Union[ModelElement, URI]
    _identifier: URI
    _g: Graph

    @property
    def refers_to(self: Association) -> Union[ModelElement, URI]:
        """Get for refers_to."""
        return self._refers_to

    @refers_to.setter
    def refers_to(self: Association, refers_to: Union[ModelElement, URI]) -> None:
        """Set for refers_to."""
        self._refers_to = refers_to

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier
        super().__init__()

    def to_rdf(
        self: Association, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the association to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format encoded as bytes.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: Association,
        type: str = MODELLDCATNO.Association,
        selfobject: URIRef = None,
    ) -> Graph:
        """Returns the association as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Association
            selfobject: a URIRef passed from a subclass Default: None

        Returns:
            the association graph
        """
        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        _self = URIRef(self.identifier)

        super(Association, self)._to_graph(MODELLDCATNO.Association, _self)

        self._refers_to_to_graph(_self)

        return self._g

    def _refers_to_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "refers_to", None):

            if isinstance(self.refers_to, ModelElement):

                if not getattr(self.refers_to, "identifier", None):
                    self._refers_to.identifier = Skolemizer.add_skolemization()

                _refers_to = URIRef(self.refers_to.identifier)

                for _s, p, o in self._refers_to._to_graph().triples((None, None, None)):
                    self._g.add((_s, p, o))

            elif isinstance(self.refers_to, str):
                _refers_to = URIRef(self.refers_to)

            self._g.add((_self, MODELLDCATNO.refersTo, _refers_to))

        return self._g


class Choice(ModelProperty):
    """A class representing a modelldcatno:Choice."""

    __slots__ = "_has_some"

    _has_some: List[Union[ModelElement, URI]]
    _identifier: URI
    _g: Graph

    @property
    def has_some(self: Choice) -> List[Union[ModelElement, URI]]:
        """Get for has_some."""
        return self._has_some

    @has_some.setter
    def has_some(self: Choice, has_some: List[Union[ModelElement, URI]]) -> None:
        """Set for has_some."""
        self._has_some = has_some

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits Choice object with default values."""
        if identifier:
            self.identifier = identifier
        super().__init__()
        self._has_some = []

    def to_rdf(
        self: Choice, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the choice to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format encoded as bytes.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: Choice, type: str = MODELLDCATNO.Choice, selfobject: URIRef = None,
    ) -> Graph:
        """Returns the role as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Choice
            selfobject: a URIRef passed from a subclass Default: None

        Returns:
            the role graph
        """
        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        _self = URIRef(self.identifier)

        super(Choice, self)._to_graph(MODELLDCATNO.Choice, _self)

        self._has_some_to_graph(_self)

        return self._g

    def _has_some_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "has_some", None):

            for has_some in self._has_some:

                if isinstance(has_some, ModelElement):

                    if not getattr(has_some, "identifier", None):
                        has_some.identifier = Skolemizer.add_skolemization()

                    _has_some = URIRef(has_some.identifier)

                    for _s, p, o in has_some._to_graph().triples((None, None, None)):
                        self._g.add((_s, p, o))

                elif isinstance(has_some, str):
                    _has_some = URIRef(has_some)

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
    _contains_object_type: Union[ObjectType, URI]
    _g: Graph
    _has_simple_type: Union[SimpleType, URI]
    _has_data_type: Union[DataType, URI]
    _has_value_from: Union[CodeList, URI]

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier
        super().__init__()

    @property
    def contains_object_type(self: Attribute) -> Union[ObjectType, URI]:
        """Get for contains_object_type."""
        return self._contains_object_type

    @contains_object_type.setter
    def contains_object_type(
        self: Attribute, contains_object_type: Union[ObjectType, URI]
    ) -> None:
        """Set for contains_object_type."""
        self._contains_object_type = contains_object_type

    @property
    def has_simple_type(self: Attribute) -> Union[SimpleType, URI]:
        """Get for has_simple_type."""
        return self._has_simple_type

    @has_simple_type.setter
    def has_simple_type(
        self: Attribute, has_simple_type: Union[SimpleType, URI]
    ) -> None:
        """Set for has_simple_type."""
        self._has_simple_type = has_simple_type

    @property
    def has_data_type(self: Attribute) -> Union[DataType, URI]:
        """Get for has_data_type."""
        return self._has_data_type

    @has_data_type.setter
    def has_data_type(self: Attribute, has_data_type: Union[DataType, URI]) -> None:
        """Set for has_data_type."""
        self._has_data_type = has_data_type

    @property
    def has_value_from(self: Attribute) -> Union[CodeList, URI]:
        """Get for has_value_from."""
        return self._has_value_from

    @has_value_from.setter
    def has_value_from(self: Attribute, has_value_from: Union[CodeList, URI]) -> None:
        """Set for has_value_from."""
        self._has_value_from = has_value_from

    def to_rdf(
        self: Attribute, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the attribute to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format encoded as bytes.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: Attribute, type: str = MODELLDCATNO.Attribute, selfobject: URIRef = None,
    ) -> Graph:
        """Returns the role as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Attribute
            selfobject: a URIRef passed from a subclass Default: None

        Returns:
            the role graph
        """
        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()
        _self = URIRef(self.identifier)

        super(Attribute, self)._to_graph(MODELLDCATNO.Attribute, _self)

        self._contains_object_type_to_graph(_self)
        self._has_simple_type_to_graph(_self)
        self._has_data_type_to_graph(_self)
        self._has_value_from_to_graph(_self)

        return self._g

    def _contains_object_type_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "contains_object_type", None):

            if isinstance(self.contains_object_type, ObjectType):

                if not getattr(self.contains_object_type, "identifier", None):
                    self.contains_object_type.identifier = (
                        Skolemizer.add_skolemization()
                    )

                _contains_object_type = URIRef(self.contains_object_type.identifier)

                for _s, p, o in self._contains_object_type._to_graph().triples(
                    (None, None, None)
                ):
                    self._g.add((_s, p, o))

            elif isinstance(self.contains_object_type, str):
                _contains_object_type = URIRef(self.contains_object_type)

            self._g.add((_self, MODELLDCATNO.containsObjectType, _contains_object_type))

    def _has_simple_type_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "has_simple_type", None):

            if isinstance(self.has_simple_type, SimpleType):

                if not getattr(self.has_simple_type, "identifier", None):
                    self.has_simple_type.identifier = Skolemizer.add_skolemization()

                _has_simple_type = URIRef(self.has_simple_type.identifier)

                for _s, p, o in self._has_simple_type._to_graph().triples(
                    (None, None, None)
                ):
                    self._g.add((_s, p, o))

            elif isinstance(self.has_simple_type, str):
                _has_simple_type = URIRef(self.has_simple_type)

            self._g.add((_self, MODELLDCATNO.hasSimpleType, _has_simple_type))

    def _has_data_type_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "has_data_type", None):

            if isinstance(self.has_data_type, DataType):

                if not getattr(self.has_data_type, "identifier", None):
                    self.has_data_type.identifier = Skolemizer.add_skolemization()

                _has_data_type = URIRef(self.has_data_type.identifier)

                for _s, p, o in self._has_data_type._to_graph().triples(
                    (None, None, None)
                ):
                    self._g.add((_s, p, o))

            elif isinstance(self.has_data_type, str):
                _has_data_type = URIRef(self.has_data_type)

            self._g.add((_self, MODELLDCATNO.hasDataType, _has_data_type))

    def _has_value_from_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "has_value_from", None):

            if isinstance(self.has_value_from, CodeList):

                if not getattr(self.has_value_from, "identifier", None):
                    self.has_value_from.identifier = Skolemizer.add_skolemization()

                _has_value_from = URIRef(self.has_value_from.identifier)

                for _s, p, o in self._has_value_from._to_graph().triples(
                    (None, None, None)
                ):
                    self._g.add((_s, p, o))

            elif isinstance(self.has_value_from, str):
                _has_value_from = URIRef(self.has_value_from)

            self._g.add((_self, MODELLDCATNO.hasValueFrom, _has_value_from))


class Specialization(ModelProperty):
    """A class representing a modelldcatno:Specialization."""

    __slots__ = "_has_general_concept"

    _has_general_concept: Union[ModelElement, URI]
    _identifier: URI
    _g: Graph

    @property
    def has_general_concept(self: Specialization) -> Union[ModelElement, URI]:
        """Get for has_general_concept."""
        return self._has_general_concept

    @has_general_concept.setter
    def has_general_concept(
        self: Specialization, has_general_concept: Union[ModelElement, URI]
    ) -> None:
        """Set for has_general_concept."""
        self._has_general_concept = has_general_concept

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier
        super().__init__()

    def to_rdf(
        self: Specialization, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the specialization to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format encoded as bytes.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: Specialization,
        type: str = MODELLDCATNO.Specialization,
        selfobject: URIRef = None,
    ) -> Graph:
        """Returns the role as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Association
            selfobject: a URIRef passed from a subclass Default: None

        Returns:
            the role graph
        """
        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        _self = URIRef(self.identifier)

        super(Specialization, self)._to_graph(MODELLDCATNO.Specialization, _self)

        self._has_general_concept_to_graph(_self)

        return self._g

    def _has_general_concept_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "has_general_concept", None):

            if isinstance(self.has_general_concept, ModelElement):

                if not getattr(self.has_general_concept, "identifier", None):
                    self.has_general_concept.identifier = Skolemizer.add_skolemization()

                _has_general_concept = URIRef(self.has_general_concept.identifier)

                for _s, p, o in self._has_general_concept._to_graph().triples(
                    (None, None, None)
                ):
                    self._g.add((_s, p, o))

            elif isinstance(self.has_general_concept, str):
                _has_general_concept = URIRef(self.has_general_concept)

            self._g.add((_self, MODELLDCATNO.hasGeneralConcept, _has_general_concept))


class Realization(ModelProperty):
    """A class representing a modelldcatno:Realization."""

    __slots__ = "_has_supplier"

    _has_supplier: Union[ModelElement, URI]
    _identifier: URI
    _g: Graph

    @property
    def has_supplier(self: Realization) -> Union[ModelElement, URI]:
        """Get for has_supplier."""
        return self._has_supplier

    @has_supplier.setter
    def has_supplier(self: Realization, has_supplier: Union[ModelElement, URI]) -> None:
        """Set for has_supplier."""
        self._has_supplier = has_supplier

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier
        super().__init__()

    def to_rdf(
        self: Realization, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the realization to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format encoded as bytes.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: Realization,
        type: str = MODELLDCATNO.Realization,
        selfobject: URIRef = None,
    ) -> Graph:
        """Returns the realization as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Association
            selfobject: a URIRef passed from a subclass Default: None

        Returns:
            the assocation graph
        """
        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        _self = URIRef(self.identifier)

        super(Realization, self)._to_graph(MODELLDCATNO.Realization, _self)

        self._has_supplier_to_graph(_self)

        return self._g

    def _has_supplier_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "has_supplier", None):

            if isinstance(self.has_supplier, ModelElement):

                if not getattr(self.has_supplier, "identifier", None):
                    self.has_supplier.identifier = Skolemizer.add_skolemization()

                _has_supplier = URIRef(self.has_supplier.identifier)

                for _s, p, o in self._has_supplier._to_graph().triples(
                    (None, None, None)
                ):
                    self._g.add((_s, p, o))

            elif isinstance(self.has_supplier, str):
                _has_supplier = URIRef(self.has_supplier)

            self._g.add((_self, MODELLDCATNO.hasSupplier, _has_supplier))


class Abstraction(ModelProperty):
    """A class representing a modelldcatno:Abstraction."""

    __slots__ = "_is_abstraction_of"

    _is_abstraction_of: Union[ModelElement, URI]
    _identifier: URI
    _g: Graph

    @property
    def is_abstraction_of(self: Abstraction) -> Union[ModelElement, URI]:
        """Get for is_abstraction_of."""
        return self._is_abstraction_of

    @is_abstraction_of.setter
    def is_abstraction_of(
        self: Abstraction, is_abstraction_of: Union[ModelElement, URI]
    ) -> None:
        """Set for is_abstraction_of."""
        self._is_abstraction_of = is_abstraction_of

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier
        super().__init__()

    def to_rdf(
        self: Abstraction, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the abstraction to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format encoded as bytes.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: Abstraction,
        type: str = MODELLDCATNO.Abstraction,
        selfobject: URIRef = None,
    ) -> Graph:
        """Returns the role as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Abstraction
            selfobject: a URIRef passed from a subclass Default: None

        Returns:
            the role graph
        """
        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        _self = URIRef(self.identifier)

        super(Abstraction, self)._to_graph(MODELLDCATNO.Abstraction, _self)

        self._is_abstraction_of_to_graph(_self)

        return self._g

    def _is_abstraction_of_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "is_abstraction_of", None):

            if isinstance(self.is_abstraction_of, ModelElement):

                if not getattr(self.is_abstraction_of, "identifier", None):
                    self.is_abstraction_of.identifier = Skolemizer.add_skolemization()

                _is_abstraction_of = URIRef(self.is_abstraction_of.identifier)

                for _s, p, o in self._is_abstraction_of._to_graph().triples(
                    (None, None, None)
                ):
                    self._g.add((_s, p, o))

            elif isinstance(self.is_abstraction_of, str):
                _is_abstraction_of = URIRef(self.is_abstraction_of)

            self._g.add((_self, MODELLDCATNO.isAbstractionOf, _is_abstraction_of))


class DataType(ModelElement):
    """A class representing a modelldcatno:DataType."""

    _identifier: URI
    _dct_identifier: str
    _g: Graph
    _belongs_to_module: List[str]

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier
        super().__init__()

    def to_rdf(
        self: DataType, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the data type to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format encoded as bytes.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: DataType, type: str = MODELLDCATNO.DataType, selfobject: URIRef = None,
    ) -> Graph:
        """Returns the data type as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.DataType
            selfobject: a URIRef passed from a subclass Default: None

        Returns:
            the object type graph
        """
        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()
        _self = URIRef(self.identifier)

        super(DataType, self)._to_graph(MODELLDCATNO.DataType, _self)

        return self._g


class RootObjectType(ModelElement):
    """A class representing a modelldcatno:RootObjectType."""

    _identifier: URI
    _dct_identifier: str
    _g: Graph
    _belongs_to_module: List[str]

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier
        super().__init__()

    def to_rdf(
        self: RootObjectType, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the root object type type to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format encoded as bytes.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: RootObjectType,
        type: str = MODELLDCATNO.RootObjectType,
        selfobject: URIRef = None,
    ) -> Graph:
        """Returns the root object type as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.RootObjectType
            selfobject: a URIRef passed from a subclass Default: None

        Returns:
            the root object type graph
        """
        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        _self = URIRef(self.identifier)

        super(RootObjectType, self)._to_graph(MODELLDCATNO.RootObjectType, _self)

        return self._g


class CodeList(ModelElement):
    """A class representing a modelldcatno:CodeList."""

    __slots__ = (
        "_identifier",
        "_dct_identifier",
        "g",
        "_code_list_reference",
    )

    _identifier: URI
    _dct_identifier: str
    _g: Graph
    _code_list_reference: Union[CodeList, URI]
    _belongs_to_module: List[str]

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier
        super().__init__()

    @property
    def code_list_reference(self: CodeList) -> Union[CodeList, URI]:
        """Get for code_list_reference."""
        return self._code_list_reference

    @code_list_reference.setter
    def code_list_reference(
        self: CodeList, code_list_reference: Union[CodeList, URI]
    ) -> None:
        """Set for code_list_reference."""
        self._code_list_reference = code_list_reference

    def to_rdf(
        self: CodeList, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the code list to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format encoded as bytes.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: CodeList, type: str = MODELLDCATNO.CodeList, selfobject: URIRef = None,
    ) -> Graph:
        """Returns the root object type as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.CodeList
            selfobject: a URIRef passed from a subclass Default: None

        Returns:
            the root object type graph
        """
        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        _self = URIRef(self.identifier)

        super(CodeList, self)._to_graph(MODELLDCATNO.CodeList, _self)

        self._code_list_reference_to_graph(_self)

        return self._g

    def _code_list_reference_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "code_list_reference", None):

            if isinstance(self.code_list_reference, CodeList):

                if not getattr(self.code_list_reference, "identifier", None):
                    self.code_list_reference.identifier = Skolemizer.add_skolemization()

                _code_list_reference = URIRef(self.code_list_reference.identifier)

                for _s, p, o in self.code_list_reference._to_graph().triples(
                    (None, None, None)
                ):
                    self._g.add((_s, p, o))

            elif isinstance(self.code_list_reference, str):
                _code_list_reference = URIRef(self.code_list_reference)

            self._g.add((_self, MODELLDCATNO.codeListReference, _code_list_reference))


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
        "_example",
        "_hiddenlabel",
        "_note",
        "_scopenote",
        "_exclusion_note",
        "_inclusion_note",
        "_next_element",
        "_previous_element",
    )

    _identifier: URI
    _dct_identifier: str
    _g: Graph
    _type: str
    _subject: Union[Concept, URI]
    _preflabel: dict
    _notation: str
    _in_scheme: List[Union[CodeList, URI]]
    _top_concept_of: List[Union[CodeList, URI]]
    _altlabel: dict
    _definition: dict
    _example: List[str]
    _hiddenlabel: dict
    _note: dict
    _scopenote: dict
    _exclusion_note: dict
    _inclusion_note: dict
    _next_element: Union[CodeElement, URI]
    _previous_element: Union[CodeElement, URI]

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier
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
    def subject(self: CodeElement) -> Union[Concept, URI]:
        """Get for subject."""
        return self._subject

    @subject.setter
    def subject(self: CodeElement, subject: Union[Concept, URI]) -> None:
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
    def in_scheme(self: CodeElement) -> List[Union[CodeList, URI]]:
        """Get for in_scheme."""
        return self._in_scheme

    @in_scheme.setter
    def in_scheme(self: CodeElement, in_scheme: List[Union[CodeList, URI]]) -> None:
        """Set for in_scheme."""
        self._in_scheme = in_scheme

    @property
    def top_concept_of(self: CodeElement) -> List[Union[CodeList, URI]]:
        """Get for top_concept_of."""
        return self._top_concept_of

    @top_concept_of.setter
    def top_concept_of(
        self: CodeElement, top_concept_of: List[Union[CodeList, URI]]
    ) -> None:
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

    @property
    def example(self: CodeElement) -> List[str]:
        """Get for example."""
        return self._example

    @example.setter
    def example(self: CodeElement, example: List[str]) -> None:
        """Set for example."""
        self._example = example

    @property
    def hiddenlabel(self: CodeElement) -> dict:
        """Get for hiddenlabel."""
        return self._hiddenlabel

    @hiddenlabel.setter
    def hiddenlabel(self: CodeElement, hiddenlabel: dict) -> None:
        """Set for hiddenlabel."""
        self._hiddenlabel = hiddenlabel

    @property
    def note(self: CodeElement) -> dict:
        """Get for note."""
        return self._note

    @note.setter
    def note(self: CodeElement, note: dict) -> None:
        """Set for note."""
        self._note = note

    @property
    def scopenote(self: CodeElement) -> dict:
        """Get for scopenote."""
        return self._scopenote

    @scopenote.setter
    def scopenote(self: CodeElement, scopenote: dict) -> None:
        """Set for scopenote."""
        self._scopenote = scopenote

    @property
    def exclusion_note(self: CodeElement) -> dict:
        """Get for exclusion_note."""
        return self._exclusion_note

    @exclusion_note.setter
    def exclusion_note(self: CodeElement, exclusion_note: dict) -> None:
        """Set for exclusion_note."""
        self._exclusion_note = exclusion_note

    @property
    def inclusion_note(self: CodeElement) -> dict:
        """Get for inclusion_note."""
        return self._inclusion_note

    @inclusion_note.setter
    def inclusion_note(self: CodeElement, inclusion_note: dict) -> None:
        """Set for inclusion_note."""
        self._inclusion_note = inclusion_note

    @property
    def next_element(self: CodeElement) -> Union[CodeElement, URI]:
        """Get for next_element."""
        return self._next_element

    @next_element.setter
    def next_element(self: CodeElement, next_element: Union[CodeElement, URI]) -> None:
        """Set for next_element."""
        self._next_element = next_element

    @property
    def previous_element(self: CodeElement) -> Union[CodeElement, URI]:
        """Get for previous_element."""
        return self._previous_element

    @previous_element.setter
    def previous_element(
        self: CodeElement, previous_element: Union[CodeElement, URI]
    ) -> None:
        """Set for previous_element."""
        self._previous_element = previous_element

    def to_rdf(
        self: CodeElement, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the code element to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format encoded as bytes.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(self: CodeElement) -> Graph:
        """Returns the code element as graph.

        Returns:
            the code element graph
        """
        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        _self = URIRef(self.identifier)

        # Set up graph and namespaces:
        self._g = Graph()
        self._g.bind("modelldcatno", MODELLDCATNO)
        self._g.bind("dct", DCTERMS)
        self._g.bind("skos", SKOS)

        self._g.add((_self, RDF.type, self._type))

        if getattr(self, "dct_identifier", None):
            self._g.add((_self, DCTERMS.identifier, Literal(self.dct_identifier)))

        if getattr(self, "notation", None):
            self._g.add((_self, SKOS.notation, Literal(self.notation)))

        self._preflabel_to_graph(_self)
        self._subject_to_graph(_self)
        self._in_scheme_to_graph(_self)
        self._top_concept_of_to_graph(_self)
        self._altlabel_to_graph(_self)
        self._definition_to_graph(_self)
        self._example_to_graph(_self)
        self._hiddenlabel_to_graph(_self)
        self._note_to_graph(_self)
        self._scopenote_to_graph(_self)
        self._exclusion_note_to_graph(_self)
        self._inclusion_note_to_graph(_self)
        self._next_element_to_graph(_self)
        self._previous_element_to_graph(_self)

        return self._g

    def _subject_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "subject", None):

            if isinstance(self.subject, Concept):

                _subject = URIRef(self.subject.identifier)

                for _s, p, o in self.subject._to_graph().triples((None, None, None)):
                    self._g.add((_subject, p, o))

            elif isinstance(self.subject, str):
                _subject = URIRef(self.subject)

            self._g.add((_self, DCTERMS.subject, _subject))

    def _preflabel_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "preflabel", None):

            for key in self.preflabel:
                self._g.add(
                    (_self, SKOS.prefLabel, Literal(self.preflabel[key], lang=key),)
                )

    def _in_scheme_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "in_scheme", None):

            for in_scheme in self._in_scheme:

                if isinstance(in_scheme, CodeList):
                    if not getattr(in_scheme, "identifier", None):
                        in_scheme.identifier = Skolemizer.add_skolemization()

                    _in_scheme = URIRef(in_scheme.identifier)

                    for _s, p, o in in_scheme._to_graph().triples((None, None, None)):
                        self._g.add((_s, p, o))

                elif isinstance(in_scheme, str):
                    _in_scheme = URIRef(in_scheme)

                self._g.add((_self, SKOS.inScheme, _in_scheme))

    def _top_concept_of_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "top_concept_of", None):

            for top_concept_of in self._top_concept_of:

                if isinstance(top_concept_of, CodeList):

                    if not getattr(top_concept_of, "identifier", None):
                        top_concept_of.identifier = Skolemizer.add_skolemization()

                    _top_concept_of = URIRef(top_concept_of.identifier)

                    for _s, p, o in top_concept_of._to_graph().triples(
                        (None, None, None)
                    ):
                        self._g.add((_s, p, o))

                elif isinstance(top_concept_of, str):
                    _top_concept_of = URIRef(top_concept_of)

                self._g.add((_self, SKOS.topConceptOf, _top_concept_of))

    def _altlabel_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "altlabel", None):

            for key in self.altlabel:
                self._g.add(
                    (_self, SKOS.altLabel, Literal(self.altlabel[key], lang=key),)
                )

    def _definition_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "definition", None):

            for key in self.definition:
                self._g.add(
                    (_self, SKOS.definition, Literal(self.definition[key], lang=key),)
                )

    def _example_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "example", None):

            for example in self.example:
                self._g.add((_self, SKOS.example, Literal(example)))

    def _hiddenlabel_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "hiddenlabel", None):

            for key in self.hiddenlabel:
                self._g.add(
                    (_self, SKOS.hiddenLabel, Literal(self.hiddenlabel[key], lang=key),)
                )

    def _note_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "note", None):

            for key in self.note:
                self._g.add((_self, SKOS.note, Literal(self.note[key], lang=key),))

    def _scopenote_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "scopenote", None):

            for key in self.scopenote:
                self._g.add(
                    (_self, SKOS.scopeNote, Literal(self.scopenote[key], lang=key),)
                )

    def _exclusion_note_to_graph(self, _self: URIRef) -> None:
        if getattr(self, "exclusion_note", None):

            for key in self.exclusion_note:
                self._g.add(
                    (
                        _self,
                        XKOS.exclusionNote,
                        Literal(self.exclusion_note[key], lang=key),
                    )
                )

    def _inclusion_note_to_graph(self, _self: URIRef) -> None:
        if getattr(self, "inclusion_note", None):

            for key in self.inclusion_note:
                self._g.add(
                    (
                        _self,
                        XKOS.inclusionNote,
                        Literal(self.inclusion_note[key], lang=key),
                    )
                )

    def _next_element_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "next_element", None):

            if isinstance(self.next_element, CodeElement):
                _next_element = (
                    URIRef(self.next_element.identifier)
                    if getattr(self.next_element, "identifier", None)
                    else BNode()
                )

                for _s, p, o in self.next_element._to_graph().triples(
                    (None, None, None)
                ):
                    self._g.add(
                        (_next_element, p, o)
                        if isinstance(_next_element, BNode)
                        else (_s, p, o)
                    )
            elif isinstance(self.next_element, str):
                _next_element = URIRef(self.next_element)

            self._g.add((_self, XKOS.next, _next_element))

    def _previous_element_to_graph(self, _self: URIRef) -> None:

        if getattr(self, "previous_element", None):

            if isinstance(self.previous_element, CodeElement):
                _previous_element = (
                    URIRef(self.previous_element.identifier)
                    if getattr(self.previous_element, "identifier", None)
                    else BNode()
                )

                for _s, p, o in self.previous_element._to_graph().triples(
                    (None, None, None)
                ):
                    self._g.add(
                        (_previous_element, p, o)
                        if isinstance(_previous_element, BNode)
                        else (_s, p, o)
                    )
            elif isinstance(self.previous_element, str):
                _previous_element = URIRef(self.previous_element)

            self._g.add((_self, XKOS.previous, _previous_element))


class Note(ModelProperty):
    """A class representing a modelldcatno:Note."""

    __slots__ = "_property_note"

    _property_note: dict
    _identifier: URI
    _g: Graph

    @property
    def property_note(self: Note) -> dict:
        """Get for property_note."""
        return self._property_note

    @property_note.setter
    def property_note(self: Note, property_note: dict) -> None:
        """Set for property_note."""
        self._property_note = property_note

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier
        super().__init__()

    def to_rdf(
        self: Note, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> bytes:
        """Maps the note to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format encoded as bytes.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(
        self: Note, type: str = MODELLDCATNO.Note, selfobject: URIRef = None,
    ) -> Graph:
        """Returns the role as graph.

        Args:
            type: type for identifying class. Default: MODELLDCATNO.Note
            selfobject: a URIRef passed from a subclass Default: None

        Returns:
            the role graph
        """
        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        _self = URIRef(self.identifier)

        super(Note, self)._to_graph(MODELLDCATNO.Note, _self)

        self._property_note_to_graph(_self)

        return self._g

    def _property_note_to_graph(self: Note, _self: URIRef) -> None:
        if getattr(self, "property_note", None):

            for key in self.property_note:
                self._g.add(
                    (
                        _self,
                        MODELLDCATNO.propertyNote,
                        Literal(self.property_note[key], lang=key),
                    )
                )
