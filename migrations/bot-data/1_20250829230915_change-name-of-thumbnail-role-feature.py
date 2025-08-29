from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "editors" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "discord_id" VARCHAR(50) NOT NULL UNIQUE,
    "discord_username" VARCHAR(100) NOT NULL,
    "soft_deleted" INT NOT NULL DEFAULT 0
);
        ALTER TABLE "guildconfig" RENAME COLUMN "thumbnail_role_id" TO "thumbnail_designer_role_id";
        CREATE TABLE "editors_creators" (
    "creator_id" INT NOT NULL REFERENCES "creators" ("id") ON DELETE CASCADE,
    "editors_id" INT NOT NULL REFERENCES "editors" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "editors_creators";
        ALTER TABLE "guildconfig" RENAME COLUMN "thumbnail_designer_role_id" TO "thumbnail_role_id";
        DROP TABLE IF EXISTS "editors";"""
