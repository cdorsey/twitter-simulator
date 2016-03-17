import unittest

import tweepy

import login
import markov


class MarkovTest(unittest.TestCase):
    # def test_process_user(self):
    #     status = markov.process_user('chaseeatsworlds', self.api, None, False)
    #     self.assertIsInstance(status, tweepy.Status)

    # def setUp(self):
    #     auth = login.get_auth()
    #     self.api = tweepy.API(auth)
    #     pass
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()
