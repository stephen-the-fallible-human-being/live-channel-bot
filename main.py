import discord
import os

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
    # Load cogs
    load_cogs()


# Replace 'YOUR_BOT_TOKEN' with your actual bot token
# For production, use environment variables or Replit secrets
if __name__ == "__main__":
    # You'll need to add your bot token here or use Replit secrets
    bot.run(os.getenv('DISCORD_BOT_TOKEN'))  # Replace with your actual token