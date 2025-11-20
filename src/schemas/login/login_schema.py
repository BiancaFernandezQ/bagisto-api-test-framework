LOGIN_SUCCESS_SCHEMA ={
    "type": "object",
    "required": [
        "data",
        "message",
        "token"
    ],
    "properties": {
        "data": {
            "type": "object",
            "required": [
                "created_at",
                "email",
                "id",
                "name",
                "role",
                "status",
                "updated_at"
            ],
            "properties": {
                "id": {
                    "type": "integer"
                },
                "name": {
                    "type": "string"
                },
                "email": {
                    "type": "string"
                },
                "status": {
                    "type": "integer"
                },
                "role": {
                    "type": "object",
                    "required": [
                        "created_at",
                        "description",
                        "id",
                        "name",
                        "permission_type",
                        "permissions",
                        "updated_at"
                    ],
                    "properties": {
                        "id": {
                            "type": "integer"
                        },
                        "name": {
                            "type": "string"
                        },
                        "description": {
                            "type": "string"
                        },
                        "permission_type": {
                            "type": "string"
                        },
                        "permissions": {
                            "type": "null"
                        },
                        "created_at": {
                            "type": "null"
                        },
                        "updated_at": {
                            "type": "null"
                        }
                    }
                },
                "created_at": {
                    "type": "string"
                },
                "updated_at": {
                    "type": "string"
                }
            }
        },
        "message": {
            "type": "string"
        },
        "token": {
            "type": "string"
        }
    }
}

LOGIN_ERROR_SCHEMA ={
    "type": "object",
    "required": [
        "errors",
        "message"
    ],
    "properties": {
        "message": {
            "type": "string"
        },
        "errors": {
            "type": "object",
            "properties": {
                "email": {
                    "type": ["array","null"],
                    "items": {
                        "type": "string"
                    }
                },
                "password": {
                    "type": ["array","null"],
                    "items": {
                        "type": ["string", "null"]
                    }
                }
            }
        }
    }
}

LOGIN_EMAIL_INVALID_SCHEMA ={
    "type": "object",
    "required": [
        "errors",
        "message"
    ],
    "properties": {
        "message": {
            "type": "string"
        },
        "errors": {
            "type": "object",
            "required": [
                "email"
            ],
            "properties": {
                "email": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        }
    }
}

LOGIN_CREDENTIALS_INCORRECT_SCHEMA = {
    "type": "object",
    "required": [
        "errors",
        "message"
    ],
    "properties": {
        "message": {
            "type": "string"
        },
        "errors": {
            "type": "object",
            "required": [
                "email"
            ],
            "properties": {
                "email": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            }
        }
    }
}