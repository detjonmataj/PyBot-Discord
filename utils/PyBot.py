from cogs.music.Music import Music
from utils.DiscordBot import DiscordBot
from cogs.main.Main import Main
from cogs.compiler.Compiler import Compiler


# TODO: Singleton


class PyBot(DiscordBot):
    def __init__(self, token: str, prefix: str):
        super(PyBot, self).__init__(command_prefix=prefix)
        self.servers = {}
        self.add_cog(Main(self))
        self.add_cog(Music(self))
        self.add_cog(Compiler(self))
        self.run(token)
