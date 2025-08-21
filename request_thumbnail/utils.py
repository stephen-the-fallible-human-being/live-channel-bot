import discord

async def send_claim_message(interaction: discord.Interaction, youtube_link: str, category: str, channel_name: str):
    """
    Send a claim message to the specified channel
    
    Args:
        interaction: Discord interaction object
        youtube_link: The YouTube video URL
        category: The selected category name
        channel_name: Target channel name (a, b, or c)
    
    Returns:
        bool: True if successful, False if channel not found
    """
    target_channel = discord.utils.get(interaction.guild.channels, name=channel_name)
    
    if not target_channel:
        return False
    
    # Create embed for the target channel
    embed = discord.Embed(
        title=f"🖼️ New Thumbnail Request - {category}",
        description=f"**YouTube Link:** {youtube_link}",
        color=discord.Color.green()
    )
    embed.add_field(name="Category", value=category, inline=True)
    embed.add_field(name="Requested by", value=interaction.user.mention, inline=True)
    
    # Create claim button view
    claim_view = ClaimButtonView(youtube_link, category, interaction.user)
    
    # Send to target channel
    await target_channel.send(embed=embed, view=claim_view)
    
    return True

class ClaimButtonView(discord.ui.View):
    def __init__(self, youtube_link: str, category: str, requester: discord.Member):
        super().__init__(timeout=None)
        self.youtube_link = youtube_link
        self.category = category
        self.requester = requester
        self.claimed_by = None

    @discord.ui.button(label='Claim Thumbnail', style=discord.ButtonStyle.success, emoji='✋')
    async def claim_thumbnail(self, interaction: discord.Interaction, button: discord.ui.Button):
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