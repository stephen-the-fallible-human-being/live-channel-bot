import discord
from dotenv import load_dotenv
import os

load_dotenv()

# environment variables
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Bot setup
intents = discord.Intents.default()
bot = discord.Bot(intents=intents)

def load_cogs():
    """Load all cogs from the cogs folder"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded cog: {filename[:-3]}')
            except Exception as e:
                print(f'Failed to load cog {filename[:-3]}: {e}')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
# For production, use environment variables or Replit secrets
if __name__ == "__main__":
    # load cogs before connecting the bot to Discord
    load_cogs()
    # You'll need to add your bot token here or use Replit secrets
    bot.run(DISCORD_BOT_TOKEN)  # Replace with your actual token