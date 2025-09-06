"""
Database configuration for Tortoise ORM
"""
from tortoise import Tortoise

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
            "models": ["database.models"],
            "default_connection": "default",
        },
    },
    "use_tz": False,
    "timezone": "UTC"
}


async def init_database():
    """Initialize the database"""
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas()
    print("Database initialized and schemas generated!")


async def close_database():
    """Close the database connection"""
    await Tortoise.close_connections()
    print("Database connections closed!")

