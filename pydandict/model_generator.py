"""
This module has functions/utilities to generate pydantic models
from schema yaml file.
"""
import copy
import logging

from . import validation_functions

from typing import Any, Dict, List
from pydantic import BaseModel, Field, create_model, validator
import yaml


def read_schema(file_path: str) -> Dict[str, Any]:
    """
    Read yaml file into dictionary.

    Args:
        filepath (str): Path to yaml schema file.

    Returns:
        Dict[str, Any]: Schema in yaml form
    """
    data = None
    with open(file_path) as fhandler:
        data = yaml.load(fhandler, Loader=yaml.FullLoader)

    return data

def get_fields_and_validators(column_dict_list: List[Dict[str, Any]]) -> Dict[str, Field]:
    """
    Create a list of pydantic field objects.

    Args:
        column_dict_list (Dict): List of column attributes.

    Returns:
        Dict[str, Field]: Returns a dict of fieldname -> Field obj and
        validators -> validator funcs.
    """
    field_validator_dict:Dict[str, Any] = {}
    print(field_validator_dict)
    
    field_validator_dict['fields'] = {}
    field_validator_dict['validators'] = {}

    for column_dict in column_dict_list:
        field_name = column_dict.get('name')
        default_value = column_dict.get('default_value')
        field_validator_dict['fields'][field_name] = Field(default_value)

        validation_func = column_dict.get("validator")
        if validation_func:
            if hasattr(validation_functions, validation_func):
                func = getattr(validation_functions, validation_func)
                validator_dict = {
                    f'{field_name}_validator':  validator(f'{field_name}', allow_reuse=True)(func)
                }
                field_validator_dict['validators'].update(validator_dict)
            else:
                err_msg = (
                    f"Please implement the validation function {validation_func} "
                    "in validation_functions module."
                )
                raise NotImplementedError(err_msg)

    return field_validator_dict

def validate_schema_dict(schema_dict:Dict[str, Any]) -> bool:
    """
    This method validates the schema of dictionary created from yaml.
    TODO: Implement this.
    Args:
        schema_dic (Dict): dictionary to be validated.
    Returns:
        bool: True if schema is valid, else false
    """
    return True

def create_model_from_yaml(file_path: str) -> BaseModel:
    """
    This method reads a yaml data dictionary and creates a pydantic
    model which can be used to validate a pandas dataframe or list of dicts.

    Args:
        file_path (str): Path to file location.
    Returns:
        BaseModel: Pydantic model.
    """
    try:
        schema_dict = read_schema(file_path)
    except Exception as excpt:
        logging.error(f'File probably not found at {file_path}')
        raise excpt

    if not validate_schema_dict(schema_dict):
        raise Exception("Schema is not valid")

    schema = schema_dict.get('schema')
    model_name = schema['name']

    column_dict_list = schema['columns']
    fields_validators_dict = get_fields_and_validators(column_dict_list)
    fields_dict = fields_validators_dict['fields']
    validators_dict = fields_validators_dict['validators']

    model = create_model(model_name,
                **fields_dict,
                __validators__=validators_dict)

    return model
