import discord
from .modals import RequestThumbnailModal

class RequestThumbnailButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Persistent view

    @discord.ui.button(label='Request Thumbnail', style=discord.ButtonStyle.primary, emoji='🖼️')
    async def request_thumbnail(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = RequestThumbnailModal()
        await interaction.response.send_modal(modal)