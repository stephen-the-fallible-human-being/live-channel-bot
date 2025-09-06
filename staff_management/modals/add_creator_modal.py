"""
Add Creator Modal
Handles adding new creators to the system
"""
import discord
from database.models import Creator


class AddCreatorModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Add A Creator Modal")
    
        self.creator_name = discord.ui.InputText(
            label="Enter the Creator Name:",
            placeholder="Creator Name",
            style=discord.InputTextStyle.short
        )
        self.add_item(self.creator_name)
    
    async def callback(self, interaction: discord.Interaction):
        # defer response because adding to database might take time
        await interaction.response.defer()
        
        # extract the creator name from form submission
        creator_name = self.creator_name.value

        # check if creator already exists
        creator = await Creator.filter(name=creator_name).first()

        # if creator already exists and wasnt deleted
        if creator and creator.soft_deleted == False:
            await interaction.followup.send(
                f"Creator **{creator.name}** already exists",
                ephemeral=True
            )
            return

        # if creator already exists, but was deleted
        if creator and creator.soft_deleted == True:
            creator.soft_deleted = False
            await creator.save()
            await interaction.followup.send(
                f"Revived Creator **{creator.name}**",
                ephemeral=True
            )
            return
        
        # if creator doesn't exist
        creator = await Creator.create(name=creator_name)
        await interaction.followup.send(
            f"You have added **{creator_name}** as a creator",
            ephemeral=True
        )
