"""
Claim Request Button
Handles claiming thumbnail requests and creating private channels
"""
import discord
from database.models import Designer, Editor, GuildConfig
from .unclaim import UnclaimButton
from .submit import SubmitButton


class ClaimRequestButton(discord.ui.Button):
    def __init__(self, creator_name, category, youtube_url, editor_name):
        super().__init__(
            label="Claim Request",
            style=discord.ButtonStyle.green,
            emoji="✋"
        )
        self.creator_name = creator_name
        self.category = category
        self.youtube_url = youtube_url
        self.editor_name = editor_name

    async def callback(self, interaction: discord.Interaction):
        try:
            # Check if user is a designer
            designer = await Designer.filter(
                discord_id=interaction.user.id,
                is_active=True
            ).first()
            
            if not designer:
                await interaction.response.send_message(
                    "❌ You are not registered as a designer!",
                    ephemeral=True
                )
                return
            
            # Disable the button
            self.disabled = True
            self.label = f"Claimed by {interaction.user.name}"
            self.style = discord.ButtonStyle.gray
            self.emoji = "✋"
            
            # Update the message (keep embed color as brand_red)
            await interaction.message.edit(embed=interaction.message.embeds[0], view=self.view)
            
            # Get the editor object to find their overseers
            editor_obj = await Editor.filter(
                discord_id=interaction.guild.get_member_named(self.editor_name).id,
                is_active=True
            ).first()
            
            if not editor_obj:
                await interaction.response.send_message(
                    "❌ Error: Editor not found in database!",
                    ephemeral=True
                )
                return
            
            # Create private channel name
            channel_name = f"thumbnail-{self.creator_name.lower().replace(' ', '-')}-{interaction.user.name.lower().replace(' ', '-')}"
            
            # Create private channel
            private_channel = await interaction.guild.create_text_channel(
                name=channel_name,
                topic=f"Private thumbnail request for {self.creator_name} - Designer: {interaction.user.name}",
                reason=f"Thumbnail request claimed by {interaction.user.name}"
            )
            
            # Get the overseer role from guild config
            guild_config = await GuildConfig.filter(guild_id=interaction.guild.id).first()
            
            if guild_config and guild_config.overseer_role_id:
                overseer_role = interaction.guild.get_role(guild_config.overseer_role_id)
                if overseer_role:
                    # Allow the designer and overseer role to see the channel
                    await private_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
                    await private_channel.set_permissions(overseer_role, read_messages=True, send_messages=True)
                    
                    # Deny everyone else
                    await private_channel.set_permissions(interaction.guild.default_role, read_messages=False, send_messages=False)
                else:
                    # Fallback: just allow the designer
                    await private_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
                    await private_channel.set_permissions(interaction.guild.default_role, read_messages=False, send_messages=False)
            else:
                # Fallback: just allow the designer
                await private_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
                await private_channel.set_permissions(interaction.guild.default_role, read_messages=False, send_messages=False)
            
            # Create control message with unclaim and submit buttons
            control_embed = discord.Embed(
                title="🎨 Thumbnail Request Control Panel",
                description=f"**Creator:** {self.creator_name}\n**Category:** {self.category}\n**YouTube URL:** {self.youtube_url}\n**Designer:** {interaction.user.name}",
                color=discord.Color.blue()
            )
            control_embed.add_field(
                name="Actions",
                value="• **Unclaim** - Close this channel and reset the claim\n• **Submit** - Mark thumbnail as completed",
                inline=False
            )
            
            control_view = PrivateChannelView(
                self.creator_name, 
                self.category, 
                self.youtube_url, 
                interaction.user.name,
                interaction.message,
                private_channel,
                self.editor_name
            )
            
            control_message = await private_channel.send(embed=control_embed, view=control_view)
            
            # Pin the control message
            await control_message.pin()
            
            # Send confirmation to designer
            await interaction.response.send_message(
                f"✅ You have claimed the thumbnail request for **{self.creator_name}**!\nPrivate channel created: {private_channel.mention}",
                ephemeral=True
            )
            
        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error claiming request: {str(e)}",
                ephemeral=True
            )


class PrivateChannelView(discord.ui.View):
    def __init__(self, creator_name, category, youtube_url, designer_name, original_message, private_channel, editor_name):
        super().__init__(timeout=None)
        self.add_item(UnclaimButton(original_message, private_channel, editor_name))
        self.add_item(SubmitButton(creator_name, category, youtube_url, designer_name, original_message, private_channel))


class ClaimRequestView(discord.ui.View):
    def __init__(self, creator_name, category, youtube_url, editor_name):
        super().__init__(timeout=None)
        self.add_item(ClaimRequestButton(creator_name, category, youtube_url, editor_name))
