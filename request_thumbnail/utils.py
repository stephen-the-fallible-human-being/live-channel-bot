import discord

async def send_claim_message(interaction: discord.Interaction, youtube_link: str, category: str, channel_name: str):
    target_channel = discord.utils.get(interaction.guild.channels, name=channel_name)
    
    if not target_channel:
        return False
    
    # Create embed for the target channel
    embed = discord.Embed(
        title=f"New Thumbnail Request - {category}",
        description=f"**YouTube Link:** {youtube_link}",
        color=discord.Color.brand_red()
    )
    embed.add_field(name="Category", value=category, inline=True)
    
    # Create claim button view
    claim_view = ClaimButtonView(youtube_link, category, interaction.user)
    
    # Send to target channel
    await target_channel.send(embed=embed, view=claim_view)

