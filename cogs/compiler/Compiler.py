import discord
import operator

from utils.DiscordBot import DiscordBot
from discord_components import DiscordComponents
from utils.CompilerExplorerAPI import CompilerExplorerAPI
from utils.Paginator import Paginator


class Compiler(DiscordBot.Commands.Cog, name="Compiler"):
    def __init__(self, bot):
        self.bot = bot
        self.DiscordComponents = DiscordComponents(bot)

    @DiscordBot.Commands.command(help="Outputs the supported compilers")
    async def compilers(self, ctx, *, language: str = None):
        if language is None:
            await ctx.send("```nim\nPlease specify a language.\n```")
            return

        compilers = CompilerExplorerAPI.get_compilers(*["id", "name", "lang"])

        filtered_compilers = {}
        for compiler in compilers:
            if compiler['lang'] not in filtered_compilers:
                filtered_compilers[compiler['lang']] = []
            filtered_compilers[compiler['lang']].append(compiler)

        language = language.lower()

        if language not in filtered_compilers:
            await ctx.send("```nim\nLanguage not found.\n```")
            return

        compilers = filtered_compilers[language]

        compilers.sort(key=operator.itemgetter('name'))

        n = 15
        chunks = [compilers[i:i + n] for i in range(0, len(compilers), n)]

        data = []

        for i, chunk in enumerate(chunks):
            description = ""
            for j, compiler in enumerate(chunk):
                description += f"**{(i * n) + j + 1})** {compiler['name']} -> **{compiler['id']}**\n"

            data.append({
                'title': f"Supported \"{language.capitalize()}\" Compilers",
                'description': description,
                'colour': discord.Colour.blue()
            })

        await Paginator(ctx=ctx, components_manager=self.bot.components_manager, pages=data, timeout=120).send()
