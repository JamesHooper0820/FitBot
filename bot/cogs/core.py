import discord
from discord.ext import commands
from discord.ext.tasks import loop
from discord.raw_models import RawReactionActionEvent
import requests
import json
import random as r

class Core(commands.Cog):
    """Initialize the core cog."""

    def __init__(self, bot) -> None:
        """Initialize the bot."""
        self.bot = bot

        self.sum = 0
        self.initialize_id = 0
        self.activities_index = 0
        self.activities = [
            discord.Activity(name=str(self.sum) + " hearts", type=discord.ActivityType.watching),
            discord.Activity(name="your health", type=discord.ActivityType.watching)
        ]

    @loop(seconds=10)
    async def statuses(self) -> None:
        """Loop different bot statuses."""
        self.activities[0].name = str(self.sum) + " hearts"

        await self.bot.change_presence(activity=self.activities[self.activities_index])
        self.activities_index += 1
        if self.activities_index >= len(self.activities):
            self.activities_index = 0

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f"Logged in as {self.bot.user}.")

        for guild in self.bot.guilds:
            members = await guild.fetch_members(limit=None).flatten()
            self.sum += len(members)

        self.posture.start()
        self.hydration.start()
        self.statuses.start()

    @commands.Cog.listener()
    async def get_quote(self) -> str:
        response = requests.get("https://type.fit/api/quotes")
        json_data = json.loads(response.text)
        random_quote = json_data[r.randint(0, len(json_data))]["text"] + " - " + json_data[r.randint(0, len(json_data))]["author"]
        return random_quote

    @commands.command(pass_context=True)
    async def quote(self, ctx) -> None:
        quote = await self.get_quote()
        await ctx.send(ctx.author.mention + ' ' + quote)

    @loop(hours=1)
    async def posture(self) -> None:
        for self.guild in self.bot.guilds:
            role = discord.utils.find(lambda r: r.name == 'Posture Check', self.guild.roles)
            members = [m for m in self.guild.members if role in m.roles]
            for m in members:
                try:
                    await m.send((m.mention + " Hourly posture check, fix your posture!"))
                except discord.Forbidden:
                    pass

    @loop(hours=1)
    async def hydration(self) -> None:
        for self.guild in self.bot.guilds:
            role = discord.utils.find(lambda r: r.name == 'Hydration Check', self.guild.roles)
            members = [m for m in self.guild.members if role in m.roles]
            for m in members:
                try:
                    await m.send((m.mention + " Hourly hydration check, drink some water!"))
                except discord.Forbidden:
                    pass

    @commands.command(pass_context=True, aliases=["createrole"])
    async def create_role(self, ctx, *, name) -> None:
        guild = ctx.guild
        await guild.create_role(name=name)
        await ctx.send(f"Role `{name}` has been created.")

    @commands.command(pass_context=True)
    async def initialize(self, ctx) -> None:
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
        embed.add_field(name="🧍", value="Posture Checker Role", inline=False)
        embed.add_field(name="🚰", value="Hydration Checker Role", inline=False)

        initial_message = await ctx.send(embed=embed)
        await initial_message.add_reaction("🧍")
        await initial_message.add_reaction("🚰")

        self.initialize_id = initial_message.id

    # WIP - Understand
    async def get_message_from_payload(self, bot: commands.Bot, payload: discord.RawReactionActionEvent, user: discord.User) -> discord.Message:
        """Return a message object from a given reaction payload."""
        channel = await bot.fetch_channel(bot, payload.channel_id)
        assert isinstance(channel, discord.abc.Messageable)

        if channel is None:
            if user.dm_channel is None:
                dm_channel = await user.create_dm()
                if dm_channel.id == payload.channel_id:
                    channel = dm_channel
            else:
                raise ValueError('Payload channel not found')

        return await channel.fetch_message(payload.message_id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent) -> None:
        if self.initialize_id != payload.message_id: 
            return
        if payload.user_id == self.bot.user.id:
            return
        emoji = payload.emoji.name

        if emoji == '🧍':
            role = discord.utils.get(self.guild.roles, name="Posture Check")
            if role is not None:
                member = await self.guild.fetch_member(payload.user_id)
                if member is not None: 
                    await member.add_roles(role) 
        if emoji == '🚰':
            role = discord.utils.get(self.guild.roles, name="Hydration Check") 
            if role is not None:
                member = await self.guild.fetch_member(payload.user_id)
                if member is not None: 
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: RawReactionActionEvent) -> None:
        if self.initialize_id != payload.message_id:
            return
        if payload.user_id == self.bot.user.id:
            return
        emoji = payload.emoji.name

        if emoji == '🧍':
            role = discord.utils.get(self.guild.roles, name="Posture Check") 
            if role is not None:
                member = await self.guild.fetch_member(payload.user_id)
                if member is not None: 
                    await member.remove_roles(role) 
        if emoji == '🚰':
            role = discord.utils.get(self.guild.roles, name="Hydration Check")
            if role is not None:
                member = await self.guild.fetch_member(payload.user_id)
                if member is not None: 
                    await member.remove_roles(role) 
