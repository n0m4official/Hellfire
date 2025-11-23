import os
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

        # Announce offline to all servers
        await announce_offline(self.bot)

        await interaction.response.send_message(
            "Shutting down... goodnight ✨", ephemeral=True)

        await self.bot.close()

    @nextcord.slash_command(name="restart", description="Restart Hellfire (bot owner only).")
    async def restart(self, interaction: nextcord.Interaction):
        if interaction.user.id != self.bot.owner_id:
            return await interaction.response.send_message(
                "Only my creator can restart me. 💫", ephemeral=True)

        # Announce offline to all servers
        await announce_offline(self.bot)

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


async def announce_offline(bot):
    """Send offline message to all servers using their configured status channel."""
    for guild in bot.guilds:
        config = bot.db.get_config(guild.id)
        
        # status_channel_id is config[4]
        status_channel_id = None
        if config and len(config) >= 5 and config[4]:
            status_channel_id = config[4]
        elif guild.system_channel:
            status_channel_id = guild.system_channel.id

        if status_channel_id:
            channel = guild.get_channel(status_channel_id)
            if channel:
                try:
                    await channel.send("⚠️ **Hellfire is going offline.** She’ll be back soon.")
                except:
                    pass


def setup(bot):
    bot.add_cog(Utility(bot))
