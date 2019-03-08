import discord
import json
import requests
import urllib.request
from discord.ext import commands
import youtube_dl
from timeit import default_timer as timer
from config import *

TOKEN = configDiscordToken

client = commands.Bot(command_prefix='.')

players = {}
queues = {}

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        players[id]
        player.start()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print(discord.__version__)
    print('------')

    print('Servers connected to:')
    for server in client.servers:
        print(server.name)
    print("------")


@client.command()
async def ping():
    await client.say('Pong!')

@client.command(pass_context=True)
async def nextgames(ctx, amount=5):
    if amount > 10:
        await client.say("max 10")
    else:
        upcomingTournamentsData = urllib.request.urlopen("https://api.pandascore.co/csgo/matches/upcoming?&token=" + configPandaToken).read()
        i = 0
        while i < amount:
            upcomingMatchLeagueImageUrl = json.loads(upcomingTournamentsData)[i]['league']['image_url']
            upcomingMatchLeagueName = json.loads(upcomingTournamentsData)[i]['league']['name']
            upcomingMatchTeamOpponentName1 = json.loads(upcomingTournamentsData)[i]['opponents'][0]['opponent']['name']
            upcomingMatchTeamOpponentName2 = json.loads(upcomingTournamentsData)[i]['opponents'][1]['opponent']['name']
            upcomingMatchNumberofgames = json.loads(upcomingTournamentsData)[i]['number_of_games']
            upcomingMatchBeginat = json.loads(upcomingTournamentsData)[i]['serie']['begin_at']
            upcomingMatchSlug = json.loads(upcomingTournamentsData)[i]['serie']['slug']
            print("NEXT OPPONENTS: {} -VS- {}" .format(upcomingMatchTeamOpponentName2, upcomingMatchTeamOpponentName1))
            print("ALL: {} - {} - {}" .format(upcomingMatchLeagueImageUrl, upcomingMatchBeginat, upcomingMatchSlug))
            i += 1

            embed = discord.Embed(
                type = 'rich',
                title = upcomingMatchLeagueName,
                colour = discord.Colour.red()
            )

            embed.set_footer(text='Botti')
            embed.set_thumbnail(url=upcomingMatchLeagueImageUrl)
            embed.add_field(name='Teams', value=upcomingMatchTeamOpponentName1 + ' -VS- ' + upcomingMatchTeamOpponentName2, inline=False)
            embed.add_field(name='Begin at', value=upcomingMatchBeginat, inline=False)
            embed.add_field(name='Game type', value='Best of {}' .format(upcomingMatchNumberofgames), inline=False)

            await client.say(embed=embed)
    
    print("ready")

@client.command()
async def ence():

    teamsData = urllib.request.urlopen("https://api.pandascore.co/csgo/teams?filter[slug]=ence&token=" + configPandaToken).read()
    teamsEnceName = json.loads(teamsData)[0]['name']

    print("----------------------------" + teamsEnceName + "----------------------------")
    i = 0
    while i < 5:
        teamsEncePlayer = json.loads(teamsData)[0]['players'][i]['name']
        teamsEnceLastname = json.loads(teamsData)[0]['players'][i]['last_name']
        teamsEnceImageurl = json.loads(teamsData)[0]['players'][i]['image_url']
        teamsEnceHometown = json.loads(teamsData)[0]['players'][i]['hometown']
        print(teamsEncePlayer)
        print(teamsEnceLastname)
        print(teamsEnceImageurl)
        print(teamsEnceHometown)
        print("------------------")
        i += 1

        embed = discord.Embed(
            title = 'Player card',
            colour = discord.Colour.red()
        )

        embed.set_footer(text='Botti')
        embed.set_image(url=teamsEnceImageurl)
        embed.add_field(name='Name', value=teamsEncePlayer, inline=False)
        embed.add_field(name='Last name', value=teamsEnceLastname, inline=False)
        embed.add_field(name='Hometown', value=teamsEnceHometown, inline=False)

        await client.say(embed=embed)

    print("----------------------------" + teamsEnceName + "----------------------------")


@client.command()
async def pvst():

    key = configYoutubeKey

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

    print("------")


    embed = discord.Embed(
        colour = discord.Colour.red()
    )

    embed.set_footer(text='😂😂😂')
    embed.set_thumbnail(url='https://www.sofakenews.com/wp-content/uploads/2018/10/pewdiepie-has-questioned-the-validity-of-tseries-subscribers-560x416.jpg')
    embed.add_field(name='PewDiePie', value="{:,d}".format(int(pewsubs)), inline=False)
    embed.add_field(name='T-series', value="{:,d}".format(int(tsersubs)), inline=False)
    embed.add_field(name='Gap between', value="{:,d}".format(int(subgap)), inline=False)

    await client.say(embed=embed)


@client.command()
async def helppiä():
    await client.say('```' + '|| .tule | .soita (URL) | .heippa | .jono (URL) | .skippi ||' + '```')

# Join and leave voice channel the author is currently in.


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
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
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
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say('viteo jonossa')


@client.command(pass_context=True)
async def miikakertoivitsin(ctx):
    channel = ctx.message.author.voice.voice_channel
    await client.join_voice_channel(channel)
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player('https://www.youtube.com/watch?v=K8E_zMLCRNg')
    players[server.id] = player
    player.start()

client.run(TOKEN)
