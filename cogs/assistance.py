import nextcord
from nextcord.ext import commands

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
        )
        await interaction.response.send_message(help_message, ephemeral=True)

def setup(bot):
    bot.add_cog(Assistance(bot))