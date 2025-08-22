import discord 
from ..views.select_category import CategorySelectView

class URLModal(discord.ui.Modal):
  def __init__(self, title="YouTube Video URL Input Form:"):
      super().__init__(title=title)
      self.youtube_link = discord.ui.InputText(
          label="YouTube Video URL",
          placeholder="Enter the URL of your YouTube video",
          style=discord.InputTextStyle.short,
          required=True
      )
      self.add_item(self.youtube_link)
    
  async def callback(self, interaction: discord.Interaction):
      # Show category selection after YouTube link submission
      embed = discord.Embed(
          title="Select Category",
          description="Please select a category for this thumbnail request:",
          color=discord.Color.brand_red()
      )

      view = CategorySelectView(str(self.youtube_link.value))
      await interaction.response.send_message(embed=embed, view=view, ephemeral=True)