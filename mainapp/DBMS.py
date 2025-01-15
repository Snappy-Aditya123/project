import sqlite3
from typing import List, Tuple

class ChatDatabase:
    def __init__(self, db_name: str = "chatbot.db"):
        """
        Initialize the ChatDatabase class.
        :param db_name: Name of the SQLite database file.
        """
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self._create_tables()

    def _create_tables(self):
        """
        Create the necessary tables for storing chats.
        """
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS all_chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_message TEXT NOT NULL,
                bot_response TEXT NOT NULL
            )
            """
        )
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS last_three_chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                user_message TEXT NOT NULL,
                bot_response TEXT NOT NULL
            )
            """
        )
        self.connection.commit()

    def insert_chat(self, user_message: str, bot_response: str):
        """
        Insert a new chat into the all_chats table and update the last_three_chats table.
        :param user_message: The user's message.
        :param bot_response: The bot's response.
        """
        self.cursor.execute(
            "INSERT INTO all_chats (user_message, bot_response) VALUES (?, ?)",
            (user_message, bot_response)
        )
        self.connection.commit()
        self._update_last_three_chats(user_message, bot_response)

    def _update_last_three_chats(self, user_message: str, bot_response: str):
        """
        Update the last_three_chats table to keep only the last three chats.
        :param user_message: The user's message.
        :param bot_response: The bot's response.
        """
        self.cursor.execute(
            "INSERT INTO last_three_chats (user_message, bot_response) VALUES (?, ?)",
            (user_message, bot_response)
        )
        self.connection.commit()

        # Ensure only the last three chats are kept
        self.cursor.execute(
            """
            DELETE FROM last_three_chats
            WHERE id NOT IN (
                SELECT id FROM last_three_chats ORDER BY timestamp DESC LIMIT 3
            )
            """
        )
        self.connection.commit()

    def fetch_all_chats(self) -> List[Tuple[int, str, str, str]]:
        """
        Fetch all chats from the all_chats table.
        :return: List of tuples containing all chat records.
        """
        self.cursor.execute("SELECT * FROM all_chats ORDER BY timestamp ASC")
        return self.cursor.fetchall()

    def fetch_last_three_chats(self) -> List[Tuple[int, str, str, str]]:
        """
        Fetch the last three chats from the last_three_chats table.
        :return: List of tuples containing the last three chat records.
        """
        self.cursor.execute("SELECT * FROM last_three_chats ORDER BY timestamp DESC")
        return self.cursor.fetchall()

    def delete_chat_by_id(self, chat_id: int, table: str = "all_chats") -> bool:
        """
        Delete a chat by its ID from the specified table.
        :param chat_id: The ID of the chat to delete.
        :param table: The table from which to delete the chat (default is "all_chats").
        :return: True if a row was deleted, False otherwise.
        """
        if table not in ["all_chats", "last_three_chats"]:
            raise ValueError("Invalid table name. Use 'all_chats' or 'last_three_chats'.")

        self.cursor.execute(f"DELETE FROM {table} WHERE id = ?", (chat_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def close(self):
        """
        Close the database connection.
        """
        self.connection.close()

# Example usage
if __name__ == "__main__":
    db = ChatDatabase()

    # Insert some sample chats
    db.insert_chat("Hello!", "Hi there! How can I assist you?")
    db.insert_chat("What jobs are available?", "There are several openings. Let me fetch them for you.")
    db.insert_chat("Tell me about software engineering roles.", "Sure, here are some software engineering roles.")
    db.insert_chat("What about data science?", "Here are some data science opportunities.")

    # Fetch all chats
    print("All Chats:")
    for chat in db.fetch_all_chats():
        print(chat)

    # Fetch the last three chats
    print("\nLast Three Chats:")
    for chat in db.fetch_last_three_chats():
        print(chat)

    # Delete a chat by ID
    print("\nDeleting chat with ID 2 from all_chats...")
    if db.delete_chat_by_id(2):
        print("Chat deleted successfully.")
    else:
        print("Chat not found.")

    # Fetch all chats after deletion
    print("\nAll Chats After Deletion:")
    for chat in db.fetch_all_chats():
        print(chat)

    db.close()
