"""
Submit Button
Handles submitting completed thumbnails and recording them in the database
"""
import discord
from database.models import Overseer, Designer, Creator, Thumbnail
from datetime import datetime


class SubmitButton(discord.ui.Button):
    def __init__(self, creator_name, category, youtube_url, designer_name, original_message, private_channel):
        super().__init__(
            label="Submit Thumbnail",
            style=discord.ButtonStyle.success,
            emoji="✅"
        )
        self.creator_name = creator_name
        self.category = category
        self.youtube_url = youtube_url
        self.designer_name = designer_name
        self.original_message = original_message
        self.private_channel = private_channel

    async def callback(self, interaction: discord.Interaction):
        try:
            # Check if user is an overseer
            overseer = await Overseer.filter(
                discord_id=interaction.user.id,
                is_active=True
            ).first()
            
            if not overseer:
                await interaction.response.send_message(
                    "❌ Only overseers can submit thumbnails!",
                    ephemeral=True
                )
                return
            
            # Get the designer object
            designer = await Designer.filter(
                discord_id=interaction.guild.get_member_named(self.designer_name).id,
                is_active=True
            ).first()
            
            if not designer:
                await interaction.response.send_message(
                    "❌ Designer not found in database!",
                    ephemeral=True
                )
                return
            
            # Get the creator object
            creator = await Creator.filter(
                name=self.creator_name,
                is_active=True
            ).first()
            
            if not creator:
                await interaction.response.send_message(
                    "❌ Creator not found in database!",
                    ephemeral=True
                )
                return
            
            # Create thumbnail record in database
            thumbnail_record = await Thumbnail.create(
                designer=designer,
                creator=creator,
                youtube_url=self.youtube_url,
                category=self.category,
                completed_at=datetime.now()
            )
            
            # Update the original message to show completed (keep embed color as brand_red)
            original_embed = self.original_message.embeds[0]
            
            # Create a new view with completed button
            completed_view = discord.ui.View(timeout=None)
            completed_button = discord.ui.Button(
                label="Completed",
                style=discord.ButtonStyle.gray,
                emoji="✅",
                disabled=True
            )
            completed_view.add_item(completed_button)
            
            # Update the original message
            await self.original_message.edit(embed=original_embed, view=completed_view)
            
            # Send success message in private channel
            success_embed = discord.Embed(
                title="✅ Thumbnail Submitted",
                description=f"Thumbnail for **{self.creator_name}** has been recorded in the database!",
                color=discord.Color.green()
            )
            success_embed.add_field(name="Creator", value=self.creator_name, inline=True)
            success_embed.add_field(name="Category", value=self.category, inline=True)
            success_embed.add_field(name="Designer", value=self.designer_name, inline=True)
            success_embed.add_field(name="Record ID", value=f"#{thumbnail_record.id}", inline=True)
            
            await self.private_channel.send(embed=success_embed)
            
            # Send confirmation to overseer
            await interaction.response.send_message(
                f"✅ Thumbnail for **{self.creator_name}** has been recorded successfully! (ID: #{thumbnail_record.id})",
                ephemeral=True
            )
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error submitting thumbnail: {str(e)}",
                ephemeral=True
            )
