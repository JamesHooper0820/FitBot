import json
from discord.ext import commands

async def get_prefix(_, message) -> str:
    with open("bot/cogs/prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes.get(str(message.guild.id), "!")

class Prefixes(commands.Cog):
    """Initialize the prefixes cog."""

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open("bot/cogs/prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = "!"

        with open("bot/cogs/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open("bot/cogs/prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open("bot/cogs/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

    @commands.command()
    async def changeprefix(self, ctx, prefix):
        with open("bot/cogs/prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open("bot/cogs/prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f"Command prefix changed to: `{prefix}`")
