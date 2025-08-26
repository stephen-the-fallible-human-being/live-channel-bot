import discord
from .unclaim import UnclaimView

OVERSEER_ROLE_ID = 1407876576741163101

class ClaimView(discord.ui.View):
  def __init__(self, youtube_link: str):
    super().__init__(timeout=None)
    self.youtube_link = youtube_link
    self.claimer_id = None
    self.original_message = None
    self.private_channel = None

    # create claim button
    self.claim_button = discord.ui.Button(
      label='Claim',
      style=discord.ButtonStyle.green,
      emoji='✋'
    )
    self.claim_button.callback = self.claim_callback
    self.add_item(self.claim_button)

  async def claim_callback(self, interaction: discord.Interaction):
    # if a user clicks claim
    self.claimer_id = interaction.user.id

    # Update button to show it's claimed
    self.claim_button.label = f'Claimed by {interaction.user.display_name}'
    self.claim_button.style = discord.ButtonStyle.gray
    self.claim_button.disabled = True

    self.original_message = interaction.message
    # update the view
    await self.original_message.edit(view=self)

    # where to place new private channel
    guild = interaction.guild
    category = interaction.channel.category
    overseer_role = guild.get_role(OVERSEER_ROLE_ID)

    overwrites = {
      guild.default_role: discord.PermissionOverwrite(view_channel=False),
      interaction.user: discord.PermissionOverwrite(view_channel=True),
      overseer_role: discord.PermissionOverwrite(view_channel=True),
      guild.me: discord.PermissionOverwrite(view_channel=True)
    }

    # create private channel
    self.private_channel = await guild.create_text_channel(
      name=f"{interaction.user.name}",
      category=category,
      overwrites=overwrites
    )

    # create unclaim view
    unclaim_view = UnclaimView()
    unclaim_view.unclaim_button.callback = self.unclaim_callback
    
    # send message to private channel
    message = await self.private_channel.send(
      f"{overseer_role.mention},\n"
      f"{interaction.user.mention} has claimed a thumbnail request:\n"
      f"{self.youtube_link}",
      view=unclaim_view
    )
    await message.pin()
  
  async def unclaim_callback(self, interaction: discord.Interaction):
    # respond with nothing
    await interaction.response.defer()

    # reset claim button
    self.claim_button.label = "Claim"
    self.claim_button.style = discord.ButtonStyle.green
    self.claim_button.disabled = False

    # update view
    await self.original_message.edit(view=self)

    # close the private channel
    await self.private_channel.delete()
  
  async def submit_callback(self, interaction: discord.Interaction):
    print("submit")


