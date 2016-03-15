import json
import re
import sys
import requests
from multiprocessing import Process
import markovify
import login
import tweepy
from TriggerStreamListener import TriggerStreamListener

KEY_WORD = 'whoami'


def process_user(user, api, tweet_id):
    """
    This function is the workhorse which retreives the user's timeline, formats it into a format acceptable to the
    markovify library, and retrieves the resulting string from markovify, which is then passed on to the reply_tweet()
    function

    :param user: Screen name of user to be processed
    :param api: Tweepy API wrapper
    :param tweet_id: ID of the tweet that invoked the process
    :return:
    """
    raw_text = ""

    tweets = api.user_timeline(screen_name=user, count=200)

    for tweet in tweets:
        raw_text += tweet.text
        raw_text += " "

    # Filter out emoji
    try:
        # UCS-4
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        # UCS-2
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

    raw_text = highpoints.sub('', raw_text)

    # Filter out newline and links
    raw_text = re.sub(r'\n', " ", raw_text)
    raw_text = re.sub(r'https://t.co/([A-Za-z0-9]{10})', "", raw_text)

    text_model = markovify.Text(raw_text)

    response = text_model.make_short_sentence(120)

    reply_tweet(user, response, auth, tweet_id)


def reply_tweet(user, tweet, auth, id):
    """
    This function builds and sends the response tweet containing the markov string via a reply tweet

    :param user: Screen name of the user to send the tweet to
    :param tweet: Contents of the tweet to send
    :param auth: OAuth1 object to authenticate with Twitter's API
    :param id: Tweet ID of the tweet to reply to
    :return:
    """
    url = "https://api.twitter.com/1.1/statuses/update.json"

    full_tweet = "@" + user + " " + tweet

    request = requests.post(url, data={'status': full_tweet, 'in_reply_to_status_id': id}, auth=auth)
    request.close()


def start_stream():
    """
    This function starts the stream for listening for user interactions. Any tweet mentioning the bot's name (defined
    in name.txt) and a keyword (defined at the top of markov.py) will be passed into the processing function
    :return:
    """
    auth = login.get_auth()
    api = tweepy.API(auth)

    listener = TriggerStreamListener(api)
    stream = tweepy.Stream(auth = api.auth, listener=listener())

    stream.filter(track='{0} {1}'.format(BOT_NAME, KEY_WORD))


if __name__ == "__main__":
    with open("name.txt") as name_file:
        BOT_NAME = re.sub(r"\n", "", name_file.read())
    start_stream()
