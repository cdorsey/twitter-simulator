import json
import requests
import sys
from requests_oauthlib import OAuth1


def get_auth():
    """
    Builds and validates an OAuth1 object that can be used to authenticate with the Twitter API. Keys are retrieved
    from keys.json. See README for more info

    :return: OAuth1 object
    """
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

    valid.close()

    return auth


def twitter_error(code, msg, fatal=False):
    """
    Helper function to report errors returned by Twitter

    :param code: Numerical code of the error returned by Twitter
    :param msg: Error string
    :param fatal: Should this error stop the program from running? (Yes = True, No = False), default: False
    :return:
    """
    print('Twitter returned an error: {0} (Code {1})'.format(msg, code), file=sys.stderr)
    if fatal:
        sys.exit(1)
