import discord
from ..modals.url_modal import URLModal

class RequestThumbnailButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Persistent view

    @discord.ui.button(label='Request Thumbnail', style=discord.ButtonStyle.secondary, emoji="✋")
    async def request_thumbnail(self, button: discord.ui.Button, interaction: discord.Interaction):
        modal = URLModal()
        await interaction.response.send_modal(modal)