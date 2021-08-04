import discord
from bot.cogs.core import Core
from bot.cogs.commands import Commands
from bot.cogs.background import Background
import os
from discord.ext.commands import Bot
from os.path import join, dirname
from dotenv import load_dotenv
from discord_slash import SlashCommand


intents = discord.Intents.all()

bot = Bot(command_prefix='/', intents=intents, help_command=None)
slash = SlashCommand(bot, sync_commands=True)

bot.add_cog(Core(bot))
bot.add_cog(Commands(bot))
bot.add_cog(Background(bot))

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
bot.run(os.environ.get("TOKEN"))

# TO DO:
# Fix slash commands responding in DMs
# Discord Buttons & Dropdowns - Improve flow of bot
# Weekly Calorie Tracker - Tracks last 7 days of calorie inputs, with 7-day average
# EOD Summary - Total calories and water that day
# Leaderboard - Sub-leaderboards (sub-commands) could include Running, Steps, Cycling, Swimming, Calories Burnt
# Remove specific guild from slash commands decorator
# Logging
# FitBit Integration
# Strava Integration
