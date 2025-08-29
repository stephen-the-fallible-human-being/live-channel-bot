from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "creators" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(50) NOT NULL,
    "soft_deleted" INT NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "designers" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "discord_id" VARCHAR(50) NOT NULL UNIQUE,
    "discord_username" VARCHAR(100) NOT NULL,
    "soft_deleted" INT NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
