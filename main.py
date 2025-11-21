import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

from database import Database
from scheduler import auto_clean_loop

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = nextcord.Intents.default()
intents.members = True

bot = commands.Bot(intents=intents)
bot.db = Database()

initial_cogs = [
    "cogs.cleanup",
    "cogs.config",
    "cogs.utility",
    "cogs.anti_raid",
    "cogs.welcome"
]

@bot.event
async def on_ready():
    print(f"Hellfire online as {bot.user}")

async def main():
    for cog in initial_cogs:
        bot.load_extension(cog)

    bot.loop.create_task(auto_clean_loop(bot))

    await bot.start(TOKEN)

asyncio.run(main())
