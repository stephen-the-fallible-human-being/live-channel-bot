import discord

class AddDeleteView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_button = discord.ui.Button(
            label="Add",
            style=discord.ButtonStyle.green
        )
        self.add_item(self.add_button)
        self.add_button.callback = self.add_callback

        self.delete_button = discord.ui.Button(
            label="Delete",
            style=discord.ButtonStyle.red
        )
        self.add_item(self.delete_button)
        self.delete_button.callback = self.delete_callback
    
    # callback that should be overwritten
    async def add_callback(self, interaction:discord.Interaction):
        await interaction.response.send_message("Add")

    async def delete_callback(self, interaction:discord.Interaction):
        await interaction.response.send_message("Delete")