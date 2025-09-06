"""
Thumbnail Request Commands
Handles all slash commands for thumbnail requests
"""
import discord
from discord.ext import commands
from database.models import GuildConfig, ThumbnailCategory
from .views.request_view import ThumbnailRequestView
from .export import export_thumbnails_current_month, export_thumbnails_month


class ThumbnailCommands:
    """Commands for thumbnail request management"""
    
    @commands.slash_command(name="send-thumbnail-request-panel", description="Send a thumbnail request panel")
    async def send_thumbnail_request_panel(self, ctx):
        """Create a thumbnail request panel with a button for editors"""
        try:
            # Check if all required roles are configured
            guild_config = await GuildConfig.filter(guild_id=ctx.guild.id).first()
            
            missing_roles = []
            if not guild_config or not guild_config.editor_role_id:
                missing_roles.append("Editor")
            if not guild_config or not guild_config.thumbnail_designer_role_id:
                missing_roles.append("Designer")
            if not guild_config or not guild_config.overseer_role_id:
                missing_roles.append("Overseer")
            
            if missing_roles:
                roles_text = ", ".join(missing_roles)
                await ctx.respond(
                    f"❌ The following roles are not configured: **{roles_text}**\n"
                    f"Please use `/set-editor-role`, `/set-designer-role`, and `/set-overseer-role` to configure all required roles first.",
                    ephemeral=True
                )
                return
            
            # Check configuration based on mode
            guild_config = await GuildConfig.filter(guild_id=ctx.guild.id).first()
            
            if guild_config and guild_config.single_thumbnail_channel:
                # Single channel mode - check if channel is configured
                if not guild_config.single_thumbnail_channel_id:
                    await ctx.respond(
                        "❌ Single thumbnail channel mode is enabled but no channel is configured! Please use `/set-single-thumbnail-channel` to set a channel first.",
                        ephemeral=True
                    )
                    return
            else:
                # Category mode - check if any thumbnail categories exist
                categories = await ThumbnailCategory.filter(is_active=True).first()
                if not categories:
                    await ctx.respond(
                        "❌ No thumbnail categories have been configured yet! Please use `/add-thumbnail-category-channel` to add existing channels as category channels first.",
                        ephemeral=True
                    )
                    return
            
            # Determine mode description
            if guild_config and guild_config.single_thumbnail_channel:
                mode_description = "All thumbnail requests will be sent to a single channel."
            else:
                mode_description = "Thumbnail requests will be sent to category-specific channels."
            
            embed = discord.Embed(
                title="🎨 Thumbnail Request System",
                description=f"Click the button below to request a thumbnail design for your video.\n\n**Mode:** {mode_description}",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="How it works:",
                value="1. Click 'Request Thumbnail' button\n"
                      "2. Select the creator from the dropdown\n"
                      "3. Choose the video category\n"
                      "4. Provide the YouTube URL\n"
                      "5. Submit your request",
                inline=False
            )
            embed.add_field(
                name="Requirements:",
                value="• You must be an active editor\n"
                      "• You must be assigned to the creator\n"
                      "• Valid YouTube URL required",
                inline=False
            )
            
            view = ThumbnailRequestView()
            await ctx.respond(embed=embed, view=view)
            
        except Exception as e:
            await ctx.respond(f"❌ Error creating request panel: {str(e)}")



    @commands.slash_command(name="list-thumbnail-categories", description="List all thumbnail categories")
    async def list_thumbnail_categories(self, ctx):
        """List all thumbnail categories and their channels"""
        try:
            categories = await ThumbnailCategory.filter(is_active=True).order_by('category_name')
            
            embed = discord.Embed(
                title="📂 Thumbnail Categories",
                description=f"Total categories: {len(categories)}",
                color=discord.Color.blue()
            )
            
            if not categories:
                embed.add_field(name="No Categories", value="No thumbnail categories found. Use `/add-thumbnail-category-channel` to add existing channels as category channels.", inline=False)
            else:
                for category in categories:
                    channel_mention = f"<#{category.channel_id}>"
                    embed.add_field(
                        name=f"🎨 {category.category_name.title()}",
                        value=f"Channel: {channel_mention}\nName: `{category.channel_name}`",
                        inline=True
                    )
            
            await ctx.respond(embed=embed)
            
        except Exception as e:
            await ctx.respond(f"❌ Error listing categories: {str(e)}")

    @commands.slash_command(name="remove-thumbnail-category", description="Remove a channel from being a thumbnail category")
    async def remove_thumbnail_category(self, ctx, category_name: str):
        """Remove a channel from being a thumbnail category (does not delete the Discord channel)"""
        try:
            # Find the category
            category = await ThumbnailCategory.filter(
                category_name=category_name.lower(),
                is_active=True
            ).first()
            
            if not category:
                await ctx.respond(f"❌ Category '{category_name}' not found!")
                return
            
            # Get the channel
            channel = ctx.guild.get_channel(category.channel_id)
            
            # Deactivate in database (don't delete the actual Discord channel)
            category.is_active = False
            await category.save()
            
            embed = discord.Embed(
                title="✅ Category Removed",
                description=f"Successfully removed **{category_name}** from thumbnail categories",
                color=discord.Color.orange()
            )
            embed.add_field(name="Category Name", value=category_name, inline=True)
            if channel:
                embed.add_field(name="Channel", value=f"{channel.mention} (still exists)", inline=True)
            else:
                embed.add_field(name="Channel", value="❌ Channel not found", inline=True)
            embed.add_field(name="Note", value="The Discord channel was not deleted, only removed from thumbnail categories.", inline=False)
            
            await ctx.respond(embed=embed, ephemeral=True)
            
        except Exception as e:
            await ctx.respond(f"❌ Error removing category: {str(e)}", ephemeral=True)

    @commands.slash_command(name="export-thumbnails-current-month", description="Export thumbnail records for the current month as CSV")
    async def export_thumbnails_current_month_cmd(self, ctx):
        """Export thumbnail records for the current month as CSV file"""
        await export_thumbnails_current_month(ctx)

    @commands.slash_command(name="export-thumbnails-month", description="Export thumbnail records for a specific month as CSV")
    async def export_thumbnails_month_cmd(self, ctx, year: int, month: str):
        """Export thumbnail records for a specific month and year as CSV file"""
        await export_thumbnails_month(ctx, year, month)

    @commands.slash_command(name="toggle-single-thumbnail-channel", description="Toggle between single channel and category channels for thumbnail requests")
    async def toggle_single_thumbnail_channel(self, ctx):
        """Toggle between single channel and category channels for thumbnail requests"""
        try:
            # Get or create guild config
            guild_config, created = await GuildConfig.get_or_create(guild_id=ctx.guild.id)
            
            # Toggle the setting
            guild_config.single_thumbnail_channel = not guild_config.single_thumbnail_channel
            
            if guild_config.single_thumbnail_channel:
                # If enabling single channel, clear the channel ID
                guild_config.single_thumbnail_channel_id = None
                await guild_config.save()
                
                embed = discord.Embed(
                    title="✅ Single Channel Mode Enabled",
                    description="Thumbnail requests will now be sent to a single channel instead of category-specific channels.",
                    color=discord.Color.green()
                )
                embed.add_field(
                    name="Next Step",
                    value="Use `/set-single-thumbnail-channel` to specify which channel should receive all thumbnail requests.",
                    inline=False
                )
            else:
                await guild_config.save()
                
                embed = discord.Embed(
                    title="✅ Category Channels Mode Enabled",
                    description="Thumbnail requests will now be sent to category-specific channels.",
                    color=discord.Color.blue()
                )
                embed.add_field(
                    name="Next Step",
                    value="Use `/add-thumbnail-category-channel` to add channels for different categories.",
                    inline=False
                )
            
            await ctx.respond(embed=embed, ephemeral=True)
            
        except Exception as e:
            await ctx.respond(f"❌ Error toggling single channel mode: {str(e)}", ephemeral=True)

    @commands.slash_command(name="set-single-thumbnail-channel", description="Set the channel for single thumbnail requests")
    async def set_single_thumbnail_channel(self, ctx, channel: discord.TextChannel):
        """Set the channel for single thumbnail requests"""
        try:
            # Get or create guild config
            guild_config, created = await GuildConfig.get_or_create(guild_id=ctx.guild.id)
            
            # Set the channel
            guild_config.single_thumbnail_channel = True
            guild_config.single_thumbnail_channel_id = channel.id
            await guild_config.save()
            
            embed = discord.Embed(
                title="✅ Single Thumbnail Channel Set",
                description=f"All thumbnail requests will now be sent to {channel.mention}",
                color=discord.Color.green()
            )
            embed.add_field(name="Channel", value=channel.mention, inline=True)
            embed.add_field(name="Channel ID", value=str(channel.id), inline=True)
            
            await ctx.respond(embed=embed, ephemeral=True)
            
        except Exception as e:
            await ctx.respond(f"❌ Error setting single thumbnail channel: {str(e)}", ephemeral=True)

    @commands.slash_command(name="add-thumbnail-category-channel", description="Add an existing channel as a thumbnail category channel")
    async def add_thumbnail_category_channel(self, ctx, channel: discord.TextChannel, category_name: str):
        """Add an existing channel as a thumbnail category channel"""
        try:
            # Check if category already exists
            existing_category = await ThumbnailCategory.filter(
                category_name=category_name.lower(),
                is_active=True
            ).first()
            
            if existing_category:
                await ctx.respond(f"❌ Category '{category_name}' already exists!")
                return
            
            # Check if channel is already used by another category
            existing_channel = await ThumbnailCategory.filter(
                channel_id=channel.id,
                is_active=True
            ).first()
            
            if existing_channel:
                await ctx.respond(f"❌ Channel {channel.mention} is already used by category '{existing_channel.category_name}'!")
                return
            
            # Store in database
            category_channel = await ThumbnailCategory.create(
                category_name=category_name.lower(),
                channel_id=channel.id,
                channel_name=channel.name,
                is_active=True
            )
            
            # Create welcome embed
            embed = discord.Embed(
                title=f"🎨 {category_name} Thumbnail Requests",
                description=f"Welcome to the {category_name} thumbnail request channel!",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="How it works:",
                value="• Editors submit thumbnail requests here\n"
                      "• Designers can claim requests using the claim button\n"
                      "• Private channels are created for claimed requests",
                inline=False
            )
            
            await channel.send(embed=embed)
            
            # Success response
            success_embed = discord.Embed(
                title="✅ Category Channel Added",
                description=f"Successfully added {channel.mention} as category: **{category_name}**",
                color=discord.Color.green()
            )
            success_embed.add_field(name="Category Name", value=category_name, inline=True)
            success_embed.add_field(name="Channel", value=channel.mention, inline=True)
            
            await ctx.respond(embed=success_embed, ephemeral=True)
            
        except Exception as e:
            await ctx.respond(f"❌ Error adding category channel: {str(e)}", ephemeral=True)

    @commands.slash_command(name="show-thumbnail-config", description="Show current thumbnail request configuration")
    async def show_thumbnail_config(self, ctx):
        """Show current thumbnail request configuration"""
        try:
            # Get guild config
            guild_config = await GuildConfig.filter(guild_id=ctx.guild.id).first()
            
            embed = discord.Embed(
                title="🎨 Thumbnail Request Configuration",
                description="Current settings for thumbnail requests",
                color=discord.Color.blue()
            )
            
            if not guild_config:
                embed.add_field(
                    name="Configuration",
                    value="No configuration found. Use `/toggle-single-thumbnail-channel` to get started.",
                    inline=False
                )
            else:
                # Show mode
                if guild_config.single_thumbnail_channel:
                    embed.add_field(
                        name="Mode",
                        value="🔄 **Single Channel Mode**",
                        inline=False
                    )
                    
                    if guild_config.single_thumbnail_channel_id:
                        channel = ctx.guild.get_channel(guild_config.single_thumbnail_channel_id)
                        if channel:
                            embed.add_field(
                                name="Single Channel",
                                value=f"{channel.mention}",
                                inline=True
                            )
                        else:
                            embed.add_field(
                                name="Single Channel",
                                value="❌ Channel not found (may have been deleted)",
                                inline=True
                            )
                    else:
                        embed.add_field(
                            name="Single Channel",
                            value="❌ Not configured",
                            inline=True
                        )
                else:
                    embed.add_field(
                        name="Mode",
                        value="📂 **Category Channels Mode**",
                        inline=False
                    )
                    
                    # Show categories
                    categories = await ThumbnailCategory.filter(is_active=True).order_by('category_name')
                    if categories:
                        category_list = []
                        for cat in categories:
                            channel = ctx.guild.get_channel(cat.channel_id)
                            if channel:
                                category_list.append(f"• **{cat.category_name.title()}** → {channel.mention}")
                            else:
                                category_list.append(f"• **{cat.category_name.title()}** → ❌ Channel not found")
                        
                        embed.add_field(
                            name=f"Category Channels ({len(categories)})",
                            value="\n".join(category_list),
                            inline=False
                        )
                    else:
                        embed.add_field(
                            name="Category Channels",
                            value="No categories configured",
                            inline=False
                        )
            
            await ctx.respond(embed=embed, ephemeral=True)
            
        except Exception as e:
            await ctx.respond(f"❌ Error showing configuration: {str(e)}", ephemeral=True)
