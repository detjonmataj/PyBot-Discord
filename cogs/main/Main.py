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

    @DiscordBot.Commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.bot.servers[guild.id] = {
            "name": guild.name,
            "id": guild.id,
            "guild": guild,
            "Music": {
                'songs_queue': [],
                'current_index': 0,
                'playing': False,
                'paused': False,
                'vc': None
            }
        }

    @DiscordBot.Commands.Cog.listener()
    async def on_guild_remove(self, guild):
        del self.bot.servers[guild.id]

    @DiscordBot.Commands.Cog.listener()
    async def on_guild_update(self, before, after):
        del self.bot.servers[before.id]
        self.bot.servers[after.id] = {
            "name": after.name,
            "id": after.id,
            "guild": after,
            "Music": {
                'songs_queue': [],
                'current_index': 0,
                'playing': False,
                'paused': False,
                'vc': None
            }
        }

    @DiscordBot.Commands.command(help="Outputs the bot's ping")
    async def ping(self, ctx):
        await ctx.send(f":ping_pong: Pong!"
                       f"\n\n:heartbeat: {round(self.bot.latency * 1000)}ms")
