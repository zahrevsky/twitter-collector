import json
import re

# the function checks a tweet for cryptonames appearance and returns
# the list of found cryptos


def analyze_tweet(tweet: str) -> list:

    # get dict of cryptoes names from json files
    # symbol: {symbol,name,slug}
    with open("cryptonames.json") as json_file:
        data = json.load(json_file)

    # x - list of all words in tweet which starts with '#' or '$'
    x = re.findall(r"\$[a-zA-Z]+|\#[a-zA-Z]+", tweet)

    # make all letters upper
    for i in range(len(x)):
        x[i] = x[i].upper()

    # list of found markers which matches with markers from markers from crypto dictionary
    marker_list = list()

    # looking for matches
    if x:
        for word in x:
            for key in data:
                # exludes '#' and '$' from word
                # looks for match to crypto symbol or crypto name
                if (word[1:] == key) or (word[1:] == data[key]['name'].upper()):
                    # add found match to list
                    marker_list.append(key)

    return marker_list


if __name__ == "__main__":
    # print(analyze_tweet("Just swapped 1k $SOL for $AVAX using v2 cross-chain aggregator by @atlas_dex"))

    with open("flat_tweets.json") as json_file:
        file = json.load(json_file)

    # dictionary of crypto mentions
    marker_dict = dict()
    counter = 0

    for tweet in file:
        marker_list = analyze_tweet(tweet)

        for marker in marker_list:
            if marker in marker_dict:
                marker_dict[marker] += 1

            else:
                marker_dict[marker] = 1
            
            counter += 1

    print(sorted(marker_dict.items(), key=lambda item: item[1], reverse=True))
    print(counter)
    