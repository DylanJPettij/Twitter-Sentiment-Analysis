from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from tweepy import Cursor
import Keys
import numpy as np
import pandas as pd 
import re 
from textblob import TextBlob
import datetime
class TwitterClient():
    def __init__(self,twitter_user=None):
        self.auth=TwitterAuthentication().authenticate_twitter_app()
        self.TwitterClient=API(self.auth)
        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.TwitterClient
#############################
class TwitterAuthentication():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(Keys.CONSUMER_KEY, Keys.CONSUMER_SECRET)
        auth.set_access_token(Keys.ACCESS_TOKEN,Keys.ACCESS_TOKEN_SECRET)
        return auth

class TweetAnalyzer():
    def clean_tweet(self,tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

    def analyze_sentiment(self,tweet):
        analysis = TextBlob(self.clean_tweet(tweet))

        if analysis.sentiment.polarity>0:
            return 1
        elif analysis.sentiment.polarity==0:
            return 0
        else:
            return -1
    
    def TweetsToDF(self,tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
        df['Time'] =  np.array([tweet.created_at for tweet in tweets])
        return df
def select():
    i =True
    while i == True:
        print("1). NQ")
        print("2). YM")
        print("3). RTY")
        print("4). ES")
        tickerSymbol = input("Select From the following: ")
        if tickerSymbol != "RTY" or "NQ" or "YM" or "ES" or "1" or "2" or"3" or "4":
            i=True
        if tickerSymbol == "1":
            tickerSymbol = "NQ"
            i = False
        if tickerSymbol == "2":
            tickerSymbol = "YM"
            i = False
        if tickerSymbol == "3":
            tickerSymbol = "RTY"
            i = False
        if tickerSymbol == "4":
            tickerSymbol = "ES"
            i = False
        if tickerSymbol =="RTY":
            i = False
        if tickerSymbol =="YM":
            i = False
        if tickerSymbol =="NQ":
            i = False
        if tickerSymbol =="ES":
            i = False
    return tickerSymbol
def GetSentiment():
    x = ("#" + select() + "_F")
    api = twitter_client.get_twitter_client_api()
    tweets = api.search(q=x, count = 100,retweeted = False)
    newtweets=[]
    for tweet in tweets:
        if not "@earn2trade" in tweet.text:
            if not "@WarlusTrades" in tweet.text:
               if not "@TradingWarz:" in tweet.text: 
                       if not "RT" in tweet.text:
                           if not "Free Trial" in tweet.text:
                                if "short" in tweet.text.lower():
                                    tweet.text = "Negative"
                                    newtweets.append(tweet)
                                if not "Short" in tweet.text:
                                    newtweets.append(tweet)
    df = tweet_analysis.TweetsToDF(newtweets)
    df['sentiment'] = np.array([tweet_analysis.analyze_sentiment(tweet) for tweet in df['Tweets']])
    return df
def Results(DataFrame):
    print(sentiment)
    x = sum(sentiment['sentiment'])
    i =0
    m = datetime.datetime.now().timestamp()
    for i in sentiment['Time']:
        m=m + i.timestamp()
    m = m - datetime.datetime.now().timestamp()
    print("Datetime: ",datetime.datetime.fromtimestamp(m/len(sentiment['Time'])))
    print("Sentiment: ", x)
    print("Out of:", len(sentiment['sentiment']))
    print("Percentage: ", ("{:.2f}".format((x/len(sentiment['sentiment'])*100))),"%")
if __name__=="__main__":
       
    twitter_client= TwitterClient()
    tweet_analysis = TweetAnalyzer()
    sentiment = GetSentiment()
    Results(sentiment)