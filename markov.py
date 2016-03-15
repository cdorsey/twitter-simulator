import json
import re
import sys
import requests
from multiprocessing import Process
import markovify
import login

KEY_WORD = 'whoami'


def process_user(user, auth, tweet_id):
    """
    This function is the workhorse which retreives the user's timeline, formats it into a format acceptable to the
    markovify library, and retrieves the resulting string from markovify, which is then passed on to the reply_tweet()
    function

    :param user: Screen name of user to be processed
    :param auth: OAuth1 object to authenticate with Twitter's API
    :param tweet_id: ID of the tweet that invoked the process
    :return:
    """
    raw_text = ""
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    tweets = requests.get(url, params={'screen_name': user, 'count': 200, 'exclude_replies': True,
                                       'include_rts': False}, auth=auth)

    for tweet in tweets.json():
        raw_text += tweet['text']
        raw_text += " "

    tweets.close()

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
                    json_obj = json.loads(line.decode('utf-8'))
                    user = json_obj['user']['screen_name']
                    tweet_id = json_obj['id']
                    print("Analyzing {0}...".format(user))
                    process_user(user, auth, tweet_id)
                except ValueError:
                    print("Error was encountered processing the following:\n\t{0}".format(line.decode('utf-8')),
                          file=sys.stderr)
                    pass
    except SystemExit:
        stream.close()


if __name__ == "__main__":
    with open("name.txt") as name_file:
        BOT_NAME = re.sub(r"\n", "", name_file.read())
    start_stream()
