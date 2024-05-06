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
        Setup the database.
        """
        if not os.path.exists("data"):
            os.makedirs("data")

    def _create_table(self) -> None:
        """
        Creates the 'users' table in the database if such a table does not already exist.
        """
        check_table_sql = """
        SELECT name FROM sqlite_master WHERE type='table' AND name='users';
        """
        cursor = self._connection.cursor()
        cursor.execute(check_table_sql)
        result = cursor.fetchone()
        if not result:
            create_table_sql = """
            CREATE TABLE users (
                ID INTEGER PRIMARY KEY,
                DiscordID TEXT NOT NULL,
                Ckey TEXT,
                RoleLevel INTEGER
            );
            """
            cursor.execute(create_table_sql)
            self._connection.commit()

    def __getitem__(self, discord_id: str) -> dict:
        """
        Returns information about a user by their Discord ID.

        Args:
            discord_id (str): Discord ID пользователя.

        Returns:
            dict: User information in the form of a dictionary {'Ckey': ckey, 'RoleLevel': role_level}.
        """
        select_sql = """
        SELECT Ckey, RoleLevel
        FROM users
        WHERE DiscordID = ?;
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(select_sql, (discord_id,))
            row = cursor.fetchone()
            if row:
                return {'Ckey': row[0], 'RoleLevel': row[1]}
            else:
                return {'Ckey': None, 'RoleLevel': None}
        except sqlite3.Error as err:
            logging.error(f"sqlite3 error: __getitem__: {err}")

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
        insert_sql = """
        INSERT INTO users (DiscordID, Ckey, RoleLevel) VALUES (?, ?, ?);
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(insert_sql, (discord_id, ckey, role_level))
            self._connection.commit()
        except sqlite3.Error as err:
            logging.error(f"sqlite3 error: add_member: {err}")

    def update_member(self, discord_id: str, new_ckey: str = None, new_role_level: int = None) -> None:
        """
        Update the information of a member in the database.

        Args:
            discord_id (str): The Discord ID of the member.
            new_ckey (str, optional): The new Ckey of the member. Defaults to None.
            new_role_level (int, optional): The new role level of the member. Defaults to None.
        """
        update_sql = """
        UPDATE users
        SET Ckey = COALESCE(?, Ckey),
            RoleLevel = COALESCE(?, RoleLevel)
        WHERE DiscordID = ?;
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(update_sql, (new_ckey, new_role_level, discord_id))
            self._connection.commit()
        except sqlite3.Error as err:
            logging.error(f"sqlite3 error: update_member: {err}")
    
    def add_or_update_member(self, discord_id: str, ckey: str, role_level: int) -> None:
        """
        Add a new member to the database or update existing member's information.

        Args:
            discord_id (str): The Discord ID of the member.
            ckey (str): The Ckey of the member.
            role_level (int): The role level of the member.
        """
        try:
            select_sql = """
            SELECT DiscordID FROM users WHERE DiscordID = ?;
            """
            cursor = self._connection.cursor()
            cursor.execute(select_sql, (discord_id,))
            existing_user = cursor.fetchone()

            if existing_user:
                self.update_member(discord_id, ckey, role_level)
            else:
                self.add_member(discord_id, ckey, role_level)
        except sqlite3.Error as err:
            logging.error(f"sqlite3 error: add_or_update_member: {err}")

    def get_all_users(self) -> list:
        """
        Get all users with their Ckey and RoleLevel if RoleLevel is not 0.

        Returns:
            list: A list of dictionaries containing information about the users.
        """
        select_sql = """
        SELECT DiscordID, Ckey, RoleLevel
        FROM users
        WHERE RoleLevel != 0;
        """
        try:
            cursor = self._connection.cursor()
            cursor.execute(select_sql)
            rows = cursor.fetchall()
            users = [{"DiscordID": row[0], "Ckey": row[1], "RoleLevel": row[2]} for row in rows]
            return users
        except sqlite3.Error as err:
            logging.error(f"sqlite3 error: get_all_users: {err}")
