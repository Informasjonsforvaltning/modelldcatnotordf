"""InformationModel module for mapping a model to rdf.

This module contains methods for mapping a model object to rdf
according to the modelldcat-ap-no specification._

Refer to sub-class for typical usage examples.
"""
from typing import List, Optional

from datacatalogtordf import Agent, Resource, URI
from rdflib import BNode, Graph, Namespace, RDF, URIRef

from modelldcatnotordf.modelelement import ModelElement

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
