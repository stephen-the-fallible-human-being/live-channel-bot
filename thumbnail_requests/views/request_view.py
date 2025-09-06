"""
Thumbnail Request View
Main view containing the request thumbnail button
"""
import discord
from .request_button import RequestThumbnailButton


class ThumbnailRequestView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(RequestThumbnailButton())
