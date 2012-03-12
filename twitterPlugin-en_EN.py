#!/usr/bin/python
# -*- coding: utf-8 -*-

#author: iamcytec@googlemail.com
#todo: da ist noch viel möglich
#project: SiriServer
#Hilfe: IRC Freenode Channel: #SiriPlugins #SiriServer
#commands: twitter sende !Nachricht!
#easy_install python-twitter

from plugin import *
import oauth2
import twitter
import re

cs_key = APIKeyForAPI("twitter_consumer_key")
cs_secret = APIKeyForAPI("twitter_consumer_secret")
ac_key = APIKeyForAPI("twitter_access_token_key")
ac_secret = APIKeyForAPI("twitter_access_token_secret")

class tweet(Plugin):

    res = {
        'setTweet': {
            'en-EN': 'tweet (.*)'
        },
    }
    
    @register("de-DE", res['setTweet']['en-EN'])
    def tweet_status(self, speech, language):
		tapi = twitter.Api(consumer_key='', consumer_secret='', access_token_key='', access_token_secret='')
		TweetString = re.match(tweet.res['setTweet'][language], speech, re.IGNORECASE)
		answer = self.ask(u"Do you want to tweet "+TweetString.group(1)+" ?")	
		if (answer.lower() == 'yes'):
			self.say("OK, tweeting")
			tweetstatus = tapi.PostUpdate(TweetString.group(1))
			self.say('Tweet '+TweetString.group(1)+ ' successfully send.')
		else:
			self.say("No? Ok, you'r the boss!")	
		self.complete_request()
