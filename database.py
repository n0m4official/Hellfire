import sqlite3

class Database:
    def __init__(self, path="hellfire.db"):
        self.con = sqlite3.connect(path)
        self.cur = self.con.cursor()
        self.setup()

    def setup(self):
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS server_config (
            guild_id INTEGER PRIMARY KEY,
            member_role_id INTEGER
        )
        """)
        self.con.commit()

    def set_member_role(self, guild_id, role_id):
        self.cur.execute("""
        INSERT INTO server_config (guild_id, member_role_id)
        VALUES (?, ?)
        ON CONFLICT(guild_id) DO UPDATE SET member_role_id=excluded.member_role_id
        """, (guild_id, role_id))
        self.con.commit()

    def get_member_role(self, guild_id):
        row = self.cur.execute("""
        SELECT member_role_id FROM server_config WHERE guild_id = ?
        """, (guild_id,)).fetchone()
        return row[0] if row else None
