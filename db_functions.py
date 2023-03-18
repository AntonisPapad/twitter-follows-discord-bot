from contextlib import contextmanager
import mysql.connector
from twitter_functions import get_user
from config import read_config


@contextmanager
def mysql_cursor(commit_changes=False):
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
    with mysql_cursor(commit_changes=True) as cursor:
        friends_number = get_user(user).friends_count

        query = "INSERT INTO tracked_users (username, friends_number) VALUES (%s, %s)"
        val = (user, friends_number)
        cursor.execute(query, val)


def remove_user(user):
    with mysql_cursor(commit_changes=True) as cursor:
        query = "DELETE FROM tracked_users WHERE username = %s"
        cursor.execute(query, (user,))


def check_for_user(user):
    with mysql_cursor() as cursor:
        query = "SELECT * FROM tracked_users WHERE username = %s"
        cursor.execute(query, (user,))
        user_data = cursor.fetchone()
        return user_data


def get_tracked_users():
    with mysql_cursor() as cursor:
        query = "SELECT * FROM tracked_users"
        cursor.execute(query)
        user_list = cursor.fetchall()
        return user_list


def read_channel_id():
    with mysql_cursor() as cursor:
        query = "SELECT id FROM channel_ids LIMIT 1"
        cursor.execute(query)
        channel_data = cursor.fetchone()
        return channel_data[0] if channel_data else None


def write_channel_id(channel_id, user):
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
    with mysql_cursor(commit_changes=True) as cursor:
        query = "DELETE FROM channel_ids WHERE id = %s"
        cursor.execute(query, (channel_id,))


def update_friends_number(username, new_friends_num):
    with mysql_cursor(commit_changes=True) as cursor:
        query = "UPDATE tracked_users SET friends_number = friends_number + %s WHERE username = %s"
        cursor.execute(query, (new_friends_num, username))
