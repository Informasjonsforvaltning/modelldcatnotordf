"""Property module for mapping a property to rdf.

This module contains methods for mapping a property object to rdf
for use in the modelldcat-ap-no specification._

Refer to sub-class for typical usage examples.
"""
from typing import List, Optional

from datacatalogtordf import URI
from rdflib import BNode, Graph, Namespace, RDF, URIRef

from modelldcatnotordf.modelelement import ModelElement

MODELLDCATNO = Namespace("https://data.norge.no/vocabulary/modelldcatno#")
DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


class Property:
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

        self._g.add((_self, RDF.type, URIRef(self._type)))

        return self._g
