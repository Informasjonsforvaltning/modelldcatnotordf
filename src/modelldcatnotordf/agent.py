"""Agent module for mapping a model to rdf.

This module contains methods for mapping a agent object to rdf
for use in the modelldcat-ap-no specification._

Refer to sub-class for typical usage examples.
"""
from typing import Optional

from datacatalogtordf import URI
from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef

FOAF = Namespace("http://xmlns.com/foaf/0.1/")
DCT = Namespace("http://purl.org/dc/terms/")
OWL = Namespace("http://www.w3.org/2002/07/owl#")


class Agent:
    """A class representing a foaf:Agent."""

    __slots__ = ("_g", "_identifier", "_name", "_type", "_orgnr", "_sameas")

    _g: Graph
    _identifier: URI
    _name: str
    _orgnr: str
    _sameas: URI

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

    @property
    def orgnr(self) -> str:
        """Get/set for orgnr."""
        return self._orgnr

    @orgnr.setter
    def orgnr(self, value: str) -> None:
        self._orgnr = value

    @property
    def sameas(self) -> str:
        """Get/set for sameas."""
        return self._sameas

    @sameas.setter
    def sameas(self, value: str) -> None:
        self._sameas = value

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
        return self.to_graph().serialize(format=format, encoding=encoding)

    def to_graph(self: BNode) -> Graph:
        """Returns the agent as graph.

        Returns:
            the agent graph
        """
        self._g = Graph()
        self._g.bind("foaf", FOAF)

        self._g.add((URIRef(self.identifier), RDF.type, URIRef(self._type)))
        self._name_to_graph()
        self._orgnr_to_graph()
        self._sameas_to_graph()

        return self._g

    def _name_to_graph(self: BNode) -> None:
        if getattr(self, "name", None):
            self._g.add((URIRef(self.identifier), FOAF.name, Literal(self._name)))

    def _orgnr_to_graph(self: BNode) -> None:
        if getattr(self, "orgnr", None):
            self._g.add((URIRef(self.identifier), DCT.identifier, Literal(self._orgnr)))

    def _sameas_to_graph(self: BNode) -> None:
        if getattr(self, "sameas", None):
            self._g.add((URIRef(self.identifier), OWL.sameAs, (URIRef(self._sameas))))
