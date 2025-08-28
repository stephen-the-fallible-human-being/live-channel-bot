import discord
from .add_editor_modal import AddEditorModal

from ..multi_use_views import SingleStringSelectView

# trying something else instead of subclassing add delete view, probably need to add an embed accompanying this, as well
# as buttons to navigate the embed
class ManageEditorsViews(discord.ui.View):
    def __init__(self):
        super().__init__()

        self.add_button = discord.ui.Button(
            label="Add Editor",
            style=discord.ButtonStyle.green
        )
        self.add_item(self.add_button)
        
        self.delete_button = discord.ui.Button(
            label="Delete Editor",
            style=discord.ButtonStyle.red
        )
        self.add_item(self.delete_button)

    async def add_button_callback(self, interaction: discord.Interaction):
        pass
        
    async def delete_button_callback(self, interaction: discord.Interaction):
        pass