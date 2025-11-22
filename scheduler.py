import asyncio

# Auto-cleanup loop for removing inactive members
# Runs every 24 hours
# Checks each guild for auto-cleanup settings
# If enabled, removes members inactive for the configured number of days

# Kudos to nextcord for making bot integration straightforward
# This was surprisingly easy to implement correctly
# Kinda shocked me how smoothly this went compared to other features

async def auto_clean_loop(bot):
    await bot.wait_until_ready()

    while not bot.is_closed():
        for guild in bot.guilds:
            config = bot.db.get_config(guild.id)

            if not config:
                continue

            member_role_id, inactive_days, auto_clean_enabled, _ = config

            if auto_clean_enabled:
                cleanup_cog = bot.get_cog("Cleanup")
                if cleanup_cog:
                    await cleanup_cog.perform_auto_cleanup(guild)

        await asyncio.sleep(86400)  # 24 hours
