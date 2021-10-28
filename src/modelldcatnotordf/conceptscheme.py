"""Module for mapping a ConceptScheme to rdf.

This module contains methods for mapping to rdf
according to the modelldcat-ap-no specification.


"""
from __future__ import annotations

from typing import Optional

from datacatalogtordf import URI
from rdflib import DCTERMS, Graph, Literal, RDF, SKOS, URIRef
from skolemizer import Skolemizer


class ConceptScheme:
    """A class representing a skos:ConceptScheme."""

    __slots__ = ("_g", "_identifier", "_title")

    _g: Graph
    _identifier: URI
    _title: dict

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits ConceptScheme object with default values."""
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

    def to_rdf(self, format: str = "turtle", encoding: Optional[str] = "utf-8") -> str:
        """Maps the concept scheme to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(self) -> Graph:
        """Returns the concept scheme as graph.

        Returns:
            the concept scheme graph
        """
        self._g = Graph()
        self._g.bind("skos", SKOS)

        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        _self = URIRef(self.identifier)

        self._g.add((_self, RDF.type, SKOS.ConceptScheme))

        if getattr(self, "title", None):
            for key in self.title:
                self._g.add((_self, DCTERMS.title, Literal(self.title[key], lang=key),))

        return self._g
