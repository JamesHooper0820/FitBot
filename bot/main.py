import discord
import os
import requests
import json
import random as r

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')

@client.event
async def status():
    activity = discord.Activity(name='Watching your health...', type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)

@client.event
async def get_quote():
    response = requests.get('https://type.fit/api/quotes')
    json_data = json.loads(response.text)
    random_quote = json_data[r.randint(0, len(json_data))]['text'] + " - " + json_data[r.randint(0, len(json_data))]['author']
    return random_quote

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    
    if msg.content.startswith('!quote'):
        quote = await get_quote()
        await msg.channel.send(msg.author.mention + ' ' + quote)


client.run(os.getenv('TOKEN'))
