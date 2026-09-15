class PlaceholdersRepository:  # bot.repos.placeholders
    def __init__(self, db, repos):
        self.db = db
        self.repos = repos

    def add(self, guild_id: int, placeholder: str, replace_text: str, role_id: int = None):
        self.db.cursor.execute("""
            DELETE FROM placeholders
            WHERE guild_id = ? AND placeholder = ?
        """, (guild_id, placeholder))
        self.db.cursor.execute("""
            INSERT INTO placeholders
            (guild_id, placeholder, replace_text, role_id)
            VALUES (?, ?, ?, ?)
        """, (guild_id, placeholder, replace_text, role_id))
        self.db.connection.commit()
        return True

    def list(self, guild_id: int):
        self.db.cursor.execute("""
            SELECT placeholder, replace_text, role_id
            FROM placeholders
            WHERE guild_id = ?
            ORDER BY placeholder
        """, (guild_id,))
        rows = self.db.cursor.fetchall()
        return [
            {
                "placeholder": row[0],
                "replace_text": row[1],
                "role_id": row[2],
            }
            for row in rows
        ]

    def remove(self, guild_id: int, placeholder: str):
        self.db.cursor.execute("""
            DELETE FROM placeholders
            WHERE guild_id = ? AND placeholder = ?
        """, (guild_id, placeholder))
        self.db.connection.commit()
        return self.db.cursor.rowcount > 0
