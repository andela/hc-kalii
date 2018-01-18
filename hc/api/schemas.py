check = {
    "properties": {
        "name": {"type": "string"},
        "tags": {"type": "string"},
        "timeout": {"type": "number", "minimum": 60, "maximum": 7776000},
        "grace": {"type": "number", "minimum": 60, "maximum": 7776000},
        "channels": {"type": "string"}
    }
}
