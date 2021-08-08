import discord
from discord.errors import HTTPException
from discord.ext import commands
from discord.ext.tasks import loop
from .background import Background
from discord_slash import cog_ext
from discord_slash.utils.manage_components import *
from discord_slash.model import ButtonStyle


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

        for guild in self.bot.guilds:
            print(f"Connected to {guild} (id: {guild.id}).")

            members = await guild.fetch_members(limit=None).flatten()
            self.sum += len(members)

        self.background.posture.start()
        self.background.hydration.start()
        self.statuses.start()

    @commands.Cog.listener()
    async def on_guild_join(self, guild) -> None:
        embed = discord.Embed(
            title=(f"Thank you for adding FitBot to {guild.name}!"),
            description=(f"To setup FitBot, type `/initialize`."),
            colour=discord.Color.blue())

        embed.set_footer(text="Stay healthy!")
        embed.set_author(
            name="FitBot",
            icon_url="https://e7.pngegg.com/pngimages/416/261/png-clipart-8-bit-color-8bit-heart-pixel-art-color-depth-allanon-heart-video-game.png")

        channels = guild.text_channels
        for i, channel in enumerate(channels):
            if i == len(channels):
                return
            if (guild.me.permissions_in(channel).send_messages is False and
               guild.me.permissions_in(channel).embed_links is False):
                continue
            else:
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

    @cog_ext.cog_slash(name="initialize",
                       description="Initializes FitBot.",
                       guild_ids=[799768142045249606, 873664168685883422])
    async def initialize(self, ctx) -> None:
        await ctx.guild.create_role(name="Posture Check", mentionable=True, colour=discord.Colour(0x34e12f))
        await ctx.guild.create_role(name="Hydration Check", mentionable=True, colour=discord.Colour(0x45c7ea))

        embed = discord.Embed(
            title="Introducing FitBot!",
            description="FitBot is Discord's first dedicated fitness, health and well-being bot, designed to enhance and encourage people to take care of their physical and mental health.",
            colour=discord.Color.blue())

        embed.set_footer(text="Stay healthy!")
        embed.set_author(
            name="FitBot",
            icon_url="https://e7.pngegg.com/pngimages/416/261/png-clipart-8-bit-color-8bit-heart-pixel-art-color-depth-allanon-heart-video-game.png")
        embed.add_field(
            name="Roles",
            value="Click on the buttons below to access FitBot's roles.",
            inline=False)
        embed.add_field(
            name="Help",
            value="Use the `/help` command for assistance.",
            inline=False)

        buttons = [
            create_button(
                style=ButtonStyle.green,
                label="Posture Checker",
                custom_id="Posture Checker",
                emoji="🧍"
            ),
            create_button(
                style=ButtonStyle.green,
                label="Hydration Checker",
                custom_id="Hydration Checker",
                emoji="🚰"
            ),
            create_button(
                style=ButtonStyle.red,
                label="Reset FitBot Roles",
                custom_id="Reset FitBot Roles"
            ),
        ]
        action_row = create_actionrow(*buttons)

        await ctx.send(embed=embed, components=[action_row])

        while True:
            def check_ctx(button_ctx):
                return ctx.channel == button_ctx.channel

            button_ctx: ComponentContext = await wait_for_component(self.bot, check=check_ctx, components=[action_row])

            self.member = await button_ctx.guild.fetch_member(button_ctx.author_id)
            self.posture_role = discord.utils.get(button_ctx.guild.roles, name="Posture Check")
            self.hydration_role = discord.utils.get(button_ctx.guild.roles, name="Hydration Check")

            if button_ctx.custom_id == "Posture Checker":
                if self.posture_role is not None:
                    if self.posture_role in self.member.roles:
                        await button_ctx.defer(hidden=True)
                        await self.member.remove_roles(self.posture_role)
                        await button_ctx.send(button_ctx.author.mention + " `Posture Checker` role successfully **removed**.", hidden=True)
                    else:
                        try:
                            await button_ctx.defer(hidden=True)
                            await self.member.add_roles(self.posture_role)
                            await button_ctx.send(button_ctx.author.mention + " `Posture Checker` role successfully **added**.", hidden=True)
                        except HTTPException:
                            pass

            elif button_ctx.custom_id == "Hydration Checker":
                self.posture_role = discord.utils.get(button_ctx.guild.roles, name="Posture Check")
                if self.hydration_role is not None:
                    if self.hydration_role in self.member.roles:
                        await button_ctx.defer(hidden=True)
                        await self.member.remove_roles(self.hydration_role)
                        await button_ctx.send(button_ctx.author.mention + " `Hydration Checker` role successfully **removed**.", hidden=True)
                    else:
                        try:
                            await button_ctx.defer(hidden=True)
                            await self.member.add_roles(self.hydration_role)
                            await button_ctx.send(button_ctx.author.mention + " `Hydration Checker` role successfully **added**.", hidden=True)
                        except HTTPException:
                            pass

            elif button_ctx.custom_id == "Reset FitBot Roles":
                try:
                    await self.member.remove_roles(self.posture_role, self.hydration_role)
                    await button_ctx.send(button_ctx.author.mention + " Sucessfully **removed** all FitBot roles.", hidden=True)
                except HTTPException:
                    pass
