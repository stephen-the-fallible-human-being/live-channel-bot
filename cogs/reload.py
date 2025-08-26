
import discord
from discord.ext import commands

import asyncio

class ReloadCog(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @discord.slash_command(name="reload", description="Reload a specific cog")
    async def reload_cog(self, ctx: discord.ApplicationContext, cog_name: str):
        await ctx.defer()
        extension_path = f'cogs.{cog_name}'
        action = "reloaded"
        try:
            try:
                # Try to reload if already loaded
                await asyncio.to_thread(self.bot.reload_extension, extension_path)
            except commands.ExtensionNotLoaded:
                # Load if not loaded yet
                await asyncio.to_thread(self.bot.load_extension, extension_path)
                action = "loaded"
            
            # Sync commands after reload/load
            await self.bot.sync_commands()
            await ctx.followup.send(f"✅ Successfully {action} cog: {cog_name}", ephemeral=True)

        except Exception as e:
            await ctx.followup.send(f"❌ Failed to reload/load cog {cog_name}: {e}", ephemeral=True)

    @discord.slash_command(name="reload_all", description="Reload all cogs")
    async def reload_all_cogs(self, ctx: discord.ApplicationContext):
        reloaded = []
        failed = []

        for cog_name in list(self.bot.extensions.keys()):
            if cog_name.startswith('cogs.'):
                try:
                    try:
                        await asyncio.to_thread(self.bot.reload_extension, cog_name)
                        reloaded.append(cog_name.split('.')[-1])
                    except commands.ExtensionNotLoaded:
                        await asyncio.to_thread(self.bot.load_extension, cog_name)
                except Exception as e:
                    failed.append(f"{cog_name.split('.')[-1]}: {e}")

        # Sync commands after all reloads
        await self.bot.sync_commands()

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
