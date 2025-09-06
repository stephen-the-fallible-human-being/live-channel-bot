"""
Creator management commands
"""
import discord
from discord.ext import commands
from database.models import Creator
from .autocomplete import get_creator_names


class CreatorCommands:
    """Creator management command methods"""
    
    @commands.slash_command(name="add-creator", description="Add a non-Discord creator manually")
    async def add_creator(self, ctx, name: str):
        """Add a YouTube creator who is not on Discord"""
        try:
            # Check if creator already exists (active or inactive)
            existing = await Creator.filter(name=name).first()
            if existing:
                if existing.is_active:
                    await ctx.respond(f"❌ Creator '{name}' already exists and is active!", ephemeral=True)
                    return
                else:
                    # Reactivate inactive creator
                    existing.is_active = True
                    await existing.save()
                    
                    embed = discord.Embed(
                        title="✅ Creator Reactivated",
                        description=f"Successfully reactivated creator: **{name}**",
                        color=discord.Color.green()
                    )
                    embed.add_field(name="Creator ID", value=existing.id, inline=True)
                    embed.add_field(name="Status", value="Active", inline=True)
                    
                    await ctx.respond(embed=embed, ephemeral=True)
                    return
            
            # Create new creator
            creator = await Creator.create(
                name=name,
                is_active=True
            )
            
            embed = discord.Embed(
                title="✅ Creator Added",
                description=f"Successfully added creator: **{name}**",
                color=discord.Color.green()
            )
            embed.add_field(name="Creator ID", value=creator.id, inline=True)
            embed.add_field(name="Status", value="Active", inline=True)
            embed.add_field(name="Note", value="This creator is not on Discord", inline=False)
            
            await ctx.respond(embed=embed, ephemeral=True)
            
        except Exception as e:
            await ctx.respond(f"❌ Error adding creator: {str(e)}", ephemeral=True)

    @commands.slash_command(name="remove-creator", description="Remove a creator from the system")
    async def remove_creator(
        self, 
        ctx, 
        creator: discord.Option(str, description="Select a creator to remove", autocomplete=discord.utils.basic_autocomplete(get_creator_names))
    ):
        """Remove a creator from the system (soft delete)"""
        try:
            # Find the creator by exact name
            creator_obj = await Creator.filter(
                name=creator,
                is_active=True
            ).first()
            
            if not creator_obj:
                await ctx.respond(f"❌ Creator '{creator}' not found or already inactive!", ephemeral=True)
                return
            
            # Soft delete the creator
            creator_obj.is_active = False
            await creator_obj.save()
            
            # Create response embed
            embed = discord.Embed(
                title="✅ Creator Removed",
                description=f"Successfully removed creator: **{creator}**",
                color=discord.Color.red()
            )
            embed.add_field(name="Creator ID", value=creator_obj.id, inline=True)
            embed.add_field(name="Status", value="Inactive", inline=True)
            
            await ctx.respond(embed=embed, ephemeral=True)
            
        except Exception as e:
            await ctx.respond(f"❌ Error removing creator: {str(e)}", ephemeral=True)
