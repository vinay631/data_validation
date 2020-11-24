import pytest

from pydandict.validation_functions import (
    validate_latitude,
    validate_longitude,
    validate_zipcode
)

def test_validate_latitude():
    latitude = 10
    assert latitude == validate_latitude(latitude)

    latitude = -1000
    with pytest.raises(AssertionError):
        validate_latitude(latitude)

def test_validate_longitude():
    longitude = 10
    assert longitude == validate_longitude(longitude)

    longitude = -1000
    with pytest.raises(AssertionError):
        validate_longitude(longitude)

def test_validate_zipcode():
    zipcode = '10025'
    assert zipcode == validate_zipcode(zipcode)

    zipcode = 'abcd'
    with pytest.raises(AssertionError):
        validate_zipcode(zipcode)