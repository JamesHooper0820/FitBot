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
        for self.guild in self.bot.guilds:
            role = discord.utils.find(
                lambda r: r.name == 'Posture Check',
                self.guild.roles)
            members = [m for m in self.guild.members if role in m.roles]
            for m in members:
                try:
                    await m.send((m.mention + " Hourly posture check, fix your posture!"))
                except discord.Forbidden:
                    pass


    @loop(hours=1)
    async def hydration(self) -> None:
        for self.guild in self.bot.guilds:
            role = discord.utils.find(
                lambda r: r.name == 'Hydration Check',
                self.guild.roles)
            members = [m for m in self.guild.members if role in m.roles]
            for m in members:
                try:
                    await m.send((m.mention + " Hourly hydration check, drink some water!"))
                except discord.Forbidden:
                    pass
