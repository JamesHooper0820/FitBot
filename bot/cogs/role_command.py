import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_commands import create_permission

class RoleCommands(commands.Cog):
    """Initialize the Role Commands cog."""

    def __init__(self, bot) -> None:
        """Initialize the bot."""
        self.bot = bot
        self.posture_hours = 1
        self.hydration_hours = 1

        self.posture_role = discord.utils.find(
                lambda r: r.name == 'Posture Check',
                self.bot.guild.roles)
        self.hydration_role = discord.utils.find(
                lambda r: r.name == 'Hydration Check',
                self.bot.guild.roles)

    def has_role(self, ctx):
        return (self.posture_role in ctx.author.roles) or (self.hydration_role in ctx.author.roles)
    
    user_has_roles = commands.check(has_role)

    @cog_ext.cog_slash(name="rolesettings",
                       description="Role settings.",
                       guild_ids=[799768142045249606, 873664168685883422],
                       #permissions={
                       # [
                       #     create_permission(self.role.id, SlashCommandPermissionType.ROLE, True),]}
                        )
    @user_has_roles
    async def role_settings(self, ctx):
        embed = discord.Embed(
            title="Role Settings",
            description="Use the buttons below to customize your roles' settings.",
            colour=discord.Color.blue())

        embed.set_footer(text="Stay healthy!")
        embed.set_author(
            name="FitBot",
            icon_url="https://e7.pngegg.com/pngimages/416/261/png-clipart-8-bit-color-8bit-heart-pixel-art-color-depth-allanon-heart-video-game.png")
        embed.add_field(
            name="Exercises:",
            value="For exercises that require weights, please use whatever you are comfortable with.",
            inline=False)
        embed.add_field(name="\u200b", value="\u200b")

        await ctx.send(embed=embed, hidden=True)
