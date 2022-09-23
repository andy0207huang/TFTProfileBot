# importing libraries
import discord;
import os;
from riotwatcher import LolWatcher, TftWatcher;
from collections import Counter;
from webserver import keep_alive;

# riot api token
riot_key = os.environ['RIOT_API'];
lolw = LolWatcher(riot_key)
tftw = TftWatcher(riot_key)

# discord client
client = discord.Client();

# on ready event call
@client.event
async def on_ready():
  print('Test logged in username {0.user}'.format(client))

# on disconnect event call
@client.event
async def on_disconnect():
  print('Test disconected')


# TFT League query
def getTFTLeagueJSON(summonerName):
  summonerID = tftw.summoner.by_name('NA1', summonerName)['id'];  # get summonerID thru summoner parameter
  TFTLeagueJSON = tftw.league.by_summoner('NA1', summonerID)[0];  # get tft league json
  return(TFTLeagueJSON);

# TFT Match data query
def getTFTMatchJSON(summonerName):
  placementSum = 0;
  numberOfGames = 5;
  trait="";   # gray af require reference wtf
  traitsList = [];
  unitsList = [];

  summonerpuuid = tftw.summoner.by_name('NA1', summonerName)['puuid'];  # get puuid
  TFTMatchJSON = tftw.match.by_puuid('AMERICAS', summonerpuuid, numberOfGames);    # number of games
  
  # for each match ID in the 20 matches
  for matchID in TFTMatchJSON:

    # for each participant in each match
    for x in tftw.match.by_id('AMERICAS', matchID)['info']['participants']:

      # find the participant with the same puuid
      if summonerpuuid == x['puuid']:

        # placement sum
        placement = x['placement'];
        placementSum += placement; 

        # traits
        for y in x['traits']:
          if y['tier_current'] >= 1:
            if "_" in y['name']:
              trait = (y['name'].split("_")[1], y['num_units']);
            else:
              trait = (y['name'], y['num_units'])
          
          traitsList.append(trait);

        # units
        for y in x['units']:
          if "_" in y['character_id']:
            unit = y['character_id'].split("_")[1];
          else:
            unit = y['character_id']
          
          unitsList.append(unit);
  
  # ITEM 1
  avgPlacement = format((placementSum / numberOfGames), '.2f'); 
  # ITEM 2
  mostPlayedTraits = Counter(traitsList).most_common(1)[0][0][0];  # ((('trait', num), count))
  # ITEM 3
  mostPlayedUnits = Counter(unitsList).most_common(1)[0][0];    # (('champ'), count)

  return(avgPlacement, mostPlayedTraits, mostPlayedUnits);

# on message event call
@client.event
async def on_message(msg):
  # check if message is from discord bot
  if msg.author == client:
    return

  # # TEST QUERY [DELETE LATER] 
  # if msg.content.startswith('$t '):
  #   # sumName = msg.content.split(" ", 1)[1].strip()
  #   # tier = getTFTLeagueJSON(sumName)['tier'];
  #   # rank = getTFTLeagueJSON(sumName)['rank'];
  #   # await msg.channel.send(tier + " " + rank);
  #   return
    

  # check if message is from discord bot 
  if msg.content.startswith('$tftprofile '):
    # get summoner name by split
    sumName = msg.content.split(" ", 1)[1].strip()

    # get info needed for the embeded message
    sN = getTFTLeagueJSON(sumName)['summonerName'];
    tier = getTFTLeagueJSON(sumName)['tier'];
    rank = getTFTLeagueJSON(sumName)['rank'];
    lp = getTFTLeagueJSON(sumName)['leaguePoints'];
    wins = getTFTLeagueJSON(sumName)['wins'];
    losses = getTFTLeagueJSON(sumName)['losses'];

    avgPlace = getTFTMatchJSON(sumName)[0];
    mPT = getTFTMatchJSON(sumName)[1];
    mPU = getTFTMatchJSON(sumName)[2];

    # set up embed
    myEmbed = discord.Embed(title = "TFT Ranked Profile Bot (BETA)", color = 0xCC8899);


    # thumbnail (current rank OR tft pet)
    # profile icon

    
    # first row
    myEmbed.add_field(name = "Summoner Name", value = sN, inline = True);
    myEmbed.add_field(name = "Rank", value = tier + " " + rank + " - " + str(lp) + "LP", inline = True);

    # second row
    myEmbed.add_field(name = "Avg.Placement (last 10 played games)", value = avgPlace, inline = True);
    myEmbed.add_field(name = "Win", value = wins, inline = True);
    myEmbed.add_field(name = "Loss", value = losses, inline = True);
    

    # third row
    myEmbed.add_field(name = "Most Played Comp", value = mPT, inline = True);
    myEmbed.add_field(name = "Most Played Champion", value = mPU, inline = True);

    # tft image (currently set 5.5)
    myEmbed.set_image(url = "https://cdnportal.mobalytics.gg/production/2021/07/e793f485-tft-set-5.5-dawn-of-heroes.png")

    # tft footer
    myEmbed.set_footer(text = "Supported by replit & uptime robot")

    await msg.channel.send(embed = myEmbed)

# run the bot
keep_alive()
client.run(os.getenv('BOT_TOKEN'))

