import discord

class ClaimButtonView(discord.ui.View):
  def __init__(self, youtube_link: str, category: str, requester: discord.Member):
    super().__init__(timeout=None)
    self.youtube_link = youtube_link
    self.category = category
    self.requester = requester
    self.claimed_by = None

  @discord.ui.button(label='Claim', style=discord.ButtonStyle.red, emoji='✋')
  async def claim_thumbnail(self, button: discord.ui.Button, interaction: discord.Interaction):
    # if the button is clicked, someone decides to claim the thumbnail
    # if it was already clicked (claimed), send an message to the user
    if self.claimed_by:
      await interaction.response.send_message(
          f"❌ This thumbnail has already been claimed by {self.claimed_by.mention}!", 
          ephemeral=True
      )
      return

      # Mark as claimed
      self.claimed_by = interaction.user

      # Update button to show it's claimed
      button.label = f'Claimed by {interaction.user.display_name}'
      button.style = discord.ButtonStyle.secondary
      button.disabled = True

      # Update embed
      embed = discord.Embed(
          title=f"🖼️ Thumbnail Request - {self.category} [CLAIMED]",
          description=f"**YouTube Link:** {self.youtube_link}",
          color=discord.Color.orange()
      )
      embed.add_field(name="Category", value=self.category, inline=True)
      embed.add_field(name="Requested by", value=self.requester.mention, inline=True)
      embed.add_field(name="Claimed by", value=interaction.user.mention, inline=True)

      await interaction.response.edit_message(embed=embed, view=self)

      # Send confirmation to claimer
      try:
          await interaction.followup.send(
              f"✅ You have successfully claimed the thumbnail request for: {self.youtube_link}", 
              ephemeral=True
          )
      except:
          pass  # In case followup fails