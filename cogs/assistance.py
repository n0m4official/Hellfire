import nextcord
from nextcord.ext import commands

# Assistance cog providing help command
# Provides users with a list of available commands and their descriptions
# Helps users understand how to interact with the bot

# Pretty straightforward cog
# Just a simple help command to improve user experience
# Pretty obvious implementation and why it's needed

class Assistance(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="help",
        description="Get a list of available commands."
    )
    async def help(self, interaction: nextcord.Interaction):
        help_message = (
            "**Available Commands:**\n"
            "/help - Show this help message.\n"
            "/setwelcome - Set the welcome message channel (Admin only).\n"
            "/setmemberrole - Define the member role for cleanup (Admin only).\n"
            "/test - Check if the bot is online.\n"
            "/shutdown - Shutdown the bot (Owner only).\n"
            "/inspire - Get an inspirational quote.\n"
            "/anime - Search for anime information.\n"
            "/manga - Search for manga information.\n"
            "/purgenoroles - Remove users without the member role (Admin only).\n"
            "/purgeinactive - Remove inactive users (Admin only).\n"
            "/trending - Displays the current top 10 most popular anime\n"
            "/character - Search anime characters"
        )
        await interaction.response.send_message(help_message, ephemeral=True)

def setup(bot):
    bot.add_cog(Assistance(bot))