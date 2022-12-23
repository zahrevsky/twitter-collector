import json
from datetime import datetime

from db import all_tweets
from env import env


def dump_tweets(filename):
    to_dump = {
        'dumped_at': datetime.now().isoformat(),
        'data': [tweet for tweet in all_tweets()]
    }

    with open(filename, 'w') as out:
        json.dump(to_dump, out, default=str)


if __name__ == '__main__':
    dump_tweets(env('DUMP_PATH'))

