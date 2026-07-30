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

@bot.command()
async def testbot(ctx):
    await ctx.send("Mon bot fonctionne !")

bot.run(TOKEN)
