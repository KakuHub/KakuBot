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

@nextcord.slash_command()
async def play(ctx: nextcord.Interaction):
    if ctx.user.voice.channel is None:
        return await ctx.send("no vc")
    
    vc = await ctx.user.voice.channel.connect()
    things[ctx.channel.id] = vc

    while True:
        try:
            song = nextcord.FFmpegPCMAudio(f"./music/{random.choice(os.listdir('./music/'))}")
            vc.play(song)


            while vc.is_playing() or vc.is_paused():
                await asyncio.sleep(.1)

        except Exception:
            traceback.print_exc()
            break

@nextcord.slash_command()
async def pause(ctx: nextcord.Interaction):
    if ctx.user.voice.channel is None:
        return await ctx.send("no vc")
    
    if things[ctx.channel_id].is_paused():
        return things[ctx.channel_id].resume()
    
    things[ctx.channel.id].pause()

client.run("token")
