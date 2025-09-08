import discord
from discord.ext import commands
from database.models import GuildConfig, ThumbnailCategory, Editor, Creator, Overseer, ThumbnailDesigner, Thumbnail
from dataclasses import dataclass

def is_valid_youtube_url(url: str):
    """Check if the provided URL is a valid YouTube URL"""
    return "youtube.com" in url or "youtu.be" in url


@dataclass
class ThumbnailRequestData:
    creator_id: int
    creator_name: str
    video_url: str
    category_id: int
    category_name: str
    original_message_id: int = None
    original_message_channel_id: int = None
    designer_id: int = None


# Big Note: ComponentsV2 cannot be sent with message content / embeds
class ThumbnailClaimView(discord.ui.View):
    def __init__(self, thumbnail_request_data: ThumbnailRequestData):
        super().__init__(timeout=None)
        self.thumbnail_request_data = thumbnail_request_data

        self.claim_button = discord.ui.Button(
            label="Claim",
            style=discord.ButtonStyle.green,
            emoji="✋",
            custom_id=f"claim_button_{self.thumbnail_request_data.video_url}"
        )
        self.claim_button.callback = self.claim_callback
        
        self.add_item(self.claim_button)

    async def claim_callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True)
            self.claim_button.disabled = True
            self.claim_button.label = f"Claimed by {interaction.user.name}"
            self.claim_button.style = discord.ButtonStyle.gray
            content = interaction.message.content
            await interaction.message.edit(content=content, view=self)

            # create private channel (thumbnail + username of claimant)
            channel_name = f"thumbnail-{interaction.user.name.lower().replace(' ', '-')}"
            guild_config = await GuildConfig.filter(guild_id=interaction.guild.id).first()
            overseer_role = interaction.guild.get_role(guild_config.overseer_role_id)
            overwrites = {
                # everyone
                interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
                # claimant
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                # all overseers (for now)
                overseer_role: discord.PermissionOverwrite(view_channel=True, send_messages=True),
                # bot itself
                interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True)
            }
            private_channel = await interaction.guild.create_text_channel(
                name=channel_name,
                overwrites=overwrites
            )

            # create private channel view (submit and unclaim buttons)
            self.thumbnail_request_data.designer_id = interaction.user.id
            self.thumbnail_request_data.original_message_id = interaction.message.id
            self.thumbnail_request_data.original_message_channel_id = interaction.message.channel.id
            view = PrivateChannelView(thumbnail_request_data=self.thumbnail_request_data)
            private_channel_msg = await private_channel.send(
                f"**{interaction.user.name}** has offered to help out with a thumbnail request\n"
                f"Creator: {self.thumbnail_request_data.creator_name}\n"
                f"Category: {self.thumbnail_request_data.category_name}\n"
                f"Video URL: {self.thumbnail_request_data.video_url}",
                view=view
            )

            # pin the message
            await private_channel_msg.pin()

            # confirmation message
            await interaction.followup.send(
                f"You have claimed the thumbnail request for **{self.thumbnail_request_data.creator_name}**",
                ephemeral=True
            )
        except Exception as e:
            await interaction.followup.send(
                f"❌ Error claiming thumbnail request: {str(e)}",
                ephemeral=True
            )


