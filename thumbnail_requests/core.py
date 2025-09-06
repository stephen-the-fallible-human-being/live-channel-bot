"""
Core Thumbnail Requests Cog
Main cog that combines all thumbnail request functionality
"""
import discord
from discord.ext import commands
from .commands import ThumbnailCommands


class ThumbnailRequests(ThumbnailCommands, commands.Cog):
    """Main thumbnail requests cog that combines all functionality"""

    def __init__(self, bot):
        self.bot = bot
        super().__init__()
