# # LEARNING PURPOSE ONLY
# # LEARNING PROGRESS

# # check if message is from discord bot 
#   if msg.content.startswith('$hello'):  # user sends $hello
#     await msg.channel.send('Hello!')    # bot sends Hello!

# # get encouragement quote
# def get_quote():
#   response = requests.get("https://zenquotes.io/api/random");
#   json_data = json.loads(response.text);

#   # q - quote key, a - author key
#   quote = json_data[0]['q'] + " - " + json_data[0]['a'];
#   return(quote);

# if msg.content.startswith('$zenquote'):
#     quote = get_quote();
#     await msg.channel.send(quote);