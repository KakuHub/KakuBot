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
    if ctx.user.voice.channel is None:
        return await ctx.send("no vc")

    vc = await ctx.user.voice.channel.connect()
    things[ctx.channel.id] = vc
    await ctx.response.send_message("ðŸ¤“")

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
    if ctx.user.voice.channel is None:
        return await ctx.send("no vc")

    if things[ctx.channel_id].is_paused():
        return await ctx.response.send_message("I'm already paused DUMBASS LMAO ðŸ¤“")

    things[ctx.channel.id].pause()
    return await ctx.response.send_message("ðŸ¤“")

@client.slash_command()
async def resume(ctx: nextcord.Interaction):
    if ctx.user.voice.channel is None:
        return await ctx.send("no vc")

    if things[ctx.channel_id].is_playing():
        return await ctx.response.send_message("I'm already playing DUMBASS LMAO ðŸ¤“")

    if things[ctx.channel_id].is_paused():
        things[ctx.channel_id].resume()
        return await ctx.response.send_message("ðŸ¤“")

client.run("token")
