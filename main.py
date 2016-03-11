import json

import sys

import requests

import login
from multiprocessing import Process

KEY_WORD = "whoami"
BOT_NAME = "chaseeatsworlds"


def get_tweets(id, auth):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    tweets = requests.get(url, params={'user_id': id, 'count': 200, 'trim_user': True, 'exclude_replies': True,
                                       'include_rts': False}, auth=auth)
    print(tweets.json())


def start_stream():
    auth = login.get_auth()

    stream_url = "https://stream.twitter.com/1.1/statuses/filter.json"
    stream = requests.post(stream_url, data={'track': '{0} {1}'.format(BOT_NAME, KEY_WORD)}, auth=auth, stream=True)

    if not stream.ok:
        try:
            error = stream.json()
            login.twitter_error(error['errors'][0]['code'], error['errors'][0]['message'], True)
        except ValueError:
            login.twitter_error(None, stream.content.decode('utf-8'), True)

    try:
        for line in stream.iter_lines():
            if line:
                try:
                    json_obj = json.loads(line.decode("utf-8"))
                    user_id = json_obj['user']['id']
                    print("Analyzing {0}...".format(user_id))
                    # Process(target=get_tweets, args=(user_id, auth, )).start()
                    get_tweets(user_id, auth)
                except ValueError as ex:
                    print("Error was encountered processing the following:\n\t{0}".format(line.decode('utf-8')),
                          file=sys.stderr)
                    pass
    except SystemExit:
        stream.close()


start_stream()
