import discord
from discord.ext import commands

from manage_staff.manage_staff_view import ManageStaffView

class ManageStaffCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="send-manage-staff-panel", description="Send a panel with buttons to add/remove/assign staff")
    async def send_manage_staff_panel(self, ctx: discord.ApplicationContext):
        manage_staff_embed = discord.Embed(
            title="Manage Staff",
            color=discord.Color.brand_red()
        )
        manage_staff_view = ManageStaffView()

        await ctx.respond(embed=manage_staff_embed, view=manage_staff_view)

def setup(bot):
    bot.add_cog(ManageStaffCog(bot))