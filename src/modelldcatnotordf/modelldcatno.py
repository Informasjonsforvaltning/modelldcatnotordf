"""Modelldcatno module for mapping a Modelldcatno model to rdf.

This module contains methods for mapping to rdf
according to the modelldcat-ap-no specification._

Refer to sub-class for typical usage examples.
"""
from __future__ import annotations

from typing import Any, List, Optional

from datacatalogtordf import Agent, Resource, URI
from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef

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
    )

    _title: dict
    _publisher: Agent
    _subject: List[str]
    _modelelements: List[ModelElement]

    def __init__(self) -> None:
        """Inits InformationModel object with default values."""
        super().__init__()
        self._type = MODELLDCATNO.InformationModel
        self._subject = []
        self._modelelements = []

    @property
    def type(self) -> str:
        """Get for type."""
        return self._type

    @property
    def title(self) -> dict:
        """Get/set for title."""
        return self._title

    @title.setter
    def title(self, value: dict) -> None:
        self._title = value

    @property
    def description(self) -> dict:
        """Get/set for description."""
        return self._description

    @description.setter
    def description(self, value: dict) -> None:
        self._description = value

    @property
    def theme(self) -> List[str]:
        """Get/set for theme."""
        return self._theme

    @theme.setter
    def theme(self, value: List[str]) -> None:
        self._theme = value

    @property
    def publisher(self: Resource) -> Agent:
        """Get/set for publisher."""
        return self._publisher

    @publisher.setter
    def publisher(self: Resource, publisher: Agent) -> None:
        self._publisher = publisher

    @property
    def subject(self: Resource) -> URI:
        """Get/set for subject."""
        return self._subject

    @property
    def modelelements(self: Resource) -> List[ModelElement]:
        """Get/set for modelelements."""
        return self._modelelements

    def to_rdf(
        self: Resource, format: str = "turtle", encoding: Optional[str] = "utf-8",
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

    def _to_graph(self: Resource) -> Graph:

        super(InformationModel, self)._to_graph()

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        self._publisher_to_graph()
        self._subject_to_graph()
        self._modelelements_to_graph()

        return self._g

    def _subject_to_graph(self: Resource) -> None:
        if getattr(self, "subject", None):
            for subject in self._subject:
                self._g.add((URIRef(self.identifier), SKOS.Concept, URIRef(subject)))

    def _modelelements_to_graph(self: Resource) -> None:

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


class ModelElement:
    """A class representing a modelldcatno:ModelElement."""

    __slots__ = ("_type", "_g", "_title", "_identifier", "_has_property")

    _g: Graph
    _title: dict
    _identifier: URI

    _has_property: List[ModelProperty]

    def __init__(self) -> None:
        """Inits an object with default values."""
        self._type = MODELLDCATNO.ModelElement
        self._g = Graph()
        self._g.bind("modelldcatno", MODELLDCATNO)
        self._g.bind("dct", DCT)
        self._g.bind("dcat", DCAT)

    @property
    def identifier(self) -> str:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str) -> None:
        self._identifier = URI(identifier)

    @property
    def title(self) -> dict:
        """Title attribute."""
        return self._title

    @title.setter
    def title(self, title: dict) -> None:
        self._title = title

    def to_rdf(self, format: str = "turtle", encoding: Optional[str] = "utf-8") -> str:
        """Maps the modelelement to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(self) -> Graph:
        """Returns the modelelement as graph.

        Returns:
            the modelelement graph
        """
        if getattr(self, "identifier", None):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        self._g.add((_self, RDF.type, MODELLDCATNO.ModelElement))

        if getattr(self, "title", None):
            for key in self.title:
                self._g.add((_self, DCT.title, Literal(self.title[key], lang=key),))

        return self._g


class ModelProperty:
    """A class representing a modelldcatno:Property."""

    __slots__ = ("_type", "_g", "_title", "_identifier", "_has_type")

    _g: Graph
    _identifier: URI
    _has_type: List[ModelElement]

    def __init__(self) -> None:
        """Inits an object with default values."""
        self._type = MODELLDCATNO.Property
        self._has_type = []
        self._g = Graph()
        self._g.bind("modelldcatno", MODELLDCATNO)

    @property
    def has_type(self) -> List[ModelElement]:
        """Get/set for has_type."""
        return self._has_type

    @property
    def identifier(self) -> str:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str) -> None:
        self._identifier = URI(identifier)

    def to_rdf(self, format: str = "turtle", encoding: Optional[str] = "utf-8") -> str:
        """Maps the property to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(self) -> Graph:
        """Returns the property as graph.

        Returns:
            the property graph
        """
        if getattr(self, "identifier", None):
            _self = URIRef(self.identifier)
        else:
            _self = BNode()

        self._g.add((_self, RDF.type, MODELLDCATNO.Property))

        self._has_type_to_graph(_self)

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
