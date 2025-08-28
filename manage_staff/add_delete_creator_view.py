import discord
from .add_delete_view import AddDeleteView
from .add_creator_modal import AddCreatorModal

from database.models import Creator
from multi_use_views.single_string_select_view import SingleStringSelectView
from tortoise.exceptions import DoesNotExist

class AddDeleteCreatorView(AddDeleteView):
    def __init__(self):
        super().__init__()
    
    # send a modal to type in the name of the creator
    async def add_callback(self, interaction: discord.Interaction):
        add_creator_modal = AddCreatorModal()
        await interaction.response.send_modal(modal=add_creator_modal)
    
    # send a select menu of creators to choose who to delete
    async def delete_callback(self, interaction:discord.Interaction):
        # get all creators from the database (discord's limit for a select menu is 25 items might have to start a modal for search to narrow results)
        creators = await Creator.filter(soft_deleted=False).limit(25)

        # no creators found
        if not creators:
            await interaction.response.send_message(
                "No creators found",
                ephemeral=True
            )
        
        select_options = [
            (creator.name, str(creator.id)) for creator in creators
        ]

        creator_select_view = SingleStringSelectView(select_options=select_options, callback=self.delete_creator)

        await interaction.response.send_message(
            "Select a creator to delete:",
            view=creator_select_view,
            ephemeral=True
        )
    
    # callback passed into the select menu after selection is done
    async def delete_creator(self, interaction: discord.Interaction):
        creator_id = int(interaction.data['values'][0])

        try:
            creator = await Creator.get(id=creator_id)
            creator.soft_deleted = True
            await creator.save()
            await interaction.response.send_message(
                f"Creator **{creator.name}** has been soft-deleted",
                ephemeral=True
            )
        except DoesNotExist:
            await interaction.response.send_message(
                f"Creator not found",
                ephemeral=True
            )
