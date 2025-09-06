"""
Thumbnail Request Modal
Handles the modal for requesting thumbnails
"""
import discord
from database.models import Creator, Editor, ThumbnailCategory, GuildConfig


class ThumbnailRequestModal(discord.ui.Modal):
    def __init__(self, editor, assigned_creators, available_categories):
        super().__init__(title="Request Thumbnail Design")
        self.editor = editor
        self.assigned_creators = assigned_creators
        self.available_categories = available_categories
        
        # Creator selection (select menu)
        self.creator_select = discord.ui.Select(
            label="Creator Select Menu:",
            placeholder="Select the creator for this video",
            options=[
                discord.SelectOption(
                    label=creator.name,
                    value=str(creator.id),
                    description=f"Creator: {creator.name}"
                ) for creator in assigned_creators
            ]
        )
        
        # Category selection (select menu) - only show available categories
        self.category_select = discord.ui.Select(
            label="Category Select Menu:",
            placeholder="Select the video category",
            options=[
                discord.SelectOption(
                    label=cat.category_name.title(),
                    value=cat.category_name,
                    description=f"{cat.category_name.title()} content"
                ) for cat in available_categories
            ]
        )
        
        # YouTube URL (text input)
        self.youtube_url = discord.ui.TextInput(
            label="YouTube Video URL",
            placeholder="https://www.youtube.com/watch?v=...",
            required=True,
            max_length=200
        )
        
        self.add_item(self.creator_select)
        self.add_item(self.category_select)
        self.add_item(self.youtube_url)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            # Defer the response immediately to prevent timeout
            await interaction.response.defer(ephemeral=True)
            
            # Check if any thumbnail categories exist
            categories = await ThumbnailCategory.filter(is_active=True).first()
            if not categories:
                await interaction.followup.send(
                    "❌ No thumbnail categories have been configured yet! Please ask an administrator to add existing channels as category channels first.",
                    ephemeral=True
                )
                return
            
            # Get the selected creator
            creator_id = int(self.creator_select.values[0])
            creator = await Creator.filter(id=creator_id, is_active=True).first()
            
            if not creator:
                await interaction.followup.send(
                    "❌ Selected creator not found or inactive!",
                    ephemeral=True
                )
                return
            
            # Get the selected category
            category = self.category_select.values[0]
            
            # Find the category channel
            category_channel = await ThumbnailCategory.filter(
                category_name=category.lower(),
                is_active=True
            ).first()
            
            if not category_channel:
                await interaction.followup.send(
                    f"❌ Category '{category}' channel not found! Please ask an administrator to add a channel for this category.",
                    ephemeral=True
                )
                return
            
            # Validate YouTube URL (basic check)
            if not self.youtube_url.value.startswith(('https://www.youtube.com/', 'https://youtu.be/')):
                await interaction.followup.send(
                    "❌ Please provide a valid YouTube URL!",
                    ephemeral=True
                )
                return
            
            # Get editor object
            editor_obj = await Editor.filter(
                discord_id=self.editor.id,
                is_active=True
            ).first()
            
            if not editor_obj:
                await interaction.followup.send(
                    "❌ You are not registered as an editor!",
                    ephemeral=True
                )
                return
            
            # Get guild config to check if single channel mode is enabled
            guild_config = await GuildConfig.filter(guild_id=interaction.guild.id).first()
            
            # Determine which channel to send to
            if guild_config and guild_config.single_thumbnail_channel and guild_config.single_thumbnail_channel_id:
                # Single channel mode - send to the configured channel
                channel = interaction.guild.get_channel(guild_config.single_thumbnail_channel_id)
                if not channel:
                    await interaction.followup.send(
                        f"❌ Single thumbnail channel not found! The channel may have been deleted.",
                        ephemeral=True
                    )
                    return
            else:
                # Category mode - send to the category-specific channel
                channel = interaction.guild.get_channel(category_channel.channel_id)
                if not channel:
                    await interaction.followup.send(
                        f"❌ Category channel for '{category}' not found! The channel may have been deleted.",
                        ephemeral=True
                    )
                    return
            
            # Import here to avoid circular imports
            from ..views.claim import ClaimRequestView
            
            # Create request embed
            embed = discord.Embed(
                title="🎨 Thumbnail Request",
                description=f"New thumbnail request for **{creator.name}**",
                color=discord.Color.brand_red()
            )
            embed.add_field(name="Creator", value=creator.name, inline=True)
            embed.add_field(name="Category", value=category, inline=True)
            embed.add_field(name="YouTube URL", value=self.youtube_url.value, inline=False)
            
            # Create claim button view
            view = ClaimRequestView(creator.name, category, self.youtube_url.value, self.editor.name)
            await channel.send(embed=embed, view=view)
            
            # Success response to editor
            success_embed = discord.Embed(
                title="✅ Thumbnail Request Submitted",
                description=f"Your thumbnail request has been sent to {channel.mention}!",
                color=discord.Color.green()
            )
            success_embed.add_field(name="Creator", value=creator.name, inline=True)
            success_embed.add_field(name="Category", value=category, inline=True)
            success_embed.add_field(name="Channel", value=channel.mention, inline=True)
            
            await interaction.followup.send(embed=success_embed, ephemeral=True)
            
        except Exception as e:
            await interaction.followup.send(
                f"❌ Error submitting request: {str(e)}",
                ephemeral=True
            )
