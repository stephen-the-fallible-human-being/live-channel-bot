"""
Autocomplete functions for staff management commands
"""
import discord
from database.models import Creator, Editor, Designer, Overseer


async def get_editor_names(ctx: discord.AutocompleteContext):
    """Autocomplete function for editor names"""
    editors = await Editor.filter(is_active=True)
    return [editor.discord_username for editor in editors]


async def get_creator_names(ctx: discord.AutocompleteContext):
    """Autocomplete function for creator names"""
    creators = await Creator.filter(is_active=True)
    return [creator.name for creator in creators]


async def get_designer_names(ctx: discord.AutocompleteContext):
    """Autocomplete function for designer names"""
    designers = await Designer.filter(is_active=True)
    return [designer.discord_username for designer in designers]


async def get_overseer_names(ctx: discord.AutocompleteContext):
    """Autocomplete function for overseer names"""
    overseers = await Overseer.filter(is_active=True)
    return [overseer.discord_username for overseer in overseers]
