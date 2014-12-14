import mysqldao
import urllib

address = """
REPLACE(
CONCAT(address1, ' ',address2, ' ', city, ' ', state,' ', zip),
'  ', ' ')
address"""

yelp_query = mysqldao.select('yelp', 'yelp_phone', ['phone', address, 'zip'])
# address = urllib.quote(yelp_query[1][1])
yelp_query

import json
import requests

address = [ [query[0], query[1]] for query in yelp_query ]
entries = []

del address[0]

# little = []
# little.append(address[1])
# little.append(address[2])
# little.append(address[3])


for adr in address:
	
	url = 'http://maps.googleapis.com/maps/api/geocode/json?address="%s"&sensor=true' % (urllib.quote(adr[1]))
	resp = requests.get(url)
	data = json.loads(resp.text)
	print "Getting geometry for %s" % adr
	if data["results"]:
		geo = data["results"][0]["geometry"]["location"]
		entry = {'longitude': geo["lng"], 'latitude': geo["lat"], 'phone': adr[0]}
		print "updating %s" % entry
		mysqldao.update('yelp', 'yelp_phone', ['latitude', 'longitude'], ['phone'], [entry])
		print mysqldao.select('yelp', 'yelp_phone', ['*'], ['phone'],[{'phone': entry["phone"]}])
		entries.append(entry)
  
# resp = requests.get(urls[1])
# data = json.loads(resp.text)
# geo = data["results"][0]["geometry"]["location"]

# data_entry = {'longitude': geo["lng"], 'latitude': geo["lat"], 'phone': address[1][0]}



