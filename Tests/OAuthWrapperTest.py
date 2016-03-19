import json
import os
import unittest
from tempfile import TemporaryFile

import tweepy

from OAuthWrapper import OAuthWrapper


class OAuthWrapperTest(unittest.TestCase):
    def test_init_with_dict(self):
        obj = OAuthWrapper(keys=self.keys)
        self.assertIsInstance(obj, OAuthWrapper)
        self.assertEqual(obj._keys, self.keys)

    def test_init_with_file_obj(self):
        # Create a temporary file object and fill it with keys from unittest environment variables
        # This is to stop me from pushing my API keys to github... again.
        self.key_file = TemporaryFile(mode='r+')

        json.dump(dict(consumer={
            'key': self.consumer_key,
            'secret': self.consumer_secret
        }, access_token={
            'key': self.access_key,
            'secret': self.access_secret}),
                self.key_file)

        self.key_file.seek(0)

        obj = OAuthWrapper(file_obj=self.key_file)

        self.assertIsInstance(obj, OAuthWrapper)
        self.assertEqual(obj._keys, self.keys)

        self.key_file.close()

    # def test_init_with_file_name(self):
    #     obj = OAuthWrapper(file_name='keys.json')
    #
    #     self.assertIsInstance(obj, OAuthWrapper)
    #     self.assertEqual(obj._keys, self.keys)

    def test_get_auth(self):
        obj = OAuthWrapper(keys=self.keys)

        self.assertIsInstance(obj.get_auth(), tweepy.OAuthHandler)

    def setUp(self):
        self.consumer_key = os.environ.get('CONSUMER_KEY')
        self.consumer_secret = os.environ.get('CONSUMER_SECRET')
        self.access_key = os.environ.get('ACCESS_KEY')
        self.access_secret = os.environ.get('ACCESS_SECRET')

        self.keys = {'consumer_key': self.consumer_key, 'consumer_secret': self.consumer_secret,
                     'access_key': self.access_key, 'access_secret': self.access_secret}


if __name__ == '__main__':
    unittest.main()
