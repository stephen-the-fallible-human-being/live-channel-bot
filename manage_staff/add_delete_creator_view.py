import discord
from .add_delete_view import AddDeleteView
from .add_creator_modal import AddCreatorModal

class AddDeleteCreatorView(AddDeleteView):
    def __init__(self):
        super().__init__()
    
    # send a modal to type in the name of the creator
    async def add_callback(self, interaction: discord.Interaction):
        add_creator_modal = AddCreatorModal()
        await interaction.response.send_modal(modal=add_creator_modal)
    
    # send a select menu of creators to choose who to delete
    async def delete_callback(self, interaction:discord.Interaction):
        pass