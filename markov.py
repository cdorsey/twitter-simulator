import re
import markovify
import tweepy


def process_user(user, api, tweet_id, simulate=False):
    """
    This function is the workhorse which retreives the user's timeline, formats it into a format acceptable to the
    markovify library, and retrieves the resulting string from markovify, which is then passed on to the reply_tweet()
    function

    :param simulate: If true, do everything but send the reply tweet
    :param user: Screen name of user to be processed
    :param api: Tweepy API wrapper
    :param tweet_id: ID of the tweet that invoked the process
    :return: If simulate is False, returns Status object for the sent tweet, else returns the string of the tweet that
        would have been sent.
    """
    raw_text = ""

    tweets = api.user_timeline(screen_name=user, count=3200)

    for tweet in process_tweets(tweets):
        raw_text += tweet
        raw_text += " "

    text_model = markovify.Text(raw_text)

    response = text_model.make_short_sentence(120)

    return reply_tweet(user, response, api, tweet_id, simulate)

def process_tweets(tweets):
    for tweet in tweets:
        # Filter out emoji
        try:
            # UCS-4
            highpoints = re.compile(u'[\U00010000-\U0010ffff]')
        except re.error:
            # UCS-2
            highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')

        raw_text = highpoints.sub('', tweet.text)

        # Filter out newline and links
        raw_text = re.sub(r'\n', " ", raw_text)
        raw_text = re.sub(r'https://t.co/([A-Za-z0-9]{10})', "", raw_text)

        # Remove old-style retweets
        raw_text = re.sub(r'RT @(.*)\Z', "", raw_text)

        # Fix mutliple spaces and remove trailing spaces
        raw_text = re.sub(r'\s{2,}', " ", raw_text)
        raw_text = re.sub(r'\s+\Z', "", raw_text)

        yield raw_text

def reply_tweet(user, tweet, api, id, simulate=False):
    """
    This function builds and sends the response tweet containing the markov string via a reply tweet

    :param user: Screen name of the user to send the tweet to
    :param tweet: Contents of the tweet to send
    :param api: Tweepy API wrapper
    :param id: Tweet ID of the tweet to reply to
    :return: If simulate is False, returns Status object for the sent tweet, else returns the string of the tweet that
        would have been sent.
    """

    full_tweet = "@" + user + " " + tweet

    if not simulate:
        return api.update_status(full_tweet, in_reply_to_status_id=id)
    else:
        return full_tweet
