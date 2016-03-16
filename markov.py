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

    return reply_tweet(user, response, api, tweet_id)


def reply_tweet(user, tweet, api, id):
    """
    This function builds and sends the response tweet containing the markov string via a reply tweet

    :param user: Screen name of the user to send the tweet to
    :param tweet: Contents of the tweet to send
    :param api: Tweepy API wrapper
    :param id: Tweet ID of the tweet to reply to
    :return: Tweepy Status object containing sent tweet
    """

    full_tweet = "@" + user + " " + tweet

    return api.update_status(full_tweet, in_reply_to_status_id=id)
