from utils.DiscordBot import DiscordBot


class Main(DiscordBot.Commands.Cog, name="Main"):
    def __init__(self, bot):
        self.bot = bot
        bot.servers = {}

    @DiscordBot.Commands.Cog.listener()
    async def on_ready(self):
        print("Bot started successfully!")
        print(f'Logged in as {self.bot.user}')
        for server in self.bot.guilds:
            self.bot.servers[server.id] = {
                "name": server.name,
                "id": server.id,
                "guild": server,
                "Music": {
                    'songs_queue': [],
                    'current_index': 0,
                    'playing': False,
                    'paused': False,
                    'vc': None
                }
            }

    @DiscordBot.Commands.Cog.listener()
    async def on_command_error(self, ctx: DiscordBot.Commands.Context, error: DiscordBot.Commands.CommandError):
        if isinstance(error, DiscordBot.Commands.CommandNotFound):
            await ctx.send("```nim\nCommand not found ;-;\n```")
            return
