import discord
from discord.ext.commands import Bot
from discord.ext import tasks
import os
import requests
import json
import random as r

bot = Bot(command_prefix="!")

async def status():
    activity = discord.Activity(name="your health!", type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")
    await status()

@bot.event
async def on_guild_join(guild: discord.Guild):
	await guild.create_role(name="Posture Check", mentionable=True, colour=discord.Colour.blue)

@bot.event
async def get_quote() -> str:
    response = requests.get("https://type.fit/api/quotes")
    json_data = json.loads(response.text)
    random_quote = json_data[r.randint(0, len(json_data))]["text"] + " - " + json_data[r.randint(0, len(json_data))]["author"]
    return random_quote

@bot.command(pass_context=True)
async def quote(ctx):
    quote = await get_quote()
    await ctx.send(ctx.author.mention + ' ' + quote)

@tasks.loop(seconds=60)
async def posture(guild: discord.Guild, role: discord.Role):
    role = discord.utils.get(guild.roles, name="Posture Check")
    if role is None:
        return
    for member in guild.members:
        if role in member.roles:
            await bot.send_message(member, member.mention + "Hourly posture check, fix your posture!")

@bot.command(aliases="createrole")
async def create_role(ctx, *, name):
	guild = ctx.guild
	await guild.create_role(name=name)
	await ctx.send(f"Role `{name}` has been created.")

@bot.command(pass_context=True)
async def initialize(ctx):
    embed = discord.Embed(
        title = "Introducing FitBot!",
        description = "FitBot is a fitness, health and well-being discord bot designed to enhance and encourage people to take care of their physical and mental health.",
        colour = discord.Color.blue()
    )

    embed.set_footer(text="Stay healthy!")
    embed.set_image(url="https://e7.pngegg.com/pngimages/416/261/png-clipart-8-bit-color-8bit-heart-pixel-art-color-depth-allanon-heart-video-game.png")
    embed.set_thumbnail(url="https://e7.pngegg.com/pngimages/416/261/png-clipart-8-bit-color-8bit-heart-pixel-art-color-depth-allanon-heart-video-game.png")
    embed.set_author(name="FitBot", icon_url="https://e7.pngegg.com/pngimages/416/261/png-clipart-8-bit-color-8bit-heart-pixel-art-color-depth-allanon-heart-video-game.png")
    embed.add_field(name="Reactions", value="Click on the reactions to this message in order to access roles.", inline=False)
    embed.add_field(name="🧍", value="Posture Checker Role", inline=False)

    initial_message = await ctx.send(embed=embed)
    await initial_message.add_reaction("🧍")

@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    msg_id = msg.id

    if message_id == msg_id:
        guild_id = payload.guild_id 
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == '🧍':
            role = discord.utils.get(guild.roles, name="Posture Check") 
        
        if role is not None: # If role exists
            member = await guild.fetch_member(payload.user_id)
            if member != bot.user:
                if member is not None: 
                    await member.add_roles(role)
            else:
                print("Member not found")
        else:
            print("Role not found")

@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    msg_id = msg.id

    if message_id == msg_id:
        guild_id = payload.guild_id 
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == '🧍':
            role = discord.utils.get(guild.roles, name="Posture Check") 
        
        if role is not None: # If role exists
            member = await guild.fetch_member(payload.user_id)
            if member != bot.user:
                if member is not None: 
                    await member.remove_roles(role) 
            else:
                print("Member not found")
        else:
            print("Role not found")

bot.run(os.getenv("TOKEN"))
