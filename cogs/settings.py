import discord
from discord.ext import commands

from database.models import GuildConfig

class SettingsCog(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @discord.slash_command(name="set-thumbnail-designer-role", description="Send a panel with buttons to change up settings")
    @discord.option(
        name="Role",
        description="Role to be set at the 'Thumbnail Designer' role",
        input_type=discord.SlashCommandOptionType.role
    )
    async def set_designer_role(self, ctx: discord.ApplicationContext, role: discord.Role):
        await GuildConfig.update_or_create(
            guild_id=str(ctx.guild.id),
            defaults={
                "thumbnail_designer_role_id": str(role.id)
            }
        )
        await ctx.respond(f"{role.name} has been set as the Thumbnail Designer Role.", ephemeral=True)

def setup(bot: discord.Bot):
    bot.add_cog(SettingsCog(bot))