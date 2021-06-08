"""Document module for mapping a document to rdf.

This module contains methods for mapping a document object to rdf
according to the
`dcat-ap-no v.2 standard <https://doc.difi.no/review/dcat-ap-no/#klasse-distribusjon>`__

Example:
    >>> from datacatalogtordf import Document
    >>> # Create a document:
    >>> document = Document()
    >>> document.identifier = "http://example.com/documents/1"
    >>> document.title = {"en": "The Python Language Reference Manual"}
"""
from __future__ import annotations

from typing import Optional

from datacatalogtordf import Document
from datacatalogtordf.uri import URI
from rdflib import DCTERMS, FOAF, Graph, Literal, Namespace, RDF, RDFS, URIRef
from skolemizer import Skolemizer


DCAT = Namespace("http://www.w3.org/ns/dcat#")


class FoafDocument(Document):
    """A class representing a foaf:Document.

    Attributes:
        identifier (URI): A URI uniquely identifying the document
        title (dict): A title given to the document. key is langauge code
        language (str): A reference to the language which is used in the document
        format (str): A link to a concept designating the type of the document
    """

    slots = ("_identifier", "_title", "_language", "_format")

    _identifier: URI
    _title: dict
    _language: str
    _type: str
    _format: str
    _rdfs_see_also: str

    def __init__(self, identifier: Optional[str] = None) -> None:
        """Inits an object with default values."""
        if identifier:
            self.identifier = identifier
        self._type = FOAF.Document

    @property
    def format(self: FoafDocument) -> str:
        """Get for format."""
        return self._format

    @format.setter
    def format(self: FoafDocument, format: str) -> None:
        """Set for format."""
        self._format = URI(format)

    @property
    def rdfs_see_also(self: FoafDocument) -> str:
        """Get for rdfs_see_also."""
        return self._rdfs_see_also

    @rdfs_see_also.setter
    def rdfs_see_also(self: FoafDocument, rdfs_see_also: str) -> None:
        """Set for rdfs_see_also."""
        self._rdfs_see_also = URI(rdfs_see_also)

    def to_rdf(
        self: FoafDocument, format: str = "turtle", encoding: Optional[str] = "utf-8"
    ) -> str:
        """Maps the document to rdf.

        Args:
            format: a valid format. Default: turtle
            encoding: the encoding to serialize into

        Returns:
            a rdf serialization as a bytes literal according to format.
        """
        return self._to_graph().serialize(format=format, encoding=encoding)

    def _to_graph(self: FoafDocument) -> Graph:

        self._g = Graph()
        self._g.bind("dct", DCTERMS)
        self._g.bind("foaf", FOAF)
        self._g.bind("rdfs", RDFS)

        if not getattr(self, "identifier", None):
            self.identifier = Skolemizer.add_skolemization()

        _self = URIRef(self.identifier)

        self._g.add((_self, RDF.type, FOAF.Document))

        if getattr(self, "title", None):
            for key in self.title:
                self._g.add((_self, DCTERMS.title, Literal(self.title[key], lang=key),))
        if getattr(self, "language", None):
            self._g.add(
                (
                    _self,
                    DCTERMS.language,
                    Literal(self.language, datatype=DCTERMS.LinguisticSystem),
                )
            )

        if getattr(self, "format", None):
            self._g.add(
                (
                    _self,
                    DCTERMS["format"],  # https://github.com/RDFLib/rdflib/issues/932
                    Literal(self.format, datatype=DCTERMS.MediaType),
                )
            )

        if getattr(self, "_rdfs_see_also", None):
            self._g.add((_self, RDFS.seeAlso, URIRef(self.rdfs_see_also)))

        return self._g
