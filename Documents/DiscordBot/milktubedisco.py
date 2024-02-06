import discord
from discord.ext import commands
import youtube_dl

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

class MilkTube(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix)
        self.voice_channel = None
        self.voice_client = None
        self.queue = []

    async def on_ready(self):
        print(f'Logged in as {self.user.name}')

    @commands.command()
    async def play(self, ctx, url):
        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel.")
            return

        channel = ctx.message.author.voice.channel
        if self.voice_client is None:
            self.voice_channel = await channel.connect()
        elif self.voice_client.channel != channel:
            await self.voice_client.move_to(channel)

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']

        await ctx.send("Added to queue")
        self.queue.append(url2)
        
        if not self.voice_channel.is_playing():
            self.play_music()

    def play_music(self):
        if len(self.queue) > 0:
            url = self.queue.pop(0)
            self.voice_channel.play(discord.FFmpegPCMAudio(url), after=lambda e: self.play_next())
        else:
            self.voice_client.stop()

    def play_next(self):
        self.play_music()

    @commands.command()
    async def stop(self, ctx):
        if self.voice_channel:
            self.voice_channel.stop()
            self.queue = []

    @commands.command()
    async def skip(self, ctx):
        if self.voice_channel:
            self.voice_channel.stop()
            await ctx.send("Skipped the current track.")

bot = MilkTube(command_prefix='!')

bot.run('MTIwNDM2NTQwNzgwNTM3ODU3MA.Gb7KG5.zgyAarx3FLzXjaW3Ag-Bxp4vTdGFV-TC44f0Ig')
