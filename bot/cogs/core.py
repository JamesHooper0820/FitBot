import discord
from discord.ext import commands
from discord.ext.tasks import loop
from discord.raw_models import RawReactionActionEvent
from bot.cogs.background import Background


class Core(commands.Cog):
    """Initialize the core cog."""

    def __init__(self, bot) -> None:
        """Initialize the bot."""
        self.bot = bot
        self.background = Background(bot)

        self.sum = 0
        self.initialize_id = 0
        self.activities_index = 0
        self.activities = [
            discord.Activity(
                name=str(
                    self.sum) + " hearts",
                type=discord.ActivityType.watching),
            discord.Activity(
                name="your health",
                type=discord.ActivityType.watching)]

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f"Logged in as {self.bot.user}.")

        for self.guild in self.bot.guilds:
            members = await self.guild.fetch_members(limit=None).flatten()
            self.sum += len(members)

        self.background.posture.start()
        self.background.hydration.start()
        self.statuses.start()

    @commands.Cog.listener()
    async def on_guild_join(self, guild) -> None:
        embed = discord.Embed(
            title=(f"Thank you for adding FitBot to {guild.name}!"),
            description=(f"To setup FitBot, type `!initialize`."),
            colour=discord.Color.blue())

        embed.set_footer(text="Stay healthy!")
        embed.set_author(
            name="FitBot",
            icon_url="https://e7.pngegg.com/pngimages/416/261/png-clipart-8-bit-color-8bit-heart-pixel-art-color-depth-allanon-heart-video-game.png")
        
        channel = guild.text_channels[0]
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild) -> None:
        self.background.posture.stop()
        self.background.hydration.stop()
        self.statuses.stop()

    @loop(seconds=10)
    async def statuses(self) -> None:
        """Loop different bot statuses."""
        self.activities[0].name = str(self.sum) + " hearts"

        await self.bot.change_presence(activity=self.activities[self.activities_index])
        self.activities_index += 1
        if self.activities_index >= len(self.activities):
            self.activities_index = 0

    @commands.command(pass_context=True)
    async def initialize(self, ctx) -> None:
        await ctx.guild.create_role(name="Posture Check", mentionable=True, colour=discord.Colour(0x34e12f))
        await ctx.guild.create_role(name="Hydration Check", mentionable=True, colour=discord.Colour(0x45c7ea))

        embed = discord.Embed(
            title="Introducing FitBot!",
            description="FitBot is a fitness, health and well-being discord bot designed to enhance and encourage people to take care of their physical and mental health.",
            colour=discord.Color.blue())

        embed.set_footer(text="Stay healthy!")
        embed.set_author(
            name="FitBot",
            icon_url="https://e7.pngegg.com/pngimages/416/261/png-clipart-8-bit-color-8bit-heart-pixel-art-color-depth-allanon-heart-video-game.png")
        embed.add_field(
            name="Reactions",
            value="Click on the reactions to this message in order to access roles:",
            inline=False)
        embed.add_field(name="\u200b", value="🧍 = Posture Checker Role", inline=False)
        embed.add_field(name="\u200b", value="🚰 = Hydration Checker Role", inline=False)

        initial_message = await ctx.send(embed=embed)
        await initial_message.add_reaction("🧍")
        await initial_message.add_reaction("🚰")

        self.initialize_id = initial_message.id

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
