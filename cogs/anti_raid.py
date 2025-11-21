import nextcord
from nextcord.ext import commands
from datetime import datetime, timedelta

class AntiRaid(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.join_history = {}

    @commands.Cog.listener()
    async def on_member_join(self, member):
        now = datetime.utcnow()
        guild_id = member.guild.id

        if guild_id not in self.join_history:
            self.join_history[guild_id] = []

        self.join_history[guild_id].append(now)

        self.join_history[guild_id] = [
            t for t in self.join_history[guild_id]
            if now - t < timedelta(minutes=2)
        ]

        if len(self.join_history[guild_id]) >= 5:
            channel = member.guild.system_channel
            if channel:
                await channel.send(
                    "⚠️ **Potential raid detected!** Multiple joins in 2 minutes."
                )

def setup(bot):
    bot.add_cog(AntiRaid(bot))
