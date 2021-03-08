"""Module for performing Skolemization on blank nodes."""
import os
import uuid

from datacatalogtordf import URI


class Skolemizer:
    """A class for performing skolemization."""

    skolemization: dict = {}
    baseurl_key = "modelldcatno_baseurl"
    baseurl_default_value = "http://wwww.digdir.no/"

    @staticmethod
    def is_exact_skolemization(skolemization: URI) -> bool:
        """Returns true if the URI is a skolemization that exists in the model."""
        return skolemization in Skolemizer.skolemization

    @staticmethod
    def has_skolemization_morfologi(skolemization: URI) -> bool:
        """Checks if the URI complies to a skolemized form.

        Args:
            skolemization (URI): the URI to check.

        Returns:
            True if URI complies to skolemized form.
        """
        if not Skolemizer._is_valid_uri(skolemization):
            return False

        return skolemization.startswith(
            Skolemizer.get_baseurl() + ".well-known/skolem/"
        )

    @staticmethod
    def add_skolemization() -> URI:
        """Creates a skolemization for the given classtype."""
        _skolemization = (
            Skolemizer.get_baseurl() + ".well-known/skolem/" + str(uuid.uuid4())
        )

        Skolemizer.skolemization[_skolemization] = True

        return _skolemization

    @staticmethod
    def get_baseurl() -> str:
        """Returns baseurl for skolemization."""
        _baseurl = (
            os.environ[Skolemizer.baseurl_key]
            if Skolemizer.baseurl_key in os.environ.keys()
            else Skolemizer.baseurl_default_value
        )

        if not Skolemizer._is_valid_uri(_baseurl):
            _baseurl = Skolemizer.baseurl_default_value

        if not _baseurl.endswith("/"):
            _baseurl = _baseurl + "/"

        return _baseurl

    @staticmethod
    def _is_valid_uri(uri: str) -> bool:
        """Perform basic validation of link."""
        _invalid_uri_chars = '<>" {}|\\^`'

        for c in _invalid_uri_chars:
            if c in uri:
                return False
        return True
