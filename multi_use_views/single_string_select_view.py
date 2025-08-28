import discord
from typing import Callable, Awaitable, List, Tuple

class SingleStringSelectView(discord.ui.View):
    def __init__(self, select_options: List[Tuple[str, str]], callback: Callable[[discord.Interaction], Awaitable[None]]):
        super().__init__()

        select_options = [
            discord.SelectOption(label=label, value=value) for label, value in select_options
        ]

        self.select_menu = discord.ui.Select(
            select_type=discord.ComponentType.string_select,
            min_values=1,
            max_values=1,
            options=select_options
        )
        self.add_item(self.select_menu)
        self.select_menu.callback = callback

