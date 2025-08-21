
import discord
from .views import CategorySelectView

class RequestThumbnailModal(discord.ui.Modal, title='Request Thumbnail'):
    def __init__(self):
        super().__init__()

    youtube_link = discord.ui.TextInput(
        label='YouTube Video Link',
        placeholder='Enter the YouTube video URL here...',
        required=True,
        max_length=500
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Show category selection after YouTube link submission
        embed = discord.Embed(
            title="Select Category",
            description=f"YouTube Link: {self.youtube_link.value}\n\nPlease select a category for this thumbnail request:",
            color=discord.Color.blue()
        )
        
        view = CategorySelectView(str(self.youtube_link.value))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
