"""
This module has the validation functions for pydantic models.
"""

import re

def validate_latitude(val):
    """
    This method validates latitude.
    """
    assert -90 <= val <= 90
    return val

def validate_longitude(val):
    """
    This method validates longitude.
    """
    assert -180 <= val <= 180
    return val

def validate_zipcode(val):
    """
    This method checks if the zipcode is valid.
    """
    regex_str = '^\\d{5}(?:[-\\s]\\d{4})?$'
    zipcode_regex = re.compile(regex_str)
    zipcode_match = zipcode_regex.fullmatch(val)

    assert zipcode_match

    return val
