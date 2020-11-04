"""Property module for mapping a property to rdf.

This module contains methods for mapping a property object to rdf
for use in the modelldcat-ap-no specification._

Refer to sub-class for typical usage examples.
"""

from datacatalogtordf import URI
from rdflib import Graph, Namespace

MODELLDCATNO = Namespace("https://data.norge.no/vocabulary/modelldcatno#")
DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


class Property:
    """A class representing a modelldcatno:Property."""

    __slots__ = ("_type", "_g", "_title", "_identifier")

    _g: Graph
    _identifier: URI

    def __init__(self) -> None:
        """Inits an object with default values."""
        self._type = MODELLDCATNO.Property
