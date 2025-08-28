import discord

from .add_delete_creator_view import AddDeleteCreatorView

class ManageStaffView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

        self.creators_button = discord.ui.Button(
            label="Manage Creators",
            style=discord.ButtonStyle.gray, 
            custom_id="manage-creators-button"
        )
        self.add_item(self.creators_button)
        self.creators_button.callback = self.creators_callback

        self.channel_managers_button = discord.ui.Button(
            label="Manage Editors",
            style=discord.ButtonStyle.gray,
            custom_id="manage-editors-button"
        )
        self.add_item(self.channel_managers_button)
        self.channel_managers_button.callback = self.channel_managers_callback

    async def creators_callback(self, interaction:discord.Interaction):
        add_delete_creator_view = AddDeleteCreatorView()
        await interaction.response.send_message("Manage Creators:", view=add_delete_creator_view, ephemeral=True)
    
    async def channel_managers_callback(self, interaction:discord.Interaction):
        await interaction.response.send_message("Manage Editors:", ephemeral=True)