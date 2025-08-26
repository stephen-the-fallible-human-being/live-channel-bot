from tortoise import Tortoise

DB_URL = "sqlite://db/live-channel-database.db"

config = {
    "connections": {"default": DB_URL},
    "apps": {
        "models": {
            "models": ["db.models"],  # points to your models
            "default_connection": "default",
        }
    },
}

async def init_db():
    await Tortoise.init(config=config)
    await Tortoise.generate_schemas(safe=True)

async def close_db():
    await Tortoise.close_connections()