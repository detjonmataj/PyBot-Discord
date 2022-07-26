import discord
import operator
import re

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

    @DiscordBot.Commands.command(help="Outputs the supported languages")
    async def languages(self, ctx):
        languages = CompilerExplorerAPI.get_languages(*['name', 'defaultCompiler'])
        languages.sort(key=operator.itemgetter('name'))
        n = 15
        chunks = [languages[i:i + n] for i in range(0, len(languages), n)]

        data = []
        for i, chunk in enumerate(chunks):
            description = ""
            for j, language in enumerate(chunk):
                default_compiler = language['defaultCompiler']
                description += f"**{(i * n) + j + 1})** {language['name']} -> " \
                               f"**{default_compiler or 'No default compiler'}**\n"

            data.append({
                'title': f"Supported Languages",
                'description': description,
                'colour': discord.Colour.blue()
            })

        await Paginator(ctx=ctx, components_manager=self.bot.components_manager, pages=data, timeout=120).send()

    @DiscordBot.Commands.command(aliases=['run'], help="Compile and run a code snippet")
    async def compile(self, ctx, *, user_input=None):
        async def send_error(error_message: str = None):
            # I did not want to use multi-line docstrings
            await ctx.send(
                embed=discord.Embed(
                    title="Error",
                    description=(error_message
                                 or "An error occurred "
                                    "while compiling your code.") + "\n\nUse `$languages` to see the list of supported "
                                                                    "languages. "
                                                                    "\nUse `$compilers <language name>` to see the "
                                                                    "supported compilers. "
                                                                    "\n**Format:**"
                                                                    "\n\n$compile [language] [compiler flags(optional)]"
                                                                    "\n[args (optional)]"
                                                                    "\n\\`\\`\\`[language name or alias (optional)]"
                                                                    "\n\t<your code>"
                                                                    "\n\\`\\`\\`"
                                                                    "\n[stdin (optional)]"
                                                                    "\n\n**Examples:**"
                                                                    "\n\n$compile c++ -Wall -Wextra"
                                                                    "\ncommand line arguments"
                                                                    "\n\\`\\`\\`c++"
                                                                    "\n#include <iostream>"
                                                                    "\n#include <string>"
                                                                    "\n\nint main(int argc, char *argv[]) {"
                                                                    "\n\nstd::string user_name;"
                                                                    "\nstd::cin >> user_name;"
                                                                    "\nstd::cout << \"Hello, \" << user_name << \".\" "
                                                                    "<< std::endl; "
                                                                    "\n\nreturn 0;"
                                                                    "\n}"
                                                                    "\n\\`\\`\\`"
                                                                    "\nPyBot"
                                                                    "\n\n**`Output:`** Hello, PyBot.",
                    colour=discord.Colour.red()
                )
            )

        # check if the user_input is empty
        if user_input is None or user_input == "":
            await send_error("You must provide a valid language or compiler and a code snippet.")
            return

        message = ctx.message.content.split("\n")
        first_line = message[0].strip().split(" ")
        user_input = re.sub("```(.)*\n", "```", user_input)
        temp_user_input = user_input.split("```")

        if len(temp_user_input) == 1 and len(first_line) == 1:
            await send_error("You must provide a valid language or compiler and a code snippet.")
            return
        elif len(temp_user_input) == 1:
            await send_error("You must provide  a code snippet surrounded by \\`\\`\\`.")
            return
        elif len(temp_user_input) > 3:
            await send_error("You entered too many code blocks.\nPlease only enter one code block.")
            return
        elif len(first_line) < 2:
            await send_error("You must provide a valid programming language or compiler.")
            return

        programming_language_or_compiler = first_line[1].strip()
        compiler_flags = (" ".join(first_line[2:] if len(first_line) > 2 else [])).replace("\n", " ").strip()

        compiler_id_language = CompilerExplorerAPI.find_language_or_compiler(programming_language_or_compiler)

        if compiler_id_language is None:
            await send_error("Language or compiler not found.")
            return

        command_line_arguments = message[1].strip().split(" ")

        source_code = temp_user_input[1]

        user_input = user_input.split("```", 2)[-1].strip()

        try:
            result = CompilerExplorerAPI.compile(source_code=source_code, compiler_id=compiler_id_language[0],
                                                 args=command_line_arguments, stdin=user_input,
                                                 compiler_options=compiler_flags)
            color = discord.Colour.green() if result['code'] == 0 else discord.Colour.red()

            output = ""
            if result['stdout']:
                output = "\n".join(x["text"] for x in result['stdout'])

            error = ""
            if "buildResult" in result and "stderr" in result["buildResult"]:
                error = "\n".join(x["text"] for x in result["buildResult"]['stderr'])
            if "stderr" in result:
                error += "\n".join(x["text"] for x in result['stderr'])

            ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
            output = ansi_escape.sub('', output)
            error = ansi_escape.sub('', error)

            exec_time = ""
            if "execTime" in result:
                exec_time = f"{result['execTime']}ms | "

            footer_text = f"Requested by {str(ctx.author)} | {exec_time}" \
                          f"{compiler_id_language[1]} | {compiler_id_language[0]}  | godbolt.org"

            if output and error:
                description = f"`Output:`\n" \
                              f"```\n{output}\n```\n\n" \
                              f"`Error:`\n" \
                              f"```\n{error}\n```"
            elif output:
                description = f"`Output:`\n" \
                              f"```\n{output}\n```"
            elif error:
                description = f"`Error:`\n" \
                              f"```\n{error}\n```"
            else:
                description = "No output or error."

            embed = discord.Embed(
                title="Compilation Result",
                description=description,
                colour=color
            )

            embed.set_footer(text=footer_text)

            await ctx.send(
                embed=embed
            )
        except Exception as e:
            print(e)
            return
