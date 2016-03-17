import json
from io import TextIOWrapper

import tweepy


class OAuthWrapper(object):
    def __init__(self, keys=None, file_name=None, file_obj=None):
        if keys is not None and isinstance(keys, dict):
            self._set_keys(keys)
        elif file_obj is not None and isinstance(file_obj, TextIOWrapper):
            self._set_keys_file_obj(file_obj)
        elif file_name is not None and isinstance(file_name, str):
            self._set_keys_file_name(file_name)
        else:
            raise ValueError("Invalid parameters for OAuthWrapper")

    def _set_keys(self, keys):
        self._keys = keys

    def _set_keys_file_obj(self, file_obj):
        key = json.load(file_obj)
        try:
            consumer_key = key['consumer']['key']
            consumer_secret = key['consumer']['secret']
            access_key = key['access_token']['key']
            access_secret = key['access_token']['secret']
        except KeyError:
            raise KeyError("Key file format is incorrect. See README.md for more information")

        self._set_keys(keys={'consumer_key': consumer_key, 'consumer_secret': consumer_secret, 'access_key': access_key,
                             'access_secret': access_secret})

    def _set_keys_file_name(self, file_name):
        with open(file_name) as file_obj:
            self._set_keys_file_obj(file_obj)

    def get_auth(self):
        auth = tweepy.OAuthHandler(self._keys['consumer_key'], self._keys['consumer_secret'])
        auth.set_access_token(self._keys['access_key'], self._keys['access_secret'])

        return auth
