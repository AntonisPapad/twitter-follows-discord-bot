# Twitter Tracker Discord Bot

This project consists of a Discord bot that tracks specified Twitter users and reports their new friends (users they follow) in a designated Discord channel. It includes three main files:

## File Structure

1. `discord_bot.py`: Contains the main Discord bot logic, including commands and event listeners.
2. `db_functions.py`: Contains functions for interacting with a MySQL database for storing tracked users and Discord channel information.
3. `twitter_functions.py`: Contains functions for interacting with the Twitter API to retrieve user information and new friends.

## discord_bot.py

This file contains the main Discord bot class TwitterTrackerBot, which inherits from the commands.Bot class. It has the following event listeners and commands:

- `on_ready`: Called when the bot is ready and connected to Discord.
- `track_users`: Tracks Twitter users and sends updates to the Discord channel.
- `/start`: Initializes the bot and starts tracking in the designated channel.
- `/stop`: Stops the bot from tracking users.
- `/add`: Adds a Twitter user to the tracker.
- `/remove`: Removes a Twitter user from the tracker.

## db_functions.py

This file contains functions for interacting with a MySQL database. The main functions are:

- `add_user`: Adds a user to the tracked_users table in the database.
- `remove_user`: Removes a user from the tracked_users table in the database.
- `check_for_user`: Checks if a user is in the tracked_users table in the database.
- `get_tracked_users`: Retrieves all tracked users from the database.
- `read_channel_id`: Reads the first channel ID from the channel_ids table in the database.
- `write_channel_id`: Writes or updates a channel ID in the channel_ids table in the database.
- `delete_channel_id`: Deletes a channel ID from the channel_ids table in the database.
- `update_friends_number`: Updates the friends_number field of a user in the tracked_users table in the database.

## twitter_functions.py

This file contains functions for interacting with the Twitter API using the tweepy library. The main functions are:

- `get_user`: Retrieves a Twitter user object.
- `get_new_friends`: Retrieves a list of new friends for the specified user.

## Setup

1. Install the required packages:

```sh
pip3 install -r requirements.txt
```

2. Create a MySQL database and set up the `tracked_users` and `channel_ids` tables using the following SQL commands:

```sh
CREATE TABLE tracked_users (
    username VARCHAR(50) NOT NULL,
    friends_number INT
);

CREATE TABLE channel_ids (
    id BIGINT NOT NULL,
    user VARCHAR(50) NOT NULL
);
```

3. Create a `config.ini` file in the project in the project directory with the following structure:

```sh
[discord]
api_key = YOUR_DISCORD_API_KEY

[twitter]
consumer_key = YOUR_TWITTER_CONSUMER_KEY
consumer_secret = YOUR_TWITTER_CONSUMER_SECRET
access_token = YOUR_TWITTER_ACCESS_TOKEN
access_token_secret = YOUR_TWITTER_ACCESS_TOKEN_SECRET

[database]
user = YOUR_DATABASE_USER
password = YOUR_DATABASE_PASSWORD
host = YOUR_DATABASE_HOST
database = YOUR_DATABASE_NAME
```

Replace the placeholders with your respective Discord, Twitter, and database credentials.

4. Run the bot:

```sh
python3 discord_bot.py
```

5. Use the /start, /stop, /add, and /remove commands in Discord to control the bot and manage the tracked Twitter users.