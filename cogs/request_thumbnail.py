
import discord
from discord.ext import commands
from request_thumbnail.views.request_button import RequestThumbnailButtonView

class RequestThumbnailCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="send-request-thumbnail-button", description="Send a button for thumbnail requests")
    async def setup_thumbnail(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="Thumbnail Request Panel",
            description="Click the button below to request a thumbnail for your YouTube video.",
            color=discord.Color.brand_red()
        )
        
        view = RequestThumbnailButtonView()
        await ctx.respond(embed=embed, view=view)

def setup(bot):
    bot.add_cog(RequestThumbnailCog(bot))
