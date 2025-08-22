import discord
from ..modals.url_modal import URLModal

class RequestThumbnailButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Persistent view

    @discord.ui.button(label='Request Thumbnail', style=discord.ButtonStyle.primary)
    async def request_thumbnail(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = URLModal()
        await interaction.response.send_modal(modal)