import discord
from .claim import ClaimView

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
    category_name = select.values[0]
    target_channel = discord.utils.get(interaction.guild.channels, name=category_name)

    category_role = discord.utils.get(interaction.guild.roles, name=category_name)

    claim_view = ClaimView(self.youtube_link)

    await target_channel.send(
        content=f"### Thumbnail Request {category_role.mention}\n{self.youtube_link}", view=claim_view
    )
      
    await interaction.response.send_message(
        f"✅ Your thumbnail request has been submitted!", ephemeral=True
    )

        
      