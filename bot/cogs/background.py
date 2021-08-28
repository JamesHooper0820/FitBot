import discord
from discord.ext import commands
from discord.ext.tasks import loop


class Background(commands.Cog):
    """Initialize the background cog."""

    def __init__(self, bot) -> None:
        """Initialize the bot."""
        self.bot = bot

    @loop(minutes=30)
    async def posture(self) -> None:
        for guild in self.bot.guilds:
            role_30minutes = discord.utils.find(
                lambda r: r.name == 'Posture Check - 30mins',
                guild.roles)
            role_1hour = discord.utils.find(
                lambda r: r.name == 'Posture Check - 1hr',
                guild.roles)
            role_2hours = discord.utils.find(
                lambda r: r.name == 'Posture Check - 2hrs',
                guild.roles)
            members_30minutes = [m for m in guild.members if role_30minutes in m.roles]
            members_1hour = [m for m in guild.members if role_1hour in m.roles]
            members_2hours = [m for m in guild.members if role_2hours in m.roles]

            current_iteration = self.posture.current_loop + 1
            
            for m1 in members_30minutes:
                try:
                    await m1.send((m1.mention + " Check your posture!"))
                except discord.Forbidden:
                    pass

            if current_iteration % 2 == 0:
                for m2 in members_1hour:
                    try:
                        await m2.send((m2.mention + " Check your posture!"))
                    except discord.Forbidden:
                        pass

            if current_iteration % 4 == 0:
                for m3 in members_2hours:
                    try:
                        await m3.send((m3.mention + " Check your posture!"))
                    except discord.Forbidden:
                        pass

    @loop(minutes=30)
    async def hydration(self) -> None:
        for guild in self.bot.guilds:
            role_30minutes = discord.utils.find(
                lambda r: r.name == 'Hydration Check - 30mins',
                guild.roles)
            role_1hour = discord.utils.find(
                lambda r: r.name == 'Hydration Check - 1hr',
                guild.roles)
            role_2hours = discord.utils.find(
                lambda r: r.name == 'Hydration Check - 2hrs',
                guild.roles)
            members_30minutes = [m for m in guild.members if role_30minutes in m.roles]
            members_1hour = [m for m in guild.members if role_1hour in m.roles]
            members_2hours = [m for m in guild.members if role_2hours in m.roles]

            current_iteration = self.posture.current_loop + 1
            
            for m1 in members_30minutes:
                try:
                    await m1.send((m1.mention + " Drink some water!"))
                except discord.Forbidden:
                    pass

            if current_iteration % 2 == 0:
                for m2 in members_1hour:
                    try:
                        await m2.send((m2.mention + " Drink some water!"))
                    except discord.Forbidden:
                        pass

            if current_iteration % 4 == 0:
                for m3 in members_2hours:
                    try:
                        await m3.send((m3.mention + " Drink some water!"))
                    except discord.Forbidden:
                        pass
