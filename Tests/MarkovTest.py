import os
import unittest
import tweepy
import markov
from OAuthWrapper import OAuthWrapper


class MarkovTest(unittest.TestCase):
    def test_process_user_with_simulate(self):
        status = markov.process_user(self.test_user, self.api, None, simulate=True)
        self.assertIsInstance(status, str)

        print(status)

    def setUp(self):
        self.consumer_key = os.environ.get('CONSUMER_KEY')
        self.consumer_secret = os.environ.get('CONSUMER_SECRET')
        self.access_key = os.environ.get('ACCESS_KEY')
        self.access_secret = os.environ.get('ACCESS_SECRET')

        self.keys = {'consumer_key': self.consumer_key, 'consumer_secret': self.consumer_secret,
                     'access_key': self.access_key, 'access_secret': self.access_secret}

        auth = OAuthWrapper(keys=self.keys)
        self.api = tweepy.API(auth)

        self.test_user = ''


if __name__ == '__main__':
    unittest.main()
