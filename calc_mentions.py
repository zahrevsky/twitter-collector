import requests
import json
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

import extract_currencies as c


url = "https://storage.vzvlad.dev/twitter-collector/tweets-dumped.json"
tweets = json.loads(requests.get(url).text)['data']

with_currencies = [
    dict(tweet, **{'currencies': c.extract_currencies(tweet['text'])})
    for tweet in tqdm(tweets)
]
non_empty_currencies = [
    tweet for tweet in with_currencies if len(tweet['currencies'])
]
unique_currencies = set([
    currency 
    for tweet in non_empty_currencies for currency in tweet['currencies']
])

mentions = {
    currency: [
        tweet for tweet in non_empty_currencies
        if currency in tweet['currencies']
    ] for currency in unique_currencies
}
mentions_with_dates = {
    currency: [
        tweet for tweet in non_empty_currencies
        if currency in tweet['currencies'] and 'created_at' in tweet
    ] for currency in unique_currencies
}
mentions_with_dates = {
    currency: tweets for currency, tweets in mentions_with_dates.items()
    if len(tweets)
}
mentions_count = {
    currency: len(tweets) for currency, tweets in mentions.items()
}

top20 = sorted(
    mentions_count.keys(),
    key=lambda x: mentions_count[x], reverse=True
)[0:20]

dates = {
    currency: pd.to_datetime(
        pd.DataFrame([
            datetime.strptime(tweet.get('created_at'), '%Y-%m-%d %H:%M:%S') 
            for tweet in tweets
        ])[0]
    )
    .dt.floor('d')
    .value_counts()
    .rename_axis('date')
    .reset_index(name='count')
    .sort_values('date')
    for currency, tweets in mentions_with_dates.items()
}