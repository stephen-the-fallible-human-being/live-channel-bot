"""
Staff management commands
"""
import discord
from discord.ext import commands
from database.models import Creator, Editor, Designer, Overseer
from .autocomplete import *
from .views.manage_staff_view import ManageStaffView


class StaffCommands:
    """Staff management command methods"""
    
    @commands.slash_command(name="list-staff", description="List all current staff members")
    async def list_staff(self, ctx):
        """List all current staff members"""
        try:
            embed = discord.Embed(
                title="👥 Staff Directory",
                description="Current staff members in the system",
                color=discord.Color.blue()
            )
            
            # Get all active staff
            creators = await Creator.filter(is_active=True)
            editors = await Editor.filter(is_active=True)
            designers = await Designer.filter(is_active=True)
            overseers = await Overseer.filter(is_active=True)
            
            # Add creator section
            if creators:
                creator_list = "\n".join([f"• {creator.name}" for creator in creators])
                embed.add_field(name=f"📺 Creators ({len(creators)})", value=creator_list, inline=False)
            else:
                embed.add_field(name="📺 Creators (0)", value="No creators added yet", inline=False)
            
            # Add editor section
            if editors:
                editor_list = "\n".join([f"• {editor.discord_username}" for editor in editors])
                embed.add_field(name=f"✂️ Editors ({len(editors)})", value=editor_list, inline=False)
            else:
                embed.add_field(name="✂️ Editors (0)", value="No editors added yet", inline=False)
            
            # Add designer section
            if designers:
                designer_list = "\n".join([f"• {designer.discord_username}" for designer in designers])
                embed.add_field(name=f"🎨 Designers ({len(designers)})", value=designer_list, inline=False)
            else:
                embed.add_field(name="🎨 Designers (0)", value="No designers added yet", inline=False)
            
            # Add overseer section
            if overseers:
                overseer_list = "\n".join([f"• {overseer.discord_username}" for overseer in overseers])
                embed.add_field(name=f"👑 Overseers ({len(overseers)})", value=overseer_list, inline=False)
            else:
                embed.add_field(name="👑 Overseers (0)", value="No overseers added yet", inline=False)
            
            await ctx.respond(embed=embed, ephemeral=True)
            
        except Exception as e:
            await ctx.respond(f"❌ Error listing staff: {str(e)}", ephemeral=True)

    @commands.slash_command(name="assign-editor", description="Assign an editor to creators")
    async def assign_editor(
        self, 
        ctx, 
        editor: discord.Option(str, description="Select an editor", autocomplete=discord.utils.basic_autocomplete(get_editor_names)),
        creator: discord.Option(str, description="Select a creator", autocomplete=discord.utils.basic_autocomplete(get_creator_names))
    ):
        """Assign an editor to a creator using Discord autocomplete"""
        try:
            # Find the editor by exact username
            editor_obj = await Editor.filter(
                discord_username=editor,
                is_active=True
            ).first()
            
            if not editor_obj:
                await ctx.respond(f"❌ Editor '{editor}' not found!", ephemeral=True)
                return
            
            # Find the creator by exact name
            creator_obj = await Creator.filter(
                name=creator,
                is_active=True
            ).first()
            
            if not creator_obj:
                await ctx.respond(f"❌ Creator '{creator}' not found!", ephemeral=True)
                return
            
            # Check if assignment already exists
            existing_assignments = await editor_obj.assigned_creators.filter(id=creator_obj.id)
            if existing_assignments:
                await ctx.respond(f"❌ Editor **{editor}** is already assigned to creator **{creator}**!", ephemeral=True)
                return
            
            # Assign creator to editor
            await editor_obj.assigned_creators.add(creator_obj)
            
            # Create response embed
            embed = discord.Embed(
                title="✅ Editor Assignment Complete",
                description=f"Successfully assigned editor **{editor}** to creator **{creator}**",
                color=discord.Color.green()
            )
            embed.add_field(name="Editor", value=editor, inline=True)
            embed.add_field(name="Creator", value=creator, inline=True)
            
            await ctx.respond(embed=embed, ephemeral=True)
            
        except Exception as e:
            await ctx.respond(f"❌ Error assigning editor: {str(e)}", ephemeral=True)

    @commands.slash_command(name="unassign-editor", description="Remove an editor's assignment to a creator")
    async def unassign_editor(
        self, 
        ctx, 
        editor: discord.Option(str, description="Select an editor", autocomplete=discord.utils.basic_autocomplete(get_editor_names)),
        creator: discord.Option(str, description="Select a creator", autocomplete=discord.utils.basic_autocomplete(get_creator_names))
    ):
        """Remove an editor's assignment to a creator using Discord autocomplete"""
        try:
            # Find the editor by exact username
            editor_obj = await Editor.filter(
                discord_username=editor,
                is_active=True
            ).first()
            
            if not editor_obj:
                await ctx.respond(f"❌ Editor '{editor}' not found!", ephemeral=True)
                return
            
            # Find the creator by exact name
            creator_obj = await Creator.filter(
                name=creator,
                is_active=True
            ).first()
            
            if not creator_obj:
                await ctx.respond(f"❌ Creator '{creator}' not found!", ephemeral=True)
                return
            
            # Check if assignment exists
            existing_assignments = await editor_obj.assigned_creators.filter(id=creator_obj.id)
            if not existing_assignments:
                await ctx.respond(f"❌ Editor **{editor}** is not assigned to creator **{creator}**!", ephemeral=True)
                return
            
            # Remove creator from editor
            await editor_obj.assigned_creators.remove(creator_obj)
            
            # Create response embed
            embed = discord.Embed(
                title="✅ Editor Unassignment Complete",
                description=f"Successfully unassigned editor **{editor}** from creator **{creator}**",
                color=discord.Color.orange()
            )
            embed.add_field(name="Editor", value=editor, inline=True)
            embed.add_field(name="Creator", value=creator, inline=True)
            
            await ctx.respond(embed=embed, ephemeral=True)
            
        except Exception as e:
            await ctx.respond(f"❌ Error unassigning editor: {str(e)}", ephemeral=True)

    @commands.slash_command(name="list-assignments", description="List all editor-creator assignments")
    async def list_assignments(self, ctx):
        """List all current editor-creator assignments"""
        try:
            # Get all active editors with their assignments
            editors = await Editor.filter(is_active=True).prefetch_related('assigned_creators')
            
            embed = discord.Embed(
                title="📋 Editor-Creator Assignments",
                description="Current assignments in the system",
                color=discord.Color.blue()
            )
            
            if not editors:
                embed.add_field(name="No Editors", value="No active editors found", inline=False)
            else:
                for editor in editors:
                    assigned_creators = await editor.assigned_creators.filter(is_active=True)
                    
                    if assigned_creators:
                        creator_list = "\n".join([f"• {creator.name}" for creator in assigned_creators])
                        embed.add_field(
                            name=f"✂️ {editor.discord_username} ({len(assigned_creators)} creators)",
                            value=creator_list,
                            inline=False
                        )
                    else:
                        embed.add_field(
                            name=f"✂️ {editor.discord_username} (0 creators)",
                            value="No assignments",
                            inline=False
                        )
            
            await ctx.respond(embed=embed, ephemeral=True)
            
        except Exception as e:
            await ctx.respond(f"❌ Error listing assignments: {str(e)}", ephemeral=True)

    @commands.slash_command(name="show-editor-assignments", description="Show assignments for a specific editor")
    async def show_editor_assignments(
        self, 
        ctx, 
        editor: discord.Option(str, description="Select an editor", autocomplete=discord.utils.basic_autocomplete(get_editor_names))
    ):
        """Show assignments for a specific editor using Discord autocomplete"""
        try:
            # Find the editor by exact username
            editor_obj = await Editor.filter(
                discord_username=editor,
                is_active=True
            ).prefetch_related('assigned_creators').first()
            
            if not editor_obj:
                await ctx.respond(f"❌ Editor '{editor}' not found!", ephemeral=True)
                return
            
            # Get assigned creators
            assigned_creators = await editor_obj.assigned_creators.filter(is_active=True)
            
            embed = discord.Embed(
                title=f"📋 Assignments for {editor}",
                description=f"Editor ID: {editor_obj.id}",
                color=discord.Color.blue()
            )
            
            if assigned_creators:
                creator_list = "\n".join([f"• {creator.name}" for creator in assigned_creators])
                embed.add_field(
                    name=f"📺 Assigned Creators ({len(assigned_creators)})",
                    value=creator_list,
                    inline=False
                )
            else:
                embed.add_field(
                    name="📺 Assigned Creators (0)",
                    value="No creators assigned",
                    inline=False
                )
            
            await ctx.respond(embed=embed, ephemeral=True)
            
        except Exception as e:
            await ctx.respond(f"❌ Error showing editor assignments: {str(e)}", ephemeral=True)

    @commands.slash_command(name="manage-staff", description="Open staff management interface")
    async def manage_staff(self, ctx):
        """Open the staff management interface with buttons"""
        try:
            embed = discord.Embed(
                title="👥 Staff Management",
                description="Use the buttons below to manage staff members",
                color=discord.Color.blue()
            )
            embed.add_field(
                name="Available Actions",
                value="• **Manage Creators** - Add or remove creators\n• **Assign Editors** - Assign editors to creators",
                inline=False
            )
            
            view = ManageStaffView()
            await ctx.respond(embed=embed, view=view, ephemeral=True)
            
        except Exception as e:
            await ctx.respond(f"❌ Error opening staff management: {str(e)}", ephemeral=True)
