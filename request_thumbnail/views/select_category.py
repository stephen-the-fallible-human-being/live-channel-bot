import discord
from .claim_button import ClaimButtonView

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
    channel_name = select.values[0]
    target_channel = discord.utils.get(interaction.guild.channels, name=channel_name)

    embed = discord.Embed(
      title="New Thumbnail Request",
      color=discord.Color.brand_red()
    )

    claim_button_view = ClaimButtonView(self.youtube_link, target_channel, interaction.user)

    await target_channel.send(embed=embed, view=claim_button_view)

        
      