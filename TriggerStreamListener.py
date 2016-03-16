import time
from tweepy import StreamListener

import markov


class TriggerStreamListener(StreamListener):
    def on_status(self, status):
        markov.process_user(status.author.screen_name, self.api, status.id)

    def on_error(self, status_code):
        if status_code == 420:
            time.sleep(600)
