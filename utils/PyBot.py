from cogs.music.Music import Music
from utils.DiscordBot import DiscordBot
from cogs.main.Main import Main


# TODO: Singleton


class PyBot(DiscordBot):
    def __init__(self, token: str, prefix: str):
        super(PyBot, self).__init__(command_prefix=prefix)
        self.add_cog(Main(super()))
        self.add_cog(Music(super()))
        self.run(token)
