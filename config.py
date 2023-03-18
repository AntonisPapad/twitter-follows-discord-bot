import configparser


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    return {
        'twitter': {
            'consumer_key': config.get('twitter', 'consumer_key'),
            'consumer_secret': config.get('twitter', 'consumer_secret'),
            'access_token': config.get('twitter', 'access_token'),
            'access_token_secret': config.get('twitter', 'access_token_secret'),
        },
        'database': {
            'host': config.get('database', 'host'),
            'user': config.get('database', 'user'),
            'password': config.get('database', 'password'),
            'database': config.get('database', 'database'),
        },
        'discord': {
            'api_key': config.get('discord', 'api_key'),
        }
    }
