import sqlite3


class Storage:
    def __init__(self, database_name: str):
        self.database_name = database_name
        with sqlite3.connect(database_name) as connection:
            cursor = connection.cursor()
            query = """
                CREATE TABLE IF NOT EXISTS stories(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author TEXT NOT NULL,
                title TEXT NOT NULL,
                story TEXT NOT NULL,
                created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
            )"""
            cursor.execute(query)
            connection.commit()

    def get_first_five_newest(self):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = """
                SELECT *
                FROM stories
                ORDER BY id DESC
                LIMIT 5
            """
            result = cursor.execute(query)
            return result.fetchall()

    def get_stories_by_title(self,  query_str: str):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = f"""
                SELECT *
                FROM stories
                WHERE title LIKE '%{query_str}%' OR author LIKE '%{query_str}%'
            """
            result = cursor.execute(query)
            return result.fetchall()

    def add_story(self, *, author: str, title: str, story: str):
        with sqlite3.connect(self.database_name) as connection:
            cursor = connection.cursor()
            query = """
                INSERT INTO stories(author, title, story)
                VALUES (?, ?, ?)
            """
            cursor.execute(query, (author, title, story))
            connection.commit()


database = Storage('database.sqlite3')
