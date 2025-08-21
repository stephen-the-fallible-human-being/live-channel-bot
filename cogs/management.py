
import discord
from discord.ext import commands
from discord import app_commands

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="reload", description="Reload a specific cog")
    async def reload_cog(self, interaction: discord.Interaction, cog_name: str):
        try:
            await self.bot.reload_extension(f'cogs.{cog_name}')
            await interaction.response.send_message(f'✅ Successfully reloaded cog: {cog_name}', ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f'❌ Failed to reload cog {cog_name}: {e}', ephemeral=True)

    @app_commands.command(name="reload_all", description="Reload all cogs")
    async def reload_all_cogs(self, interaction: discord.Interaction):
        reloaded = []
        failed = []
        
        for cog_name in list(self.bot.extensions.keys()):
            if cog_name.startswith('cogs.'):
                try:
                    await self.bot.reload_extension(cog_name)
                    reloaded.append(cog_name.split('.')[-1])
                except Exception as e:
                    failed.append(f"{cog_name.split('.')[-1]}: {e}")
        
        message = f"✅ Reloaded: {', '.join(reloaded)}"
        if failed:
            message += f"\n❌ Failed: {', '.join(failed)}"
        
        await interaction.response.send_message(message, ephemeral=True)

    @app_commands.command(name="list_cogs", description="List all loaded cogs")
    async def list_cogs(self, interaction: discord.Interaction):
        cogs = [ext.split('.')[-1] for ext in self.bot.extensions.keys() if ext.startswith('cogs.')]
        await interaction.response.send_message(f"Loaded cogs: {', '.join(cogs)}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Management(bot))
