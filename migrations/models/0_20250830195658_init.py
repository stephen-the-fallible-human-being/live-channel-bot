from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "creators" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(100) NOT NULL /* Display name */,
    "is_active" INT NOT NULL DEFAULT 1 /* Whether the creator is active */
) /* YouTube content creators */;
CREATE TABLE IF NOT EXISTS "designers" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "discord_id" BIGINT NOT NULL UNIQUE /* Discord user ID */,
    "discord_username" VARCHAR(100) NOT NULL /* Discord username */,
    "is_active" INT NOT NULL DEFAULT 1 /* Whether the designer is active */
) /* Thumbnail designers */;
CREATE TABLE IF NOT EXISTS "editors" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "discord_id" BIGINT NOT NULL UNIQUE /* Discord user ID */,
    "discord_username" VARCHAR(100) NOT NULL /* Discord username */,
    "is_active" INT NOT NULL DEFAULT 1 /* Whether the editor is active */
) /* Video editors */;
CREATE TABLE IF NOT EXISTS "guild_configs" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "guild_id" BIGINT NOT NULL UNIQUE /* Discord server ID */,
    "thumbnail_designer_role_id" BIGINT /* Role ID for thumbnail designers */,
    "editor_role_id" BIGINT /* Role ID for editors */,
    "overseer_role_id" BIGINT /* Role ID for overseers */
) /* Server configuration settings */;
CREATE TABLE IF NOT EXISTS "overseers" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "discord_id" BIGINT NOT NULL UNIQUE /* Discord user ID */,
    "discord_username" VARCHAR(100) NOT NULL /* Discord username */,
    "is_active" INT NOT NULL DEFAULT 1 /* Whether the overseer is active */
) /* Overseers\/managers */;
CREATE TABLE IF NOT EXISTS "thumbnails" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "youtube_url" VARCHAR(200) NOT NULL /* YouTube video URL */,
    "category" VARCHAR(50) NOT NULL /* Video category */,
    "completed_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP /* When the thumbnail was completed */,
    "creator_id" INT NOT NULL REFERENCES "creators" ("id") ON DELETE CASCADE /* Creator the video was for */,
    "designer_id" INT NOT NULL REFERENCES "designers" ("id") ON DELETE CASCADE /* Designer who completed it */
) /* Completed thumbnail records for export */;
CREATE TABLE IF NOT EXISTS "thumbnail_categories" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "category_name" VARCHAR(50) NOT NULL UNIQUE /* Category name (e.g., Gaming, Tech) */,
    "channel_id" BIGINT NOT NULL UNIQUE /* Discord channel ID */,
    "channel_name" VARCHAR(100) NOT NULL /* Discord channel name */,
    "is_active" INT NOT NULL DEFAULT 1 /* Whether the category is active */
) /* Thumbnail request category channels */;
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);
CREATE TABLE IF NOT EXISTS "editors_creators" (
    "editors_id" INT NOT NULL REFERENCES "editors" ("id") ON DELETE CASCADE,
    "creator_id" INT NOT NULL REFERENCES "creators" ("id") ON DELETE CASCADE
) /* Creators this editor is assigned to */;
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_editors_cre_editors_3cf19e" ON "editors_creators" ("editors_id", "creator_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
