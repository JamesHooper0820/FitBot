import discord
import os

client = discord.Client()

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 820759687078084650:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'posture':
            role = discord.utils.get(guild.roles, name='Posture Check')

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
            else:
                pass
        else:
            pass

@client.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == 820759687078084650:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

        if payload.emoji.name == 'posture':
            role = discord.utils.get(guild.roles, name='Posture Check')

        if role is not None:
            member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
            else:
                pass
        else:
            pass

client.run(os.getenv('TOKEN'))
