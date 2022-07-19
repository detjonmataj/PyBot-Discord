from utils.DiscordBot import DiscordBot


class Main(DiscordBot.Commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @DiscordBot.Commands.Cog.listener()
    async def on_ready(self):
        print("Bot started successfully!")
        print(f'Logged in as {self.bot.user}')

    @DiscordBot.Commands.Cog.listener()
    async def on_command_error(self, ctx: DiscordBot.Commands.Context, error: DiscordBot.Commands.CommandError):
        if isinstance(error, DiscordBot.Commands.CommandNotFound):
            await ctx.send("```nim\nCommand not found ;-;\n```")
            return
