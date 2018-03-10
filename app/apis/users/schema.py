"""
Schema definition for users APIs request payload
"""

register_user = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "email": {"type": "string", "minLength": 1},
        "password": {"type": "string", "minLength": 1}
    },
    "additionalProperties": False,
    "required": ["name", "email", "password"]
}

update_user = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 1},
        "password": {"type": "string", "minLength": 1}
    },
    "additionalProperties": False,
}

login_user = {
    "type": "object",
    "properties": {
        "email": {"type": "string", "minLength": 1},
        "password": {"type": "string", "minLength": 1}
    },
    "additionalProperties": False,
    "required": ["email", "password"]
}
