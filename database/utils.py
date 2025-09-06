from tortoise import Tortoise
from .config import TORTOISE_ORM

async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)

async def close_db():
    await Tortoise.close_connections()