#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib
import feedparser
from plugin import *


class trafficjams(Plugin):
	@register("de-DE", u"(aktuelle|neue|heutige)? (Staumeldungen|Staus) (auf der|für die) (?P<autobahnnummer>[^^]+)")
	def get_trafficInfos(self, speech, language, matchedRegex):
		searchString = matchedRegex.group('autobahnnummer')
		found = 0;
		dom = feedparser.parse("http://www.freiefahrt.info/upload/lmst.de_DE.xml")
		listitem = {}
		for node in dom.entries:
			title = node.title
			autobahn = title.split()[0]
			if autobahn == searchString:
				title = title.replace(autobahn + ' : ', '')
				content = node.summary
				if title not in listitem:
					listitem[title] = content
				else:
					curtitle = listitem[title]
					listitem[title] = curtitle + "\n\n" + content
				found = found + 1
		if found > 0:
			self.say(u"Deine Staus auf der {0}".format(searchString))
			for title in listitem:
				content = listitem[title]
				answer = "\n\n" + title "\n" + content
				self.say(answer, ' ')
		else:
			self.say(u"Sorry kein Stau für {0} gefunden".format(searchString))


