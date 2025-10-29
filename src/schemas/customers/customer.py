CUSTOMER_SCHEMA = {
   "type": "object",
    "required": [
        "data",
        "links",
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
                    "email": {
                        "type": "string"
                    },
                    "name": {
                        "type": "string"
                    },
                    "first_name": {
                        "type": "string"
                    },
                    "last_name": {
                        "type": "string"
                    },
                    "gender": {
                        "type": "string"
                    },
                    "date_of_birth": {
                        "type": "string"
                    },
                    "phone": {
                        "type": "string"
                    },
                    "status": {
                        "type": "integer"
                    },
                    "group": {
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
                    },
                    "notes": {
                        "type": "array"
                    },
                    "created_at": {
                        "type": "string"
                    },
                    "updated_at": {
                        "type": "string"
                    }
                },
                "required": [
                    "date_of_birth",
                    "email",
                    "first_name",
                    "gender",
                    "group",
                    "id",
                    "last_name",
                    "phone",
                ]
            }
        },
        "links": {
            "type": "object",
            "required": [
                "first",
                "last",
                "next",
                "prev"
            ],
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
            "required": [
                "current_page",
                "from",
                "last_page",
                "links",
                "path",
                "per_page",
                "to",
                "total"
            ],
            "properties": {
                "current_page": {
                    "type": "integer"
                },
                "from": {
                    "type": "integer"
                },
                "last_page": {
                    "type": "integer"
                },
                "links": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": [
                                    "null", "string"
                                ]
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
                    "type": "integer"
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