import nextcord
from nextcord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="test", description="Check if Hellfire is online.")
    async def test(self, interaction: nextcord.Interaction):
        await interaction.response.send_message(
            "Hellfire is awake and ready. ✨🚀", ephemeral=True)

    @nextcord.slash_command(name="shutdown", description="Shutdown Hellfire (bot owner only).")
    async def shutdown(self, interaction: nextcord.Interaction):
        if interaction.user.id != self.bot.owner_id:
            return await interaction.response.send_message(
                "Only my creator can shut me down. 💫", ephemeral=True)

        await interaction.response.send_message(
            "Shutting down... goodnight ✨", ephemeral=True)
        await self.bot.close()

def setup(bot):
    bot.add_cog(Utility(bot))
