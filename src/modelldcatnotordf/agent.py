"""Agent module for mapping a model to rdf.

This module contains methods for mapping a agent object to rdf
for use in the modelldcat-ap-no specification._

Refer to sub-class for typical usage examples.
"""
from typing import Optional

from datacatalogtordf import URI
from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef

FOAF = Namespace("http://xmlns.com/foaf/0.1/")


class Agent(BNode):
    """A class representing a foaf:Agent."""

    __slots__ = ("_g", "_identifier", "_name", "_type")

    _g: Graph
    _identifier: URI
    _name: str

    def __init__(self) -> None:
        """Inits Agent object with default values."""
        self._type = FOAF.Agent

    @property
    def identifier(self) -> str:
        """Get/set for identifier."""
        return self._identifier

    @identifier.setter
    def identifier(self, identifier: str) -> None:
        self._identifier = URI(identifier)

    @property
    def name(self) -> str:
        """Get/set for name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    def to_rdf(
        self: BNode, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> str:
        """Maps the agent to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(self: BNode) -> Graph:
        self._g = Graph()
        self._g.bind("foaf", FOAF)

        self._g.add((URIRef(self._identifier), RDF.type, URIRef(self._type)))
        self._name_to_graph()

        return self._g

    def _name_to_graph(self: BNode) -> None:
        if getattr(self, "name", None):
            self._g.add((URIRef(self.identifier), FOAF.name, Literal(self._name)))
