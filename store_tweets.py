import os

import tweepy

from db import tweet_storage
from env import env


class MongoStorer(tweepy.StreamingClient):
    def __init__(self, mongo_db, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._db = mongo_db


    def on_tweet(self, tweet: tweepy.Tweet):
        print(f"tweet received: {tweet.text}")
        self._db['tweets'].insert_one(dict(tweet))


def store_tweets():
    storer = MongoStorer(tweet_storage(), env('API_TOKEN'))
    storer.filter(tweet_fields=['created_at'])


if __name__ == '__main__':
    store_tweets()