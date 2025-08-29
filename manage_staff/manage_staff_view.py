import discord

from .manage_creators import ManageCreatorsView

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

    async def creators_callback(self, interaction:discord.Interaction):
        add_delete_creator_view = ManageCreatorsView()
        await interaction.response.send_message(
            "Manage Creators:",
            view=add_delete_creator_view,
            ephemeral=True
        )