import discord
from discord.ext import commands
from database.models import GuildConfig, ThumbnailCategory

class Config(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    

    category = discord.app_commands.Group(name="category", description="Category commands")


    async def category_autocomplete(self, interaction: discord.Interaction, current: str):
        """Autocomplete for categories"""
        categories = await ThumbnailCategory.filter(
            name__icontains=current,
            is_active=True
        ).limit(10)
        choices = [
            discord.app_commands.Choice(name=category.name, value=category.name)
            for category in categories
        ]
        return choices


    @category.command(name="add-category", description="Add a category")
    @discord.app_commands.describe(category="The name of the category you'd like to add")
    async def add_category(self, interaction: discord.Interaction, category: str):
        """Add a category"""
        try:
            existing = await ThumbnailCategory.filter(name=category).first()
            if existing:
                if existing.is_active:
                    await interaction.response.send_message(
                        f"❌ Category **{category}** already exists!",
                        ephemeral=True
                    )
                    return
                else:
                    existing.is_active = True
                    await existing.save()
                    await interaction.response.send_message(
                        f"✅ Category **{category}** has been reactivated successfully!",
                        ephemeral=True
                    )
                    return
            
            # create the category
            category_obj = await ThumbnailCategory.create(name=category)

            await interaction.response.send_message(
                f"✅ Category **{category}** added successfully!",
                ephemeral=True
            )
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error adding category: {str(e)}",
                ephemeral=True
            )
    

    @category.command(name="remove-category", description="Remove a category")
    @discord.app_commands.describe(category="The name of the category you'd like to remove")
    @discord.app_commands.autocomplete(category=category_autocomplete)
    async def remove_category(self, interaction: discord.Interaction, category: str):
        """Remove a category"""
        try:
            # check if the category exists
            category_obj = await ThumbnailCategory.filter(
                name=category,
                is_active=True
            ).first()
            # if the category is not found, return an error
            if not category_obj:
                await interaction.response.send_message(
                    f"❌ Category **{category}** does not exist!",
                    ephemeral=True
                )
                return
            
            # if the category is found, mark it as inactive
            category_obj.is_active = False
            await category_obj.save()
            
            await interaction.response.send_message(
                f"✅ Category **{category}** removed successfully!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error removing category: {str(e)}",
                ephemeral=True
            )
    
    # list all categories
    @category.command(name="list-categories", description="List all categories")
    async def list_categories(self, interaction: discord.Interaction):
        """List all categories"""
        try:
            categories = await ThumbnailCategory.filter(is_active=True)
            if not categories:
                await interaction.response.send_message(
                    "❌ No categories found!",
                    ephemeral=True
                )
                return
            
            await interaction.response.send_message(
                f"✅ Categories: {', '.join([category.name for category in categories])}",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error listing categories: {str(e)}",
                ephemeral=True
            )
    

    @category.command(name="toggle-single-thumbnail-channel", description="Toggle single thumbnail channel")
    async def toggle_single_thumbnail_channel(self, interaction: discord.Interaction):
        """Toggle single thumbnail channel"""
        try:
            # get or create guild config
            guild_config, just_created = await GuildConfig.get_or_create(guild_id=interaction.guild.id)
            # enable/disable single thumbnail channel
            guild_config.single_thumbnail_channel = not guild_config.single_thumbnail_channel
            # push changes to the database
            await guild_config.save()

            await interaction.response.send_message(
                f"✅ Single thumbnail channel toggled {"on" if guild_config.single_thumbnail_channel else "off"}!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error toggling single thumbnail channel: {str(e)}",
                ephemeral=True
            )
    

    @category.command(name="set-single-thumbnail-channel", description="Set the channel for single thumbnail requests")
    @discord.app_commands.describe(channel="The channel to set for single thumbnail requests")
    async def set_single_thumbnail_channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        """Set the channel for single thumbnail requests"""
        try:  
            # get or create guild config
            guild_config, just_created = await GuildConfig.get_or_create(guild_id=interaction.guild.id)
            
            # set the single thumbnail channel by storing the channel id
            guild_config.single_thumbnail_channel_id = channel.id

            # push changes to the database
            await guild_config.save()

            await interaction.response.send_message(
                f"✅ Single thumbnail channel set to {channel.mention}!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error setting single thumbnail channel: {str(e)}",
                ephemeral=True
            )


    @category.command(name="set-category-channel", description="Set an existing channel as a thumbnail category channel")
    @discord.app_commands.describe(
        channel="The channel to add as a thumbnail category channel",
        category="The thumbnail category that the channel will correspond to"
    )
    @discord.app_commands.autocomplete(category=category_autocomplete)
    async def set_category_channel(self, interaction: discord.Interaction, channel: discord.TextChannel, category: str):
        """Set an existing channel as a thumbnail category channel"""
        try:
            # check if the category exists
            category_obj = await ThumbnailCategory.filter(name=category, is_active=True).first()
            if not category_obj:
                await interaction.response.send_message(
                    f"❌ Category **{category}** does not exist!",
                    ephemeral=True
                )
                return
            
            if not category_obj.is_active:
                await interaction.response.send_message(
                    f"❌ Category **{category}** is marked as inactive!",
                    ephemeral=True
                )
                return

            # not going to check if single thumbnail channel is enabled or not,
            # allow people to configure, even if it's not enabled

            # set the channel id that the category will correspond to
            category_obj.channel_id = channel.id

            # push changes to the database
            await category_obj.save()

            await interaction.response.send_message(
                f"✅ The channel for **{category}** has been set to {channel.mention}!",
                ephemeral=True
            )
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error setting category channel: {str(e)}",
                ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Config(bot))