import discord 
from .category_view import CategorySelectView

class URLModal(discord.ui.Modal):
  def __init__(self, title="YouTube Video URL Input Form:"):
      super().__init__(title=title)

  youtube_link = discord.ui.InputText(
      label='YouTube Video Link',
      placeholder='Enter the YouTube video URL:',
      required=True,
      max_length=100
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