import json
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
import os
import asyncio

import requests

from database import Database
from scheduler import auto_clean_loop

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = nextcord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents, activity=nextcord.Game(name="with Hellfire 🔥"))
bot.db = Database()

owner_id = int(os.getenv("BOT_OWNER_ID"))
bot.owner_id = owner_id

bot.synced = False

initial_cogs = [
    "cogs.cleanup",
    "cogs.config",
    "cogs.utility",
    "cogs.anti_raid",
    "cogs.welcome",
    "cogs.assistance",
    "cogs.silly"
]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote

@bot.slash_command(name="inspire", description="Use this to get an inspirational quote")
async def inspire(interaction: nextcord.Interaction):
    quote = get_quote()
    await interaction.response.send_message(quote)

@bot.event
async def on_ready():
    print(f"Hellfire online as {bot.user}")

    # Sync only once
    if not bot.synced:
        await bot.sync_application_commands()
        bot.synced = True
        print("Slash commands synced successfully.")

async def main():
    for cog in initial_cogs:
        bot.load_extension(cog)

    bot.loop.create_task(auto_clean_loop(bot))
    await bot.start(TOKEN)

asyncio.run(main())
