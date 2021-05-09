import os
from discord.ext.commands import Bot

bot = Bot(command_prefix="!")   

@bot.command
async def load(extension):
        bot.load_extension(f"cogs.{extension}")

@bot.command
async def unload(extension):
        bot.unload_extension(f"cogs.{extension}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(os.getenv("TOKEN"))  
