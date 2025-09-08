"""
Database configuration for Tortoise ORM
"""

# Database configuration
TORTOISE_ORM = {
    "connections": {
        "default": {
            "engine": "tortoise.backends.sqlite",
            "credentials": {
                "file_path": "bot_database.sqlite3",
            }
        }
    },
    "apps": {
        "models": {
            "models": ["database.models", "aerich.models"],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "UTC"
}