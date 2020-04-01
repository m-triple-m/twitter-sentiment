import tweepy
import logging
import os

logger = logging.getLogger()

def create_api():
    consumer_key = "VK3EwC1ulEAxvwXeC0inyuf3n"
    consumer_secret = "Git1Orj17FBidhwGaYUA7MD9LVtCW4uJZ0qA9Hsxy2ppy67KLb"
    access_token = "1152483648081469441-GPLJ0n8Pnh659Hh0sy2q6f2ceD26bG"
    access_token_secret = "0coTqP31WeJVVJi8r94kAWGqqhweBqGM7qICYScFz79bl"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, 
        wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except Exception as e:
        logger.error("Error creating API", exc_info=True)
        raise e
    logger.info("API created")
    return api


def getTweets(twitter_handle):

    api = create_api()
    # tweets = tweepy.Cursor(api.home_timeline).items(100)
    tweets = api.user_timeline(screen_name = twitter_handle)
    return tweets
    # for tweet in tweets:
        # print(tweet)
        # print(f"{tweet.user.name} said: {tweet.text}")
