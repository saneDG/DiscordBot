import discord
import json
import requests
from discord.ext import commands
import youtube_dl
from timeit import default_timer as timer

TOKEN = 'NTE4ODU5MzEyNzgxODUyNjky.DuW6jg.4sQFIuL7TQ6R6j2wrqlHAmO4vrU'

client = commands.Bot(command_prefix = '.')

players = {}
queues = {}

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id]
        player.start()

@client.event
async def on_ready():
    print('Bot is ready.')

@client.command()
async def ping():
    await client.say('Pong!')

@client.command()
async def helppiä():
    await client.say('```' + '|| .tule | .soita (URL) | .heippa | .jono (URL) | .skippi ||' + '```')

#Join and leave voice channel the author is currently in.
@client.command(pass_context=True)
async def tule(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)

@client.command(pass_context=True)
async def heippa(ctx):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    await voice_client.disconnect()

@client.command(pass_context=True)
async def soita(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after = lambda: check_queue(server.id))
    players[server.id] = player
    player.start()

@client.command(pass_context=True)
async def skippi(ctx):
    id = ctx.message.server.id
    players[id].stop()

@client.command(pass_context=True)
async def jatka(ctx):
    id = ctx.message.server.id
    players[id].resume()

@client.command(pass_context=True)
async def jono(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after = lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say('viteo jonossa')

@client.command(pass_context=True)
async def joke(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player('https://www.youtube.com/watch?v=K8E_zMLCRNg')
    players[server.id] = player
    player.start()

client.run(TOKEN)
