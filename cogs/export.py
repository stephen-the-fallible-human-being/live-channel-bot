import discord
from discord.ext import commands
from datetime import datetime
from database.models import Thumbnail
import pandas as pd
import io

class Export(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    export = discord.app_commands.Group(name="export", description="Export commands")


    @export.command(name="thumbnails-current-month", description="Export thumbnails for the current month")
    async def export_thumbnails_current_month(self, interaction: discord.Interaction):
        """Export thumbnail records for the current month as CSV file"""
        try:
            now = datetime.now()
            start_of_month = datetime(now.year, now.month, 1)
            if now.month == 12:
                end_of_month = datetime(now.year + 1, 1, 1)
            else:
                end_of_month = datetime(now.year, now.month + 1, 1)

            # query the db 
            rows = await Thumbnail.filter(
            created_at__gte=start_of_month,
            created_at__lt=end_of_month
            ).values(
                "id",
                "designer__discord_username",
                "creator__name",
                "category__name",
                "youtube_url",
                "created_at"
            ).order_by('created_at')
            
            # convert to dataframe, then to csv
            df = pd.DataFrame(rows)

            if df.empty:
                await interaction.response.send_message(
                    f"❌ No thumbnail records found for {now.strftime('%B %Y')}",
                    ephemeral=True
                )
                return

            # rename columns for better csv headers
            df.rename(columns={
                "id": "Thumbnail Record ID",
                "designer__discord_username": "Designer (Discord Username)",
                "creator__name": "Creator",
                "category__name": "Category",
                "youtube_url": "YouTube URL",
                "created_at": "Created Date"
            }, inplace=True)

            # create csv string
            csv_string = df.to_csv(index=False)

            # write to file and send
            filename = f"thumbnails_{now.strftime('%B_%Y')}.csv"
            file = discord.File(io.StringIO(csv_string), filename=filename)

            # view containing file
            view = discord.ui.LayoutView(
                discord.ui.TextDisplay(
                    f"📊 **Thumbnail Export of the Current Month**"
                ),
                discord.ui.File(file=file)
            )

            await interaction.response.send_message(view=view, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error exporting thumbnails: {str(e)}",
                ephemeral=True
            )


    @export.command(name="thumbnails-month", description="Export thumbnails for a specific month")
    @discord.app_commands.describe(
        month="The month to export thumbnails for",
        year="The year to export thumbnails for"
    )
    async def export_thumbnails_month(self, interaction: discord.Interaction, month: str, year: int):
        """Export thumbnail records for a specific month and year as CSV file"""
        try:
            # Month name to number mapping (full names only)
            month_mapping = {
                'January': 1,
                'February': 2,
                'March': 3,
                'April': 4,
                'May': 5,
                'June': 6,
                'July': 7,
                'August': 8,
                'September': 9,
                'October': 10,
                'November': 11,
                'December': 12
            }
            
            # Convert month name to number
            month_lower = month.lower()
            if month_lower not in month_mapping:
                await interaction.response.send_message(
                    "❌ Invalid month! Please use a full month name (e.g. January)",
                    ephemeral=True
                )
                return
        
            month_num = month_mapping[month_lower]

            # Calculate start and end of month
            start_of_month = datetime(year, month_num, 1)
            if month_num == 12:
                end_of_month = datetime(year + 1, 1, 1)
            else:
                end_of_month = datetime(year, month_num + 1, 1)

            # query the db 
            rows = await Thumbnail.filter(
            created_at__gte=start_of_month,
            created_at__lt=end_of_month
            ).values(
                "id",
                "designer__discord_username",
                "creator__name",
                "category__name",
                "youtube_url",
                "created_at"
            ).order_by('created_at')
            
            # convert to dataframe, then to csv
            df = pd.DataFrame(rows)

            if df.empty:
                await interaction.response.send_message(
                    f"❌ No thumbnail records found for {month} {year}",
                    ephemeral=True
                )
                return

            # rename columns for better csv headers
            df.rename(columns={
                "id": "Thumbnail Record ID",
                "designer__discord_username": "Designer (Discord Username)",
                "creator__name": "Creator",
                "category__name": "Category",
                "youtube_url": "YouTube URL",
                "created_at": "Created Date"
            }, inplace=True)

            # create csv string
            csv_string = df.to_csv(index=False)

            # write to file and send
            filename = f"thumbnails_{month}_{year}.csv"
            file = discord.File(io.StringIO(csv_string), filename=filename)

            view = discord.ui.LayoutView(
                discord.ui.TextDisplay(
                    f"📊 **Thumbnail Export for the Month of {month} {year}**"
                ),
                discord.ui.File(file=file)
            )
            await interaction.response.send_message(view=view, ephemeral=True)


        except Exception as e:
            await interaction.response.send_message(
                f"❌ Error exporting thumbnails: {str(e)}",
                ephemeral=True
            )