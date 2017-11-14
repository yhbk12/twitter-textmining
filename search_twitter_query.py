import re
import tweepy
import pandas as pd
from datetime import datetime
from textblob import TextBlob
import time


# Function to handle Twitter API rate limit
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.error.TweepError:
            print("RateLimitError caught, waiting 5 minutes...")
            time.sleep(5 * 60)
            print("Resuming cursor...")


# Function to return the median of a list of datetime objects.
def median_datetime(dt):
    # TODO: ensure list is sorted before returning middle element

    if len(dt) == 0:
        return 0
    else:
        return dt[round(len(dt) / 2)]


# Function to convert a Data Frame of tweets into a list of values for our explanatory variables.
def data_frame_to_results(query, start_date, df):
    result = [query,
              start_date,
              len(df.index),
              df['subjectivity'].mean(),
              df['polarity'].mean(),
              median_datetime(df['tweetCreated'].tolist()),
              df['tweetRetweetCt'].sum(),
              df['tweetFavoriteCt'].sum(),
              df['userFollowerCt'].sum(),
              df['userVerified'].sum()]

    return result


# Function to convert a list of tweets into a Pandas Data Frame capturing our explanatory variables
def to_data_frame(tweets):
    data_set = pd.DataFrame()

    data_set['tweetID'] = [tweet.id for tweet in tweets]
    data_set['tweetCreated'] = [tweet.created_at for tweet in tweets]
    data_set['tweetText'] = [tweet.text for tweet in tweets]
    data_set['tweetRetweetCt'] = [tweet.retweet_count for tweet in tweets]

    favorite_count = []

    for tweet in tweets:
        if hasattr(tweet, 'retweeted_status'):
            favorite_count.append(tweet.retweeted_status.favorite_count)
        else:
            favorite_count.append(tweet.favorite_count)

    fc = pd.Series(favorite_count)
    data_set['tweetFavoriteCt'] = fc.values

    data_set['user'] = [tweet.user.screen_name for tweet in tweets]
    data_set['userFollowerCt'] = [tweet.user.followers_count for tweet in tweets]
    data_set['userVerified'] = [tweet.user.verified for tweet in tweets]

    data_set['subjectivity'] = [TextBlob(tweet.text).sentiment.subjectivity for tweet in tweets]
    data_set['polarity'] = [TextBlob(tweet.text).sentiment.polarity for tweet in tweets]

    return data_set


# Function to clean tweet text by removing links and special characters (CURRENTLY NOT IN USE)
def clean_tweet_text(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())


# Function to perform a search using Twitter's api and return our explanatory variables.
def search_twitter_return_ev(query, start_date, end_date):


    # Dhruv's Twitter API authentication
    consumer_key = 'QyPohWOnU5rWBj0p8eitISxZm'
    consumer_secret = 'Bic1EnxYGOnaZZaNiSz0xW0Kb3Y4RGVhqbfriVP3dgm2xdj2Ln'
    access_token = '383059399-Nv6Z94gW7fMReiyKLGKANTFYay14tFvrB1Ut8c9s'
    access_token_secret = 'BsM3FhhEkkBYe7q1LPTAHQa1HyZKmhjVkaxdA5hJefwGy'

    # Yusuf's Twitter API authentication
    # consumer_key = 'GyfyFJEkU6cyGBq0PPLjHlvz0'
    # consumer_secret = 'q3ghkBA8i1qheGFFnpd5mmCmlAlrNIk02wqTqeoQ2gERHiwqLw'
    # access_token = '855727868-h0MenCCakLLaz6engeaIm2mh77j3uoOnN5DIXV07'
    # access_token_secret = 'c4TWPLTCmdx8ijhXS3gkH59Wcv8PGJ8BUFDTFXfT6hMiS'

    # Matt's Twitter API authentication
    # consumer_key = '1iQ8rHkTabqFSEaIujAHqahTW'
    # consumer_secret = 'KxnRmci0bkWpoeFF6lSyR8lzlNmutwDIaMZ6vkXF5moh68vS6v'
    # access_token = '701880260678148096-GkJ6CXuCFLjQYKnQdYl13QZI0Lk49KU'
    # access_token_secret = 'N5rwNAW7Su20FEZW741R0T992vg2xGwfqBNZzNC5FdMal'


    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    # Create an empty list to store our tweets
    tweets = []

    # Sample search parameters, can be used for troubleshooting.
    # query = "@Intel"
    # since_q = "2017-11-10"
    # until_q = "2017-11-11"

    # Create a datetime object with the open and close time for the NASDAQ market.
    open_time = datetime.strptime(start_date + " 14:00:00", "%Y-%m-%d %H:%M:%S")
    close_time = datetime.strptime(start_date + " 21:30:00", "%Y-%m-%d %H:%M:%S")

    # Search for tweets matching our query, and add them to our list
    for tweet in limit_handled(tweepy.Cursor(api.search, q=query, lang='en', since=start_date, until=end_date).items()):

        if open_time < tweet.created_at < close_time:
            tweets.append(tweet)

    # Convert our list of tweets into a Pandas data frame
    tweet_data_frame = to_data_frame(tweets)

    # Calculate the required explanatory variables from the data frame
    result = data_frame_to_results(query, start_date, tweet_data_frame)

    return result
