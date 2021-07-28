import asyncio
import discord
from discord.ext import commands
import requests
import json
import random as r


class Commands(commands.Cog):
    """Initialize the commands cog."""

    def __init__(self, bot) -> None:
        """Initialize the bot."""
        self.bot = bot

    @commands.command(pass_context=True)
    async def help(self, ctx):
        await ctx.send("```List of Commands:\n"
        "\n"
        "!initialize - Initializes bot\n"
        "!quote - Random inspirational quote\n"
        "!workout - Random 5-piece workout\n"
        "!bmi - BMI calculator\n"
        "!calories - Calorie calculator\n"
        "!changeprefix - Change command prefix\n"
        "!createrole - Create role\n"
        "!help - Help command\n```")

    @commands.command(pass_context=True, aliases=["createrole"])
    async def create_role(self, ctx, *, name) -> None:
        guild = ctx.guild
        await guild.create_role(name=name)
        await ctx.send(f"Role `{name}` has been created.")

    @commands.Cog.listener()
    async def get_quote(self) -> str:
        response = requests.get("https://type.fit/api/quotes")
        json_data = json.loads(response.text)
        random_quote = json_data[r.randint(0, len(
            json_data))]["text"] + " - " + json_data[r.randint(0, len(json_data))]["author"]
        return random_quote

    @commands.command(pass_context=True)
    async def quote(self, ctx) -> None:
        quote = await self.get_quote()
        await ctx.send(ctx.author.mention + ' ' + quote)

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

    @commands.command(pass_context=True)
    async def workout(self, ctx) -> None:
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
            description="Below is a list of 5 exercises for you to do, good luck.",
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
        embed.add_field(name="Exercise 2 " +
                        "- " +
                        str(r.choice(sets)) +
                        "x" +
                        str(r.choice(reps)) +
                        " reps", value=workouts[1], inline=False)
        embed.add_field(name="Exercise 3 " +
                        "- " +
                        str(r.choice(sets)) +
                        "x" +
                        str(r.choice(reps)) +
                        " reps", value=workouts[2], inline=False)
        embed.add_field(name="Exercise 4 " +
                        "- " +
                        str(r.choice(sets)) +
                        "x" +
                        str(r.choice(reps)) +
                        " reps", value=workouts[3], inline=False)
        embed.add_field(name="Exercise 5 " +
                        "- " +
                        str(r.choice(sets)) +
                        "x" +
                        str(r.choice(reps)) +
                        " reps", value=workouts[4], inline=False)

        await ctx.send(embed=embed)

    @commands.command(pass_context=True, aliases=["bmi"])
    async def bmi_calculator(self, ctx):
        await ctx.send("Please note, the following information is **not** saved by FitBot.")
        await ctx.send("There are limitations of the BMI, such as it not being able to "
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

        bmi = float(self.weight_msg.content) / (float(self.height_msg.content)/100)**2
        await ctx.send(ctx.author.mention + f" Your BMI (Body Mass Index) is `{bmi:.2f}`.")

        if bmi <= 18.4:
            await ctx.send("You are classed as `underweight`.")
        elif bmi <= 24.9:
            await ctx.send("You are classed as `healthy`.")
        elif bmi <= 29.9:
            await ctx.send("You are classed as `overweight`.")
        elif bmi <= 34.9:
            await ctx.send("You are classed as `severely overweight`.")
        elif bmi <= 39.9:
            await ctx.send("You are classed as `obese`.")
        else:
            await ctx.send("You are classed as `severely obese`.")

        await ctx.send("Don't worry if it's not what you want it to be, **you** can make the difference!")


    @commands.Cog.listener()
    async def height_listener(self, ctx) -> int:
        await ctx.send("Please enter your height in `cm`:")

        def check_height(msg) -> bool:
            value = msg.content
            try:
                return msg.author == ctx.author and msg.channel == ctx.channel and \
                isinstance(float(value), float)
            except ValueError:
                return False

        try:
            self.height_msg = await self.bot.wait_for("message", check=check_height, timeout=30)
            await ctx.send(f"Height selected: `{self.height_msg.content}cm`.")
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't respond in time! Please enter your height.")
            self.height = False
            return self.height
        else:
            await self.height_msg.add_reaction("👍")
            self.height = True
            return self.height

    @commands.Cog.listener()
    async def weight_listener(self, ctx) -> int:
        await ctx.send("Please enter your weight in `kg`:")

        def check_weight(msg) -> bool:
            value = msg.content
            try:
                return msg.author == ctx.author and msg.channel == ctx.channel and \
                isinstance(float(value), float)
            except ValueError:
                return False

        try:
            self.weight_msg = await self.bot.wait_for("message", check=check_weight, timeout=30)
            await ctx.send(f"Weight selected: `{self.weight_msg.content}kg`.")
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't respond in time! Please enter your weight.")
            self.weight = False
            return self.weight
        else:
            await self.weight_msg.add_reaction("👍")
            self.weight = True
            return self.weight

    @commands.Cog.listener()
    async def age_listener(self, ctx) -> int:
        await ctx.send("Please enter your age:")

        def check_age(msg) -> bool:
            value = msg.content
            try:
                return msg.author == ctx.author and msg.channel == ctx.channel and \
                isinstance(float(value), float)
            except ValueError:
                return False

        try:
            self.age_msg = await self.bot.wait_for("message", check=check_age, timeout=30)
            await ctx.send(f"Age selected: `{self.age_msg.content}`.")
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't respond in time! Please enter your age.")
            self.age = False
            return self.age
        else:
            await self.age_msg.add_reaction("👍")
            self.age = True
            return self.age

    @commands.Cog.listener()
    async def gender_listener(self, ctx) -> str:
        await ctx.send("Please enter your gender, type `m` for `male`, and `f` for `female`:")

        def check_gender(msg) -> bool:
            value = msg.content
            try:
                return msg.author == ctx.author and msg.channel == ctx.channel and \
                (value == 'm' or value == 'f')
            except ValueError:
                return False

        try:
            self.gender_msg = await self.bot.wait_for("message", check=check_gender, timeout=30)
            if self.gender_msg.content.lower() == 'm':
                await ctx.send("Gender selected: `Male`.")
            elif self.gender_msg.content.lower() == 'f':
                await ctx.send("Gender selected: `Female`.")
            else:
                await ctx.send("Invalid input, please try again.")
                self.gender = False
                return self.gender
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't respond in time! Please enter your gender.")
            self.gender = False
            return self.gender
        else:
            await self.gender_msg.add_reaction("👍")
            self.gender = True
            return self.gender

    @commands.Cog.listener()
    async def activity_listener(self, ctx) -> str:
        await ctx.send("Please enter your activity level, type:\n"
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
                return msg.author == ctx.author and msg.channel == ctx.channel and \
                (value in valid_inputs)
            except ValueError:
                return False

        try:
            self.activity_msg = await self.bot.wait_for("message", check=check_activity, timeout=30)
            if self.activity_msg.content.lower() == '1':
                await ctx.send("Activity level selected: `Sedentary: little or no exercise`.")
            elif self.activity_msg.content.lower() == '2':
                await ctx.send("Activity level selected: `Light: exercise 1-3 times/week`.")
            elif self.activity_msg.content.lower() == '3':
                await ctx.send("Activity level selected: `Moderate: exercise 4-5 times/week`.")
            elif self.activity_msg.content.lower() == '4':
                await ctx.send("Activity level selected: `Active: daily exercise or intense exercise 3-4 times/week`.")
            elif self.activity_msg.content.lower() == '5':
                await ctx.send("Activity level selected: `Very Active: intense exercise 6-7 times/week`.")
            elif self.activity_msg.content.lower() == '6':
                await ctx.send("Activity level selected: `Extremely Active: very intense exercise daily`.")
            else:
                await ctx.send("Invalid input, please try again.")
                self.activity = False
                return self.activity
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you didn't respond in time! Please enter your activity level.")
            self.activity = False
            return self.activity
        else:
            await self.activity_msg.add_reaction("👍")
            self.activity = True
            return self.activity

    @commands.command(pass_context=True, aliases=["calories"])
    async def calorie_calculator(self, ctx):
        await ctx.send("Please note, the following information is **not** saved by FitBot.")
        await ctx.send("Don't use this calorie calculator as medical advice. "
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
            msj_equation = (10 * float(self.weight_msg.content)) + (6.25 * float(self.height_msg.content)) - (5 * float(self.age_msg.content)) + 5
        elif self.gender_msg.content.lower() == 'f':
            msj_equation = (10 * float(self.weight_msg.content)) + (6.25 * float(self.height_msg.content)) - (5 * float(self.age_msg.content)) - 161
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

        await ctx.send(ctx.author.mention + f" Your Basal Metabolic Rate (BMR) is `{msj_equation:.0f}` calories. This is the "
        "number of calories your body burns just to function properly.")
        await ctx.send(f"To maintain your current weight, you should aim to consume `{total_calories:.0f}` calories per day.")
