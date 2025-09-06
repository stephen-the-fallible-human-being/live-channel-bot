"""
Manage Creators View
View for managing creators (add/delete)
"""
import discord
from ..modals.add_creator_modal import AddCreatorModal
from .select_creator import SelectCreatorView
from database.models import Creator


class ManageCreatorsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_button = discord.ui.Button(
            label="Add Creator",
            style=discord.ButtonStyle.green
        )
        self.add_item(self.add_button)
        self.add_button.callback = self.add_callback

        self.delete_button = discord.ui.Button(
            label="Delete Creator",
            style=discord.ButtonStyle.red
        )
        self.add_item(self.delete_button)
        self.delete_button.callback = self.delete_callback
    
    # send a modal to type in the name of the creator
    async def add_callback(self, interaction: discord.Interaction):
        add_creator_modal = AddCreatorModal()
        await interaction.response.send_modal(modal=add_creator_modal)
    
    # send a select menu of creators to choose who to delete
    async def delete_callback(self, interaction:discord.Interaction):
        # might take a bit
        await interaction.response.defer()

        # get all creators from the database (discord's limit for a select menu is 25 items might have to start a modal for search to narrow results)
        creators = await Creator.filter(soft_deleted=False).limit(25)

        # no creators found
        if not creators:
            await interaction.followup.send(
                "No creators found",
                ephemeral=True
            )
            return
        
        options = [discord.SelectOption(label=c.name, value=str(c.id)) for c in creators]

        creator_select_view = SelectCreatorView(options=options)

        await interaction.followup.send(
            "Select a creator to delete:",
            view=creator_select_view,
            ephemeral=True
        )
