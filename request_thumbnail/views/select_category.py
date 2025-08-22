import discord
from ..utils import send_claim_message

class CategorySelectView(discord.ui.View):
  def __init__(self, youtube_link: str):
      super().__init__(timeout=300)
      self.youtube_link = youtube_link

  @discord.ui.select(
      placeholder="Choose a category...",
      options=[
          discord.SelectOption(label="a - Large Streamer Content", value="a"),
          discord.SelectOption(label="b - IRL Content", value="b"),
          discord.SelectOption(label="c - Reactions/Gaming", value="c")
      ]
  )
  async def category_select(self, select: discord.ui.Select, interaction: discord.Interaction):

      category_map = {
          "a": "Large Streamer Content",
          "b": "IRL Content", 
          "c": "Reactions/Gaming"
      }

      selected_category = category_map[select.values[0]]
      target_channel_name = select.values[0]  # "a", "b", or "c"

      success = await send_claim_message(
          interaction, 
          self.youtube_link, 
          selected_category, 
          target_channel_name
      )

      if success:
          await interaction.response.send_message(
              f"✅ Your thumbnail request has been sent to #{target_channel_name} channel!", 
              ephemeral=True
          )
      else:
          await interaction.response.send_message(
              f"❌ Channel '{target_channel_name}' not found. Please make sure channels 'a', 'b', and 'c' exist.",
              ephemeral=True
          )