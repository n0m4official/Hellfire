import sqlite3

# Really basic database wrapper for server configurations 
# Uses SQLite for simplicity and ease of use
# Stores member role, inactive days, auto-clean status, and welcome channel
# Provides methods to get and set these configurations
# Designed to be straightforward and easy to integrate with the bot
# Kinda unnessary complexity for small bots, but useful for this one
# Kudos to SQLite for making database management so accessible

class Database:
    def __init__(self, path="hellfire.db"):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        self.setup()

    def setup(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS server_config (
            guild_id INTEGER PRIMARY KEY,
            member_role_id INTEGER,
            inactive_days INTEGER DEFAULT 90,
            auto_clean_enabled INTEGER DEFAULT 0,
            welcome_channel_id INTEGER
        )
        """)
        self.con.commit()

    def get_config(self, guild_id):
        row = self.cur.execute("""
            SELECT member_role_id, inactive_days, auto_clean_enabled, welcome_channel_id
            FROM server_config WHERE guild_id = ?
        """, (guild_id,)).fetchone()
        return row

    def set_member_role(self, guild_id, role_id):
        self.cur.execute("""
        INSERT INTO server_config (guild_id, member_role_id)
        VALUES (?, ?)
        ON CONFLICT(guild_id) DO UPDATE SET member_role_id=excluded.member_role_id
        """, (guild_id, role_id))
        self.con.commit()

    def set_inactive_days(self, guild_id, days):
        self.cur.execute("""
        INSERT INTO server_config (guild_id, inactive_days)
        VALUES (?, ?)
        ON CONFLICT(guild_id) DO UPDATE SET inactive_days=excluded.inactive_days
        """, (guild_id, days))
        self.con.commit()

    def toggle_auto_clean(self, guild_id, state):
        self.cur.execute("""
        INSERT INTO server_config (guild_id, auto_clean_enabled)
        VALUES (?, ?)
        ON CONFLICT(guild_id) DO UPDATE SET auto_clean_enabled=excluded.auto_clean_enabled
        """, (guild_id, state))
        self.con.commit()

    def set_welcome_channel(self, guild_id, channel_id):
        self.cur.execute("""
        INSERT INTO server_config (guild_id, welcome_channel_id)
        VALUES (?, ?)
        ON CONFLICT(guild_id) DO UPDATE SET welcome_channel_id=excluded.welcome_channel_id
        """, (guild_id, channel_id))
        self.con.commit()
