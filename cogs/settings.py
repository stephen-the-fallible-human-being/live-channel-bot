import discord
from discord.ext import commands

from database.models import GuildConfig

class SettingsCog(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot
    
    @discord.slash_command(
        name="set-thumbnail-designer-role",
        description="Set the role in Discord that the bot will refer to for updating our Thumbnail Designer Database"
    )
    @discord.commands.option(
        parameter_name="role",
        name="role",
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
        await ctx.respond(f"`{role.name}` has been set as the **Thumbnail Designer** Role.", ephemeral=True)


    @discord.slash_command(
        name="set-editor-role",
        description="Set the role in Discord that the bot will refer to for updating our Editor Database"
    )
    @discord.commands.option(
        parameter_name="role",
        name="role",
        description="Role to be set at the 'Editor' role",
        input_type=discord.SlashCommandOptionType.role
    )
    async def set_editor_role(self, ctx: discord.ApplicationContext, role: discord.Role):
        await GuildConfig.update_or_create(
            guild_id=str(ctx.guild.id),
            defaults={
                "editor_role_id": str(role.id)
            }
        )
        await ctx.respond(f"`{role.name}` has been set as the **Editor** Role", ephemeral=True)

def setup(bot: discord.Bot):
    bot.add_cog(SettingsCog(bot))