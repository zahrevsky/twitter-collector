from pymongo import MongoClient


def tweet_storage():
    mongo = MongoClient("mongodb://127.0.0.1:27017/")
    db = mongo['twitter-collector']
    return db


def all_tweets():
    return tweet_storage()['tweets'].find()