"""
Unclaim Button
Handles unclaiming thumbnail requests and closing private channels
"""
import discord
from .claim import ClaimRequestView


class UnclaimButton(discord.ui.Button):
    def __init__(self, original_message, private_channel, editor_name):
        super().__init__(
            label="Unclaim Request",
            style=discord.ButtonStyle.danger,
            emoji="❌"
        )
        self.original_message = original_message
        self.private_channel = private_channel
        self.editor_name = editor_name

    async def callback(self, interaction: discord.Interaction):
        try:
            # Check if user is the designer who claimed the request
            # We can identify this by checking if they have access to the private channel
            if not interaction.user.guild_permissions.manage_channels:
                await interaction.response.send_message(
                    "❌ You don't have permission to unclaim this request!",
                    ephemeral=True
                )
                return
            
            # Reset the original claim button (keep embed color as brand_red)
            original_embed = self.original_message.embeds[0]
            
            # Create a new view with reset button
            reset_view = ClaimRequestView(
                self.original_message.embeds[0].fields[0].value,  # creator_name
                self.original_message.embeds[0].fields[1].value,  # category
                self.original_message.embeds[0].fields[2].value,  # youtube_url
                self.editor_name  # We need to store this in the button
            )
            
            # Update the original message
            await self.original_message.edit(embed=original_embed, view=reset_view)
            
            # Delete the private channel
            await self.private_channel.delete(reason=f"Unclaimed by {interaction.user.name}")
            
            # Send confirmation
            await interaction.response.send_message(
                "✅ Request unclaimed! Private channel has been closed.",
                ephemeral=True
            )
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error unclaiming request: {str(e)}",
                ephemeral=True
            )
