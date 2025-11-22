import nextcord
from nextcord.ext import commands


# half of these just refused to work until I rebooted my laptop, like why did doing THAT fix it???
# REMINDER: 
#           DO NOT FUCKING TOUCH THIS FILE AGAIN I SWEAR TO GOD
#           IT WORKS NOW AND I DONT WANT TO SPEND ANOTHER 5 HOURS DEBUGGING THIS BULLSHIT
# sorry for my crash out, was frustrated and this file probably caused me the most issues today

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

    @nextcord.slash_command(name="restart", description="Restart Hellfire (bot owner only).")
    async def restart(self, interaction: nextcord.Interaction):
        if interaction.user.id != self.bot.owner_id:
            return await interaction.response.send_message(
                "Only my creator can restart me. 💫", ephemeral=True)

        await interaction.response.send_message(
            "Restarting... be right back! ✨", ephemeral=True)
        await self.bot.close()

    @nextcord.slash_command(name="reload", description="Reload all cogs (bot owner only).")
    async def reload(self, interaction: nextcord.Interaction):
        if interaction.user.id != self.bot.owner_id:
            return await interaction.response.send_message(
                "Only my creator can reload me. 💫", ephemeral=True)

        reloaded = []
        failed = []

        for ext in list(self.bot.extensions.keys()):
            try:
                self.bot.reload_extension(ext)
                reloaded.append(ext)
            except Exception as e:
                failed.append(f"{ext}: {e}")

        msg = f"🔄 Reloaded {len(reloaded)} modules.\n"
        if failed:
            msg += "\n❌ Failed:\n" + "\n".join(failed)

        await interaction.response.send_message(msg, ephemeral=True)



def setup(bot):
    bot.add_cog(Utility(bot))
