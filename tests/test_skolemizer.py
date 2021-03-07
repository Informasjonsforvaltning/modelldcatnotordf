"""Test cases for the skolemizer module."""
import os

from modelldcatnotordf.modelldcatno import ObjectType
from modelldcatnotordf.modelldcatno import Skolemizer

"""
A test class for testing the class InformationModel.

"""


def test_add_skolemization() -> None:
    """Tests skolemization."""
    os.environ[
        Skolemizer.baseurl_key
    ] = "https://altinn-model-publisher.digdir.no/models/4985-5704/"

    modelelement = ObjectType()

    _classtype = modelelement.__class__.__name__

    skolemization1 = (
        "https://altinn-model-publisher.digdir.no/models/4985-5704/ObjectType/1"
    )

    skolemization2 = (
        "https://altinn-model-publisher.digdir.no/models/4985-5704/ObjectType/2"
    )

    assert not Skolemizer.is_exact_skolemization(skolemization1)
    assert skolemization1 == Skolemizer.add_skolemization(_classtype)
    assert Skolemizer.is_exact_skolemization(skolemization1)
    assert not Skolemizer.is_exact_skolemization(skolemization2)
    assert skolemization2 == Skolemizer.add_skolemization(_classtype)
    assert Skolemizer.is_exact_skolemization(skolemization2)


def test_has_skolemization_morfologi_success() -> None:
    """Tests skolemization morfologi."""
    os.environ[
        Skolemizer.baseurl_key
    ] = "https://altinn-model-publisher.digdir.no/models/4985-5704/"

    _skolemization = (
        "https://altinn-model-publisher.digdir.no/models/4985-5704/ObjectType/2"
    )

    assert Skolemizer.has_skolemization_morfologi(_skolemization)


def test_has_skolemization_morfologi_incorrect_identifier() -> None:
    """Tests skolemization morfologi."""
    os.environ[
        Skolemizer.baseurl_key
    ] = "https://altinn-model-publisher.digdir.no/models/4985-5704/"

    _skolemization = "https://someWrongIdentifier/ObjectType/2"

    assert not Skolemizer.has_skolemization_morfologi(_skolemization)


def test_has_skolemization_morfologi_incorrect_counter() -> None:
    """Tests skolemization morfologi."""
    os.environ[
        Skolemizer.baseurl_key
    ] = "https://altinn-model-publisher.digdir.no/models/4985-5704/"

    _skolemization = (
        "https://altinn-model-publisher.digdir.no/models/4985-5704/ObjectType/X"
    )

    assert not Skolemizer.has_skolemization_morfologi(_skolemization)


def test_has_skolemization_morfologi_incorrect_class() -> None:
    """Tests skolemization morfologi."""
    os.environ[
        Skolemizer.baseurl_key
    ] = "https://altinn-model-publisher.digdir.no/models/4985-5704/"

    _skolemization = "https://altinn-model-publisher.digdir.no/models/4985-5704/Foo/1"

    assert not Skolemizer.has_skolemization_morfologi(_skolemization)


def test_get_baseurl() -> None:
    """Tests the retrieving of the baseurl for skolemization."""
    if Skolemizer.baseurl_key in os.environ.keys():
        del os.environ[Skolemizer.baseurl_key]

    assert Skolemizer.get_baseurl() == Skolemizer.baseurl_default_value

    os.environ[Skolemizer.baseurl_key] = Skolemizer.baseurl_default_value

    assert Skolemizer.baseurl_key in os.environ
    assert os.environ[Skolemizer.baseurl_key] == Skolemizer.baseurl_default_value


def test_get_baseurl_not_valid_url() -> None:
    """Tests the retrieving of the baseurl for skolemization."""
    if Skolemizer.baseurl_key in os.environ.keys():
        del os.environ[Skolemizer.baseurl_key]

    os.environ[Skolemizer.baseurl_key] = Skolemizer.baseurl_default_value + "<>"

    assert Skolemizer.get_baseurl() == Skolemizer.baseurl_default_value


def test_get_baseurl_missing_slash_at_end() -> None:
    """Tests the retrieving of the baseurl for skolemization."""
    if Skolemizer.baseurl_key in os.environ.keys():
        del os.environ[Skolemizer.baseurl_key]

    os.environ[Skolemizer.baseurl_key] = Skolemizer.baseurl_default_value[:-1]

    assert Skolemizer.get_baseurl() == Skolemizer.baseurl_default_value
