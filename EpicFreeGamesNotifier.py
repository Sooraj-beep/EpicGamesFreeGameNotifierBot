import discord
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

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == '!get free games':
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

        await message.channel.send(currentGames+upcomingGames)

client.run('AUTH') # Use your bot auth id here

