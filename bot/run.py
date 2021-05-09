import os
from discord.ext import commands
from discord.ext.commands import Bot

class Run(commands.Cog):
    def runbot(self):
        bot = Bot(command_prefix="!", help_command=None)
        bot.run(os.getenv("TOKEN"))
        self.autoload()       

    @commands.command
    async def load(self, extension):
        self.bot.load_extension(f"cogs.{extension}")

    @commands.command
    async def unload(self, extension):
        self.bot.unload_extension(f"cogs.{extension}")

    async def autoload(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                self.bot.load_extension(f"cogs.{filename[:-3]}")
