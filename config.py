import tweepy
from secrets import *
import logging
import json


# Authenticate to Twitter
auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)

# Create API object
# api = tweepy.API(auth, wait_on_rate_limit=True,
#                  wait_on_rate_limit_notify=True)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def create_api():
    auth = tweepy.OAuthHandler(C_KEY, C_SECRET)
    auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api
