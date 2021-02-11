import tweepy
import logging
from config import create_api
import json
from banned_words import BANNED_WORDS


# Authenticate to Twitter


# Create API object
# api = tweepy.API(auth, wait_on_rate_limit=True,
#                  wait_on_rate_limit_notify=True)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        logger.info(f"Processing tweet id {tweet.id}")
        if tweet.in_reply_to_status_id is not None or \
                tweet.user.id == self.me.id:
            # This tweet is a reply or I'm its author so, ignore it
            print("Already Tweeted")
            return
        for banned_word in BANNED_WORDS:
            if banned_word in set(tweet.text.lower().split(" ")):
                print("Not Harry Styles", tweet.text)
                return
        if not tweet.favorited:
            # Mark it as Liked, since we have not done it yet
            try:
                tweet.favorite()
            except Exception as e:
                logger.error("Error on fav", exc_info=True)
        if not tweet.retweeted:
            # Retweet, since we have not retweeted it yet
            try:
                tweet.retweet()
            except Exception as e:
                logger.error("Error on fav and retweet", exc_info=True)

    def on_error(self, status):
        logger.error(status)


def main(keywords):
    api = create_api()
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(track=keywords, languages=["en"], is_async=True)


if __name__ == "__main__":
    main(["Harry", "harry"])
