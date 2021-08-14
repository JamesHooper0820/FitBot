import discord
from discord.ext.commands import Bot
from bot.cogs.core import Core
from bot.cogs.role_commands import RoleCommands
from bot.cogs.background import Background
from bot.cogs.commands import Commands
import os
from os.path import join, dirname
from dotenv import load_dotenv
from discord_slash import SlashCommand
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        intents = discord.Intents.all()
        
        bot = Bot(command_prefix='/', intents=intents, help_command=None)
        slash = SlashCommand(bot, sync_commands=True)

        bot.add_cog(Core(bot))
        bot.add_cog(Commands(bot))
        bot.add_cog(RoleCommands(bot))
        bot.add_cog(Background(bot))

        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        bot.run(os.environ.get("TOKEN"))

# TODO:
# Exclusive command for those with posture/hydration check role to edit frequency of pings
# Weekly Calorie Tracker - Tracks last 7 days of calorie inputs, with 7-day average, subcommand /log into calorie tracker, water tracker etc
# EOD Summary - Total calories and water that day
# Leaderboard - Sub-leaderboards (sub-commands) could include Running, Steps, Cycling, Swimming, Calories Burnt, leaderboards for across all servers and current servers
# Logging
# Remove specific guild from slash commands decorator
# Turn off Debug Mode in Django settings.py
# FitBit Integration
# Strava Integration
