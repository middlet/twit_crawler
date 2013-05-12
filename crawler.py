#!/usr/bin/env python

"""
new version of twitter crawler. designed to run in VM and using a more up to
date version of tweepy
"""

from config import consumer_key, consumer_secret, access_token, access_token_secret
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import logging
import logging.handlers


class MyRotatingHandler(logging.handlers.RotatingFileHandler):
    """
    A modified form of the stadard rotating logger
    this creates a new directory for each day. otherwise it
    will just rotate on size of file
    """
    def doRollover(self):
        print 'rollover'
        super(MyRotatingHandler, self).doRollover()

class StdOutListener(StreamListener):
    """ 
    A listener handles tweets are the received from the stream. 
    This is a basic listener that just prints received tweets to stdout.
    """
    def on_data(self, data):
        #print data
        my_logger.info(data)
        return True
  
    def on_error(self, status):
        my_logger.error(status)
        #print status

if __name__ == '__main__':
    LOG_FNAME = 'log/rotate.log'
    # Set up a specific logger with our desired output level
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.DEBUG)

    # Add the log message handler to the logger
    handler = MyRotatingHandler(LOG_FNAME, maxBytes=65536, backupCount=10)
    my_logger.addHandler(handler)
    
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)	
    stream.filter(track=['facup'])
