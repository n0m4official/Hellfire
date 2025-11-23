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

# Sacred architecture block
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
    "cogs.anime_cog"
]

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    return json_data[0]['q'] + " -" + json_data[0]['a']

@bot.slash_command(name="inspire", description="Use this to get an inspirational quote")
async def inspire(interaction: nextcord.Interaction):
    await interaction.response.send_message(get_quote())


@bot.event
async def on_ready():
    print(f"Hellfire online as {bot.user}")

    # Send online announcements
    for guild in bot.guilds:
        config = bot.db.get_config(guild.id)

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

    if not bot.synced:
        await bot.sync_application_commands()
        bot.synced = True
        print("Slash commands synced successfully.")


# SAFE startup structure
if __name__ == "__main__":
    for cog in initial_cogs:
        bot.load_extension(cog)

    # Safe background task attach
    bot.loop.create_task(auto_clean_loop(bot))

    # Safe entry point
    bot.run(TOKEN)
