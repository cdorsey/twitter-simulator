import json
import requests
import sys
from requests_oauthlib import OAuth1

KEY_WORD = "whoami"


def get_auth():
    try:
        with open('keys.json') as key_file:
            key = json.load(key_file)
    except FileNotFoundError:
        sys.exit("Key file does not exist. See README.md for more information")

    try:
        consumer_key = key['consumer']['key']
        consumer_secret = key['consumer']['secret']
        access_key = key['access_token']['key']
        access_secret = key['access_token']['secret']
    except KeyError:
        sys.exit("Key file format is incorrect. See README.md for more information")

    validate_url = "https://api.twitter.com/1.1/account/verify_credentials.json"

    auth = OAuth1(consumer_key, client_secret=consumer_secret, resource_owner_key=access_key,
                  resource_owner_secret=access_secret)

    valid = requests.get(validate_url, auth=auth)
    content = json.loads(valid.content.decode("utf-8"))
    if not valid.ok:
        twitter_error(content['errors'][0]['code'], content['errors'][0]['message'], True)

    bot_name = content['screen_name']

    stream_url = "https://stream.twitter.com/1.1/statuses/filter.json"
    request = requests.post(stream_url, data='track={0}%20{1}'.format(bot_name, KEY_WORD), auth=auth, stream=True)

    if not request.ok:
        try:
            error = request.json()
            twitter_error(error['errors'][0]['code'], error['errors'][0]['message'], True)
        except ValueError:
            twitter_error(None, request.content.decode('utf-8'), True)

    return request


def twitter_error(code, msg, fatal=False):
    print('Twitter returned an error: {0} (Code {1})'.format(msg, code), file=sys.stderr)
    if fatal:
        sys.exit(1)
