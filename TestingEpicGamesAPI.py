# For testing purposes only, without discord support

import discord
import datetime
from epicstore_api import EpicGamesStoreAPI
client = discord.Client(intents=discord.Intents.all())
epic_api = EpicGamesStoreAPI()

def free_games(api):
    games_dict = api.get_free_games(allow_countries = "US")
    games_list = games_dict["data"]["Catalog"]["searchStore"]["elements"]
    free_games_dict = {}
    base_url = 'store.epicgames.com/en-US/p/'
    for game in games_list:
        game_url = None 
        if game['catalogNs']['mappings']:
            game_url = base_url + game['catalogNs']['mappings'][0]['pageSlug']
        free_games_dict[game['title']] = [game['description'], game['effectiveDate'], game['promotions'], game_url]
    return free_games_dict
free_games_dict = free_games(epic_api)

currentGames = "\n*Currently Free*\n"
upcomingGames = "\n*Free next week*\n"
for key in free_games_dict.keys():
    gameDate = int(free_games_dict[key][1][:4])
    currentYear = datetime.date.today().year
    promotions = free_games_dict[key][2]
    if promotions:
        if promotions['promotionalOffers']:
            print("current ", key)
        elif promotions['upcomingPromotionalOffers']:
            print("upcoming ", key)
