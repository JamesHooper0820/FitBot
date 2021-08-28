import discord
from discord.ext import commands
from discord.ext.tasks import loop


class Background(commands.Cog):
    """Initialize the background cog."""

    def __init__(self, bot) -> None:
        """Initialize the bot."""
        self.bot = bot

    @loop(hours=1)
    async def posture(self) -> None:
        for guild in self.bot.guilds:
            role = discord.utils.find(
                lambda r: r.name == 'Posture Check',
                guild.roles)
            members = [m for m in guild.members if role in m.roles]
            for m in members:
                try:
                    await m.send((m.mention + " Check your posture!"))
                except discord.Forbidden:
                    pass
    # TODO
    @loop(hours=1)
    async def posture(self) -> None:
        for guild in self.bot.guilds:
            role_30minutes = discord.utils.find(
                lambda r: r.name == 'PLACEHOLDER',
                guild.roles)
            role_1hour = discord.utils.find(
                lambda r: r.name == 'PLACEHOLDER',
                guild.roles)
            role_2hours = discord.utils.find(
                lambda r: r.name == 'PLACEHOLDER',
                guild.roles)
            members_30minutes = [m for m in guild.members if role_30minutes in m.roles]
            members_1hour = [m for m in guild.members if role_1hour in m.roles]
            members_2hours = [m for m in guild.members if role_2hours in m.roles]

            current_iteration = self.posture.current_loop
            

    @loop(hours=1)
    async def hydration(self) -> None:
        for guild in self.bot.guilds:
            role = discord.utils.find(
                lambda r: r.name == 'Hydration Check',
                guild.roles)
            members = [m for m in guild.members if role in m.roles]
            for m in members:
                try:
                    await m.send((m.mention + " Drink some water!"))
                except discord.Forbidden:
                    pass
