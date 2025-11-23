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
intents.message_content = True

# REMINDER:
#          DO NOT FUCKING TOUCH LINES 23 -> 28
#          DO NOT TOUCH THE ARCHITECHTURE, I SWEAR IF I HAVE TO REBUILD IT AGAIN... -_-
bot = commands.Bot(command_prefix="!", intents=intents, activity=nextcord.Game(name="with Hellfire 🔥"))
bot.db = Database()

owner_id = int(os.getenv("BOT_OWNER_ID"))
bot.owner_id = owner_id

# Also, fuck you pylint, my lines are a reasonable length!

bot.synced = False

initial_cogs = [
    "cogs.cleanup",
    "cogs.config",
    "cogs.utility",
    "cogs.anti_raid",
    "cogs.welcome",
    "cogs.assistance",
    "cogs.anime_cog"
]

# Inspirational Quote Command
# Fetch quote from API
# https://zenquotes.io/
# Example response: [{"q":"Your time is limited, so don't waste it living someone else's life.","a":"Steve Jobs"}]
# Does not store any user data
# This was surprisingly easy to implement correctly with nextcord's slash commands
# Kudos to their devs for making it straightforward
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

    # Send online announcement to each server
    for guild in bot.guilds:
        config = bot.db.get_config(guild.id)

        # status channel is config[4]
        status_channel_id = None
        if config and len(config) >= 5 and config[4]:
            status_channel_id = config[4]
        elif guild.system_channel:
            status_channel_id = guild.system_channel.id

        if status_channel_id:
            channel = guild.get_channel(status_channel_id)
            if channel:
                try:
                    await channel.send("🔥 **Hellfire is now online!**")
                except:
                    pass

    # Sync slash commands
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
