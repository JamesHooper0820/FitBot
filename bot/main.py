import discord
from discord.ext.commands import Bot
from discord.ext.tasks import loop
import os
import requests
import json
import random as r

intents = discord.Intents.default()
intents.members = True

bot = Bot(command_prefix="!", intents=intents)

async def status():
    activity = discord.Activity(name="your health!", type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}.")
    posture.start()
    hydration.start()
    await status()

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

@loop(hours=1)
async def posture():
    for guild in bot.guilds:
        role = discord.utils.find(lambda r: r.name == 'Posture Check', guild.roles)
        members = [m for m in guild.members if role in m.roles]
        for m in members:
            await m.send((m.mention + " Hourly posture check, fix your posture!"))

@loop(hours=1)
async def hydration():
    for guild in bot.guilds:
        role = discord.utils.find(lambda r: r.name == 'Hydration Check', guild.roles)
        members = [m for m in guild.members if role in m.roles]
        for m in members:
            await m.send((m.mention + " Hourly hydration check, drink some water!"))

@bot.command(aliases=["createrole"])
async def create_role(ctx, *, name):
	guild = ctx.guild
	await guild.create_role(name=name)
	await ctx.send(f"Role `{name}` has been created.")

@bot.command(pass_context=True)
async def initialize(ctx):
    await ctx.guild.create_role(name="Posture Check", mentionable=True, colour=discord.Colour(0x34e12f))
    await ctx.guild.create_role(name="Hydration Check", mentionable=True, colour=discord.Colour(0x45c7ea))

    embed = discord.Embed(
        title = "Introducing FitBot!",
        description = "FitBot is a fitness, health and well-being discord bot designed to enhance and encourage people to take care of their physical and mental health.",
        colour = discord.Color.blue()
    )

    embed.set_footer(text="Stay healthy!")
    embed.set_image(url="https://e7.pngegg.com/pngimages/416/261/png-clipart-8-bit-color-8bit-heart-pixel-art-color-depth-allanon-heart-video-game.png")
    embed.set_thumbnail(url="https://e7.pngegg.com/pngimages/416/261/png-clipart-8-bit-color-8bit-heart-pixel-art-color-depth-allanon-heart-video-game.png")
    embed.set_author(name="FitBot", icon_url="https://e7.pngegg.com/pngimages/416/261/png-clipart-8-bit-color-8bit-heart-pixel-art-color-depth-allanon-heart-video-game.png")
    embed.add_field(name="Reactions", value="Click on the reactions to this message in order to access roles:", inline=False)
    embed.add_field(name=":person_standing:", value="Posture Checker Role", inline=False)
    embed.add_field(name=":potable_water:", value="Hydration Checker Role", inline=False)

    initial_message = await ctx.send(embed=embed)
    await initial_message.add_reaction(":person_standing:")
    await initial_message.add_reaction(":potable_water:")

@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    msg_id = msg.id

    if message_id == msg_id:
        guild_id = payload.guild_id 
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == ':person_standing:':
            role = discord.utils.get(guild.roles, name="Posture Check")
            if role is not None:
                member = await guild.fetch_member(payload.user_id)
                if member != bot.user:
                    if member is not None: 
                        await member.add_roles(role) 
        if payload.emoji.name == ':potable_water:':
            role = discord.utils.get(guild.roles, name="Hydration Check") 
            if role is not None:
                member = await guild.fetch_member(payload.user_id)
                if member != bot.user:
                    if member is not None: 
                        await member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    msg_id = msg.id

    if message_id == msg_id:
        guild_id = payload.guild_id 
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == ':person_standing:':
            role = discord.utils.get(guild.roles, name="Posture Check") 
            if role is not None:
                member = await guild.fetch_member(payload.user_id)
                if member != bot.user:
                    if member is not None: 
                        await member.remove_roles(role) 
        if payload.emoji.name == ':potable_water:':
            role = discord.utils.get(guild.roles, name="Hydration Check")
            if role is not None:
                member = await guild.fetch_member(payload.user_id)
                if member != bot.user:
                    if member is not None: 
                        await member.remove_roles(role) 

bot.run(os.getenv("TOKEN"))
