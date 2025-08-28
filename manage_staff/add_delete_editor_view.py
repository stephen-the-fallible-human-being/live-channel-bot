import discord
from .add_delete_view import AddDeleteView
from .add_creator_modal import AddCreatorModal

class AddDeleteEditorView(AddDeleteView):
    def __init__(self):
        super().__init__()
    
    # send a modal to type in the name of the creator
    async def add_callback(interaction: discord.Interaction):
        modal = AddCreatorModal()
        await interaction.response.send_message(modal=modal)
    
    # send a select menu of creators to choose who to delete
    async def delete_callback(interaction:discord.Interaction):
        return await super().delete_callback()