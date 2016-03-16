import re
import tweepy

import login
from TriggerStreamListener import TriggerStreamListener

KEY_WORD = 'whoami'


def start_stream():
    """
    This function starts the stream for listening for user interactions. Any tweet mentioning the bot's name (defined
    in name.txt) and a keyword (defined at the top of markov.py) will be passed into the processing function
    :return:
    """
    auth = login.get_auth()
    api = tweepy.API(auth)

    listener = TriggerStreamListener(api)
    stream = tweepy.Stream(auth=api.auth, listener=listener())

    stream.filter(track='{0} {1}'.format(BOT_NAME, KEY_WORD))


if __name__ == "__main__":
    with open("name.txt") as name_file:
        BOT_NAME = re.sub(r"\n", "", name_file.read())
    start_stream()
