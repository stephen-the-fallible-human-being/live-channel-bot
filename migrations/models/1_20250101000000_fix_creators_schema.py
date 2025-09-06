from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        -- Remove discord_id column from creators table
        CREATE TABLE "creators_new" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "name" VARCHAR(100) NOT NULL,
            "is_active" INT NOT NULL DEFAULT 1
        );
        
        -- Copy data from old table to new table (excluding discord_id)
        INSERT INTO "creators_new" ("id", "created_at", "updated_at", "name", "is_active")
        SELECT "id", "created_at", "updated_at", "name", "is_active" FROM "creators";
        
        -- Drop the old table
        DROP TABLE "creators";
        
        -- Rename new table to original name
        ALTER TABLE "creators_new" RENAME TO "creators";
        """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        -- Recreate the old schema with discord_id
        CREATE TABLE "creators_old" (
            "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            "discord_id" BIGINT NOT NULL,
            "name" VARCHAR(100) NOT NULL,
            "is_active" INT NOT NULL DEFAULT 1
        );
        
        -- Copy data back (with 0 for discord_id)
        INSERT INTO "creators_old" ("id", "created_at", "updated_at", "discord_id", "name", "is_active")
        SELECT "id", "created_at", "updated_at", 0, "name", "is_active" FROM "creators";
        
        -- Drop the new table
        DROP TABLE "creators";
        
        -- Rename old table back
        ALTER TABLE "creators_old" RENAME TO "creators";
        """
