import nextcord
from nextcord.ext import commands
from datetime import datetime, timedelta

# Cleanup Cog for removing users without roles or inactive users
# Provides commands for admins to manage server membership
# Includes purging users without the configured member role
# and purging users inactive for a specified number of days
# Also supports automatic cleanup based on server configuration
# Integrates with the bot's existing database methods
# Ensures only admins can use the cleanup commands

# This was the original use case for the bot
# So this cog is pretty important for the bot's core functionality
# This one was fairly straightforward to implement compared to others
# Also shockingly easy to code, worked first try with 0 bugs -_- (which is kinda sus tbh)

class Cleanup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="purgenoroles",
        description="Remove users who do not have the configured member role."
    )
    async def purgenoroles(self, interaction: nextcord.Interaction):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message(
                "You must be an admin to use this.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)

        guild = interaction.guild
        config = self.bot.db.get_config(guild.id)

        if not config or not config[0]:
            return await interaction.followup.send(
                "No member role set! Use `/setmemberrole` first.", ephemeral=True)

        member_role = guild.get_role(config[0])
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
            f"Cleanup complete! ✨ Removed **{removed}** accounts.", ephemeral=True
        )

    @nextcord.slash_command(
        name="purgeinactive",
        description="Remove users inactive for X days without storing user data."
    )
    async def purgeinactive(self, interaction: nextcord.Interaction, days: int):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message(
                "You must be an admin.", ephemeral=True)

        await interaction.response.defer(ephemeral=True)

        cutoff = datetime.utcnow() - timedelta(days=days)
        removed = 0

        for member in interaction.guild.members:
            if member.bot:
                continue

            if member.activity or member.status != nextcord.Status.offline:
                continue

            joined = member.joined_at
            if joined and joined < cutoff:
                try:
                    await member.kick(reason=f"Inactive for {days}+ days")
                    removed += 1
                except:
                    pass

        await interaction.followup.send(
            f"Inactive purge complete! ✨ Removed **{removed}** users.",
            ephemeral=True
        )

    async def perform_auto_cleanup(self, guild):
        config = self.bot.db.get_config(guild.id)
        if not config:
            return

        member_role_id, inactive_days, enabled, _ = config

        if not enabled:
            return

        cutoff = datetime.utcnow() - timedelta(days=inactive_days)

        for member in guild.members:
            if member.bot:
                continue
            if member.joined_at and member.joined_at < cutoff:
                try:
                    await member.kick(reason="Auto-clean inactive")
                except:
                    pass

def setup(bot):
    bot.add_cog(Cleanup(bot))
