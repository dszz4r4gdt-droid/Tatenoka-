import discord
from discord.ext import commands
import os

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

@bot.event
async def on_ready():
    print(f"{bot.user} is online!")
    print("Commands:", [command.name for command in bot.commands])


@bot.command()
async def testbot(ctx):
    await ctx.send("Mon bot fonctionne !")


@bot.command()
async def ping(ctx):
    await ctx.send("Pong !")


@bot.command()
async def hello(ctx):
    await ctx.send(f"Salut {ctx.author.mention} !")


@bot.command()
async def info(ctx):
    await ctx.send("Je suis un bot Discord hébergé sur Railway.")


bot.run(TOKEN)
