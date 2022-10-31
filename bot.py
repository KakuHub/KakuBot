import nextcord
import os
import random
import asyncio
import traceback
from nextcord.ext import commands

client = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())

things = {}

@client.event
async def on_ready():
    print("nice", client.user)

@client.slash_command()
async def play(ctx: nextcord.Interaction):
    if ctx.user.voice is None:
        return await ctx.send("no vc? <:nobitches:953506027528130630>")

    try:
        vc = await ctx.user.voice.channel.connect()
    except:
        return await ctx.response.send_message("I'm already in vc DUMBASS LMAO <:goofylittleshit:1028545843449565204>")
    things[ctx.channel.id] = vc
    await ctx.response.send_message("PLAYING NOW! <:NOW:1036428369782378567>")

    while True:
        try:
            song = nextcord.FFmpegPCMAudio(f"./music/{random.choice(os.listdir('./music/'))}")
            vc.play(song)

            while vc.is_playing() or vc.is_paused():
                await asyncio.sleep(.1)

        except Exception:
            traceback.print_exc()
            break

@client.slash_command()
async def pause(ctx: nextcord.Interaction):
    if ctx.user.voice is None:
        return await ctx.send("no vc? <:nobitches:953506027528130630>")

    if things[ctx.channel_id].is_paused():
        return await ctx.response.send_message("I'm already paused DUMBASS LMAO ðŸ¤“")
    else:
        things[ctx.channel.id].pause()
        return await ctx.response.send_message("PAUSING NOW! <:NOW:1036428369782378567>")

@client.slash_command()
async def resume(ctx: nextcord.Interaction):
    if ctx.user.voice is None:
        return await ctx.send("no vc? <:nobitches:953506027528130630>")

    if things[ctx.channel_id].is_playing():
        return await ctx.response.send_message("I'm already playing DUMBASS LMAO ðŸ¤“")
    else:
        things[ctx.channel_id].resume()
        return await ctx.response.send_message("PLAYING NOW! <:NOW:1036428369782378567>")

client.run("token")
