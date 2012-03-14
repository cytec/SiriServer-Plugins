
#!/usr/bin/python
# -*- coding: utf-8 -*-

from plugin import *
import urllib
import re
from BeautifulSoup import BeautifulSoup
import datetime



class ferienPlugin(Plugin):

	res = {
		'feriencommands': {
			'de-DE': '.*ferien in ([\w ]+)'
		},
		'searching': {
			'de-DE': 'Einen moment bitte...'
		},
		'error': {
			'de-DE': 'etwas ist schief gelaufen'
		},
		'answer': {
			'de-DE': '{0} {1} in {2}: {3}'
		}
	}

	@register("de-DE", res["feriencommands"]["de-DE"])
	def get_ferien(self, speech, language):
		self.say(ferienPlugin.res['searching'][language])
		bundesland = re.match("(?u).* in ([\w ]+)$", speech, re.IGNORECASE)
		ferienart = re.match("([\w ]+).* in .*", speech, re.IGNORECASE)
		now = datetime.datetime.now()
		year = str(now.year)
		if bundesland != None:
			bundesland = bundesland.group(1).strip()
			try:
				ferienart = ferienart.group(1).strip()
			except:
				ferienart = "alle"
			if bundesland.lower() == "nrw":
				bundesland = "Nordrhein-Westfalen"
			if bundesland.lower() == "mecklenburg-vorpommern":
				bundesland = "Meckl.-Vorpommern"
			url = "http://www.deutschland-feiertage.de/schulferien-" + year
			html = urllib.urlopen(url).read()
			soup = BeautifulSoup(html)
			ferientabelle = soup.find("table", {"class":"schulferien"})
			allTR = ferientabelle.tbody.findAll("tr")
			ergebnis = {}
			if "sommerferien" in speech.lower():
				ferienart = "Sommerferien"
			elif "winterferien" in speech.lower():
				ferienart = "Winterferien"
			elif "pfingsten" in speech.lower() or "pfingstferien" in speech.lower():
				ferienart = "Pfingstferien"
			elif "ostern" in speech.lower() or "osterferien" in speech.lower():
				ferienart = "Osterferien"
			elif "herbstferien" in speech.lower():
				ferienart = "Herbstferien"
			elif "weihnachtsferien" in speech.lower():
				ferienart = "Weihnachtsferien"
			else:
				ferienart = "alle"
			feriengefunden = False
			for row in allTR:
				land, winter, ostern, pfingsten, sommer, herbst, weihnachten = row.findAll("td")
				#print moreInfo
				if land.text.lower() == bundesland.lower():
					if winter.text != "-":
						ergebnis["Winterferien"]=winter.text
					if ostern.text != "-":
						ergebnis["Osterferien"]=ostern.text
					if pfingsten.text != "-":
						ergebnis["Pfingstferien"]=pfingsten.text
					if sommer.text != "-":
						ergebnis["Sommerferien"]=sommer.text
					if herbst.text != "-":
						ergebnis["Herbstferien"]=herbst.text
					if weihnachten.text != "-":
						ergebnis["Weihnachtsferien"]=weihnachten.text
					feriengefunden = True
			
			if feriengefunden:
				if ferienart == "alle":
					#print ergebnis
					self.say("Leider ist es momentan nicht moeglich alle ferien anzuzeigen")
				else:
					if ferienart in ergebnis:
						#print ferienart, year + " in " + bundesland + ": " + ergebnis[ferienart]
						self.say(ferienPlugin.res['answer'][language].format(ferienart, year, bundesland, ergebnis[ferienart]))
					else: 
						#print bundesland + " hat leider keine " + ferienart
						self.say("{0} hat leider keine {1}").format(bundesland, ferienart)
			else:
				#print "Ich konnte leider keine Ferien fuer " + bundesland + " finden"
				self.say("Ich konnte leider keine Ferien fuer {0} finden").format(bundesland)


