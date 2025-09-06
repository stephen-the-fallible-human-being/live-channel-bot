"""
Core Staff Management Cog
Main cog that combines all staff management functionality
"""
import discord
from discord.ext import commands
from .commands import StaffCommands
from .creator_commands import CreatorCommands


class StaffManagement(StaffCommands, CreatorCommands, commands.Cog):
    """Main staff management cog that combines all functionality"""
    
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
