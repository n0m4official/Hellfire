import nextcord
from nextcord.ext import commands
from database import Database

class Cleanup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db: Database = bot.db if hasattr(bot, "db") else Database()

    @nextcord.slash_command(
        name="purgenoroles",
        description="Remove users with no member role assigned."
    )
    async def purgenoroles(self, interaction: nextcord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message(
                "You need admin permissions to launch cleanup.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)

        guild = interaction.guild
        member_role_id = self.db.get_member_role(guild.id)

        if not member_role_id:
            return await interaction.followup.send(
                "No member role configured! Use `/setmemberrole` first.", ephemeral=True)

        member_role = guild.get_role(member_role_id)
        removed = 0

        for member in guild.members:
            if member.bot:
                continue

            if member_role in member.roles:
                continue

            try:
                await member.kick(reason="No member role (Hellfire cleanup)")
                removed += 1
            except:
                pass

        await interaction.followup.send(
            f"Cleanup complete! ✨ Hellfire successfully removed **{removed}** accounts.",
            ephemeral=True
        )

def setup(bot):
    if not hasattr(bot, "db"):
        bot.db = Database()
    bot.add_cog(Cleanup(bot))
