import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.model import SlashCommandPermissionType
from discord_slash.utils.manage_commands import create_permission, generate_permissions


class RoleCommands(commands.Cog):
    """Initialize the Role Commands cog."""

    def __init__(self, bot) -> None:
        """Initialize the bot."""
        self.bot = bot
        self.posture_hours = 1
        self.hydration_hours = 1

    async def role_settings_helper(self, ctx):
        posture_role = discord.utils.find(
                lambda r: r.name == 'Posture Check',
                ctx.guild.roles)
        hydration_role = discord.utils.find(
                lambda r: r.name == 'Hydration Check',
                ctx.guild.roles)

        posture_id = posture_role.id
        hydration_id = hydration_role.id

        return [posture_id, hydration_id]

    @cog_ext.cog_slash(name="rolesettings",
                       description="Role settings.",
                       guild_ids=[799768142045249606, 873664168685883422],
                       default_permission = False)
    @cog_ext.permission(generate_permissions(ctx.guild.id, allowed_roles=role_settings_helper()))
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
