import tweepy
from config import read_config


# Read the configuration values
config_values = read_config()

# Extract the Twitter credentials from the configuration
twitter_credentials = config_values['twitter']

# Set up OAuth authentication with the Twitter credentials
auth = tweepy.OAuthHandler(
    twitter_credentials['consumer_key'], twitter_credentials['consumer_secret'])
auth.set_access_token(
    twitter_credentials['access_token'], twitter_credentials['access_token_secret'])

# Create the API object
api = tweepy.API(auth, wait_on_rate_limit=True)


def get_user(username):
    """
    Retrieves a Twitter user object.

    Args:
        username (str): The Twitter username of the user.

    Returns:
        user (tweepy.models.User or None): The user object if the user is found, otherwise None.
    """
    try:
        # Try to retrieve the user information
        user = api.get_user(screen_name=username)
        return user
    except tweepy.TweepyException:
        # If the user could not be found, return None
        return None


def get_new_friends(username, friends_num):
    """
    Retrieves a list of new friends for the specified user.

    Args:
        username (str): The Twitter username of the user.
        friends_num (int): The previous number of friends for comparison.

    Returns:
        new_friends (list or None): A list of new friends as tweepy.models.User objects if there are any new friends,
                                     otherwise None.
        diff (int): The difference in the number of friends compared to the previous friends count (positive or negative).
    """
    user = api.get_user(screen_name=username)
    if (diff := user.friends_count - friends_num) > 0:
        new_friends = tweepy.Cursor(
            api.get_friends, screen_name=username).items(diff)
        return list(new_friends), diff
    return None, diff
