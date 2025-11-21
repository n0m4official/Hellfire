import nextcord
from nextcord.ext import commands

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="setmemberrole",
        description="Define the role counted as 'member' for cleanup."
    )
    async def setmemberrole(self, interaction: nextcord.Interaction, role: nextcord.Role):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message(
                "Admin only.", ephemeral=True)

        self.bot.db.set_member_role(interaction.guild.id, role.id)

        await interaction.response.send_message(
            f"Member role updated to **{role.name}**.", ephemeral=True
        )

def setup(bot):
    bot.add_cog(Config(bot))
