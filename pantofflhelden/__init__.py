#!/usr/bin/python
# -*- coding: utf-8 -*-

# author: cytec iamcytec@googlemail.com
# needs feedparser (easy_install feedparser)
import feedparser
from plugin import *


class fflh(Plugin):   

	@register("de-DE", ".*neues.*(pantoffelhelden|pantoffelheld).*")
	def fflh_updates(self, speech, language):
		if language == "de-DE":
			rss_url = "http://feeds.feedburner.com/Pantofflhelden?format=xml"
			feed = feedparser.parse( rss_url )
			answer = self.ask("Updates mit zusammenfassung?")
			self.say("Aktuelles von den Pantofflhelden:")
			feedcontent = ""
			for entry in feed["items"]:
				#self.say(entry["title"])
				if format(answer) == "Ja":
					#self.say(summary)
					feedcontent = feedcontent + "\"" + entry["title"] + "\": " + entry["summary"] + "\n\n"
				else:
					feedcontent = feedcontent + "\"" + entry["title"] + "\",\n"
			self.say(feedcontent, ' ')
		self.complete_request()



