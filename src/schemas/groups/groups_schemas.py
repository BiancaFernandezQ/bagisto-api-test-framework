GROUPS_SCHEMA_BODY = {
"type": "object",
    "required": [
        "data",
        "meta"
    ],
    "properties": {
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {
                        "type": "integer"
                    },
                    "name": {
                        "type": "string"
                    },
                    "created_at": {
                        "type": [
                            "null",
                            "string"
                        ]
                    },
                    "updated_at": {
                        "type": [
                            "null",
                            "string"
                        ]
                    }
                },
                "required": [
                    "created_at",
                    "id",
                    "name",
                    "updated_at"
                ]
            }
        },
        "links": {
            "type": "object",
            "properties": {
                "first": {
                    "type": "string"
                },
                "last": {
                    "type": "string"
                },
                "prev": {
                    "type": "null"
                },
                "next": {
                    "type": "null"
                }
            }
        },
        "meta": {
            "type": "object",
            "properties": {
                "current_page": {
                    "type": "integer"
                },
                "from": {
                    "type": ["integer", "null"]
                },
                "last_page": {
                    "type": ["integer", "null"]
                },
                "links": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": [ "null", "string"]
                            },
                            "label": {
                                "type": "string"
                            },
                            "active": {
                                "type": "boolean"
                            }
                        },
                        "required": [
                            "active",
                            "label",
                            "url"
                        ]
                    }
                },
                "path": {
                    "type": "string"
                },
                "per_page": {
                    "type": ["integer", "null"]
                },
                "to": {
                    "type": "integer"
                },
                "total": {
                    "type": "integer"
                }
            }
        }
    }
}