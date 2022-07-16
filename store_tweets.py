import os

import tweepy

from db import tweet_storage


class MongoStorer(tweepy.StreamingClient):
    def __init__(self, mongo_db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._db = mongo_db


    def on_tweet(self, tweet: tweepy.Tweet):
        print(f"tweet received: {tweet.text}")
        self._db['tweets'].insert_one(dict(tweet))


def api_token():
    return {
        'stage': os.environ['TWCOL_API_TOKEN_STAGING'],
        'dev': os.environ['TWCOL_API_TOKEN_DEV'],
        None: 'TWCOL_API_TOKEN_DEV'
    }[os.getenv('TWCOL_ENV', None)]


def store_tweets():
    storer = MongoStorer(tweet_storage(), api_token())
    storer.filter(tweet_fields=['created_at'])


if __name__ == '__main__':
    store_tweets()