import discord

class ClaimButtonView(discord.ui.View):
  def __init__(self, youtube_link: str, category: str, requester: discord.Member):
    super().__init__(timeout=None)
    self.youtube_link = youtube_link
    self.claimed_by = None

  @discord.ui.button(label='Claim', style=discord.ButtonStyle.red, emoji='✋')
  async def claim_thumbnail(self, button: discord.ui.Button, interaction: discord.Interaction):
    # if the button is clicked, someone decides to claim the thumbnail
    # if it was already clicked (claimed), send an message to the user
    if self.claimed_by:
      await interaction.response.send_message(
          f"❌ This thumbnail has already been claimed by {self.claimed_by.display_name}!", 
          ephemeral=True
      )
      return

    # if it wasn't claimed, mark as claimed and update the button
    # mark as claimed
    self.claimed_by = interaction.user

    # Update button to show it's claimed
    button.label = f'Claimed by {interaction.user.display_name}'
    button.style = discord.ButtonStyle.gray
    button.disabled = True

    await interaction.response.edit_message(view=self)

    # Send confirmation to claimer
    try:
      await interaction.followup.send(
        f"✅ You have successfully claimed the thumbnail request for: {self.youtube_link}", 
        ephemeral=True
      )
    except:
      pass