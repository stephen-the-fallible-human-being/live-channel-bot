"""
Role Events Cog
Handles automatic staff management based on Discord roles
"""
import discord
from discord.ext import commands
from database.models import Editor, ThumbnailDesigner, Overseer, GuildConfig


class RoleEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """" Role Event Listeners """

    @commands.Cog.listener("on_member_update")
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        try:
            # Get roles that were added and removed
            added_roles = set(after.roles) - set(before.roles)
            removed_roles = set(before.roles) - set(after.roles)
            
            # Handle added roles
            for role in added_roles:
                await self._handle_role_added(after, role)
            
            # Handle removed roles
            for role in removed_roles:
                await self._handle_role_removed(after, role)
                
        except Exception as e:
            print(f"Error in on_member_update: {e}")
    

    @commands.Cog.listener("on_member_remove")
    async def on_member_remove(self, member: discord.Member):
        try:
            for role in member.roles:
                await self._handle_role_removed(member, role)
        except Exception as e:
            print(f"Error in on_member_remove: {e}")


    async def _handle_role_added(self, member: discord.Member, role: discord.Role):
        print(f"Role '{role.name}' (ID: {role.id}) added to {member.name}")
        
        # Get guild config to check if this role is configured
        guild_config = await GuildConfig.filter(guild_id=member.guild.id).first()
        if not guild_config:
            return
        
        # Determine which type of role this is
        model_class = None
        role_type = None
        
        if role.id == guild_config.editor_role_id:
            model_class = Editor
            role_type = "Editor"
        elif role.id == guild_config.thumbnail_designer_role_id:
            model_class = ThumbnailDesigner
            role_type = "Thumbnail Designer"
        elif role.id == guild_config.overseer_role_id:
            model_class = Overseer
            role_type = "Overseer"
        else:
            return
        
        try:
            # Check if the user is already assigned to the added role
            existing = await model_class.filter(discord_id=member.id).first()
            
            if existing:
                # if the user already has the role, and is marked as active, do nothing
                if existing.is_active:
                    return
                # if the user already has the role, but is marked as inactive, reactivate them
                else:
                    existing.is_active = True
                    # update the username if it's different
                    if existing.discord_username != member.name:
                        existing.discord_username = member.name
                    await existing.save()
                    print(f"Reactivated {role_type} role for {member.name}")
            else:
                # Create new staff member
                staff_member = await model_class.create(
                    discord_id=member.id,
                    discord_username=member.name,
                    is_active=True
                )
                
                print(f"Added {role_type} role for {member.name}")
                
        except Exception as e:
            print(f"Error adding {role_type} role for {member.name}: {e}")


    async def _handle_role_removed(self, member, role):
        print(f"Role '{role.name}' (ID: {role.id}) removed from {member.name}")
        
        # Get guild config to check if this role is configured
        guild_config = await GuildConfig.filter(guild_id=member.guild.id).first()
        if not guild_config:
            return
        
        # Determine which type of role this is
        model_class = None
        role_type = None
        
        if role.id == guild_config.editor_role_id:
            model_class = Editor
            role_type = "Editor"
        elif role.id == guild_config.thumbnail_designer_role_id:
            model_class = ThumbnailDesigner
            role_type = "Thumbnail Designer"
        elif role.id == guild_config.overseer_role_id:
            model_class = Overseer
            role_type = "Overseer"
        else:
            return
        
        try:
            # Find and deactivate the staff member
            existing = await model_class.filter(discord_id=member.id).first()

            if existing and existing.is_active:
                existing.is_active = False
                await existing.save()
                print(f"Deactivated {role_type} role for {member.name}")
                
        except Exception as e:
            print(f"Error removing {role_type} role for {member.name}: {e}")
        


    """" Role Setting Commands """
    role = discord.app_commands.Group(name="role", description="Role setting commands")

    @role.command(name="set-editor-role", description="Set the role ID for editors")
    @discord.app_commands.describe(role="The role to set for editors")
    async def set_editor_role(self, interaction: discord.Interaction, role: discord.Role):
        """Set the role ID for editors in the database"""
        try:
            # Get or create guild config
            guild_config, created = await GuildConfig.get_or_create(
                guild_id=interaction.guild.id,
                defaults={}
            )
            
            # Update the role ID of the role to be set for editors
            guild_config.editor_role_id = role.id
            await guild_config.save()

            view = discord.ui.LayoutView()
            container = discord.ui.Container(
                discord.ui.TextDisplay(
                    "## Editor Role Set ✅\n"
                    f"**Role:** {role.mention}\n"
                    f"**Role ID:** {role.id}\n"
                ),
                accent_color=discord.Color.green(),
            )
            view.add_item(container)
            
            await interaction.response.send_message(view=view, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error setting editor role: {str(e)}", ephemeral=True)
    

    @role.command(name="set-thumbnail-designer-role", description="Set the role ID for thumbnail designers")
    @discord.app_commands.describe(role="The role to set for thumbnail designers")
    async def set_thumbnail_designer_role(self, interaction: discord.Interaction, role: discord.Role):
        """Set the role ID for thumbnail designers in the database"""
        try:
            # Get or create guild config
            guild_config, created = await GuildConfig.get_or_create(
                guild_id=interaction.guild.id,
                defaults={}
            )
            
            # Update the designer role ID
            guild_config.thumbnail_designer_role_id = role.id
            await guild_config.save()
            
            view = discord.ui.LayoutView()
            container = discord.ui.Container(
                discord.ui.TextDisplay(
                    "## ✅ Thumbnail Designer Role Set\n"
                    f"**Role:** {role.mention}\n"
                    f"**Role ID:** {role.id}"
                ),
                accent_color=discord.Color.green(),
            )
            view.add_item(container)
            
            await interaction.response.send_message(view=view, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error setting thumbnail designer role: {str(e)}", ephemeral=True)


    @role.command(name="set-overseer-role", description="Set the role ID for overseers")
    @discord.app_commands.describe(role="The role to set for overseers")
    async def set_overseer_role(self, interaction: discord.Interaction, role: discord.Role):
        """Set the role ID for overseers in the database"""
        try:
            # Get or create guild config
            guild_config, created = await GuildConfig.get_or_create(
                guild_id=interaction.guild.id,
                defaults={}
            )
            
            # Update the overseer role ID
            guild_config.overseer_role_id = role.id
            await guild_config.save()
            
            view = discord.ui.LayoutView()
            container = discord.ui.Container(
                discord.ui.TextDisplay(
                    "## ✅ Overseer Role Set\n"
                    f"**Role:** {role.mention}\n"
                    f"**Role ID:** {role.id}"
                ),
                accent_color=discord.Color.green(),
            )
            view.add_item(container)
            
            await interaction.response.send_message(view=view, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error setting overseer role: {str(e)}", ephemeral=True)


    @role.command(name="list-role-config", description="List current role configuration")
    async def list_role_config(self, interaction: discord.Interaction):
        """List the current role configuration for this server"""
        try:
            # Get guild config
            guild_config = await GuildConfig.filter(guild_id=interaction.guild.id).first()

            if not guild_config:
                await interaction.response.send_message(
                    f"❌ No role configuration found! Please set up roles first.",
                    ephemeral=True
                )
                return
            
            view = discord.ui.LayoutView()
            container = discord.ui.Container(
                discord.ui.TextDisplay(
                    "### ⚙️ Role Configuration"
                ),
                discord.ui.Separator()
            )
            if guild_config.editor_role_id:
                editor_role = interaction.guild.get_role(guild_config.editor_role_id)
                container.add_item(discord.ui.TextDisplay(
                    f"**Editor Role:**\n"
                    f"Role Name: {editor_role.mention}\n"
                    f"Role ID: {editor_role.id}"
                ))
            else:
                container.add_item(discord.ui.TextDisplay(
                    f"**Editor Role:** Not Set"
                ))
            if guild_config.thumbnail_designer_role_id:
                thumbnail_designer_role = interaction.guild.get_role(guild_config.thumbnail_designer_role_id)
                container.add_item(discord.ui.TextDisplay(
                    f"**Thumbnail Designer Role:**\n"
                    f"Role Name: {thumbnail_designer_role.mention}\n"
                    f"Role ID: {thumbnail_designer_role.id}"
                ))
            else:
                container.add_item(discord.ui.TextDisplay(
                    f"**Thumbnail Designer Role:** Not Set"
                ))
            if guild_config.overseer_role_id:
                overseer_role = interaction.guild.get_role(guild_config.overseer_role_id)
                container.add_item(discord.ui.TextDisplay(
                    f"**Overseer Role:**\n"
                    f"Role Name: {overseer_role.mention}\n"
                    f"Role ID: {overseer_role.id}"
                ))
            else:
                container.add_item(discord.ui.TextDisplay(
                    f"**Overseer Role:** Not Set"
                ))
            view.add_item(container)
            await interaction.response.send_message(view=view, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(f"❌ Error listing role config: {str(e)}", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(RoleEvents(bot))
