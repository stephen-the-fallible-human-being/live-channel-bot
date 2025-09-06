"""
Migration runner script to update the creators table schema
"""
import asyncio
import sqlite3
from database.config import init_database, close_database


async def run_migration():
    """Run the migration to remove discord_id from creators table"""
    print("🔄 Starting migration...")
    
    # Initialize database connection
    await init_database()
    
    try:
        # Connect to SQLite directly for the migration
        conn = sqlite3.connect('bot_database.sqlite3')
        cursor = conn.cursor()
        
        print("📋 Current creators table schema:")
        cursor.execute("PRAGMA table_info(creators)")
        current_schema = cursor.fetchall()
        for column in current_schema:
            print(f"  - {column[1]} ({column[2]})")
        
        print("\n🔄 Running migration...")
        
        # Create new table without discord_id
        cursor.execute("""
            CREATE TABLE "creators_new" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                "updated_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                "name" VARCHAR(100) NOT NULL,
                "is_active" INT NOT NULL DEFAULT 1
            )
        """)
        
        # Copy data from old table to new table (excluding discord_id)
        cursor.execute("""
            INSERT INTO "creators_new" ("id", "created_at", "updated_at", "name", "is_active")
            SELECT "id", "created_at", "updated_at", "name", "is_active" FROM "creators"
        """)
        
        # Drop the old table
        cursor.execute("DROP TABLE creators")
        
        # Rename new table to original name
        cursor.execute("ALTER TABLE creators_new RENAME TO creators")
        
        # Commit the changes
        conn.commit()
        
        print("✅ Migration completed successfully!")
        
        print("\n📋 New creators table schema:")
        cursor.execute("PRAGMA table_info(creators)")
        new_schema = cursor.fetchall()
        for column in new_schema:
            print(f"  - {column[1]} ({column[2]})")
        
        # Show any existing data
        cursor.execute("SELECT id, name, is_active FROM creators")
        creators = cursor.fetchall()
        if creators:
            print(f"\n📊 Found {len(creators)} creators in database:")
            for creator in creators:
                print(f"  - ID: {creator[0]}, Name: {creator[1]}, Active: {creator[2]}")
        else:
            print("\n📊 No creators found in database")
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()
        await close_database()


if __name__ == "__main__":
    asyncio.run(run_migration())
