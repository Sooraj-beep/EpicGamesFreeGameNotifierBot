import discord
import asyncio
from discord.ext import tasks
from datetime import datetime
from epicstore_api import EpicGamesStoreAPI
client = discord.Client(intents=discord.Intents.all())
epic_api = EpicGamesStoreAPI()

def free_games(api):
    games_dict = api.get_free_games()
    games_list = games_dict["data"]["Catalog"]["searchStore"]["elements"]
    free_games_dict = {}
    base_url = 'store.epicgames.com/en-US/p/'
    for game in games_list:
        game_url = None 
        if game['catalogNs']['mappings']:
            game_url = base_url + game['catalogNs']['mappings'][0]['pageSlug']
        free_games_dict[game['title']] = [game['description'], game['promotions'], game_url]
    return free_games_dict

def createFreeGamesMessage():
    free_games_dict = free_games(epic_api)
    currentGames = "\n*Currently Free*\n"
    upcomingGames = "\n*Free next week*\n"

    for key in free_games_dict.keys():
        promotions = free_games_dict[key][1]
        if promotions:
            if promotions['promotionalOffers']:
                currentGames += "**"+key+"**\n"
                currentGames += free_games_dict[key][0]+"\n"
                if free_games_dict[key][2]:
                    currentGames += "**Link**: https://" + free_games_dict[key][2] + "\n\n"
            elif promotions['upcomingPromotionalOffers']:
                upcomingGames += "**"+key+"**\n"
                upcomingGames += free_games_dict[key][0]+"\n\n"
    
    return currentGames+upcomingGames
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '!get free games':
        msg = createFreeGamesMessage()
        await message.channel.send(msg)

@tasks.loop(hours=168)
async def weekly_announcement():
    await client.wait_until_ready()
    channel_ids = [] # add your channel ids here
    for id in channel_ids:
        channel = client.get_channel(id)
        msg = createFreeGamesMessage()
        await channel.send(msg)

@client.event
async def on_ready():
   if not weekly_announcement.is_running():
      weekly_announcement.start()

client.run('') # Use your bot auth id here

