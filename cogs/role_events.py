import discord
from discord.ext import commands

from database.models import GuildConfig
from utils.crud_helpers import add_designer, remove_designer, add_editor, remove_editor

class RoleEventsCog(commands.Cog):
    def __init__(self, bot:discord.Bot):
        self.bot: discord.Bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        # fetch thumbnail role id
        guild_config = await GuildConfig.get_or_none(guild_id=str(after.guild.id))
        if not guild_config:
            return
        
        thumbnail_role_id = guild_config.thumbnail_role_id
        editor_role_id = guild_config.editor_role_id

        # get roles before, get roles after
        role_ids_before = set(r.id for r in before.roles)
        role_ids_after = set(r.id for r in after.roles)

        # diff them, and get the roles that actually changed
        added_role_ids = role_ids_after - role_ids_before
        removed_role_ids = role_ids_before - role_ids_after

        # handle added roles
        for role_id in added_role_ids:
            if thumbnail_role_id and str(role_id) == thumbnail_role_id:
                await add_designer(after)
            elif editor_role_id and str(role_id) == editor_role_id:
                await add_editor(after)
         
        # handle removed roles
        for role_id in removed_role_ids:
            # if the guild has a thumbnail role set (meaning we have set a role to watch for that acts as our designer store)
            # then, if someone gets the designer role removed, they must be removed from the designer table in our db
            if thumbnail_role_id and str(role_id) == thumbnail_role_id:
                await remove_designer(after) 
            elif editor_role_id and str(role_id) == editor_role_id:
                await remove_editor(after)


def setup(bot: discord.Bot):
    bot.add_cog(RoleEventsCog(bot))