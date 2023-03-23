from contextlib import contextmanager
import mysql.connector
from twitter_functions import get_user
from config import read_config


@contextmanager
def mysql_cursor(commit_changes=False):
    """
    A context manager for MySQL cursor connections.

    Args:
        commit_changes (bool, optional): If True, the changes made to the database will be committed; otherwise not.
                                        Defaults to False.
    Yields:
        cursor (mysql.connector.cursor): A MySQL cursor object.
    """
    config_values = read_config()
    db_config = config_values['database']
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    try:
        yield cursor
        if commit_changes:
            db.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        db.close()


def add_user(user):
    """
    Adds a user to the tracked_users table in the database.

    Args:
        user (str): The Twitter username of the user to be added.
    """
    with mysql_cursor(commit_changes=True) as cursor:
        friends_number = get_user(user).friends_count

        query = "INSERT INTO tracked_users (username, friends_number) VALUES (%s, %s)"
        val = (user, friends_number)
        cursor.execute(query, val)


def remove_user(user):
    """
    Removes a user from the tracked_users table in the database.

    Args:
        user (str): The Twitter username of the user to be removed.
    """
    with mysql_cursor(commit_changes=True) as cursor:
        query = "DELETE FROM tracked_users WHERE username = %s"
        cursor.execute(query, (user,))


def check_for_user(user):
    """
    Checks if a user is in the tracked_users table in the database.

    Args:
        user (str): The Twitter username of the user to check.

    Returns:
        user_data (tuple or None): The user data if the user is found, otherwise None.
    """
    with mysql_cursor() as cursor:
        query = "SELECT * FROM tracked_users WHERE username = %s"
        cursor.execute(query, (user,))
        user_data = cursor.fetchone()
        return user_data


def get_tracked_users():
    """
    Retrieves all tracked users from the database.

    Returns:
        user_list (list): A list of tuples containing user data.
    """
    with mysql_cursor() as cursor:
        query = "SELECT * FROM tracked_users"
        cursor.execute(query)
        user_list = cursor.fetchall()
        return user_list


def read_channel_id():
    """
    Reads the first channel ID from the channel_ids table in the database.

    Returns:
        channel_id (int or None): The first channel ID if it exists, otherwise None.
    """
    with mysql_cursor() as cursor:
        query = "SELECT id FROM channel_ids LIMIT 1"
        cursor.execute(query)
        channel_data = cursor.fetchone()
        return channel_data[0] if channel_data else None


def write_channel_id(channel_id, user):
    """
    Writes or updates a channel ID in the channel_ids table in the database.

    Args:
        channel_id (int): The channel ID to be written or updated.
        user (str): The associated user's Discord username.
    """
    with mysql_cursor(commit_changes=True) as cursor:
        # First, check if there's an existing entry
        query = "SELECT id FROM channel_ids LIMIT 1"
        cursor.execute(query)
        existing_entry = cursor.fetchone()
        if existing_entry:
            # Update the existing entry
            query = "UPDATE channel_ids SET id = %s, user = %s WHERE id = %s"
            cursor.execute(query, (channel_id, user, existing_entry[0]))
        else:
            # Insert a new entry
            query = "INSERT INTO channel_ids (id, user) VALUES (%s, %s)"
            cursor.execute(query, (channel_id, user))


def delete_channel_id(channel_id):
    """
    Deletes a channel ID from the channel_ids table in the database.

    Args:
        channel_id (int): The channel ID to be deleted.
    """
    with mysql_cursor(commit_changes=True) as cursor:
        query = "DELETE FROM channel_ids WHERE id = %s"
        cursor.execute(query, (channel_id,))


def update_friends_number(username, new_friends_num):
    """
    Updates the friends_number field of a user in the tracked_users table in the database.

    Args:
        username (str): The Twitter username of the user whose friends_number is to be updated.
        new_friends_num (int): The change in the number of friends (positive or negative).
    """
    with mysql_cursor(commit_changes=True) as cursor:
        query = "UPDATE tracked_users SET friends_number = friends_number + %s WHERE username = %s"
        cursor.execute(query, (new_friends_num, username))
