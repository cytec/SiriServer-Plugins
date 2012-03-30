#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import uuid

from plugin import *

from siriObjects.baseObjects import *
from siriObjects.uiObjects import *
from siriObjects.systemObjects import *
from siriObjects.contactObjects import *

class meCard(Plugin):
	
	res = {
		"command" {
			"de-DE": "Wer bin ich",
			"en-US": "Who am I"
		},
		"response" {
			"de-DE": "Du bist {0}, das hast du mir jedenfalls so gesagt...",
			"en-US": "You're {0}, that's what you told me anyway...",
		}
	}

	@register("en-US", res["command"]["en-US"])
	@register("de-DE", res["command"]["de-DE"])
	def mePerson(self, speech, language):
		self.say(meCard.res["response"][language].format(self.user_name()))		
		person_search = PersonSearch(self.refId)
		person_search.scope = PersonSearch.ScopeLocalValue
		person_search.me = "true"        
		person_return = self.getResponseForRequest(person_search)
		person_ = person_return["properties"]["results"]
		mecard = PersonSnippet(persons=person_)
		view = AddViews(self.refId, dialogPhase="Completion")		
		view.views = [mecard]
		self.sendRequestWithoutAnswer(view)
		self.complete_request()
