from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "guild_configs" ADD "single_thumbnail_channel" INT NOT NULL DEFAULT 0 /* Whether to use a single channel for all thumbnail requests */;
        ALTER TABLE "guild_configs" ADD "single_thumbnail_channel_id" BIGINT /* Discord channel ID for single thumbnail requests */;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "guild_configs" DROP COLUMN "single_thumbnail_channel";
        ALTER TABLE "guild_configs" DROP COLUMN "single_thumbnail_channel_id";"""
