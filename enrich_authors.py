from tweepy import Client
from tqdm import tqdm

from db import tweet_storage
from env import env


def enrich_authors():
    strg = tweet_storage()
    client = Client(env('API_TOKEN'), wait_on_rate_limit=True)

    already_dumped = 0
    unretrievable = 0
    total = 0
    for tweet in tqdm(strg['tweets'].find()):
        total += 1
        if 'author_id' not in tweet:
            try:
                author = client.get_tweet(
                    tweet['id'],
                    tweet_fields=['author_id']
                ).data['author_id']
                strg['tweets'].update_one(
                    {'id': tweet['id']}, 
                    {'$set': {'author_id': author}}
                )
            except Exception:
                unretrievable += 1
        else:
            already_dumped += 1

    print(
        f"Processed {total} tweets, " 
        f"{already_dumped} already have author, "
        f"{unretrievable} failed to retrieve"
    )


if __name__ == '__main__':
    enrich_authors()