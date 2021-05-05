import discord
from discord.ext.commands import Bot
import os
import requests
import json
import random as r

bot = Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")
    await status()

async def status():
    activity = discord.Activity(name="your health!", type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)

@bot.event
async def get_quote():
    response = requests.get("https://type.fit/api/quotes")
    json_data = json.loads(response.text)
    random_quote = json_data[r.randint(0, len(json_data))]["text"] + " - " + json_data[r.randint(0, len(json_data))]["author"]
    return random_quote

@bot.command()
async def quote(ctx):
    quote = await get_quote()
    await ctx.send(ctx.author.mention + ' ' + quote)

### WORK ON THIS NEXT
@bot.command()
async def posture(ctx):
    user_id_list = [243348545585938433]
    for user_id in user_id_list:
        user = await bot.get_user_info(user_id)
        await user.send(user.mention + "Posture check!")

@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id

    if message_id == 821018526357651457: 
        guild_id = payload.guild_id 
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds) 

        if payload.emoji.name == '🧍':
            role = discord.utils.get(guild.roles, name="Posture Check") 

        if role is not None: # If role exists
            member = await guild.fetch_member(payload.user_id)
            if member is not None: 
                await member.add_roles(role) 
            else:
                print("Member not found")
        else:
            print("Role not found")

@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
  
    if message_id == 821018526357651457:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == '🧍':
            role = discord.utils.get(guild.roles, name="Posture Check")

        if role is not None:
            member = await guild.fetch_member(payload.user_id)
            if member is not None:
                await member.remove_roles(role)
            else:
                print("Member not found")
        else:
            print("Role not found")

bot.run(os.getenv("TOKEN"))
