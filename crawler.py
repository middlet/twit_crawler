#!/usr/bin/env python

"""
new version of twitter crawler. designed to run in VM and using a more up to
date version of tweepy
"""

from config import consumer_key, consumer_secret, access_token, access_token_secret
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


class StdOutListener(StreamListener):
  """ 
  A listener handles tweets are the received from the stream. 
  This is a basic listener that just prints received tweets to stdout.
  """
  def on_data(self, data):
    print data
    return True
  
  def on_error(self, status):
    print status

if __name__ == '__main__':
  l = StdOutListener()
  auth = OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_token, access_token_secret)

  stream = Stream(auth, l)	
  stream.filter(track=['evacuate'])
