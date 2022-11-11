import nextcord
import os
import random
import asyncio
import traceback
from nextcord.ext import commands
from tinytag import TinyTag

client = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())

things = {}

@client.event
async def on_ready():
    print("nice", client.user)

cur_song = ""

@client.slash_command(description="Plays music in your voice channel")
async def play(ctx: nextcord.Interaction):
    if ctx.user.voice is None:
        return await ctx.send("no vc? <:nobitches:953506027528130630>")
    
    try: vc = await ctx.user.voice.channel.connect()
    except: return await ctx.send("I'm already in vc DUMBASS LMAO <:goofylittleshit:1028545843449565204>")
    things[ctx.user.voice.channel.id] = vc
    await ctx.response.send_message("PLAYING NOW! <:NOW:1036428369782378567>")

    while True:
        try:
            global cur_song
            cur_song = f"./music/{random.choice(os.listdir('./music/'))}"
            song = nextcord.FFmpegOpusAudio(cur_song, bitrate=192)
            vc.play(song)

            while vc.is_playing() or vc.is_paused():
                await asyncio.sleep(.1)

        except Exception:
            traceback.print_exc()
            break

@client.slash_command(description="Stops playing music and leaves your voice channel")
async def stop(ctx: nextcord.Interaction):
    if ctx.user.voice is None:
        return await ctx.response.send_message("I'm not in a vc DUMBASS LMAO <:goofylittleshit:1028545843449565204>")

    await things[ctx.voice.channel.id].disconnect()
    del things[ctx.voice.channel.id]
    return await ctx.response.send_message("LEAVING NOW! <:NOW:1036428369782378567>")

@client.slash_command(description="Pauses the current song")
async def pause(ctx: nextcord.Interaction):
    if ctx.user.voice is None:
        return await ctx.send("no vc? <:nobitches:953506027528130630>")

    if things[ctx.user.voice.channel.id].is_paused():
        return await ctx.response.send_message("I'm already paused DUMBASS LMAO ðŸ¤“")
    else:
        things[ctx.user.voice.channel.id].pause()
        return await ctx.response.send_message("PAUSING NOW! <:NOW:1036428369782378567>")

@client.slash_command(description="Unpauses the current song")
async def resume(ctx: nextcord.Interaction):
    if ctx.user.voice is None:
        return await ctx.send("no vc? <:nobitches:953506027528130630>")

    if things[ctx.user.voice.channel.id].is_playing():
        return await ctx.response.send_message("I'm already playing DUMBASS LMAO ðŸ¤“")
    else:
        things[ctx.user.voice.channel.id].resume()
        return await ctx.response.send_message("PLAYING NOW! <:NOW:1036428369782378567>")

@client.slash_command(description="Displays the currently playing songs artist/title")
async def np(ctx: nextcord.Interaction):
    song = TinyTag.get(cur_song)
    _, song_filename = os.path.split(cur_song)
    if song is not None:
        return await ctx.response.send_message(f"{song.artist} - {song.title}")

    return await ctx.repsonse.send_message(song_filename)

client.run("token")
