"""
Export functionality for thumbnail records
Handles CSV export of thumbnail data
"""
import discord
from discord.ext import commands
from database.models import Thumbnail
import io
import pandas as pd
from datetime import datetime


async def export_thumbnails_current_month(ctx):
    """Export thumbnail records for the current month as CSV file"""
    try:
        # Get current month and year
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        if now.month == 12:
            end_of_month = datetime(now.year + 1, 1, 1)
        else:
            end_of_month = datetime(now.year, now.month + 1, 1)
        
        # Use Tortoise ORM values() method for efficient data retrieval
        rows = await Thumbnail.filter(
            completed_at__gte=start_of_month,
            completed_at__lt=end_of_month
        ).values(
            "id",
            "category",
            "youtube_url",
            "completed_at",
            "designer__discord_username",
            "creator__name"
        ).order_by('completed_at')
        
        # Convert to DataFrame
        df = pd.DataFrame(rows)
        
        # Rename columns for better CSV headers
        df = df.rename(columns={
            'id': 'Record ID',
            'creator__name': 'Creator',
            'designer__discord_username': 'Designer',
            'category': 'Category',
            'youtube_url': 'YouTube URL',
            'completed_at': 'Completed Date'
        })
        
        if df.empty:
            await ctx.respond(f"❌ No thumbnail records found for {now.strftime('%B %Y')}")
            return
        
        # Create file
        filename = f"thumbnails_{now.strftime('%Y_%m')}.csv"
        
        # Export to CSV using pandas
        csv_content = df.to_csv(index=False, encoding='utf-8')
        
        # Send file
        await ctx.respond(
            f"📊 **Thumbnail Export - {now.strftime('%B %Y')}**\n"
            f"Total records: **{len(df)}**\n"
            f"File: `{filename}`",
            file=discord.File(
                io.StringIO(csv_content),
                filename=filename
            )
        )
        
    except Exception as e:
        await ctx.respond(f"❌ Error exporting thumbnails: {str(e)}")


async def export_thumbnails_month(ctx, year: int, month: str):
    """Export thumbnail records for a specific month and year as CSV file"""
    try:
        # Month name to number mapping (full names only)
        month_mapping = {
            'january': 1,
            'february': 2,
            'march': 3,
            'april': 4,
            'may': 5,
            'june': 6,
            'july': 7,
            'august': 8,
            'september': 9,
            'october': 10,
            'november': 11,
            'december': 12
        }
        
        # Convert month name to number
        month_lower = month.lower()
        if month_lower not in month_mapping:
            await ctx.respond("❌ Invalid month! Please use a full month name (e.g., 'January', 'February', etc.)")
            return
        
        month_num = month_mapping[month_lower]
        
        # Validate year
        if year < 2020 or year > 2030:
            await ctx.respond("❌ Year must be between 2020 and 2030!")
            return
        
        # Calculate start and end of month
        start_of_month = datetime(year, month_num, 1)
        if month_num == 12:
            end_of_month = datetime(year + 1, 1, 1)
        else:
            end_of_month = datetime(year, month_num + 1, 1)
        
        # Use Tortoise ORM values() method for efficient data retrieval
        rows = await Thumbnail.filter(
            completed_at__gte=start_of_month,
            completed_at__lt=end_of_month
        ).values(
            "id",
            "category",
            "youtube_url",
            "completed_at",
            "designer__discord_username",
            "creator__name"
        ).order_by('completed_at')
        
        # Convert to DataFrame
        df = pd.DataFrame(rows)
        
        # Rename columns for better CSV headers
        df = df.rename(columns={
            'id': 'Record ID',
            'creator__name': 'Creator',
            'designer__discord_username': 'Designer',
            'category': 'Category',
            'youtube_url': 'YouTube URL',
            'completed_at': 'Completed Date'
        })
        
        if df.empty:
            month_name = start_of_month.strftime('%B')
            await ctx.respond(f"❌ No thumbnail records found for {month_name} {year}")
            return
        
        # Create file
        month_name = start_of_month.strftime('%B')
        filename = f"thumbnails-{month_num:02d}-{year}.csv"
        
        # Export to CSV using pandas
        csv_content = df.to_csv(index=False, encoding='utf-8')
        
        # Send file
        await ctx.respond(
            f"📊 **Thumbnail Export - {month_name} {year}**\n"
            f"Total records: **{len(df)}**\n"
            f"File: `{filename}`",
            file=discord.File(
                io.StringIO(csv_content),
                filename=filename
            )
        )
        
    except Exception as e:
        await ctx.respond(f"❌ Error exporting thumbnails: {str(e)}")
