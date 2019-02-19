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
async def pvst():

    key = "AIzaSyBCqQlYK5QFDIgXu4bhqQcMtoG9_0SFaFo"

    pewname = "pewdiepie"
    tsername = "tseries"

    pewdata = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername="+pewname+"&key="+key).read()
    pewsubs = json.loads(pewdata)["items"][0]["statistics"]["subscriberCount"]
    print(pewname + ": " + "{:,d}".format(int(pewsubs)) + " subscribers!")

    tserdata = urllib.request.urlopen("https://www.googleapis.com/youtube/v3/channels?part=statistics&forUsername="+tsername+"&key="+key).read()
    tsersubs = json.loads(tserdata)["items"][0]["statistics"]["subscriberCount"]
    print(tsername + ": " + "{:,d}".format(int(tsersubs)) + " subscribers!")

    subgap = int(pewsubs) - int(tsersubs)
    print("Subgap is " + "{:,d}".format(int(subgap)) + " subscribers!")


    embed = discord.Embed(
        colour = discord.Colour.red()
    )

    embed.set_footer(text='😂😂😂')
    embed.set_thumbnail(url='https://www.sofakenews.com/wp-content/uploads/2018/10/pewdiepie-has-questioned-the-validity-of-tseries-subscribers-560x416.jpg')
    embed.add_field(name='PewDiePie', value=pewsubs, inline=False)
    embed.add_field(name='T-series', value=tsersubs, inline=False)
    embed.add_field(name='Gap between', value=subgap, inline=False)

    await client.say(embed=embed)

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
