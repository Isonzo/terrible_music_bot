import discord
from discord.ext import commands
import youtube_dl
import os
from dotenv import load_dotenv

load_dotenv()

discord_api_key = os.getenv("DISCORD_API")

client = commands.Bot(command_prefix=".")


@client.command()
async def play(ctx, url: str):
    song_there = os.path.isfile("song.webm")
    try:
        if song_there:
            os.remove("song.webm")
    except PermissionError:
        await ctx.send("Wait for music to end or use .stop to halt me manually.")

    voice_channel = discord.utils.get(ctx.guild.voice_channels, name="General")
    try:
        await voice_channel.connect()
    except:
        pass
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        "format": "249/250/251",
        "source_address": "0.0.0.0"
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".webm"):
            os.rename(file, "song.webm")

    voice.play(discord.FFmpegOpusAudio("song.webm"))


@client.command()
async def repeat(ctx):
    voice_channel = ctx.author.voice.channel
    try:
        await voice_channel.connect()
    except:
        pass
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegOpusAudio("song.webm"))


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        await voice.disconnect()
    else:
        await ctx.send("I have no voice yet I must leave.")


@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_playing():
        voice.pause()
    else:
        await ctx.send("I can't possibly stop if I haven't even started.")


@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else:
        await ctx.send("I can't resume if nothing is paused")


@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    voice.stop()

@client.command()
async def helpme(ctx):
    await ctx.send("Hi, I'm a terrible music bot that uses youtube-dl.")
    await ctx.send("The commands you can use are .helpme, .resume, .pause, .leave, .stop, and .repeat")
    await ctx.send("Please improve my source code if you can :c")
    pass
    


client.run(discord_api_key)
