

TORTOISE_ORM = {
    "connections": {"default": "sqlite://db.sqlite3"},
    "apps": {
        "bot-data": {
            "models": ["database.models", "aerich.models"],  # points to your models
            "default_connection": "default",
        }
    },
}

