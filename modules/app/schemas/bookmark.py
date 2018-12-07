from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

bookmark_schema = {
    "title": "The bookmark Schema",
    "type": "object",
    "properties": {
        "emailId": {
            "type": "string"
        },
        "name" : {
            "type": "string"
        },
        "service" : {
            "type": "string"
        },
        "url" : {
            "type": "string",
            "format": "url"
        },
        "platform" : { 
            "type" : "string",
            "length": 4
        },
        "public" : {
            "type" : "boolean"
        },
        "active" : {
            "type" : "boolean"
        },
        "dateCreated" : {
            "type": "string",
            "format": "date-time"
        },
        "dateUpdated" : {
            "type": "string",
            "format": "date-time"
        },
        "dateDeleted" : {
            "type": "string",
            "format": "date-time"
        },
        "visitCounter" : {
            "type": "integer"
        },
        "history" : {
            "type" : "array",
            "date" : {
                "type": "string",
                "format": "date-time"
            }
        }
    },
    "required" : ["emailId", "service"],
    "additionalProperties": False
}

def validate_bookmark(data):
    try:
        validate(data, bookmark_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}