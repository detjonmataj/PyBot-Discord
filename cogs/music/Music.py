from utils.DiscordBot import DiscordBot


class Music(DiscordBot.Commands.Cog, name="Music"):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing: bool = False
        # Using list because I need random access
        self.songs_queue: list = []
        self.current_index: int = -1
