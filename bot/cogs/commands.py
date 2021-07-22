import discord
from discord.ext import commands
import requests
import json
import random as r


class Commands(commands.Cog):
    """Initialize the commands cog."""

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
