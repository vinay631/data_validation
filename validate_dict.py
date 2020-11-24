"""
Provides a method to validate a dict given a pydantic model.
"""

from pydantic import BaseModel, ValidationError, parse_obj_as
from typing import Any, Dict, List
from pydandict.model_generator import create_model_from_yaml

def validate_data(data_dict: Dict[str, Any], model: BaseModel) -> bool:
    """
    Validates data in list of dict based on pydantic model.
    """
    try:
        data = parse_obj_as(List[model], data_dict)
    except ValidationError as excp:
        print(excp)
        raise excp

    return True

if __name__ == "__main__":
    data = [
        {'latitude': 60, 'longitude': -100, 'zipcode': '02474'},
        {'latitude': 70, 'longitude': -100, 'zipcode': '02478'},
    ]
    SCHEMA_FILE = 'schema_example.yml'
    data_model = create_model_from_yaml(SCHEMA_FILE)
    validate_data(data, data_model)
