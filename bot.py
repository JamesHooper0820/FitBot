from bot.cogs.background import Background
import discord
from bot.cogs.core import Core
from bot.cogs.commands import Commands
from bot.cogs.background import Background
from bot.cogs.prefixes import Prefixes, get_prefix
import os
from discord.ext.commands import Bot
from os.path import join, dirname
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True

bot = Bot(command_prefix=get_prefix, intents=intents)  

bot.add_cog(Core(bot))
bot.add_cog(Commands(bot))
bot.add_cog(Background(bot))
bot.add_cog(Prefixes(bot))

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
bot.run(os.environ.get("TOKEN"))  

# TO DO:
    # FitBit Integration
    # Strava Integration