from jsonschema import validate
from jsonschema.exceptions import ValidationError
from jsonschema.exceptions import SchemaError

userHistory_schema = {
    "title": "The bookmark schema",
    "type": "object",
    "properties": {
        "emailId": {
            "type": "string"
        },
        "isDeleted": {
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
        "bookmarks" : {
            "type" : "array",
            "bookmarkId" : {
                "type": "string"
            }
        },
        "searches" : {
            "type" : "array",
            "searchId" : {
                "type": "string"
            }
        }
    },
    "required" : ["emailId"],
    "additionalProperties": False
}

def validate_userHistory(data):
    try:
        validate(data, userHistory_schema)
    except ValidationError as e:
        return {'ok': False, 'message': e}
    except SchemaError as e:
        return {'ok': False, 'message': e}
    return {'ok': True, 'data': data}