"""InformationModel module for mapping a model to rdf.

This module contains methods for mapping a model object to rdf
according to the modelldcat-ap-no specification._

Refer to sub-class for typical usage examples.
"""
from typing import List, Optional
from datacatalogtordf import Resource
from rdflib import Graph, Namespace, RDF, URIRef

DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
PROV = Namespace("http://www.w3.org/ns/prov#")
MODELLDCATNO = Namespace("https://data.norge.no/vocabulary/modelldcatno#")

class InformationModel(Resource):
    """A class representing a modelldatno:InformationModel."""

    __slots__ = (
        "_title",
        "_type",
    )

    _title: DCAT.title
    _type: DCAT.Resource

    def __init__(self) -> None:
        """Inits InformationModel object with default values."""
        #self._type = MODELLDCATNO.InformationModel
        self._type = DCAT.Resource
        super().__init__()

    @property
    def type(self) -> DCAT.Resource:
        """Get/set for title."""
        return self._type

    @property
    def title(self) -> DCAT.Resource:
        """Get/set for title."""
        return self._title

    def to_rdf(
        self: Resource,
        format: str = "turtle",
        encoding: Optional[str] = "utf-8",
    ) -> str:
        """Maps the catalog to rdf.

        Available formats:
         - turtle (default)
         - xml
         - json-ld

        Args:
            format (str): a valid format.
            encoding (str): the encoding to serialize into
            include_datasets (bool): includes the dataset graphs in the catalog
            include_services (bool): includes the services in the catalog

        Returns:
            a rdf serialization as a string according to format.
        """
        return self._to_graph().serialize(
            format=format, encoding=encoding
        )

    # -

    def _to_graph(
        self: Resource
    ) -> Graph:
        super(InformationModel, self)._to_graph()

        self._g.add((URIRef(self.identifier), RDF.type, self._type))


        return self._g

    @title.setter
    def title(self, value):
        self._title = value