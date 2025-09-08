import discord
from discord.ext import commands
from database.models import Creator

class Creators(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    creator = discord.app_commands.Group(name="creator", description="Creator commands")

    @creator.command(name="add-creator", description="Add a creator to the database")
    @discord.app_commands.describe(name="The name of the creator")
    async def add_creator(self, interaction: discord.Interaction, name: str):
        """Add a creator to the database"""
        try:
            existing = await Creator.filter(name=name).first()

            if existing: # if creator already exists
                if existing.is_active: # if creator is marked as active
                    await interaction.response.send_message(
                        f"❌ Creator '{name}' already exists and is active!",
                        ephemeral=True
                    )
                    return
                else: # if creator is marked as inactive
                    existing.is_active = True
                    await existing.save()
                    view = discord.ui.LayoutView()
                    container = discord.ui.Container(
                        discord.ui.TextDisplay(
                            "### Creator Reactivated ✅\n"
                            f"Successfully reactivated creator: **{name}**"
                        )
                    )
                    view.add_item(container)
                    await interaction.response.send_message(view=view, ephemeral=True)
                    return
            # if creator does not exist, create it
            creator = await Creator.create(name=name, is_active=True)
            view = discord.ui.LayoutView()
            container = discord.ui.Container(
                discord.ui.TextDisplay(
                    "### Creator Added ✅\n"
                    f"Successfully added creator: **{name}**"
                )
            )
            view.add_item(container)
            await interaction.response.send_message(view=view, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error adding creator: {str(e)}",
                ephemeral=True
            )
    
    @creator.command(name="remove-creator", description="Remove a creator from the database")
    @discord.app_commands.describe(name="The name of the creator")
    async def remove_creator(self, interaction: discord.Interaction, name: str):
        """Remove a creator from the database"""
        try:
            existing = await Creator.filter(name=name).first()

            if not existing:
                await interaction.response.send_message(
                    f"❌ Creator '{name}' does not exist!",
                    ephemeral=True
                )
                return
            existing.is_active = False
            await existing.save()
            view = discord.ui.LayoutView()
            container = discord.ui.Container(
                discord.ui.TextDisplay(
                    "### Creator Removed ✅\n"
                    f"Successfully removed creator: **{name}**"
                )
            )
            view.add_item(container)
            await interaction.response.send_message(view=view, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error removing creator: {str(e)}",
                ephemeral=True
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(Creators(bot))