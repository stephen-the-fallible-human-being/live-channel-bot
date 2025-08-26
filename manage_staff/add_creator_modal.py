import discord

class AddCreatorModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Add A Creator Modal")
    
        self.creator_name = discord.ui.InputText(
            label="Enter the Creator Name:",
            placeholder="Creator Name",
            style=discord.InputTextStyle.short
        )
        self.add_item(self.creator_name)
    
    async def on_submit(self, interaction: discord.Interaction):
        # defer response because adding to database might take time
        await interaction.response.defer()

        creator_name = self.creator_name.value

        # add to database
        await interaction.response.send_message(f"You have added {creator_name} as a creator.", ephemeral=True)