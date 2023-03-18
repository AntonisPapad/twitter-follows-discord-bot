import tweepy
from config import read_config


config_values = read_config()
twitter_credentials = config_values['twitter']

auth = tweepy.OAuthHandler(
    twitter_credentials['consumer_key'], twitter_credentials['consumer_secret'])
auth.set_access_token(
    twitter_credentials['access_token'], twitter_credentials['access_token_secret'])

# Create the API object
api = tweepy.API(auth, wait_on_rate_limit=True)


def get_user(username):
    try:
        # Try to retrieve the user information
        user = api.get_user(screen_name=username)
        return user
    except tweepy.TweepyException:
        # If the user could not be found, return None
        return None


def get_new_friends(username, friends_num):
    user = api.get_user(screen_name=username)
    if (diff := user.friends_count - friends_num) > 0:
        new_friends = tweepy.Cursor(
            api.get_friends, screen_name=username).items(diff)
        return [friend for friend in new_friends]
    return None
