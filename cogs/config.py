import nextcord
from nextcord.ext import commands
from database import Database

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db: Database = bot.db if hasattr(bot, "db") else Database()

    @nextcord.slash_command(
        name="setmemberrole",
        description="Set the role that counts as a 'member' for cleanup."
    )
    async def setmemberrole(self, interaction: nextcord.Interaction, role: nextcord.Role):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message(
                "You need admin permissions to use this.", ephemeral=True)

        self.db.set_member_role(interaction.guild.id, role.id)

        await interaction.response.send_message(
            f"Member role updated to **{role.name}**! Hellfire is locked on target. 🔧✨",
            ephemeral=True
        )

def setup(bot):
    if not hasattr(bot, "db"):
        bot.db = Database()
    bot.add_cog(Config(bot))
