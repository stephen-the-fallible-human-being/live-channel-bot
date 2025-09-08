import discord
from discord.ext import commands
from database.models import Editor, Creator

class StaffManagement(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    staff = discord.app_commands.Group(name="staff", description="Staff management commands")

    async def editor_active_autocomplete(self, interaction: discord.Interaction, current: str):
        """Autocomplete for editors"""
        editors = await Editor.filter(
            is_active=True,
            discord_username__icontains=current
        ).limit(10)
        choices = [
            discord.app_commands.Choice(name=editor.discord_username, value=editor.discord_username)
            for editor in editors
        ]
        return choices
    

    async def creator_active_autocomplete(self, interaction: discord.Interaction, current: str):
        """Autocomplete for creators"""
        creators = await Creator.filter(
            is_active=True,
            name__icontains=current
        ).limit(10)
        choices = [
            discord.app_commands.Choice(name=creator.name, value=creator.name)
            for creator in creators
        ]
        return choices


    @staff.command(name="assign-editor", description="Assign an editor to a creator")
    @discord.app_commands.describe(editor_name="The editor to assign", creator_name="The creator to assign")
    @discord.app_commands.autocomplete(editor_name=editor_active_autocomplete)
    @discord.app_commands.autocomplete(creator_name=creator_active_autocomplete)
    async def assign_editor(self, interaction: discord.Interaction, editor_name: str, creator_name: str):
        """Assign an editor to a creator"""
        try:
            # Find the editor and check if active
            editor = await Editor.filter(discord_username=editor_name).first()

            if not editor:
                await interaction.response.send_message(
                    f"❌ Editor '{editor_name}' not found!",
                    ephemeral=True
                )
                return
            if not editor.is_active:
                await interaction.response.send_message(
                    f"❌ Editor '{editor_name}' is not active!",
                    ephemeral=True
                )
                return

            # Find the creator and check if active
            creator = await Creator.filter(name=creator_name).first()
            
            if not creator:
                await interaction.response.send_message(
                    f"❌ Creator '{creator_name}' not found!",
                    ephemeral=True
                )
                return
            if not creator.is_active:
                await interaction.response.send_message(
                    f"❌ Creator '{creator_name}' is not active!",
                    ephemeral=True
                )
                return
            
            # Check if assignment already exists
            existing_assignments = await editor.assigned_creators.filter(name=creator_name)
            if existing_assignments:
                await interaction.response.send_message(
                    f"❌ Editor '{editor_name}' is already assigned to creator '{creator_name}'!",
                    ephemeral=True
                )
                return
            
            # Assign creator to editor
            await editor.assigned_creators.add(creator)
            await interaction.response.send_message(
                f"✅ **Editor:** {editor_name} has been assigned to **Creator:** {creator_name}",
                ephemeral=True
            )
        
        # Error handling
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error assigning editor: {str(e)}",
                ephemeral=True
            )

    
    async def find_editor_given_creator(self, interaction: discord.Interaction, current: str):
        """Find an editor given a creator passed in to the other parameter"""
        creator_name = interaction.namespace.creator_name

        if not creator_name:
            editors = await Editor.filter(is_active=True).limit(10)
            choices = [
                discord.app_commands.Choice(name=editor.discord_username, value=editor.discord_username)
                for editor in editors
            ]
            return choices
        else:
            editors = await Editor.filter(
                assigned_creators__name=creator_name,
                discord_username__icontains=current,
                is_active=True
            ).limit(10)
            choices = [
                discord.app_commands.Choice(name=editor.discord_username, value=editor.discord_username)
                for editor in editors
            ]
            return choices


    async def find_creator_given_editor(self, interaction: discord.Interaction, current: str):
        """Find an creator given a editor passed in to the other parameter"""
        # gotta access the namespace of the interaction to get the given creator name
        editor_name = interaction.namespace.editor_name

        # if an editor name has not been passed in, return first 25 creators
        if not editor_name:
            creators = await Creator.filter(is_active=True).limit(10)
            choices = [
                discord.app_commands.Choice(name=creator.name, value=creator.name)
                for creator in creators
            ]
        # else, return first 25 creators that the editor is assigned to AND contains current string
        else:
            creators = await Creator.filter(
                assigned_editors__discord_username=editor_name,
                name__icontains=current,
                is_active=True
            ).limit(10)
            choices = [
                discord.app_commands.Choice(name=creator.name, value=creator.name)
                for creator in creators
            ]
        
        return choices


    @staff.command(name="unassign-editor", description="Unassign an editor from a creator")
    @discord.app_commands.describe(editor_name="The editor to unassign", creator_name="The creator to unassign")
    @discord.app_commands.autocomplete(editor_name=find_editor_given_creator)
    @discord.app_commands.autocomplete(creator_name=find_creator_given_editor)
    async def unassign_editor(self, interaction: discord.Interaction, editor_name: str, creator_name: str):
        """Unassign an editor from a creator"""
        try:
            # Find the editor, check if active
            editor = await Editor.filter(discord_username=editor_name).first()

            if not editor:
                await interaction.response.send_message(
                    f"❌ Editor '{editor_name}' not found!",
                    ephemeral=True
                )
                return
            if not editor.is_active:
                await interaction.response.send_message(
                    f"❌ Editor '{editor_name}' is not active!",
                    ephemeral=True
                )
                return

            # Find the creator, check if active
            creator = await Creator.filter(name=creator_name).first()
            
            if not creator:
                await interaction.response.send_message(
                    f"❌ Creator '{creator_name}' not found!",
                    ephemeral=True
                )
                return
            if not creator.is_active:
                await interaction.response.send_message(
                    f"❌ Creator '{creator_name}' is not active!",
                    ephemeral=True
                )
                return
            
            # Check if assignment between editor and creator exists
            is_assigned = await editor.assigned_creators.filter(name=creator_name).exists()
            if not is_assigned:
                await interaction.response.send_message(
                    f"❌ Editor '{editor_name}' is not assigned to creator '{creator_name}'!",
                    ephemeral=True
                )
                return
            
            # Unassign creator from editor
            await editor.assigned_creators.remove(creator)
            await interaction.response.send_message(
                f"✅ **Editor:** {editor_name} has been unassigned from **Creator:** {creator_name}",
                ephemeral=True
            )
        
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error unassigning editor: {str(e)}",
                ephemeral=True
            )


    async def editor_all_autocomplete(self, interaction: discord.Interaction, current: str):
        """Autocomplete for all editors"""
        editors = await Editor.filter(discord_username__icontains=current).limit(5)
        choices = [
            discord.app_commands.Choice(name=editor.discord_username, value=editor.discord_username)
            for editor in editors
        ]
        return choices


    async def creator_all_autocomplete(self, interaction: discord.Interaction, current: str):
        """Autocomplete for all creators"""
        creators = await Creator.filter(name__icontains=current).limit(5)
        choices = [
            discord.app_commands.Choice(name=creator.name, value=creator.name)
            for creator in creators
        ]
        return choices
    

    @staff.command(name="list-editor-assignments", description="List all creators that an editor is assigned to")
    @discord.app_commands.describe(editor_name="The editor to list assignments for")
    @discord.app_commands.autocomplete(editor_name=editor_all_autocomplete)
    async def list_editor_assignments(self, interaction: discord.Interaction, editor_name: str):
        """List all creators that an editor is assigned to"""
        try:
            # Check if editor exists
            editor = await Editor.filter(discord_username=editor_name).first()
            if not editor:
                await interaction.response.send_message(
                    f"❌ Editor '{editor_name}' not found!",
                    ephemeral=True
                )
                return
            
            # List all creators that the editor is assigned to
            creators = await editor.assigned_creators.all()
            if not creators:
                await interaction.response.send_message(
                    f"❌ Editor '{editor_name}' is not assigned to any creators!",
                    ephemeral=True
                )
                return
            
            view = discord.ui.LayoutView()
            container = discord.ui.Container(
                discord.ui.TextDisplay(f"### Creators assigned to {editor_name}:"),
                discord.ui.TextDisplay("\n".join([f"• {creator.name}" for creator in creators]))
            )
            view.add_item(container)
            await interaction.response.send_message(view=view, ephemeral=True)
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error listing editor assignments: {str(e)}",
                ephemeral=True
            )
    
    @staff.command(name="list-creator-assignments", description="List all editors that are assigned to a creator")
    @discord.app_commands.describe(creator_name="The creator to list assignments for")
    @discord.app_commands.autocomplete(creator_name=creator_all_autocomplete)
    async def list_creator_assignments(self, interaction: discord.Interaction, creator_name: str):
        """List all editors that are assigned to a creator"""
        try:
            # Check if creator exists
            creator = await Creator.filter(name=creator_name).first()
            if not creator:
                await interaction.response.send_message(
                    f"❌ Creator '{creator_name}' not found!",
                    ephemeral=True
                )
                return
            
            # List all editors that are assigned to the creator
            editors = await creator.assigned_editors.all()
            if not editors:
                await interaction.response.send_message(
                    f"❌ Creator '{creator_name}' is not assigned to any editors!",
                    ephemeral=True
                )
                return
            
            view = discord.ui.LayoutView()
            container = discord.ui.Container(
                discord.ui.TextDisplay(f"### Editors assigned to {creator_name}:"),
                discord.ui.TextDisplay("\n".join([f"• {editor.discord_username}" for editor in editors]))
            )
            view.add_item(container)
            await interaction.response.send_message(view=view, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error listing creator assignments: {str(e)}",
                ephemeral=True
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(StaffManagement(bot))