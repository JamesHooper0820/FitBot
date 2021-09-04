import discord
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

    def has_role():
        async def predicate(ctx):
            posture_role_30mins = discord.utils.find(
                    lambda r: r.name == 'Posture Check - 30mins',
                    ctx.guild.roles)
            posture_role_1hr = discord.utils.find(
                    lambda r: r.name == 'Posture Check - 1hr',
                    ctx.guild.roles)
            posture_role_2hrs = discord.utils.find(
                    lambda r: r.name == 'Posture Check - 2hrs',
                    ctx.guild.roles)
            hydration_role_30mins = discord.utils.find(
                    lambda r: r.name == 'Hydration Check - 30mins',
                    ctx.guild.roles)
            hydration_role_1hr = discord.utils.find(
                    lambda r: r.name == 'Hydration Check - 1hr',
                    ctx.guild.roles)
            hydration_role_2hrs = discord.utils.find(
                    lambda r: r.name == 'Hydration Check - 2hrs',
                    ctx.guild.roles)

            if (posture_role_30mins or posture_role_1hr or posture_role_2hrs or hydration_role_30mins or hydration_role_1hr or hydration_role_2hrs in ctx.author.roles):
                return True
            else:
                await ctx.send(ctx.author.mention + " You do not have any roles yet.", hidden=True)
                return False 

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
            self.posture_role_30mins = discord.utils.get(button_ctx.guild.roles, name="Posture Check - 30mins")
            self.posture_role_1hr = discord.utils.get(button_ctx.guild.roles, name="Posture Check - 1hr")
            self.posture_role_2hrs = discord.utils.get(button_ctx.guild.roles, name="Posture Check - 2hrs")
            self.hydration_role_30mins = discord.utils.get(button_ctx.guild.roles, name="Hydration Check - 30mins")
            self.hydration_role_1hr = discord.utils.get(button_ctx.guild.roles, name="Hydration Check - 1hr")
            self.hydration_role_2hrs = discord.utils.get(button_ctx.guild.roles, name="Hydration Check - 2hrs")

            self.all_posture_roles = [self.posture_role_30mins, self.posture_role_1hr, self.posture_role_2hrs]
            self.all_hydration_roles = [self.hydration_role_30mins, self.hydration_role_1hr, self.hydration_role_2hrs]
            self.all_roles = [self.posture_role_30mins, self.posture_role_1hr, self.posture_role_2hrs, self.hydration_role_30mins, self.hydration_role_1hr, self.hydration_role_2hrs]

            if button_ctx.custom_id == "Remove FitBot Roles":
                await self.member.remove_roles(*self.all_roles)
                await button_ctx.send(button_ctx.author.mention + " Sucessfully **removed** all FitBot roles.", hidden=True)

            elif button_ctx.custom_id == "Posture Check Settings":
                if None not in (self.posture_role_30mins, self.posture_role_1hr, self.posture_role_2hrs):
                    if any(x in self.member.roles for x in (self.posture_role_30mins, self.posture_role_1hr, self.posture_role_2hrs)):
                        buttons = [
                            create_button(
                                style=ButtonStyle.green,
                                label="Change 'Check' Frequency",
                                custom_id="Change 'Check' Frequency"
                            ),
                            create_button(
                                style=ButtonStyle.red,
                                label="Remove Posture Check Roles",
                                custom_id="Remove Posture Check Roles"
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
                            if button_ctx.custom_id == "Remove Posture Check Roles":
                                await self.member.remove_roles(*self.all_posture_roles)
                                await button_ctx.send(button_ctx.author.mention + " Sucessfully **removed** all FitBot Posture roles.", hidden=True)
                            elif button_ctx.custom_id == "Change 'Check' Frequency":
                                buttons = [
                                    create_button(
                                        style=ButtonStyle.green,
                                        label="Posture Check - 30mins",
                                        custom_id="Posture Check - 30mins"
                                    ),
                                    create_button(
                                        style=ButtonStyle.green,
                                        label="Posture Check - 1hr",
                                        custom_id="Posture Check - 1hr"
                                    ),
                                    create_button(
                                        style=ButtonStyle.green,
                                        label="Posture Check - 2hrs",
                                        custom_id="Posture Check - 2hrs"
                                    ),
                                ]
                                action_row = create_actionrow(*buttons)

                                embed.description = ""
                                embed.add_field(name="Posture Check Frequency", value="Use the buttons below to configure the frequency of pings.", inline=False)
                                await button_ctx.edit_origin(embed=embed, components=[action_row], hidden=True)

                                while True:
                                    def check_ctx(button_ctx):
                                        return ctx.channel == button_ctx.channel

                                    button_ctx: ComponentContext = await wait_for_component(self.bot, check=check_ctx, components=[action_row])
                                    if button_ctx.custom_id == "Posture Check - 30mins":
                                        if self.posture_role_30mins is not None:
                                            if self.posture_role_30mins in self.member.roles:
                                                await button_ctx.send(button_ctx.author.mention + " You already have the `Posture Check - 30mins` role selected.", hidden=True)
                                            else:
                                                await self.member.remove_roles(*self.all_posture_roles)
                                                await self.member.add_roles(self.posture_role_30mins)
                                                await button_ctx.send(button_ctx.author.mention + " `Posture Check - 30mins` role successfully **added**.", hidden=True)

                                    if button_ctx.custom_id == "Posture Check - 1hr":
                                        if self.posture_role_1hr is not None:
                                            if self.posture_role_1hr in self.member.roles:
                                                await button_ctx.send(button_ctx.author.mention + " You already have the `Posture Check - 1hr` role selected.", hidden=True)
                                            else:
                                                await self.member.remove_roles(*self.all_posture_roles)
                                                await self.member.add_roles(self.posture_role_1hr)
                                                await button_ctx.send(button_ctx.author.mention + " `Posture Check - 1hr` role successfully **added**.", hidden=True)

                                    if button_ctx.custom_id == "Posture Check - 2hrs":
                                        if self.posture_role_2hrs is not None:
                                            if self.posture_role_2hrs in self.member.roles:
                                                await button_ctx.send(button_ctx.author.mention + " You already have the `Posture Check - 2hrs` role selected.", hidden=True)
                                            else:
                                                await self.member.remove_roles(*self.all_posture_roles)
                                                await self.member.add_roles(self.posture_role_2hrs)
                                                await button_ctx.send(button_ctx.author.mention + " `Posture Check - 2hrs` role successfully **added**.", hidden=True)
                    else:
                        await button_ctx.send(ctx.author.mention + " You do not have any `Posture Check` roles.", hidden=True)
                        pass

            elif button_ctx.custom_id == "Hydration Check Settings":
                if None not in (self.hydration_role_30mins, self.hydration_role_1hr, self.hydration_role_2hrs):
                    if any(x in self.member.roles for x in (self.hydration_role_30mins, self.hydration_role_1hr, self.hydration_role_2hrs)):
                        buttons = [
                            create_button(
                                style=ButtonStyle.green,
                                label="Change 'Check' Frequency",
                                custom_id="Change 'Check' Frequency"
                            ),
                            create_button(
                                style=ButtonStyle.red,
                                label="Remove Hydration Check Roles",
                                custom_id="Remove Hydration Check Roles"
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
                            if button_ctx.custom_id == "Remove Hydration Check Roles":
                                await self.member.remove_roles(*self.all_hydration_roles)
                                await button_ctx.send(button_ctx.author.mention + " Sucessfully **removed** all FitBot Hydration roles.", hidden=True)
                            elif button_ctx.custom_id == "Change 'Check' Frequency":
                                buttons = [
                                    create_button(
                                        style=ButtonStyle.green,
                                        label="Hydration Check - 30mins",
                                        custom_id="Hydration Check - 30mins"
                                    ),
                                    create_button(
                                        style=ButtonStyle.green,
                                        label="Hydration Check - 1hr",
                                        custom_id="Hydration Check - 1hr"
                                    ),
                                    create_button(
                                        style=ButtonStyle.green,
                                        label="Hydration Check - 2hrs",
                                        custom_id="Hydration Check - 2hrs"
                                    ),
                                ]
                                action_row = create_actionrow(*buttons)

                                embed.description = ""
                                embed.add_field(name="Hydration Check Frequency", value="Use the buttons below to configure the frequency of pings.", inline=False)
                                await button_ctx.edit_origin(embed=embed, components=[action_row], hidden=True)

                                while True:
                                    def check_ctx(button_ctx):
                                        return ctx.channel == button_ctx.channel

                                    button_ctx: ComponentContext = await wait_for_component(self.bot, check=check_ctx, components=[action_row])
                                    if button_ctx.custom_id == "Hydration Check - 30mins":
                                        if self.hydration_role_30mins is not None:
                                            if self.hydration_role_30mins in self.member.roles:
                                                await button_ctx.send(button_ctx.author.mention + " You already have the `Hydration Check - 30mins` role selected.", hidden=True)
                                            else:
                                                await self.member.remove_roles(*self.all_posture_roles)
                                                await self.member.add_roles(self.hydration_role_30mins)
                                                await button_ctx.send(button_ctx.author.mention + " `Hydration Check - 30mins` role successfully **added**.", hidden=True)

                                    if button_ctx.custom_id == "Hydration Check - 1hr":
                                        if self.hydration_role_1hr is not None:
                                            if self.hydration_role_1hr in self.member.roles:
                                                await button_ctx.send(button_ctx.author.mention + " You already have the `Hydration Check - 1hr` role selected.", hidden=True)
                                            else:
                                                await self.member.remove_roles(*self.all_posture_roles)
                                                await self.member.add_roles(self.hydration_role_1hr)
                                                await button_ctx.send(button_ctx.author.mention + " `Hydration Check - 1hr` role successfully **added**.", hidden=True)

                                    if button_ctx.custom_id == "Hydration Check - 2hrs":
                                        if self.hydration_role_2hrs is not None:
                                            if self.hydration_role_2hrs in self.member.roles:
                                                await button_ctx.send(button_ctx.author.mention + " You already have the `Hydration Check - 2hrs` role selected.", hidden=True)
                                            else:
                                                await self.member.remove_roles(*self.all_posture_roles)
                                                await self.member.add_roles(self.hydration_role_2hrs)
                                                await button_ctx.send(button_ctx.author.mention + " `Hydration Check - 2hrs` role successfully **added**.", hidden=True)
                    else:
                        await button_ctx.send(ctx.author.mention + " You do not have any `Hydration Check` roles.", hidden=True)
                        pass
