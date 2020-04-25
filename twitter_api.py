import tweepy
import logging
import os

logger = logging.getLogger()

class TweetScraper:

    def __init__(self):
        consumer_key = "VK3EwC1ulEAxvwXeC0inyuf3n"
        consumer_secret = "Git1Orj17FBidhwGaYUA7MD9LVtCW4uJZ0qA9Hsxy2ppy67KLb"
        access_token = "1152483648081469441-GPLJ0n8Pnh659Hh0sy2q6f2ceD26bG"
        access_token_secret = "0coTqP31WeJVVJi8r94kAWGqqhweBqGM7qICYScFz79bl"

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True, 
            wait_on_rate_limit_notify=True)
        try:
            self.api.verify_credentials()
        except Exception as e:
            logger.error("Error creating API", exc_info=True)
            raise e
        logger.info("API created")


    def getTweets(self, twitter_handle):
        # tweets = tweepy.Cursor(api.home_timeline).items(100)
        tweets = self.api.user_timeline(screen_name = twitter_handle)
        return tweets
        # for tweet in tweets:
            # print(tweet)
            # print(f"{tweet.user.name} said: {tweet.text}")

    def getTagTweets(self, tag, max):
        tweets = tweepy.Cursor(self.api.search, q=tag, rpp=100).items(max)
        return list(tweets)
        
if __name__ == "__main__":
    twet = TweetScraper()
    twet.getTagTweets('#python', 10)