import logging
import os
import sqlite3


class DBManager:
    # Some magic staff
    def __init__(self, db_name: str) -> None:
        """
        Initialize the DBManager object.

        Args:
            db_name (str): The name of the database.
        """
        try:
            self._setup_db()
            self._connection = sqlite3.connect(f"data/{db_name}.db")
            self._create_table()
        except Exception as err:
            logging.error(f"sqlite3 error: __init__: {err}")

    def _setup_db(self) -> None:
        """
        Setup the database dir.
        """
        if not os.path.exists("data"):
            os.makedirs("data")

    def _create_table(self) -> None:
        """
        Creates the 'users' table in the database if such a table does not already exist.
        """
        cursor = self._connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (ID INTEGER PRIMARY KEY, DiscordID TEXT UNIQUE NOT NULL, Ckey TEXT, RoleLevel INTEGER);")
        self._connection.commit()

    def __getitem__(self, discord_id: str) -> dict:
        """
        Returns information about a user by their Discord ID.

        Args:
            discord_id (str): User Discord ID.

        Returns:
            dict: User information in the form of a dictionary {'Ckey': ckey, 'RoleLevel': role_level}.
        """
        cursor = self._connection.cursor()
        cursor.execute("SELECT Ckey, RoleLevel FROM users WHERE DiscordID = ?;", (discord_id))
        row = cursor.fetchone()
        if row:
            return {'Ckey': row[0], 'RoleLevel': row[1]}
        
        return {'Ckey': None, 'RoleLevel': None}

    def __del__(self):
        """
        Class destructor. Closes the connection to the database.
        """
        try:
            if hasattr(self, '_connection') and self._connection is not None:
                self._connection.close()
        except sqlite3.Error as err:
            logging.error(f"sqlite3 error: __del__: {err}")

    # U can use this metods.
    def add_member(self, discord_id: str, ckey: str, role_level: int) -> None:
        """
        Add a new member to the database.

        Args:
            discord_id (str): The Discord ID of the member.
            ckey (str): The Ckey of the member.
            role_level (int): The role level of the member.
        """
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO users (DiscordID, Ckey, RoleLevel) VALUES (?, ?, ?);", (discord_id, ckey, role_level))
        self._connection.commit()

    def update_member(self, discord_id: str, new_ckey: str = None, new_role_level: int = None) -> None:
        """
        Update the information of a member in the database.

        Args:
            discord_id (str): The Discord ID of the member.
            new_ckey (str, optional): The new Ckey of the member. Defaults to None.
            new_role_level (int, optional): The new role level of the member. Defaults to None.
        """
        cursor = self._connection.cursor()
        cursor.execute("UPDATE users SET Ckey = COALESCE(?, Ckey), RoleLevel = COALESCE(?, RoleLevel) WHERE DiscordID = ?;", (new_ckey, new_role_level, discord_id))
        self._connection.commit()
    
    def add_or_update_member(self, discord_id: str, ckey: str, role_level: int) -> None:
        """
        Add a new member to the database or update existing member's information.

        Args:
            discord_id (str): The Discord ID of the member.
            ckey (str): The Ckey of the member.
            role_level (int): The role level of the member.
        """
        try:
            self.add_member(discord_id, ckey, role_level)
        except sqlite3.IntegrityError:
            self.update_member(discord_id, ckey, role_level)
        except Exception as e:
            logging.error(f"An error occurred during add_or_update_member: {e}")

    def get_all_users(self) -> list:
        """
        Get all users with their Ckey and RoleLevel if RoleLevel is not 0.

        Returns:
            list: A list of dictionaries containing information about the users.
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute("SELECT DiscordID, Ckey, RoleLevel FROM users WHERE RoleLevel != 0;")
            rows = cursor.fetchall()
            users = [{"DiscordID": row[0], "Ckey": row[1], "RoleLevel": row[2]} for row in rows]
            return users
        except sqlite3.Error as err:
            logging.error(f"sqlite3 error: get_all_users: {err}")
