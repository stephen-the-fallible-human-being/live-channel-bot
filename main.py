"""
Simple Discord Bot - Step 4: Organized with Cogs (using py-cord)
"""
import discord
from discord.ext import commands
from database.config import init_database, close_database
import os
from dotenv import load_dotenv

# Create a bot instance
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)


async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded cog: {filename[:-3]}')


@bot.event
async def on_ready():
    """This function runs when the bot starts up"""
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} servers')
    await bot.tree.sync()
    print(f"Bot has connected with {len(bot.commands)} commands")


# Run the bot
if __name__ == "__main__":
    import asyncio
    async def setup_bot():
        load_dotenv()
        await load_cogs()
        await init_database()
    asyncio.run(setup_bot())
    bot.run(os.getenv('DISCORD_TOKEN'))
    