class PrivateChannelView(discord.ui.View): 
    def __init__(self, thumbnail_request_data: ThumbnailRequestData):
        super().__init__(timeout=None)
        self.thumbnail_request_data = thumbnail_request_data

        self.unclaim_button = discord.ui.Button(
            label="Unclaim",
            style=discord.ButtonStyle.red,
            emoji="✋",
            custom_id=f"unclaim_button_{self.thumbnail_request_data.video_url}"
        )
        self.unclaim_button.callback = self.unclaim_callback

        self.add_item(self.unclaim_button)

        self.approve_button = discord.ui.Button(
            label="Approve Thumbnail",
            style=discord.ButtonStyle.success,
            emoji="✅",
            custom_id=f"approve_button_{self.thumbnail_request_data.video_url}"
        )
        self.approve_button.callback = self.approve_callback

        self.add_item(self.approve_button)
        
    async def unclaim_callback(self, interaction: discord.Interaction):
        try:
            # delete original claim view
            message_id = self.thumbnail_request_data.original_message_id
            channel_id = self.thumbnail_request_data.original_message_channel_id
            original_channel = interaction.guild.get_channel(channel_id)
            original_message = await original_channel.fetch_message(message_id)
            await original_message.delete()

            # create brand new claim view
            view = ThumbnailClaimView(thumbnail_request_data=self.thumbnail_request_data)
            await original_channel.send(content=original_message.content, view=view)

            # delete private channel
            private_channel = interaction.channel
            await private_channel.delete()
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error unclaiming request: {str(e)}",
                ephemeral=True
            )

    async def approve_callback(self, interaction: discord.Interaction):
        try:
            # check if user is an overseer or administrator
            if not interaction.user.guild_permissions.administrator:
                guild_config = await GuildConfig.filter(guild_id=interaction.guild.id).first()
                overseer = await Overseer.filter(discord_id=interaction.user.id, is_active=True).first()
                if not overseer:
                    await interaction.response.send_message(
                        "❌ You are not authorized to approve thumbnails!",
                        ephemeral=True
                    )
                    return
            
            # ask if the clicker wants to record the thumbnail in the database
            view = discord.ui.LayoutView(timeout=None)
            view.add_item(discord.ui.TextDisplay(
                "Would you like to record this thumbnail in the database?"
            ))
            confirm_button = discord.ui.Button(
                label="Yes",
                style=discord.ButtonStyle.success,
                emoji="✅",
                custom_id=f"confirm_button_{self.thumbnail_request_data.video_url}"
            )
            confirm_button.callback = self.confirm_callback
            cancel_button = discord.ui.Button(
                label="No",
                style=discord.ButtonStyle.danger,
                emoji="❌",
                custom_id=f"cancel_button_{self.thumbnail_request_data.video_url}"
            )
            cancel_button.callback = self.cancel_callback
            view.add_item(discord.ui.ActionRow(
                confirm_button,
                cancel_button
            ))
            await interaction.response.send_message(view=view, ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error approving thumbnail: {str(e)}",
                ephemeral=True
            )

    async def cancel_callback(self, interaction: discord.Interaction):
        try:
            await interaction.response.send_message(
                "✅ Approval cancelled!",
                ephemeral=True
            )

        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error cancelling approval: {str(e)}",
                ephemeral=True
            )

    async def confirm_callback(self, interaction: discord.Interaction):
        try:
            # get the designer object
            designer = await ThumbnailDesigner.filter(
                discord_id=self.thumbnail_request_data.designer_id,
                is_active=True
            ).first()
            if not designer:
                await interaction.response.send_message(
                    "❌ Designer not found!",
                    ephemeral=True
                )
                return
            
            # get the creator object
            creator = await Creator.filter(
                id=self.thumbnail_request_data.creator_id,
                is_active=True
            ).first()
            if not creator:
                await interaction.response.send_message(
                    "❌ Creator not found!",
                    ephemeral=True
                )
                return

            # get the category object
            category = await ThumbnailCategory.filter(
                id=self.thumbnail_request_data.category_id,
                is_active=True
            ).first()
            if not category:
                await interaction.response.send_message(
                    "❌ Category not found!",
                    ephemeral=True
                )
                return
                        
            # create a thumbnail record in the database
            thumbnail_record = await Thumbnail.create(
                designer=designer,
                creator=creator,
                category=category,
                youtube_url=self.thumbnail_request_data.video_url
            )

            # mark original claim view as completed
            completed_view = discord.ui.View(timeout=None)
            completed_button = discord.ui.Button(
                label="Completed",
                style=discord.ButtonStyle.gray,
                emoji="✅",
                disabled=True
            )
            completed_view.add_item(completed_button)
            original_channel = interaction.guild.get_channel(self.thumbnail_request_data.original_message_channel_id)
            original_message = await original_channel.fetch_message(self.thumbnail_request_data.original_message_id)
            await original_message.edit(content=original_message.content, view=completed_view)
            
            # confirmation message
            view = discord.ui.LayoutView()
            view.add_item(discord.ui.TextDisplay(
                f"✅ Thumbnail recorded in the database!\n"
                f"Creator: {creator.name}\n"
                f"Category: {category.name}\n"
                f"Designer: {designer.discord_username}\n"
                f"Video URL: {self.thumbnail_request_data.video_url}"
            ))
            await interaction.response.send_message(view=view, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error approving thumbnail: {str(e)}",
                ephemeral=True
            )


async def creator_autocomplete(interaction: discord.Interaction, current: str):
    """Autocomplete for creators (Assumes the user is an administrator or editor)"""
    if interaction.user.guild_permissions.administrator:
        creators = await Creator.filter(
            name__icontains=current,
            is_active=True
        ).limit(10)
        return [discord.app_commands.Choice(name=creator.name, value=creator.name) for creator in creators]
    else:
        creators = await Creator.filter(
            name__icontains=current,
            is_active=True,
            assigned_editors__discord_id=interaction.user.id
        ).limit(10)
        return [discord.app_commands.Choice(name=creator.name, value=creator.name) for creator in creators]


async def category_autocomplete(interaction: discord.Interaction, current: str):
    """Autocomplete for categories"""
    categories = await ThumbnailCategory.filter(
        name__icontains=current,
        is_active=True
    ).limit(10)
    return [discord.app_commands.Choice(name=category.name, value=category.name) for category in categories]



