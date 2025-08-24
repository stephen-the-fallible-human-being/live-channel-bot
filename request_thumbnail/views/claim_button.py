import discord

class ClaimButtonView(discord.ui.View):
  def __init__(self, youtube_link: str, category: str, requester: discord.Member):
    super().__init__(timeout=None)
    self.youtube_link = youtube_link
    self.claimer_id = None

    self.claim_button = discord.ui.Button(
      label='Claim',
      style=discord.ButtonStyle.green,
      emoji='✋'
    )
    self.claim_button.callback = self.claim_callback
    self.add_item(self.claim_button)

  async def claim_callback(self, interaction: discord.Interaction):
    self.claimer_id = interaction.user.id

    # Update button to show it's claimed
    self.claim_button.label = f'Claimed by {interaction.user.display_name}'
    self.claim_button.style = discord.ButtonStyle.gray
    self.claim_button.disabled = True

    # add an unclaim button
    unclaim_button = discord.ui.Button(
      label="Unclaim",
      style=discord.ButtonStyle.red
    )
    unclaim_button.callback = self.unclaim_callback
    self.add_item(unclaim_button)

    await interaction.response.edit_message(view=self)

    # Send confirmation to claimer
    try:
      await interaction.followup.send(
        f"✅ You have successfully claimed the thumbnail request for: {self.youtube_link}", 
        ephemeral=True
      )
    except:
      pass
  
  async def unclaim_callback(self, interaction: discord.Interaction):
    # if non-claimer tries to unclaim the thumbnail
    if interaction.user.id != self.claimer_id:
      await interaction.response.send_message(
        "Only the claimer can unclaim a thumbnail request",
        ephemeral=True
      )
    # if claimer decides to unclaim thumbnail
    else:
      self.claimer_id = None
      # clear all buttons
      self.clear_items()
      # add a fresh new claim button
      self.claim_button = discord.ui.Button(
        label="Claim",
        style=discord.ButtonStyle.green,
        emoji="✋"
      )
      self.claim_button.callback = self.claim_callback
      self.add_item(self.claim_button)
      await interaction.response.edit_message(view=self)

    
