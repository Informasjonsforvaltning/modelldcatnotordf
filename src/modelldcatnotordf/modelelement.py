"""Model element module for mapping a model element to rdf.

This module contains methods for mapping a model element object to rdf
for use in the modelldcat-ap-no specification._

Refer to sub-class for typical usage examples.
"""
from typing import Optional

from datacatalogtordf import URI
from rdflib import BNode, Graph, Literal, Namespace, RDF, URIRef

MODELLDCATNO = Namespace("https://data.norge.no/vocabulary/modelldcatno#")
DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


class ModelElement:
    """A class representing a modelldcatno:ModelElement."""

    __slots__ = ("_type", "_g", "_title", "_identifier")

    _g: Graph
    _title: dict
    _identifier: URI

    def __init__(self) -> None:
        """Inits an object with default values."""
        self._type = MODELLDCATNO.ModelElement
        self._g = Graph()
        self._g.bind("modelldcatno", MODELLDCATNO)

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

        self._g.add((_self, RDF.type, URIRef(self._type)))

        self._title_to_graph()

        return self._g

    def _title_to_graph(self) -> None:
        if getattr(self, "title", None):

            if getattr(self, "identifier", None):
                _self = URIRef(self.identifier)
            else:
                _self = BNode()

            for key in self.title:
                self._g.add((_self, DCT.title, Literal(self.title[key], lang=key),))
