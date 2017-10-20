import json

path = 'settings.json'
definitions = ["host", "port", "user", "password", "original_db_name", "new_db_name"]


def load_settings():
    settings = {}

    try:
        with open(path, 'r') as f:
            data = json.load(f) or {}
    except FileNotFoundError:
        data = {}

    for d in definitions:
        key = d
        if key in data:
            settings[key] = data[key]

    return settings
