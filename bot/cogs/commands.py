import asyncio
import discord
from discord.ext import commands
import requests
import json
import random as r
from discord_slash import cog_ext
from discord_slash.utils.manage_components import *
from discord_slash.model import ButtonStyle
from .core import Core
from oauth2.models import CalorieLogEntry


class Commands(commands.Cog):
    """Initialize the commands cog."""

    def __init__(self, bot) -> None:
        """Initialize the bot."""
        self.bot = bot
        self.core = Core(bot)

    @cog_ext.cog_slash(name="log",
                       description="Log command.",
                       guild_ids=[799768142045249606, 873664168685883422])
    async def log(self, ctx) -> None:
        await self.send_dm(ctx, ctx.author, content="Please note, the following information is **not** saved by FitBot.")
        
        self.log = False

        self.log = await self.log_listener(ctx)
        while (self.log == False):
            await self.log_listener(ctx)
    
    @commands.Cog.listener()
    async def log_listener(self, ctx) -> bool:
        await ctx.send(ctx.author.mention + " Please visit your DM's to enter the information safely and securely.", hidden=True)
        await self.send_dm(ctx, ctx.author, content="Please input the number of calories you've consumed today:")

        def check_calories(msg) -> bool:
            value = msg.content
            try:
                return msg.author == ctx.author and isinstance(
                    msg.channel, discord.channel.DMChannel) and isinstance(
                    int(value), int)
            except ValueError:
                return False

        try:
            self.calorie_msg = await self.bot.wait_for("message", check=check_calories, timeout=30)
            await self.send_dm(ctx, ctx.author, content=f"Value inputted: `{self.calorie_msg.content}` calories.")

            # BUG
            CalorieLogEntry.objects.create(calories=self.calorie_msg.content, user=self.calorie_msg.author)
        except asyncio.TimeoutError:
            await self.send_dm(ctx, ctx.author, content="Sorry, you didn't respond in time! Please input the number of calories consumed today: ")
            self.log = False
            return self.log
        else:
            await self.calorie_msg.add_reaction("👍")
            self.log = True
            return self.log

    @cog_ext.cog_slash(name="help",
                       description="Help command.",
                       guild_ids=[799768142045249606, 873664168685883422])
    async def help(self, ctx) -> None:
        select = create_select(
            options=[
                create_select_option(
                    "/initialize",
                    value="initialize",
                    description="Initializes FitBot"),
                create_select_option(
                    "/quote",
                    value="quote",
                    description="Random inspirational quote"),
                create_select_option(
                    "/workout",
                    value="workout",
                    description="Random 5-piece workout"),
                create_select_option(
                    "/bmi", value="bmi", description="BMI calculator"),
                create_select_option(
                    "/calories",
                    value="calories",
                    description="Calorie calculator"),
                create_select_option(
                    "/help", value="help", description="Help command"),
            ],
            placeholder="Select...",
            # The placeholder text to show when no options have been chosen
            min_values=1,  # The minimum number of options a user must select
            max_values=1,  # The maximum number of options a user can select
        )
        await ctx.send("List of Commands:", components=[create_actionrow(select)], hidden=True)

        while True:
            def check_ctx(button_ctx):
                return ctx.author_id == button_ctx.author_id and ctx.channel == button_ctx.channel

            select_ctx: ComponentContext = await wait_for_component(self.bot, check=check_ctx, components=select)

            if select_ctx.channel != ctx.channel:
                return
            if select_ctx.channel == ctx.channel:
                if select_ctx.selected_options[0] == "initialize":
                    await self.core.initialize.invoke(select_ctx)
                elif select_ctx.selected_options[0] == "quote":
                    await self.quote.invoke(select_ctx)
                elif select_ctx.selected_options[0] == "workout":
                    await self.workout.invoke(select_ctx)
                elif select_ctx.selected_options[0] == "bmi":
                    await self.bmi_calculator.invoke(select_ctx)
                elif select_ctx.selected_options[0] == "calories":
                    await self.calorie_calculator.invoke(select_ctx)
                elif select_ctx.selected_options[0] == "help":
                    await self.help.invoke(select_ctx)

    async def send_dm(self, ctx, member: discord.Member, *, content):
        channel = await member.create_dm()
        await channel.send(content)

    @commands.Cog.listener()
    async def get_quote(self) -> str:
        response = requests.get("https://type.fit/api/quotes")
        json_data = json.loads(response.text)
        random_quote = json_data[r.randint(0, len(
            json_data))]["text"] + " - " + json_data[r.randint(0, len(json_data))]["author"]
        return random_quote

    @cog_ext.cog_slash(name="quote",
                       description="Random inspirational quote.",
                       guild_ids=[799768142045249606, 873664168685883422])
    async def quote(self, ctx) -> None:
        quote = await self.get_quote()
        await ctx.send(ctx.author.mention + ' ' + quote, hidden=True)

    @commands.Cog.listener()
    async def get_workout(self) -> list:
        response = requests.get("https://wger.de/api/v2/exercise/?language=2")
        json_data = json.loads(response.text)
        workouts = []
        for i in range(5):
            workouts.append(json_data["results"][r.randint(0, len(json_data["results"]) - 3)]["name"] + \
                            ": " + "\n" + json_data["results"][r.randint(0, len(json_data["results"]) - 3)]["description"])
            i += 1
        return workouts

    @cog_ext.cog_slash(name="workout",
                       description="Random 5-piece workout.",
                       guild_ids=[799768142045249606, 873664168685883422])
    async def workout(self, ctx) -> None:
        buttons = [
            create_button(
                style=ButtonStyle.green,
                label="<<",
                custom_id="<<"
            ),
            create_button(
                style=ButtonStyle.blue,
                label="Generate New Workout",
                custom_id="Generate New Workout"
            ),
            create_button(
                style=ButtonStyle.green,
                label=">>",
                custom_id=">>"
            ),
        ]
        action_row = create_actionrow(*buttons)

        workout = await self.get_workout()
        workouts = [
            w.replace(
                "<p>",
                "").replace(
                "</p>",
                "").replace(
                "<ul>",
                "").replace(
                "</ul>",
                "").replace(
                "<em>",
                "").replace(
                "</em>",
                "").replace(
                "<li>",
                "").replace(
                "</li>",
                "").replace(
                "<ol>",
                "").replace(
                "</ol>",
                "") for w in workout]

        sets = [1, 2, 3]
        reps = [5, 10, 15]

        embed = discord.Embed(
            title="Quick Workout",
            description="The following is a set of 5 exercises, please use the arrows to move between exercises, good luck.",
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
        embed.add_field(name="Exercise 1 " +
                        "- " +
                        str(r.choice(sets)) +
                        "x" +
                        str(r.choice(reps)) +
                        " reps", value=workouts[0], inline=False)

        await ctx.send(embed=embed, components=[action_row], hidden=True)

        i = 1
        while True:
            def check_ctx(button_ctx):
                return ctx.author_id == button_ctx.author_id and ctx.channel == button_ctx.channel

            button_ctx: ComponentContext = await wait_for_component(self.bot, check=check_ctx, components=[action_row])

            if button_ctx.custom_id == ">>":
                try:
                    if i >= 5:
                        i = 1
                        embed.remove_field(2)
                        embed.add_field(name="Exercise 1 " +
                                        "- " +
                                        str(r.choice(sets)) +
                                        "x" +
                                        str(r.choice(reps)) +
                                        " reps", value=workouts[i - 1], inline=False)
                        await button_ctx.edit_origin(embed=embed, components=[action_row], hidden=True)

                    else:
                        embed.remove_field(2)
                        embed.add_field(name=f"Exercise {i + 1} " +
                                        "- " +
                                        str(r.choice(sets)) +
                                        "x" +
                                        str(r.choice(reps)) +
                                        " reps", value=workouts[i], inline=False)
                        await button_ctx.edit_origin(embed=embed, components=[action_row], hidden=True)
                        i += 1
                except IndexError:
                    pass

            elif button_ctx.custom_id == "<<":
                try:
                    if i <= 1:
                        i = 5
                        embed.remove_field(2)
                        embed.add_field(name="Exercise 5 " +
                                        "- " +
                                        str(r.choice(sets)) +
                                        "x" +
                                        str(r.choice(reps)) +
                                        " reps", value=workouts[i - 1], inline=False)
                        await button_ctx.edit_origin(embed=embed, components=[action_row], hidden=True)
                    else:
                        embed.remove_field(2)

                        embed.add_field(name=f"Exercise {i - 1} " +
                                        "- " +
                                        str(r.choice(sets)) +
                                        "x" +
                                        str(r.choice(reps)) +
                                        " reps", value=workouts[i - 2], inline=False)
                        await button_ctx.edit_origin(embed=embed, components=[action_row], hidden=True)
                        i -= 1
                except IndexError:
                    pass

            elif button_ctx.custom_id == "Generate New Workout":
                await button_ctx.edit_origin(content="A new workout has been generated below.", embed=None, components=None, hidden=True)
                await self.workout.invoke(button_ctx)
                return

    @cog_ext.cog_slash(name="bmi",
                       description="BMI calculator.",
                       guild_ids=[799768142045249606, 873664168685883422])
    async def bmi_calculator(self, ctx):
        await ctx.send(ctx.author.mention + " Please visit your DM's to enter the information safely and securely.", hidden=True)
        await self.send_dm(ctx, ctx.author, content="Please note, the following information is **not** saved by FitBot.")
        await self.send_dm(ctx, ctx.author, content="There are limitations of the BMI, such as it not being able to "
                           "tell the difference between excess fat, muscle or bone. It also doesn't take into account "
                           "age, gender or muscle mass. Please don't use the BMI as a form of medical advice.")

        self.height = False
        self.weight = False

        self.height = await self.height_listener(ctx)
        while (self.height == False):
            await self.height_listener(ctx)

        self.weight = await self.weight_listener(ctx)
        while (self.weight == False):
            await self.weight_listener(ctx)

        bmi = float(self.weight_msg.content) / \
            (float(self.height_msg.content) / 100)**2
        await self.send_dm(ctx, ctx.author, content=ctx.author.mention + f" Your BMI (Body Mass Index) is `{bmi:.2f}`.")

        if bmi <= 18.4:
            await self.send_dm(ctx, ctx.author, content="You are classed as `underweight`.")
        elif bmi <= 24.9:
            await self.send_dm(ctx, ctx.author, content="You are classed as `healthy`.")
        elif bmi <= 29.9:
            await self.send_dm(ctx, ctx.author, content="You are classed as `overweight`.")
        elif bmi <= 34.9:
            await self.send_dm(ctx, ctx.author, content="You are classed as `severely overweight`.")
        elif bmi <= 39.9:
            await self.send_dm(ctx, ctx.author, content="You are classed as `obese`.")
        else:
            await self.send_dm(ctx, ctx.author, content="You are classed as `severely obese`.")

        await self.send_dm(ctx, ctx.author, content="Don't worry if it's not what you want it to be, **you** can make the difference!")

    @commands.Cog.listener()
    async def height_listener(self, ctx) -> bool:
        await self.send_dm(ctx, ctx.author, content="Please enter your height in `cm`:")

        def check_height(msg) -> bool:
            value = msg.content
            try:
                return msg.author == ctx.author and isinstance(
                    msg.channel, discord.channel.DMChannel) and isinstance(
                    float(value), float)
            except ValueError:
                return False

        try:
            self.height_msg = await self.bot.wait_for("message", check=check_height, timeout=30)
            await self.send_dm(ctx, ctx.author, content=f"Height selected: `{self.height_msg.content}cm`.")
        except asyncio.TimeoutError:
            await self.send_dm(ctx, ctx.author, content="Sorry, you didn't respond in time! Please enter your height.")
            self.height = False
            return self.height
        else:
            await self.height_msg.add_reaction("👍")
            self.height = True
            return self.height

    @commands.Cog.listener()
    async def weight_listener(self, ctx) -> bool:
        await self.send_dm(ctx, ctx.author, content="Please enter your weight in `kg`:")

        def check_weight(msg) -> bool:
            value = msg.content
            try:
                return msg.author == ctx.author and isinstance(
                    msg.channel, discord.channel.DMChannel) and isinstance(
                    float(value), float)
            except ValueError:
                return False

        try:
            self.weight_msg = await self.bot.wait_for("message", check=check_weight, timeout=30)
            await self.send_dm(ctx, ctx.author, content=f"Weight selected: `{self.weight_msg.content}kg`.")
        except asyncio.TimeoutError:
            await self.send_dm(ctx, ctx.author, content="Sorry, you didn't respond in time! Please enter your weight.")
            self.weight = False
            return self.weight
        else:
            await self.weight_msg.add_reaction("👍")
            self.weight = True
            return self.weight

    @commands.Cog.listener()
    async def age_listener(self, ctx) -> bool:
        await self.send_dm(ctx, ctx.author, content="Please enter your age:")

        def check_age(msg) -> bool:
            value = msg.content
            try:
                return msg.author == ctx.author and isinstance(
                    msg.channel, discord.channel.DMChannel) and isinstance(
                    float(value), float)
            except ValueError:
                return False

        try:
            self.age_msg = await self.bot.wait_for("message", check=check_age, timeout=30)
            await self.send_dm(ctx, ctx.author, content=f"Age selected: `{self.age_msg.content}`.")
        except asyncio.TimeoutError:
            await self.send_dm(ctx, ctx.author, content="Sorry, you didn't respond in time! Please enter your age.")
            self.age = False
            return self.age
        else:
            await self.age_msg.add_reaction("👍")
            self.age = True
            return self.age

    @commands.Cog.listener()
    async def gender_listener(self, ctx) -> bool:
        await self.send_dm(ctx, ctx.author, content="Please enter your gender, type `m` for `male`, and `f` for `female`:")

        def check_gender(msg) -> bool:
            value = msg.content.lower()
            try:
                return msg.author == ctx.author and isinstance(
                    msg.channel, discord.channel.DMChannel) and (
                    value == 'm' or value == 'f')
            except ValueError:
                return False

        try:
            self.gender_msg = await self.bot.wait_for("message", check=check_gender, timeout=30)
            if self.gender_msg.content.lower() == 'm':
                await self.send_dm(ctx, ctx.author, content="Gender selected: `Male`.")
            elif self.gender_msg.content.lower() == 'f':
                await self.send_dm(ctx, ctx.author, content="Gender selected: `Female`.")
            else:
                await self.send_dm(ctx, ctx.author, content="Invalid input, please try again.")
                self.gender = False
                return self.gender
        except asyncio.TimeoutError:
            await self.send_dm(ctx, ctx.author, content="Sorry, you didn't respond in time! Please enter your gender.")
            self.gender = False
            return self.gender
        else:
            await self.gender_msg.add_reaction("👍")
            self.gender = True
            return self.gender

    @commands.Cog.listener()
    async def activity_listener(self, ctx) -> bool:
        await self.send_dm(ctx, ctx.author, content="Please enter your activity level, type:\n"
                           "`1` for Sedentary: little or no exercise\n"
                           "`2` for Light: exercise 1-3 times/week\n"
                           "`3` for Moderate: exercise 4-5 times/week\n"
                           "`4` for Active: daily exercise or intense exercise 3-4 times/week\n"
                           "`5` for Very Active: intense exercise 6-7 times/week\n"
                           "`6` for Extremely Active: very intense exercise daily\n")

        def check_activity(msg) -> bool:
            value = msg.content
            try:
                valid_inputs = ['1', '2', '3', '4', '5', '6']
                return msg.author == ctx.author and isinstance(
                    msg.channel, discord.channel.DMChannel) and (
                    value in valid_inputs)
            except ValueError:
                return False

        try:
            self.activity_msg = await self.bot.wait_for("message", check=check_activity, timeout=30)
            if self.activity_msg.content.lower() == '1':
                await self.send_dm(ctx, ctx.author, content="Activity level selected: `Sedentary: little or no exercise`.")
            elif self.activity_msg.content.lower() == '2':
                await self.send_dm(ctx, ctx.author, content="Activity level selected: `Light: exercise 1-3 times/week`.")
            elif self.activity_msg.content.lower() == '3':
                await self.send_dm(ctx, ctx.author, content="Activity level selected: `Moderate: exercise 4-5 times/week`.")
            elif self.activity_msg.content.lower() == '4':
                await self.send_dm(ctx, ctx.author, content="Activity level selected: `Active: daily exercise or intense exercise 3-4 times/week`.")
            elif self.activity_msg.content.lower() == '5':
                await self.send_dm(ctx, ctx.author, content="Activity level selected: `Very Active: intense exercise 6-7 times/week`.")
            elif self.activity_msg.content.lower() == '6':
                await self.send_dm(ctx, ctx.author, content="Activity level selected: `Extremely Active: very intense exercise daily`.")
            else:
                await self.send_dm(ctx, ctx.author, content="Invalid input, please try again.")
                self.activity = False
                return self.activity
        except asyncio.TimeoutError:
            await self.send_dm(ctx, ctx.author, content="Sorry, you didn't respond in time! Please enter your activity level.")
            self.activity = False
            return self.activity
        else:
            await self.activity_msg.add_reaction("👍")
            self.activity = True
            return self.activity

    @cog_ext.cog_slash(name="calories",
                       description="Calorie calculator.",
                       guild_ids=[799768142045249606, 873664168685883422])
    async def calorie_calculator(self, ctx):
        await ctx.send(ctx.author.mention + " Please visit your DM's to enter the information safely and securely.", hidden=True)
        await self.send_dm(ctx, ctx.author, content="Please note, the following information is **not** saved by FitBot.")
        await self.send_dm(ctx, ctx.author, content="Don't use this calorie calculator as medical advice. "
                           "If you are unsure about your diet, please consult a professional dietician.")

        self.height = False
        self.weight = False
        self.age = False
        self.gender = False
        self.activity = False

        self.height = await self.height_listener(ctx)
        while (self.height == False):
            await self.height_listener(ctx)

        self.weight = await self.weight_listener(ctx)
        while (self.weight == False):
            await self.weight_listener(ctx)

        self.age = await self.age_listener(ctx)
        while (self.age == False):
            await self.age_listener(ctx)

        self.gender = await self.gender_listener(ctx)
        while (self.gender == False):
            await self.gender_listener(ctx)

        self.acitivty = await self.activity_listener(ctx)
        while (self.acitivty == False):
            await self.activity_listener(ctx)

        if self.gender_msg.content.lower() == 'm':
            msj_equation = (10 * float(self.weight_msg.content)) + (6.25 * float(
                self.height_msg.content)) - (5 * float(self.age_msg.content)) + 5
        elif self.gender_msg.content.lower() == 'f':
            msj_equation = (10 * float(self.weight_msg.content)) + (6.25 * float(
                self.height_msg.content)) - (5 * float(self.age_msg.content)) - 161
        else:
            return

        if self.activity_msg.content == '1':
            total_calories = msj_equation * 1.2
        elif self.activity_msg.content == '2':
            total_calories = msj_equation * 1.375
        elif self.activity_msg.content == '3':
            total_calories = msj_equation * 1.465
        elif self.activity_msg.content == '4':
            total_calories = msj_equation * 1.55
        elif self.activity_msg.content == '5':
            total_calories = msj_equation * 1.725
        elif self.activity_msg.content == '6':
            total_calories = msj_equation * 1.9
        else:
            return

        await self.send_dm(ctx, ctx.author, content=ctx.author.mention + f" Your Basal Metabolic Rate (BMR) is `{msj_equation:.0f}` calories. This is the "
                           "number of calories your body burns just to function properly.")
        await self.send_dm(ctx, ctx.author, content=f"To maintain your current weight, you should aim to consume `{total_calories:.0f}` calories per day.")
