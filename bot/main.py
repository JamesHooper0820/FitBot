import discord
import os
import requests
import json
import random as r

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}.')
    await status()

async def status():
    activity = discord.Activity(name='your health!', type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)

@client.event
async def get_quote():
    response = requests.get('https://type.fit/api/quotes')
    json_data = json.loads(response.text)
    random_quote = json_data[r.randint(0, len(json_data))]['text'] + " - " + json_data[r.randint(0, len(json_data))]['author']
    return random_quote

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('!quote'):
        quote = await get_quote()
        await message.channel.send(message.author.mention + ' ' + quote)

client.run(os.getenv('TOKEN'))
