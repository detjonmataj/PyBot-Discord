from asyncio import ProactorEventLoop

import discord
from youtube_dl import YoutubeDL
import asyncio

from utils.DiscordBot import DiscordBot


class Music(DiscordBot.Commands.Cog, name="Music"):
    def __init__(self, bot):
        self.playing: bool = False
        self.bot = bot
        # Using list because I need random access
        self.songs_queue: list = []
        self.current_index: int = 0
        self.vc = None
        self.loop = asyncio.get_event_loop()

    @DiscordBot.Commands.command(help="Ask bot to join your Voice Channel")
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Connect to a voice channel!")

        voice_channel = ctx.author.voice.channel

        if ctx.voice_client is None:
            self.vc = await voice_channel.connect()
        else:
            self.vc = ctx.voice_client
            await ctx.voice_client.move_to(voice_channel)

    @DiscordBot.Commands.command(aliases=["leave"], help="Ask bot to leave your Voice Channel")
    async def disconnect(self, ctx):
        if ctx.voice_client is None:
            await ctx.send("I'm not in a voice channel!")
            return
        self.playing = False
        self.current_index = 0
        self.songs_queue = []
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

        if self.current_index >= len(self.songs_queue):
            self.playing = False
            return

        try:
            self.playing = True

            self.vc.play(
                discord.FFmpegPCMAudio(self.songs_queue[self.current_index]['source'], **{
                    'before_options':
                        '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                    'options': '-vn'
                }),
                after=lambda x: self.play_music(ctx)
            )

            self.current_index += 1

            try:
                asyncio.run_coroutine_threadsafe(self.now_playing(ctx), self.loop)
            except Exception as ee:
                print(str(ee))

        except Exception as e:
            print(e)
            self.playing = False

    @DiscordBot.Commands.command(aliases=["p"], help="Play a song from YouTube")
    async def play(self, ctx, *args):
        await self.join(ctx)

        song_name = " ".join(args)

        if song_name == "":
            await ctx.send("Please specify a song name!")
            return

        song = self.search_yt(song_name)

        if song is None:
            await ctx.send("Error while searching for the song!")
            return

        self.songs_queue.append(song)

        if not self.playing:
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
        if self.playing:
            link = f"https://www.youtube.com/watch?v={self.songs_queue[self.current_index - 1]['id']}"
            await ctx.send(
                embed=discord.Embed(
                    title="Now Playing",
                    description=f"[{self.songs_queue[self.current_index - 1]['title']}]({link})",
                    colour=discord.Colour.blue()
                )
            )
        else:
            await ctx.send("Nothing is playing!")

    @DiscordBot.Commands.command(aliases=["q", "playlist"], help="Show the queue")
    async def queue(self, ctx):
        if len(self.songs_queue) == 0:
            await ctx.send("```nim\nThe queue is empty ;-;\n```")
            return

        queue_list = "```nim\n"

        for i, song in enumerate(self.songs_queue):
            index = i + 1

            song_name = f"{index}) {song['title']}"

            if i == self.current_index - 1:
                song_name = f"\t\t⬐ current track\n{song_name}\n\t\t⬑ current track"

            queue_list += f"{song_name}\n"

        queue_list += "\n\t\tThis is the end of the queue!```"

        await ctx.send(queue_list)

    @DiscordBot.Commands.command(aliases=["s"], help="Skip the currently playing song")
    async def skip(self, ctx):
        if not self.playing and self.current_index >= len(self.songs_queue):
            await ctx.send("Nothing is playing!")
            return

        self.playing = False
        self.vc.stop()

        await ctx.send("Skipped the current song!")
