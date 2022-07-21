from datetime import datetime
from discord.ext import commands
from typing import Any


class DiscordBot(commands.Bot):
    Commands = commands
    uptime: datetime = datetime.now()

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
