import discord
from discord.ext import commands
from discord_slash import cog_ext


class RoleCommands(commands.Cog):
    """Initialize the Role Commands cog."""

    def __init__(self, bot) -> None:
        """Initialize the bot."""
        self.bot = bot
        self.posture_hours = 1
        self.hydration_hours = 1

    def has_role():
        async def predicate(ctx):
            posture_role = discord.utils.find(
                    lambda r: r.name == 'Posture Check',
                    ctx.guild.roles)
            hydration_role = discord.utils.find(
                    lambda r: r.name == 'Hydration Check',
                    ctx.guild.roles)

            if (posture_role in ctx.author.roles) or (hydration_role in ctx.author.roles):
                return True
            else:
                await ctx.send(ctx.author.mention + " You do not have any roles yet.", hidden=True)
                return False 
        # BUG: Have it pass on a CheckFailure error
        return commands.check(predicate)


    @cog_ext.cog_slash(name="rolesettings",
                       description="Role settings.",
                       guild_ids=[799768142045249606, 873664168685883422])
    @has_role()
    async def role_settings(self, ctx):
        embed = discord.Embed(
            title="Role Settings",
            description="Use the buttons below to customize your roles' settings.",
            colour=discord.Color.blue())

        embed.set_footer(text="Stay healthy!")
        embed.set_author(
            name="FitBot",
            icon_url="https://e7.pngegg.com/pngimages/416/261/png-clipart-8-bit-color-8bit-heart-pixel-art-color-depth-allanon-heart-video-game.png")

        await ctx.send(embed=embed, hidden=True)
