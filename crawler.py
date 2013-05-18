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
import os
import time


class MyRotatingHandler(logging.handlers.TimedRotatingFileHandler):
    """
    A modified form of the standard timed rotating logger
    this creates a new directory for each day. otherwise it
    will just rotate on size of file
    """
    
    def __init__(self, filename, when='h', interval=1, backupCount=0, encoding=None, delay=0, utc=0, maxBytes=0):
        """
        this is a combination of TimedRotatingFileHandler and
        RotatingFileHandler. adds maxBytes to TimedRotatingFileHandler
        """
        logging.handlers.TimedRotatingFileHandler.__init__(self, filename, when, interval, backupCount, encoding, delay, utc)
        self.maxBytes = maxBytes
    
    def shouldRollover(self, record):
        """
        determine if we should rollover
        check
        1) adding record will exceed size limit
        2) time is right
        
        stolen from python source (:
        """
        if self.stream is None:                  # delay was set ...
            self.stream = self._open()
        if self.maxBytes>0:                  # are we rolling over
            msg = "%s\n" % self.format(record)
            self.stream.seek(0, 2) # due to non-posix Windows feature
            if self.stream.tell() + len(msg) >= self.maxBytes:
                return 1
        t = int(time.time())
        if t >= self.rolloverAt:
            return 1
        #print "No need to rollover: %d, %d" % (t, self.rolloverAt)
        return 0
                
    
    def doRollover(self):
        """
        do a rollover
        this will create a new directory with the datestamp and store subsequent
        log files inside. the time stamp is when the rollover happens
        """
        if self.stream:
            self.stream.close()
            self.stream = None
        # get the time that this sequence started and make it a TimeTuple
        currentTime = int(time.time())
        dstNow = time.localtime(currentTime)[-1]
        t = self.rolloverAt - self.interval
        if self.utc:
            timeTuple = time.gmtime(t)
        else:
            timeTuple = time.localtime(t)
            dstThen = timeTuple[-1]
            if dstNow != dstThen:
                if dstNow:
                    addend = 3600
                else:
                    addend = -3600
                timeTuple = time.localtime(t+addend)
        # the output filename, we are not deleting for this application
        path, fname = os.path.split(self.baseFilename)
        fname, fnameext = os.path.splitext(fname)
        dname = path + '/' + time.strftime('%Y%m%d%H%M', timeTuple) + '/'
        if not os.path.exists(dname):
            os.mkdir(dname)
        dfn = dname + fname + '.' + time.strftime('%Y%m%d%H%M%S', timeTuple) + fnameext
        os.rename(self.baseFilename, dfn)
        #
        self.mode = 'w'
        self.stream = self._open()
        curentTime = int(time.time())
        newRolloverAt = self.computeRollover(currentTime)
        while newRolloverAt <= currentTime:
            newRolloverAt = newRolloverAt + self.interval
        #If DST changes and midnight or weekly rollover, adjust for this.
        if (self.when == 'MIDNIGHT' or self.when.startswith('W')) and not self.utc:
            dstAtRollover = time.localtime(newRolloverAt)[-1]
            if dstNow != dstAtRollover:
                if not dstNow:  # DST kicks in before next rollover, so we need to deduct an hour
                    newRolloverAt -= 3600
                else:           # DST bows out before next rollover, so we need to add an hour
                    newRolloverAt += 3600
        self.rolloverAt = newRolloverAt        


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
    LOG_FNAME = 'log/tweets.log'
    # Set up a specific logger with our desired output level
    my_logger = logging.getLogger('MyLogger')
    my_logger.setLevel(logging.DEBUG)

    # Add the log message handler to the logger
    handler = MyRotatingHandler(LOG_FNAME, maxBytes=16384, when='M')
    my_logger.addHandler(handler)
    
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)	
    stream.filter(track=['sport'])
