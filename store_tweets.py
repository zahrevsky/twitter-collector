import os
from datetime import datetime

import tweepy
from pymongo import MongoClient


class MongoStorer(tweepy.StreamingClient):
	def __init__(self, mongo_db, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self._db = mongo_db


	def on_tweet(self, tweet: tweepy.Tweet):
		print(f"tweet received: {tweet.text}")
		self._db['tweets'].insert_one(dict(tweet))


def run():
	mongo = MongoClient("mongodb://127.0.0.1:27017/")
	db = mongo['twitter-collector']

	api_token = {
		'stage': os.environ['TWCOL_API_TOKEN_STAGING'],
		'dev': os.environ['TWCOL_API_TOKEN_DEV'],
		None: 'TWCOL_API_TOKEN_DEV'
	}[os.getenv('TWCOL_ENV', None)]

	storer = MongoStorer(db, api_token)
	storer.filter(tweet_fields=['created_at'])


if __name__ == '__main__':
	run()