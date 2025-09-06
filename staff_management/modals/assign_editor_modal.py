"""
Assign Editor Modal
Modal for assigning editors to creators
"""
import discord
from typing import List


class AssignEditorModal(discord.ui.Modal):
    def __init__(self, editor_options: List[discord.SelectOption], creator_options=List[discord.SelectOption]):
        super().__init__(title="Assign Editor Modal")

        self.editor_select_menu = discord.ui.Select(
            select_type=discord.ComponentType.string_select,
            min_values=1,
            max_values=1,
            options=editor_options,
            label="Select an Editor:",
            description="this is supposed to be a description lol but i don't think we need it",
            required=True
        )
        self.add_item(self.editor_select_menu)

        self.creator_select_menu = discord.ui.Select(
            select_type=discord.ComponentType.string_select,
            min_values=1,
            max_values=1,
            options=creator_options,
            label="Select a Creator:",
            required=True
        )
        self.add_item(self.creator_select_menu)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message("done with modal", ephemeral=True)
