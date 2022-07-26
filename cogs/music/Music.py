import discord
from youtube_dl import YoutubeDL
import asyncio

from utils.DiscordBot import DiscordBot


class Music(DiscordBot.Commands.Cog, name="Music"):
    def __init__(self, bot):
        self.bot = bot
        self.loop = asyncio.get_event_loop()

    @DiscordBot.Commands.command(help="Ask bot to join your Voice Channel")
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Connect to a voice channel!")

        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            self.bot.servers[ctx.guild.id]['Music']['vc'] = await voice_channel.connect()
        else:
            self.bot.servers[ctx.guild.id]['Music']['vc'] = ctx.voice_client
            await ctx.voice_client.move_to(voice_channel)

    @DiscordBot.Commands.command(aliases=["leave"], help="Ask bot to leave your Voice Channel")
    async def disconnect(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("I'm not in a voice channel!")
            return

        self.bot.servers[ctx.guild.id]['Music']['playing'] = False
        self.bot.servers[ctx.guild.id]['Music']['current_index'] = 0
        self.bot.servers[ctx.guild.id]['Music']['songs_queue'] = []
        await ctx.voice_client.disconnect()

    def search_yt(self, item):
        with YoutubeDL({'format': 'bestaudio', 'noplaylist': 'True'}) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item,
                                        download=False)['entries'][0]
            except Exception as e:
                print(str(e))
                return None

        return {'source': info['formats'][0]['url'], 'title': info['title'], 'id': info['id']}

    def play_music(self, ctx):
        current_index = self.bot.servers[ctx.guild.id]['Music']['current_index']

        if current_index >= len(self.bot.servers[ctx.guild.id]['Music']['songs_queue']):
            self.bot.servers[ctx.guild.id]['Music']['playing'] = False
            return
        source = self.bot.servers[ctx.guild.id]['Music']['songs_queue'][current_index]['source']
        try:
            self.bot.servers[ctx.guild.id]['Music']['vc'].play(
                discord.FFmpegPCMAudio(source, **{
                    'before_options':
                        '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                    'options': '-vn'
                }),
                after=lambda x: self.play_music(ctx)
            )

            self.bot.servers[ctx.guild.id]['Music']['playing'] = True
            self.bot.servers[ctx.guild.id]['Music']['current_index'] += 1

            try:
                asyncio.run_coroutine_threadsafe(self.now_playing(ctx), self.loop)
            except Exception as ee:
                print(str(ee))

        except Exception as e:
            print(e)
            self.bot.servers[ctx.guild.id]['Music']['playing'] = False

    @DiscordBot.Commands.command(aliases=["p"], help="Play a song from YouTube")
    async def play(self, ctx, *, song_name):
        # TODO: The bot may be in a different voice channel than the one the user is in.
        #     This should be fixed. Currently, the bot will move to the user's voice channel.
        await self.join(ctx)
        if song_name == "":
            await ctx.send("Please specify a song name!")
            return

        song = self.search_yt(song_name)

        if song is None:
            await ctx.send("Error while searching for the song!")
            return

        self.bot.servers[ctx.guild.id]['Music']['songs_queue'].append(song)

        if not self.bot.servers[ctx.guild.id]['Music']['playing']:
            self.play_music(ctx)
        else:
            link = f"https://www.youtube.com/watch?v={song['id']}"
            await ctx.send(
                embed=discord.Embed(
                    title="Added to Queue",
                    description=f"[{song['title']}]({link})",
                    colour=discord.Colour.blue()
                )
            )

    @DiscordBot.Commands.command(aliases=["np", "nowplaying"], help="Show the currently playing song")
    async def now_playing(self, ctx):
        if self.bot.servers[ctx.guild.id]['Music']['playing']:

            current_index = self.bot.servers[ctx.guild.id]['Music']['current_index'] - 1
            song_id = self.bot.servers[ctx.guild.id]['Music']['songs_queue'][current_index]['id']
            song_title = self.bot.servers[ctx.guild.id]['Music']['songs_queue'][current_index]['title']
            link = f"https://www.youtube.com/watch?v={song_id}"

            await ctx.send(
                embed=discord.Embed(
                    title="Now Playing",
                    description=f"[{song_title}]({link})",
                    colour=discord.Colour.blue()
                )
            )
        else:
            await ctx.send("Nothing is playing!")

    @DiscordBot.Commands.command(aliases=["q", "playlist"], help="Show the queue")
    async def queue(self, ctx):
        songs_queue = self.bot.servers[ctx.guild.id]['Music']['songs_queue']
        current_index = self.bot.servers[ctx.guild.id]['Music']['current_index']
        paused = self.bot.servers[ctx.guild.id]['Music']['paused']
        if len(songs_queue) == 0:
            await ctx.send("```nim\nThe queue is empty ;-;\n```")
            return

        queue_list = "```nim\n"

        for i, song in enumerate(songs_queue):
            index = i + 1

            song_name = f"{index}) {song['title']}"

            if i == current_index - 1:
                song_name = f"\t\t⬐ current track\n{song_name} {'| (paused)' * paused}\n\t\t⬑ current track"

            queue_list += f"{song_name}\n"

        queue_list += "\n\t\tThis is the end of the queue!```"

        await ctx.send(queue_list)

    @DiscordBot.Commands.command(aliases=["s"], help="Skip the currently playing song.")
    async def skip(self, ctx):

        if not self.bot.servers[ctx.guild.id]['Music']['playing'] and \
                self.bot.servers[ctx.guild.id]['Music'][
                    'current_index'] >= len(self.bot.servers[ctx.guild.id]['Music']['songs_queue']):
            await ctx.send("Nothing is playing!")
            return

        self.bot.servers[ctx.guild.id]['Music']['playing'] = False
        self.bot.servers[ctx.guild.id]['Music']['paused'] = False
        self.bot.servers[ctx.guild.id]['Music']['vc'].stop()

        await ctx.send("Skipped the current song!")

    @DiscordBot.Commands.command(aliases=[], help="Pauses a playing song.")
    async def pause(self, ctx):
        if not self.bot.servers[ctx.guild.id]['Music']['playing']:
            await ctx.send("Nothing is playing!")
            return

        if self.bot.servers[ctx.guild.id]['Music']['paused']:
            await ctx.send("The song is already paused!")
            return

        self.bot.servers[ctx.guild.id]['Music']['vc'].pause()
        self.bot.servers[ctx.guild.id]['Music']['paused'] = True
        await ctx.send("Paused the current song!")

    @DiscordBot.Commands.command(aliases=["unpause"], help="Resumes a paused song.")
    async def resume(self, ctx):
        if not self.bot.servers[ctx.guild.id]['Music']['playing']:
            await ctx.send("Nothing is playing!")
            return

        if not self.bot.servers[ctx.guild.id]['Music']['paused']:
            await ctx.send("The song is not paused!")
            return

        self.bot.servers[ctx.guild.id]['Music']['vc'].resume()
        self.bot.servers[ctx.guild.id]['Music']['paused'] = False
        await ctx.send("Resumed the current song!")
