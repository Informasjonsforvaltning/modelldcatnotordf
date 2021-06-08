"""Module for mapping a LicenseDocument to rdf.

This module contains methods for mapping to rdf
according to the modelldcat-ap-no specification._

Refer to sub-class for typical usage examples.
"""
from __future__ import annotations

from typing import List, Optional, Union

from concepttordf import Concept
from datacatalogtordf import URI
from rdflib import Graph, Namespace, RDF, URIRef
from skolemizer import Skolemizer


DCT = Namespace("http://purl.org/dc/terms/")


class LicenseDocument:
    """A class representing a dct:LicenseDocument."""

    __slots__ = ("_g", "_identifier", "_type")

    _g: Graph
    _identifier: URI
    _type: List[Union[Concept, URI]]

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits LicenseDocument object with default values."""
        if identifier:
            self.identifier = identifier
        self._type = []

    @property
    def type(self: LicenseDocument) -> List[Union[Concept, URI]]:
        """Get for type."""
        return self._type

    @property
    def identifier(self) -> str:
        """Get for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str) -> None:
        self._identifier = URI(identifier)

    def to_rdf(self, format: str = "turtle", encoding: Optional[str] = "utf-8") -> str:
        """Maps the license document to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(self) -> Graph:
        """Returns the license document as graph.

        Returns:
            the license document graph
        """
        self._g = Graph()
        self._g.bind("dct", DCT)

        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        _self = URIRef(self.identifier)

        self._g.add((_self, RDF.type, DCT.LicenseDocument))

        if getattr(self, "type", None):

            for type in self._type:

                if isinstance(type, Concept):
                    _type = URIRef(type.identifier)

                    for _s, p, o in type._to_graph().triples((None, None, None)):
                        self._g.add((_type, p, o))

                elif isinstance(type, str):
                    _type = URIRef(type)

                self._g.add((_self, DCT.type, _type,))

        return self._g
