"""
Manage Staff View
Main view for managing staff members
"""
import discord
from .manage_creators import ManageCreatorsView
from ..modals.assign_editor_modal import AssignEditorModal
from database.models import Editor, Creator


class ManageStaffView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        # manage creators button
        self.creators_button = discord.ui.Button(
            label="Manage Creators",
            style=discord.ButtonStyle.gray, 
            custom_id="manage-creators-button"
        )
        self.add_item(self.creators_button)
        self.creators_button.callback = self.creators_callback

        # assign editors button
        self.assign_editors_button = discord.ui.Button(
            label="Assign Editors",
            style=discord.ButtonStyle.gray,
            custom_id="assign-editors-button"
        )
        self.add_item(self.assign_editors_button)
        self.assign_editors_button.callback = self.assign_editor_callback

    async def creators_callback(self, interaction:discord.Interaction):
        add_delete_creator_view = ManageCreatorsView()
        await interaction.response.send_message(
            "Manage Creators:",
            view=add_delete_creator_view,
            ephemeral=True
        )
    
    async def assign_editor_callback(self, interaction: discord.Interaction):
        editors = await Editor.filter(soft_deleted=False).limit(25)
        if not editors:
            await interaction.response.send_message("No editors found in the database.", ephemeral=True)
            return

        creators = await Creator.filter(soft_deleted=False).limit(25)
        if not creators:
            await interaction.response.send_message("No creators found in the database.", ephemeral=True)
            return
        
        editor_options = [discord.SelectOption(label=e.discord_username, value=str(e.id)) for e in editors]
        creator_options = [discord.SelectOption(label=c.name, value=str(c.id)) for c in creators]

        assign_editor_modal = AssignEditorModal(editor_options=editor_options, creator_options=creator_options)

        await interaction.response.send_modal(modal=assign_editor_modal)
