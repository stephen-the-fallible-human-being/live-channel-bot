
import discord
from discord.ext import commands
from discord import app_commands

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

class YouTubeLinkModal(discord.ui.Modal, title='Submit YouTube Video'):
    def __init__(self):
        super().__init__()

    youtube_link = discord.ui.TextInput(
        label='YouTube Video Link',
        placeholder='Enter the YouTube video URL here...',
        required=True,
        max_length=500
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Store the YouTube link and show category select menu
        embed = discord.Embed(
            title="Select Category",
            description=f"YouTube Link: {self.youtube_link.value}\n\nPlease select a category for this video:",
            color=discord.Color.blue()
        )
        
        view = CategorySelectView(str(self.youtube_link.value))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

class CategorySelectView(discord.ui.View):
    def __init__(self, youtube_link: str):
        super().__init__(timeout=300)
        self.youtube_link = youtube_link

    @discord.ui.select(
        placeholder="Choose a category...",
        options=[
            discord.SelectOption(label="Large Streamer Content", value="a", emoji="🎮"),
            discord.SelectOption(label="IRL Content", value="b", emoji="🎬"),
            discord.SelectOption(label="Reactions/Gameplay", value="c", emoji="🎯")
        ]
    )
    async def category_select(self, interaction: discord.Interaction, select: discord.ui.Select):
        category_map = {
            "a": "Large Streamer Content",
            "b": "IRL Content", 
            "c": "Reactions/Gameplay"
        }
        
        selected_category = category_map[select.values[0]]
        
        # Find the target channel based on selection
        target_channel_name = select.values[0]  # "a", "b", or "c"
        target_channel = discord.utils.get(interaction.guild.channels, name=target_channel_name)
        
        if target_channel:
            # Create embed for the target channel
            embed = discord.Embed(
                title=f"New {selected_category} Submission",
                description=f"**YouTube Link:** {self.youtube_link}",
                color=discord.Color.green()
            )
            embed.add_field(name="Category", value=selected_category, inline=True)
            embed.add_field(name="Submitted by", value=interaction.user.mention, inline=True)
            
            # Send to target channel
            await target_channel.send(embed=embed)
            
            # Confirm to user
            await interaction.response.send_message(
                f"✅ Your submission has been sent to #{target_channel_name} channel!", 
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"❌ Channel '{target_channel_name}' not found. Please make sure channels 'a', 'b', and 'c' exist.",
                ephemeral=True
            )

class SubmitButtonView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Persistent view

    @discord.ui.button(label='Submit YouTube Video', style=discord.ButtonStyle.primary, emoji='📹')
    async def submit_video(self, interaction: discord.Interaction, button: discord.ui.Button):
        modal = YouTubeLinkModal()
        await interaction.response.send_modal(modal)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="setup_submit", description="Send a button for YouTube video submissions")
async def setup_submit(interaction: discord.Interaction):
    embed = discord.Embed(
        title="YouTube Video Submission",
        description="Click the button below to submit a YouTube video with category selection.",
        color=discord.Color.blue()
    )
    
    view = SubmitButtonView()
    await interaction.response.send_message(embed=embed, view=view)

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
# For production, use environment variables or Replit secrets
if __name__ == "__main__":
    # You'll need to add your bot token here or use Replit secrets
    bot.run('YOUR_BOT_TOKEN')  # Replace with your actual token
