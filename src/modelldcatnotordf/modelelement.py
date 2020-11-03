"""Model element module for mapping a model element to rdf.

This module contains methods for mapping a model element object to rdf
for use in the modelldcat-ap-no specification._

Refer to sub-class for typical usage examples.
"""
from rdflib import Namespace

MODELLDCATNO = Namespace("https://data.norge.no/vocabulary/modelldcatno#")
DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")


class ModelElement:
    """A class representing a modelldcatno:ModelElement."""

    pass
