from tortoise import Tortoise
from .config import TORTOISE_ORM


async def init_database():
    """Initialize the database"""
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)
    print("Database initialized and schemas generated!")


async def close_database():
    """Close the database connection"""
    await Tortoise.close_connections()
    print("Database connections closed!")