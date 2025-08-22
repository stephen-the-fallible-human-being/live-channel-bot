
import discord
from discord.ext import commands

class ReloadCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="reload", description="Reload a specific cog")
    async def reload_cog(self, ctx: discord.ApplicationContext, cog_name: str):
        try:
            await self.bot.reload_extension(f'cogs.{cog_name}')
            await ctx.respond(f'✅ Successfully reloaded cog: {cog_name}', ephemeral=True)
        except Exception as e:
            await ctx.respond(f'❌ Failed to reload cog {cog_name}: {e}', ephemeral=True)

    @discord.slash_command(name="reload_all", description="Reload all cogs")
    async def reload_all_cogs(self, ctx: discord.ApplicationContext):
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
        
        await ctx.respond(message, ephemeral=True)

    @discord.slash_command(name="list_cogs", description="List all loaded cogs")
    async def list_cogs(self, ctx: discord.ApplicationContext):
        cogs = [ext.split('.')[-1] for ext in self.bot.extensions.keys() if ext.startswith('cogs.')]
        await ctx.respond(f"Loaded cogs: {', '.join(cogs)}", ephemeral=True)

def setup(bot):
    bot.add_cog(ReloadCog(bot))
