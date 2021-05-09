from bot.cogs.core import Core
import os
from discord.ext.commands import Bot
from os.path import join, dirname
from dotenv import load_dotenv

bot = Bot(command_prefix="!")  

bot.add_cog(Core(bot))

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
bot.run(os.environ.get("TOKEN"))  
