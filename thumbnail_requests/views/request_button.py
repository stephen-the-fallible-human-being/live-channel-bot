"""
Request Thumbnail Button
Handles the button that opens the thumbnail request modal
"""
import discord
from database.models import Editor, ThumbnailCategory
from ..modals.request_modal import ThumbnailRequestModal


class RequestThumbnailButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Request Thumbnail",
            style=discord.ButtonStyle.primary,
            emoji="🎨"
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            # Check if user is an editor
            editor = await Editor.filter(
                discord_id=interaction.user.id,
                is_active=True
            ).prefetch_related('assigned_creators').first()
            
            if not editor:
                await interaction.response.send_message(
                    "❌ You are not registered as an editor!",
                    ephemeral=True
                )
                return
            
            # Get assigned creators
            assigned_creators = await editor.assigned_creators.filter(is_active=True)
            
            if not assigned_creators:
                await interaction.response.send_message(
                    "❌ You are not assigned to any creators! Please contact an administrator.",
                    ephemeral=True
                )
                return
            
            # Get available categories
            available_categories = await ThumbnailCategory.filter(is_active=True).order_by('category_name')
            
            if not available_categories:
                await interaction.response.send_message(
                    "❌ No thumbnail categories have been created yet! Please ask an administrator to create categories first.",
                    ephemeral=True
                )
                return
            
            # Show modal
            modal = ThumbnailRequestModal(interaction.user, assigned_creators, available_categories)
            await interaction.response.send_modal(modal)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error: {str(e)}",
                ephemeral=True
            )
