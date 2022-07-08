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


def rule_len(infls):
	return 9 * len(infls) - 4 + sum(len(infl) for infl in infls)


def build_rules(infls):
	while len(infls):
		n = 1
		first_n = infls[:n]
		while not (rule_len(first_n) >= 512 or len(infls) < n):
			n += 1
			first_n = infls[:n]
		yield ' OR '.join(f'from:{infl}' for infl in first_n[:-1])
		infls = infls[(n-1):]


def run():
	mongo = MongoClient("mongodb://127.0.0.1:27017/")
	db = mongo['twitter-collector']

	storer = MongoStorer(db, os.environ['API_TOKEN'])


if __name__ == '__main__':
	run()