"""InformationModel module for mapping a model to rdf.

This module contains methods for mapping a model object to rdf
according to the modelldcat-ap-no specification._

Refer to sub-class for typical usage examples.
"""
from rdflib import Namespace


DCT = Namespace("http://purl.org/dc/terms/")
DCAT = Namespace("http://www.w3.org/ns/dcat#")
ODRL = Namespace("http://www.w3.org/ns/odrl/2/")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")
PROV = Namespace("http://www.w3.org/ns/prov#")
MODELLDCATNO = Namespace("https://data.norge.no/vocabulary/modelldcatno#")


class InformationModel:
    """A class representing a modelldatno:InformationModel."""

    pass
