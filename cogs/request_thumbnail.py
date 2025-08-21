
import discord
from discord.ext import commands
from request_thumbnail.views import RequestThumbnailButtonView

class RequestThumbnail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setup_thumbnail", description="Send a button for thumbnail requests")
    async def setup_thumbnail(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🖼️ Thumbnail Request System",
            description="Click the button below to request a thumbnail for your YouTube video.\n\nSelect a category and your request will be sent to the appropriate channel for creators to claim.",
            color=discord.Color.blue()
        )
        
        view = RequestThumbnailButtonView()
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(RequestThumbnail(bot))
