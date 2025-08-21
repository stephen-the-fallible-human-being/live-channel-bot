
import discord
from discord.ext import commands
from discord import app_commands
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

    @app_commands.command(name="thumbnail_help", description="Show help for the thumbnail request system")
    async def thumbnail_help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="🖼️ Thumbnail Request System Help",
            description="How to use the thumbnail request system:",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="📝 Requesting a Thumbnail",
            value="1. Click the 'Request Thumbnail' button\n2. Enter your YouTube video URL\n3. Select the appropriate category\n4. Your request will be sent to the category channel",
            inline=False
        )
        
        embed.add_field(
            name="🎨 For Thumbnail Creators",
            value="1. Check the category channels (a, b, c)\n2. Click 'Claim Thumbnail' on requests you want to work on\n3. Once claimed, the request is marked as yours",
            inline=False
        )
        
        embed.add_field(
            name="📂 Categories",
            value="**a** - Large Streamer Content 🎮\n**b** - IRL Content 🎬\n**c** - Reactions/Gaming 🎯",
            inline=False
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(RequestThumbnail(bot))
