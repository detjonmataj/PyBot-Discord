from utils.DiscordBot import DiscordBot


class Compiler(DiscordBot.Commands.Cog, name="Compiler"):
    def __init__(self, bot):
        self.bot = bot
