import discord
from discord.errors import HTTPException
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.context import ComponentContext
from discord_slash.model import ButtonStyle
from discord_slash.utils.manage_components import create_actionrow, create_button, wait_for_component


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
            description="Please select the role you want to edit.",
            colour=discord.Color.blue())

        embed.set_footer(text="Stay healthy!")
        embed.set_author(
            name="FitBot",
            icon_url="https://e7.pngegg.com/pngimages/416/261/png-clipart-8-bit-color-8bit-heart-pixel-art-color-depth-allanon-heart-video-game.png")

        buttons = [
            create_button(
                style=ButtonStyle.blue,
                label="Posture Check Settings",
                custom_id="Posture Check Settings"
            ),
            create_button(
                style=ButtonStyle.blue,
                label="Hydration Check Settings",
                custom_id="Hydration Check Settings"
            ),
            create_button(
                style=ButtonStyle.red,
                label="Remove FitBot Roles",
                custom_id="Remove FitBot Roles"
            ),
        ]
        action_row = create_actionrow(*buttons)

        await ctx.send(embed=embed, components=[action_row], hidden=True)

        while True:
            def check_ctx(button_ctx):
                return ctx.channel == button_ctx.channel

            button_ctx: ComponentContext = await wait_for_component(self.bot, check=check_ctx, components=[action_row])

            self.member = await button_ctx.guild.fetch_member(button_ctx.author_id)
            self.posture_role = discord.utils.get(button_ctx.guild.roles, name="Posture Check")
            self.hydration_role = discord.utils.get(button_ctx.guild.roles, name="Hydration Check")

            if button_ctx.custom_id == "Remove FitBot Roles":
                await self.member.remove_roles(self.posture_role, self.hydration_role)
                await button_ctx.send(button_ctx.author.mention + " Sucessfully **removed** all FitBot roles.", hidden=True)

            elif button_ctx.custom_id == "Posture Check Settings":
                if self.posture_role is not None:
                    if self.posture_role in self.member.roles:
                        buttons = [
                            create_button(
                                style=ButtonStyle.green,
                                label="Change 'Check' Frequency",
                                custom_id="Change 'Check' Frequency"
                            ),
                            create_button(
                                style=ButtonStyle.red,
                                label="Remove Posture Check Role",
                                custom_id="Remove Posture Check Role"
                            ),
                        ]
                        action_row = create_actionrow(*buttons)

                        embed.description = ""
                        embed.add_field(name="Posture Check Settings", value="Use the buttons below to configure the Posture Check role's settings.", inline=False)
                        await button_ctx.edit_origin(embed=embed, components=[action_row], hidden=True)

                        while True:
                            def check_ctx(button_ctx):
                                return ctx.channel == button_ctx.channel

                            button_ctx: ComponentContext = await wait_for_component(self.bot, check=check_ctx, components=[action_row])
                            if button_ctx.custom_id == "Remove Posture Check Role":
                                await self.member.remove_roles(self.posture_role)
                                await button_ctx.send(button_ctx.author.mention + " Sucessfully **removed** the `Posture Check` role.", hidden=True)
                            # TODO
                            elif button_ctx.custom_id == "Change 'Check' Frequency":
                                pass
                    else:
                        await button_ctx.send(ctx.author.mention + " You do not have the `Posture Check` role.", hidden=True)
                        pass

            elif button_ctx.custom_id == "Hydration Check Settings":
                if self.hydration_role is not None:
                    if self.hydration_role in self.member.roles:
                        buttons = [
                            create_button(
                                style=ButtonStyle.green,
                                label="Change 'Check' Frequency",
                                custom_id="Change 'Check' Frequency"
                            ),
                            create_button(
                                style=ButtonStyle.red,
                                label="Remove Hydration Check Role",
                                custom_id="Remove Hydration Check Role"
                            ),
                        ]
                        action_row = create_actionrow(*buttons)

                        embed.description = ""
                        embed.add_field(name="Hydration Check Settings", value="Use the buttons below to configure the Hydration Check role's settings.", inline=False)
                        await button_ctx.edit_origin(embed=embed, components=[action_row], hidden=True)

                        while True:
                            def check_ctx(button_ctx):
                                return ctx.channel == button_ctx.channel

                            button_ctx: ComponentContext = await wait_for_component(self.bot, check=check_ctx, components=[action_row])
                            if button_ctx.custom_id == "Remove Hydration Check Role":
                                await self.member.remove_roles(self.hydration_role)
                                await button_ctx.send(button_ctx.author.mention + " Sucessfully **removed** the `Hydration Check` role.", hidden=True)
                            # TODO
                            elif button_ctx.custom_id == "Change 'Check' Frequency":
                                pass
                    else:
                        await button_ctx.send(ctx.author.mention + " You do not have the `Hydration Check` role.", hidden=True)
                        pass
