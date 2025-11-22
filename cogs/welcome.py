import nextcord
from nextcord.ext import commands

# Welcome cog to handle welcome messages
# Allows admins to set a welcome channel
# Sends a welcome message when a new member joins
# Simple and straightforward implementation

# Not necessary tbh, but nice to have for community servers
# Threw it in bc why not - adds a bit of flair to the bot (also because a server owner requested it)

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="setwelcome",
        description="Set the welcome message channel."
    )
    async def setwelcome(self, interaction: nextcord.Interaction, channel: nextcord.TextChannel):
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message(
                "You must be an admin.", ephemeral=True)

        self.bot.db.set_welcome_channel(interaction.guild.id, channel.id)
        await interaction.response.send_message(
            f"Welcome channel set to {channel.mention}!", ephemeral=True
        )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        config = self.bot.db.get_config(member.guild.id)
        if not config or not config[3]:
            return

        channel = member.guild.get_channel(config[3])
        if channel:
            await channel.send(f"Welcome {member.mention}! ✨")

def setup(bot):
    bot.add_cog(Welcome(bot))
