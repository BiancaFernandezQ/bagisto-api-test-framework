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
                    "type": ["string", "null"]
                },
                "last": {
                    "type": ["string", "null"]
                },
                "prev": {
                    "type": ["string", "null"]
                },
                "next": {
                    "type": ["string", "null"]
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

GROUPS_BODY_PAGINATION_0 = {
    "type": "object",
    "required": [
        "data"
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
                        "type": [ "null", "string" ]
                    },
                    "updated_at": {
                        "type": [ "null", "string" ]
                    }
                },
                "required": [
                    "created_at",
                    "id",
                    "name",
                    "updated_at"
                ]
            }
        }
    }
}

GROUP_SCHEMA_IND = {
    "type": "object",
    "required": [
        "data"
    ],
    "properties": {
        "data": {
            "type": "object",
            "required": [
                "created_at",
                "id",
                "name",
                "updated_at"
            ],
            "properties": {
                "id": {
                    "type": "integer"
                },
                "name": {
                    "type": "string"
                },
                "created_at": {
                    "type": ["string", "null"]
                },
                "updated_at": {
                    "type": ["string", "null"]
                }
            }
        }
    }
}

CREATE_BODY_GROUP_SCHEMA = {
    "type": "object",
    "required": [
        "data",
        "message"
    ],
    "properties": {
        "data": {
            "type": "object",
            "required": [
                "created_at",
                "id",
                "name",
                "updated_at"
            ],
            "properties": {
                "id": {
                    "type": "integer"
                },
                "name": {
                    "type": ["string", "integer"]
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
        }
    }
}

GROUPS_PAYLOAD_SCHEMA = {
    "type": "object",
    "required": [
        "code",
        "name"
    ],
    "properties": {
        "code": {
            "type": "string"
        },
        "name": {
            "type": ["string", "integer"]
        }
    }
}