class ThumbnailRequest(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    thumbnail = discord.app_commands.Group(name="thumbnail", description="Thumbnail request commands")


    @thumbnail.command(name="request-thumbnail", description="Send a thumbnail request")
    @discord.app_commands.describe(
        creator="The creator of the video that you want to request a thumbnail for",
        video_url="The URL of the video",
        category="The category of the video (optional for single channel mode)"
    )
    @discord.app_commands.autocomplete(creator=creator_autocomplete)
    @discord.app_commands.autocomplete(category=category_autocomplete)
    async def send_thumbnail_request(
        self,
        interaction: discord.Interaction,
        creator: str,
        video_url: str,
        category: str = None
    ):
        """Send a thumbnail request"""
        try:
            # Check if all required roles are configured
            guild_config = await GuildConfig.filter(guild_id=interaction.guild.id).first()
            if not guild_config:
                await interaction.response.send_message(
                    f"❌ Role configuration not found\n"
                    "Make sure to set the editor, designer, and overseer roles first",
                    ephemeral=True
                )
                return
            
            missing_roles = []
            if not guild_config.editor_role_id:
                missing_roles.append("Editor")
            if not guild_config.thumbnail_designer_role_id:
                missing_roles.append("Thumbnail Designer")
            if not guild_config.overseer_role_id:
                missing_roles.append("Overseer")
            
            if missing_roles:
                roles_text = ", ".join(missing_roles)
                await interaction.response.send_message(
                    f"❌ The following roles are not configured: **{roles_text}**",
                    ephemeral=True
                )
                return
            
            # if all roles are configured, check if single thumbnail channel is enabled
            if guild_config.single_thumbnail_channel:
                # if single channel is enabled but no channel is configured, return an error
                if not guild_config.single_thumbnail_channel_id:
                    await interaction.response.send_message(
                        "❌ Single thumbnail channel mode is enabled but no channel is configured! Please use `/set-single-thumbnail-channel` to set a channel first",
                        ephemeral=True
                    )
                    return
                
                # if a category is optionally provided, check if the category exists
                if category:
                    category_obj = await ThumbnailCategory.filter(category_name=category, is_active=True).first()
                    if not category_obj:
                        await interaction.response.send_message(
                            f"❌ Category **{category}** does not exist!",
                            ephemeral=True
                        )
                        return
                
                # set the destination channel as the single thumbnail channel
                destination_channel_id = guild_config.single_thumbnail_channel_id
            
            # if single channel mode is not enabled
            else:
                # check if a category is provided
                if not category:
                    await interaction.response.send_message(
                        "❌ Category is required when single thumbnail channel mode is not enabled",
                        ephemeral=True
                    )
                    return

                # check if the category exists
                category_obj = await ThumbnailCategory.filter(name=category, is_active=True).first()
                if not category_obj:
                    await interaction.response.send_message(
                        f"❌ Category **{category}** does not exist!",
                        ephemeral=True
                    )
                    return

                # if the category doesn't have a corresponding channel configured, return an error
                if not category_obj.channel_id:
                    await interaction.response.send_message(
                        f"❌ Category **{category}** does not have a corresponding channel configured!",
                        ephemeral=True
                    )
                    return
                
                # set the destination channel as the channel that corresponds to the category
                destination_channel_id = category_obj.channel_id
            
            # check if the creator exists
            creator_obj = await Creator.filter(name=creator, is_active=True).first()
            if not creator_obj:
                await interaction.response.send_message(
                    f"❌ Creator **{creator}** does not exist!",
                    ephemeral=True
                )
                return
            
            # check if the command was invoked by an administrator
            if not interaction.user.guild_permissions.administrator:
                # check if invoked by an editor
                if not guild_config.editor_role_id in [role.id for role in interaction.user.roles]:
                    await interaction.response.send_message(
                        "❌ You are not authorized to use this command! (Editors and Administrators only)",
                        ephemeral=True
                    )
                    return
                # check if the editor is one of the assigned editors to the creator
                if not creator_obj.assigned_editors.filter(discord_id=interaction.user.id).exists():
                    await interaction.response.send_message(
                        "❌ You are not assigned to the selected creator!",
                        ephemeral=True
                    )
                    return

            # get the destination channel
            destination_channel = interaction.guild.get_channel(destination_channel_id)
            thumbnail_request_data = ThumbnailRequestData(
                creator_id=creator_obj.id,
                creator_name=creator,
                video_url=video_url,
                category_name=category,
                category_id=category_obj.id
            )
            view = ThumbnailClaimView(thumbnail_request_data=thumbnail_request_data)
            await destination_channel.send(
                f"New thumbnail request for **{creator}**\n"
                f"Category: {category}\n"
                f"Video URL: {video_url}\n",
                view=view
            )

            # confirmation message
            await interaction.response.send_message(
                f"✅ Thumbnail request sent to {destination_channel.mention}",
                ephemeral=True
            )
 
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error sending thumbnail request: {str(e)}",
                ephemeral=True
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(ThumbnailRequest(bot))
