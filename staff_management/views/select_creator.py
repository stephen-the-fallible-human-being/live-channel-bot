"""
Select Creator View
View for selecting creators from a dropdown
"""
import discord
from typing import List
from database.models import Creator
from tortoise.exceptions import DoesNotExist


class SelectCreatorView(discord.ui.View):
    def __init__(self, options: List[discord.SelectOption]):
        super().__init__()

        self.select_menu = discord.ui.Select(
            select_type=discord.ComponentType.string_select,
            min_values=1,
            max_values=1,
            options=options
        )
        self.add_item(self.select_menu)
        self.select_menu.callback = self.delete_creator

    # callback after selection
    async def delete_creator(self, interaction: discord.Interaction):
        # might take a bit
        await interaction.response.defer()

        # get id
        creator_id = int(self.select_menu.values[0])

        try:
            # get creator using the id
            creator = await Creator.get(id=creator_id)
            creator.soft_deleted = True
            await creator.save()
            await interaction.followup.send(
                f"Creator **{creator.name}** has been soft-deleted",
                ephemeral=True
            )
        except DoesNotExist:
            # if creator somehow wasn't found
            await interaction.followup.send(
                f"Creator not found",
                ephemeral=True
            )
