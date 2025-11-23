import nextcord
from nextcord.ext import commands

# Config Cog for setting member role
# Used in cleanup operations
# Allows admins to define which role is considered 'member'
# This is important for bots that perform member management tasks
# such as auto-cleanup of inactive members
# Provides a slash command to set the member role
# Stores the role ID in the bot's database for later use
# Ensures only admins can use the command
# Sends confirmation message upon successful update
# Utilizes ephemeral messages for privacy
# Integrates with the bot's existing database methods
# Designed to be simple and straightforward for ease of use
# Kudos to nextcord for making slash command implementation easy

# Also, why was this the easiest cog to implement correctly? -_-
# No seriously, this took me like 10 minutes to code and test compared to hours for other cogs, why was this so easy???

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
    
    @nextcord.slash_command(
    name="setstatuschannel",
    description="Set the channel Hellfire uses for online/offline announcements."
    )
    async def setstatuschannel(self, interaction: nextcord.Interaction,
                            channel: nextcord.TextChannel):

        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message(
                "Admin only.", ephemeral=True)

        self.bot.db.set_status_channel(interaction.guild.id, channel.id)

        await interaction.response.send_message(
            f"Status channel set to {channel.mention}.", ephemeral=True
        )


def setup(bot):
    bot.add_cog(Config(bot))
