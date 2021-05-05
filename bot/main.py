import discord
from discord import client
from discord.ext.commands import Bot
import os
import requests
import json
import random as r
from bot.logger import create_logger

logger = create_logger(__name__)

bot = Bot(command_prefix="!")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")
    await status()

async def status():
    activity = discord.Activity(name="your health!", type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)

@bot.event
async def get_quote() -> str:
    response = requests.get("https://type.fit/api/quotes")
    json_data = json.loads(response.text)
    random_quote = json_data[r.randint(0, len(json_data))]["text"] + " - " + json_data[r.randint(0, len(json_data))]["author"]
    return random_quote

@bot.command()
async def quote(ctx):
    quote = await get_quote()
    await ctx.send(ctx.author.mention + ' ' + quote)

@bot.command(pass_context=True)
async def intialize(ctx):
    channel = ctx.message.channel
    embed = discord.Embed(
        title = "Title",
        description = "Description",
        colour = discord.Color.blue()
    )

    embed.set_footer(text="Footer")
    embed.set_thumbnail(url="https://e7.pngegg.com/pngimages/416/261/png-clipart-8-bit-color-8bit-heart-pixel-art-color-depth-allanon-heart-video-game.png")
    embed.set_author(name="FitBot", icon_url="https://e7.pngegg.com/pngimages/416/261/png-clipart-8-bit-color-8bit-heart-pixel-art-color-depth-allanon-heart-video-game.png")
    embed.add_field(name="test", value="test value", inline=False)
    embed.add_field(name="test", value="test value", inline=False)

    await client.send_message(channel, embed=embed)

### WIP
@bot.command()
async def posture(ctx):
    user_id_list = [243348545585938433]
    for user_id in user_id_list:
        user = await bot.get_user_info(user_id)
        await user.send(user.mention + "Posture check!")

@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id

    if message_id == 839555899504590868: 
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
  
    if message_id == 839555899504590868:
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
