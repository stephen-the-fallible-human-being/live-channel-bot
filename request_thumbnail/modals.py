
import discord

class RequestThumbnailModal(discord.ui.Modal, title='Request Thumbnail'):
    def __init__(self):
        super().__init__()

    youtube_link = discord.ui.TextInput(
        label='YouTube Video Link',
        placeholder='Enter the YouTube video URL here...',
        required=True,
        max_length=500
    )

    async def on_submit(self, interaction: discord.Interaction):
        # Show category selection after YouTube link submission
        embed = discord.Embed(
            title="Select Category",
            description=f"YouTube Link: {self.youtube_link.value}\n\nPlease select a category for this thumbnail request:",
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
            discord.SelectOption(label="a - Large Streamer Content", value="a"),
            discord.SelectOption(label="b - IRL Content", value="b"),
            discord.SelectOption(label="c - Reactions/Gaming", value="c")
        ]
    )
    async def category_select(self, select: discord.ui.Select, interaction: discord.Interaction):
        from .utils import send_claim_message
        
        category_map = {
            "a": "Large Streamer Content",
            "b": "IRL Content", 
            "c": "Reactions/Gaming"
        }
        
        selected_category = category_map[select.values[0]]
        target_channel_name = select.values[0]  # "a", "b", or "c"
        
        success = await send_claim_message(
            interaction, 
            self.youtube_link, 
            selected_category, 
            target_channel_name
        )
        
        if success:
            await interaction.response.send_message(
                f"✅ Your thumbnail request has been sent to #{target_channel_name} channel!", 
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"❌ Channel '{target_channel_name}' not found. Please make sure channels 'a', 'b', and 'c' exist.",
                ephemeral=True
            )
