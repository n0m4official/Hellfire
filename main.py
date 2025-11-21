import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
import os

from database import Database

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = nextcord.Intents.default()
intents.members = True

bot = commands.Bot(intents=intents)
db = Database()

@bot.event
async def on_ready():
    print(f"Hellfire connected as {bot.user}")

# Load cogs
initial_cogs = [
    "cogs.cleanup",
    "cogs.config",
    "cogs.utility"
]

for cog in initial_cogs:
    bot.load_extension(cog)

bot.run(TOKEN)
