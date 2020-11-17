"""InformationModel module for mapping a model to rdf.

This module contains methods for mapping a model object to rdf
according to the modelldcat-ap-no specification._

Refer to sub-class for typical usage examples.
"""
from typing import List, Optional

from datacatalogtordf import Resource
from rdflib import Graph, Namespace, RDF, URIRef

from modelldcatnotordf.agent import Agent


DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
PROV = Namespace("http://www.w3.org/ns/prov#")
MODELLDCATNO = Namespace("https://data.norge.no/vocabulary/modelldcatno#")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")


class InformationModel(Resource):
    """A class representing a modelldatno:InformationModel."""

    __slots__ = ("_title", "_type", "_description", "_theme", "_publisher")

    _title: dict
    _publisher: Agent

    def __init__(self) -> None:
        """Inits InformationModel object with default values."""
        super().__init__()
        self._type = MODELLDCATNO.InformationModel

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

    def unionof(self: Resource, graph: Graph) -> Graph:
        """Creates a graph union of itself and argument graph.

        Args:
            graph (Graph): a rdf-lib graph

        Returns:
            a graph union of itself and argument graph in rdf-lib-format
        """
        union = self._g + graph
        return union

    # -

    def _to_graph(self: Resource) -> Graph:

        super(InformationModel, self)._to_graph()

        self._g.add((URIRef(self.identifier), RDF.type, self._type))

        self._publisher_to_graph()

        return self._g

    def _publisher_to_graph(self: Resource) -> None:
        if getattr(self, "publisher", None):
            self._g.add(
                (
                    URIRef(self.identifier),
                    DCT.publisher,
                    URIRef(self.publisher.identifier),
                )
            )
            self._g = self.unionof(self.publisher.to_graph())
