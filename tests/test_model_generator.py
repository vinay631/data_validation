from pathlib import Path

import pytest

from pydandict.model_generator import (
    read_schema,
    get_fields_and_validators,
    validate_schema_dict,
    create_model_from_yaml
)

BASE_PATH = Path(__file__).parent
TEST_FILE_1 = (BASE_PATH / "schema_test1.yml").resolve()

def test_read_schema():
    assert read_schema(TEST_FILE_1) == {
        'schema': {
            'columns': [{
                'default_value': 90,
                'description': 'Latitude goes here',
                'name': 'latitude',
                'validator': 'validate_latitude'}],
                'name': 'some_schema'}
    }
    
def test_get_fields_and_validators():
    column_dict_list_1 = [
        {
            'name': 'latitude',
            'description': 'Latitude goes here',
            'default_value': 90,
            'validator': 'validate_latitude'
        },
        {
            'name': 'zipcode',
            'description': 'Zip code of something',
            'default_value': 'None',
            'validator': 'validate_zipcode'
        }
    ]

    fields_validators = get_fields_and_validators(column_dict_list_1)
    fields = fields_validators['fields']
    
    assert str(fields['latitude']) == 'default=90 extra={}'

    column_dict_list_2 = [
        {
            'name': 'zipcode',
            'description': 'Latitude goes here',
            'default_value': 90,
            'validator': 'validate_wrong_method'
        }
    ]
    with pytest.raises(NotImplementedError):
        fields_validators = get_fields_and_validators(column_dict_list_2)

def test_validate_schema_dict():
    assert validate_schema_dict({})

def test_create_model_from_yaml():
    model = create_model_from_yaml(TEST_FILE_1)

    assert model.schema() == {
        'title': 'some_schema',
        'type': 'object',
        'properties': {
            'latitude': {
                'title': 'Latitude',
                'default': 90,
                'type': 'integer'
            }
        }
    }
    
    with pytest.raises(FileNotFoundError):
        create_model_from_yaml('fake_path')
