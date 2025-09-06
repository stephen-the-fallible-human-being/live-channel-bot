from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        -- Drop the existing creators table completely
        DROP TABLE IF EXISTS "creators";
        
        -- Create fresh creators table with correct schema
        CREATE TABLE "creators" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "name" VARCHAR(100) NOT NULL,
            "is_active" INT NOT NULL DEFAULT 1
        );
        """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        -- Drop the new table
        DROP TABLE IF EXISTS "creators";
        
        -- Recreate the old schema with discord_id
        CREATE TABLE "creators" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "discord_id" BIGINT NOT NULL,
            "name" VARCHAR(100) NOT NULL,
            "is_active" INT NOT NULL DEFAULT 1
        );
        """
