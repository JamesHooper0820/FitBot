import discord
from dislash import *
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

bot = Bot(command_prefix=get_prefix, intents=intents, help_command=None)
slash = slash_commands.SlashClient(bot)

bot.add_cog(Core(bot))
bot.add_cog(Commands(bot))
bot.add_cog(Background(bot))
bot.add_cog(Prefixes(bot))

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
bot.run(os.environ.get("TOKEN"))

# TO DO:
# Add Slash Commands - Reminder to change wording of any '!' command
# Discord Buttons & Dropdowns - Improve flow of Bot (discord-components)
# Weekly Calorie Tracker - Tracks last 7 days of calorie inputs, with 7-day average
# EOD Summary - Total calories and water that day
# Leaderboard - Sub-leaderboards (sub-commands) could include Running, Steps, Cycling, Swimming, Calories Burnt
# Logging
# FitBit Integration
# Strava Integration
