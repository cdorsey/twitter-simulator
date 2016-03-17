import os
import unittest

import tweepy

from OAuthWrapper import OAuthWrapper


class OAuthWrapperTest(unittest.TestCase):
    def setUp(self):
        self.consumer_key = os.environ.get('CONSUMER_KEY')
        self.consumer_secret = os.environ.get('CONSUMER_SECRET')
        self.access_key = os.environ.get('ACCESS_KEY')
        self.access_secret = os.environ.get('ACCESS_SECRET')

        self.keys = {'consumer_key': self.consumer_key, 'consumer_secret': self.consumer_secret,
                     'access_key': self.access_key, 'access_secret': self.access_secret}

    def test_init_with_dict(self):
        obj = OAuthWrapper(keys=self.keys)
        self.assertIsInstance(obj, OAuthWrapper)
        self.assertEqual(obj._keys, self.keys)

    def test_init_with_file_obj(self):
        with open('keys.json') as file_obj:
            obj = OAuthWrapper(file_obj=file_obj)

        self.assertIsInstance(obj, OAuthWrapper)
        self.assertEqual(obj._keys, self.keys)

    def test_init_with_file_name(self):
        obj = OAuthWrapper(file_name='keys.json')

        self.assertIsInstance(obj, OAuthWrapper)
        self.assertEqual(obj._keys, self.keys)

    def test_get_auth(self):
        obj = OAuthWrapper(keys=self.keys)

        self.assertIsInstance(obj.get_auth(), tweepy.OAuthHandler)
