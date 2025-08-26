import discord

class UnclaimView(discord.ui.View):
    def __init__(self):
        super().__init__()
        # unclaim button
        self.unclaim_button = discord.ui.Button(
        label="Unclaim",
        style=discord.ButtonStyle.red
        )
        self.add_item(self.unclaim_button)
        
        # submit button
        self.submit_button = discord.ui.Button(
        label="Submit",
        style=discord.ButtonStyle.blurple,
        emoji="📝"
        )
        self.add_item(self.submit_button)

