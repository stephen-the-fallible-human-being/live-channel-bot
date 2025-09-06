"""
Thumbnail Requests Package
Handles all thumbnail request functionality
"""

from .core import ThumbnailRequests


def setup(bot):
    bot.add_cog(ThumbnailRequests(bot))
