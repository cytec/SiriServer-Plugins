#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import urllib2, urllib
import json
from plugin import *


#/api/1234/?cmd=history&limit=2
#get last 5 downloads from sickbeard
sb_host = APIKeyForAPI("sickbeard_host")
sb_apikey = APIKeyForAPI("sickbeard_api_key")

class sickBeard(Plugin):   
	@register("de-DE", ".*serien.*status.*")
	def sb_history(self, speech, language):
		self.say("Deine Letzten Downloads:")
		SearchURL = u''+ sb_host + '/api/' + sb_apikey + '/?cmd=history&limit=5&type=downloaded'
		jsonResponse = urllib2.urlopen(SearchURL).read()
		jsonDecoded = json.JSONDecoder().decode(jsonResponse)
		for entry in jsonDecoded["data"]:
			content = entry["show_name"] + ": " + str(entry["season"]) + "x" + str(entry["episode"])
			self.say(content, ' ')
		self.complete_request()


