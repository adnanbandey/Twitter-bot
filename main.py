import tweepy
import time
import os
from os import environ

CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

FILE = "last_id.txt"

def reply_tweets():
    def retrieve_last_id(file):
        f_read = open(file, "r")
        last_seen_id = int(f_read.read().strip())
        f_read.close()
        return last_seen_id

    def store_last_id(last_seen_id, file):
        f_write = open(file, "w")
        f_write.write(str(last_seen_id))
        f_write.close()
        return

    last_seen_id = retrieve_last_id(FILE)
    mentions = api.mentions_timeline(last_seen_id, tweet_mode="extended")

    for mention in reversed(mentions):
        if "Hi" in mention.full_text:
            last_seen_id = mention.id
            store_last_id(last_seen_id, FILE)
            api.update_status("@" + mention.user.screen_name + " Hi! How are you?", mention.id)
            print("Replied to @" + mention.user.screen_name)

while True:
    reply_tweets()
    time.sleep(120)